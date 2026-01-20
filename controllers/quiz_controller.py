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
        Create a quiz metadata (questions will be selected randomly when starting attempt)
        If quiz with same title exists, returns existing quiz_id
        
        difficulty_matrix: dict like {'easy': 5, 'medium': 3, 'hard': 2}
        Store in description for reference
        """
        # Check if quiz already exists by title
        existing_quiz = Quiz.get_by_title(title)
        if existing_quiz:
            return existing_quiz.id
        
        # Store difficulty matrix in description if provided
        if difficulty_matrix:
            desc_parts = [description] if description else []
            matrix_str = ', '.join([f"{count} câu {name}" for name, count in difficulty_matrix.items()])
            desc_parts.append(f"({matrix_str})")
            description = ' '.join(desc_parts)
        
        # Create quiz metadata only (will also handle duplicate via UNIQUE constraint)
        quiz_id = Quiz.create(title, description, time_limit, total_questions)
        return quiz_id

    @staticmethod
    def get_quiz_with_questions(quiz_id, difficulty_matrix={'easy': 10, 'medium': 10, 'hard': 10}):
        """Get quiz with randomly selected questions each time"""
        quiz = Quiz.get_by_id(quiz_id)
        if not quiz:
            return None

        # Select random questions based on difficulty_matrix
        selected_questions = []
        
        for difficulty_name, count in difficulty_matrix.items():
            if count > 0:
                difficulty_level = {'easy': 1, 'medium': 2, 'hard': 3}.get(difficulty_name, 1)
                questions = Question.get_random_questions(count, difficulty_level)
                selected_questions.extend(questions)
        
        # Shuffle questions to randomize order
        random.shuffle(selected_questions)
        
        quiz_data = {
            'quiz': quiz,
            'questions': []
        }

        for question in selected_questions:
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
        return Question.get_statistics(question_id)

    @staticmethod
    def analyze_difficulty():
        """Analyze actual difficulty based on answer statistics"""
        return Question.analyze_difficulty()

