"""Quiz Controller - Main business logic"""
import random
from models.question import Question
from models.option import Option
from models.quiz import Quiz
from models.attempt import Attempt
from config import CORRECT_ANSWER_POINTS


class QuizController:
    """Controller for quiz operations"""

    @staticmethod
    def create_quiz_with_random_questions(title, description, total_questions, time_limit, difficulty_matrix=None):
        """
        Create a quiz with randomly selected questions
        
        difficulty_matrix: dict like {'easy': 5, 'medium': 3, 'hard': 2}
        """
        # Create quiz
        quiz_id = Quiz.create(title, description, time_limit, total_questions)

        # Get random questions based on difficulty matrix
        selected_questions = []
        
        if difficulty_matrix:
            for difficulty_name, count in difficulty_matrix.items():
                if count > 0:
                    difficulty_level = {'easy': 1, 'medium': 2, 'hard': 3}.get(difficulty_name, 1)
                    questions = Question.get_random_questions(count, difficulty_level)
                    selected_questions.extend(questions)
        else:
            # Random selection without difficulty filter
            selected_questions = Question.get_random_questions(total_questions)

        # Add questions to quiz
        for order, question in enumerate(selected_questions, 1):
            Quiz.add_question(quiz_id, question.id, order)

        return quiz_id

    @staticmethod
    def get_quiz_with_questions(quiz_id):
        """Get quiz with all its questions and options"""
        quiz = Quiz.get_by_id(quiz_id)
        if not quiz:
            return None

        questions = Quiz.get_questions(quiz_id)
        quiz_data = {
            'quiz': quiz,
            'questions': []
        }

        for question in questions:
            options = Option.get_by_question(question.id)
            # Shuffle options for randomization
            random.shuffle(options)
            quiz_data['questions'].append({
                'question': question,
                'options': options
            })

        return quiz_data

    @staticmethod
    def start_attempt(quiz_id, student_name):
        """Start a new quiz attempt"""
        quiz = Quiz.get_by_id(quiz_id)
        if not quiz:
            return None

        attempt_id = Attempt.create(quiz_id, student_name, quiz.total_questions)
        return attempt_id

    @staticmethod
    def submit_answer(attempt_id, question_id, selected_option_id):
        """Submit an answer for a question"""
        # Check if answer is correct
        correct_option = Option.get_correct_option(question_id)
        # Handle case when no option is selected (None)
        if selected_option_id is None:
            is_correct = False
        else:
            is_correct = (correct_option and correct_option.id == selected_option_id)

        # Save answer
        Attempt.save_answer(attempt_id, question_id, selected_option_id, is_correct)
        return is_correct

    @staticmethod
    def complete_attempt(attempt_id, time_taken):
        """Complete an attempt and calculate score (max 10 points)"""
        answers = Attempt.get_answers(attempt_id)
        correct_count = sum(1 for ans in answers if ans['is_correct'])
        total_questions = len(answers)
        
        # Calculate score: max 10 points, distributed evenly across all questions
        # Example: 20 questions = 0.5 points each, 5 questions = 2 points each
        points_per_question = 10.0 / total_questions if total_questions > 0 else 0
        score = correct_count * points_per_question
        
        Attempt.complete_attempt(attempt_id, score, correct_count, time_taken)
        
        return {
            'score': round(score, 1),  # Round to 1 decimal place
            'correct': correct_count,
            'total': total_questions
        }

    @staticmethod
    def get_attempt_review(attempt_id):
        """Get detailed review of an attempt"""
        attempt = Attempt.get_by_id(attempt_id)
        if not attempt:
            return None

        answers = Attempt.get_answers(attempt_id)
        review_data = {
            'attempt': attempt,
            'answers': []
        }

        for answer in answers:
            question = Question.get_by_id(answer['question_id'])
            all_options = Option.get_by_question(answer['question_id'])
            correct_option = Option.get_correct_option(answer['question_id'])

            review_data['answers'].append({
                'question': question,
                'all_options': all_options,
                'selected_option_id': answer['selected_option_id'],
                'correct_option_id': correct_option.id if correct_option else None,
                'is_correct': answer['is_correct']
            })

        return review_data

    @staticmethod
    def get_question_statistics(question_id):
        """Get statistics for a specific question"""
        conn = Attempt.get_by_id.__globals__['db'].get_connection()
        cursor = conn.cursor()

        # Total times answered
        cursor.execute('''
            SELECT COUNT(*) as total_answers
            FROM attempt_answers
            WHERE question_id = ?
        ''', (question_id,))
        total_answers = cursor.fetchone()['total_answers']

        # Correct answer rate
        cursor.execute('''
            SELECT COUNT(*) as correct_count
            FROM attempt_answers
            WHERE question_id = ? AND is_correct = 1
        ''', (question_id,))
        correct_count = cursor.fetchone()['correct_count']

        # Option selection distribution
        cursor.execute('''
            SELECT 
                o.id,
                o.option_text,
                o.is_correct,
                COUNT(aa.id) as selection_count
            FROM options o
            LEFT JOIN attempt_answers aa ON o.id = aa.selected_option_id
            WHERE o.question_id = ?
            GROUP BY o.id
        ''', (question_id,))
        option_stats = cursor.fetchall()

        return {
            'total_answers': total_answers,
            'correct_count': correct_count,
            'correct_rate': (correct_count / total_answers * 100) if total_answers > 0 else 0,
            'option_distribution': option_stats
        }

    @staticmethod
    def analyze_difficulty():
        """Analyze actual difficulty based on answer statistics"""
        conn = Attempt.get_by_id.__globals__['db'].get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                q.id,
                q.question_text,
                q.difficulty as labeled_difficulty,
                COUNT(aa.id) as total_answers,
                SUM(CASE WHEN aa.is_correct = 1 THEN 1 ELSE 0 END) as correct_answers,
                CAST(SUM(CASE WHEN aa.is_correct = 1 THEN 1 ELSE 0 END) AS FLOAT) / 
                    COUNT(aa.id) * 100 as success_rate
            FROM questions q
            LEFT JOIN attempt_answers aa ON q.id = aa.question_id
            GROUP BY q.id
            HAVING COUNT(aa.id) > 0
            ORDER BY success_rate ASC
        ''')

        return cursor.fetchall()

    @staticmethod
    def get_quiz_statistics(quiz_id):
        """Get comprehensive statistics for a quiz"""
        stats = Attempt.get_statistics(quiz_id)
        
        # Get question difficulty breakdown
        conn = Attempt.get_by_id.__globals__['db'].get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                q.difficulty,
                COUNT(*) as count
            FROM quiz_questions qq
            INNER JOIN questions q ON qq.question_id = q.id
            WHERE qq.quiz_id = ?
            GROUP BY q.difficulty
        ''', (quiz_id,))
        
        difficulty_breakdown = cursor.fetchall()
        
        return {
            'basic_stats': stats,
            'difficulty_breakdown': difficulty_breakdown
        }
