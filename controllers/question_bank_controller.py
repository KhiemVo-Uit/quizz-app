"""Question Bank Controller"""
from models.question import Question
from models.option import Option


class QuestionBankController:
    """Controller for managing question bank"""

    @staticmethod
    def add_question_with_options(question_text, difficulty, category, options_data):
        """
        Add a question with its options
        
        options_data: list of tuples [(option_text, is_correct), ...]
        """
        # Validate that exactly one option is correct
        correct_count = sum(1 for _, is_correct in options_data if is_correct)
        if correct_count != 1:
            raise ValueError("Exactly one option must be marked as correct")

        if len(options_data) < 2:
            raise ValueError("At least 2 options are required")

        # Create question
        question_id = Question.create(question_text, difficulty, category)

        # Create options
        for option_text, is_correct in options_data:
            Option.create(question_id, option_text, is_correct)

        return question_id

    @staticmethod
    def update_question_with_options(question_id, question_text=None, difficulty=None, 
                                     category=None, options_data=None):
        """Update a question and optionally its options"""
        # Update question
        if question_text or difficulty or category:
            Question.update(question_id, question_text, difficulty, category)

        # Update options if provided
        if options_data:
            # Validate
            correct_count = sum(1 for _, is_correct in options_data if is_correct)
            if correct_count != 1:
                raise ValueError("Exactly one option must be marked as correct")

            # Delete old options and create new ones
            Option.delete_by_question(question_id)
            for option_text, is_correct in options_data:
                Option.create(question_id, option_text, is_correct)

        return True

    @staticmethod
    def delete_question(question_id):
        """Delete a question and all its options"""
        # Options will be automatically deleted due to CASCADE constraint
        return Question.delete(question_id)

    @staticmethod
    def get_question_with_options(question_id):
        """Get a question with all its options"""
        question = Question.get_by_id(question_id)
        if not question:
            return None

        options = Option.get_by_question(question_id)
        return {
            'question': question,
            'options': options
        }

    @staticmethod
    def get_all_questions_with_options():
        """Get all questions with their options"""
        questions = Question.get_all()
        result = []

        for question in questions:
            options = Option.get_by_question(question.id)
            result.append({
                'question': question,
                'options': options
            })

        return result

    @staticmethod
    def search_questions(keyword=None, difficulty=None, category=None):
        """Search questions by various criteria"""
        questions = Question.get_all()

        # Filter by keyword
        if keyword:
            keyword = keyword.lower()
            questions = [q for q in questions if keyword in q.question_text.lower()]

        # Filter by difficulty
        if difficulty:
            questions = [q for q in questions if q.difficulty == difficulty]

        # Filter by category
        if category:
            questions = [q for q in questions if q.category == category]

        return questions

    @staticmethod
    def get_questions_by_difficulty_range(min_difficulty, max_difficulty):
        """Get questions within a difficulty range"""
        questions = Question.get_all()
        return [q for q in questions if min_difficulty <= q.difficulty <= max_difficulty]

    @staticmethod
    def validate_question_bank():
        """Validate entire question bank for data integrity"""
        questions = Question.get_all()
        issues = []

        for question in questions:
            options = Option.get_by_question(question.id)
            
            # Check if question has options
            if not options:
                issues.append(f"Question {question.id} has no options")
                continue

            # Check if question has exactly one correct answer
            correct_options = [opt for opt in options if opt.is_correct]
            if len(correct_options) != 1:
                issues.append(f"Question {question.id} has {len(correct_options)} correct options (should be 1)")

            # Check minimum number of options
            if len(options) < 2:
                issues.append(f"Question {question.id} has only {len(options)} options (minimum 2 required)")

        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'total_questions': len(questions)
        }
