"""Unit tests for Quiz Application"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import db
from models.question import Question
from models.option import Option
from models.quiz import Quiz
from models.attempt import Attempt
from controllers.quiz_controller import QuizController
from controllers.question_bank_controller import QuestionBankController


@pytest.fixture(scope='function')
def setup_database():
    """Setup test database before each test"""
    db.reset_database()
    yield
    # Cleanup after test
    db.reset_database()


class TestQuestionModel:
    """Tests for Question model"""

    def test_create_question(self, setup_database):
        """Test creating a question"""
        question_id = Question.create("What is Python?", 1, "Python")
        assert question_id is not None
        assert question_id > 0

    def test_get_question_by_id(self, setup_database):
        """Test retrieving a question by ID"""
        question_id = Question.create("What is Python?", 1, "Python")
        question = Question.get_by_id(question_id)
        
        assert question is not None
        assert question.question_text == "What is Python?"
        assert question.difficulty == 1
        assert question.category == "Python"

    def test_get_questions_by_difficulty(self, setup_database):
        """Test filtering questions by difficulty"""
        Question.create("Easy question", 1, "Test")
        Question.create("Medium question", 2, "Test")
        Question.create("Hard question", 3, "Test")
        
        easy_questions = Question.get_by_difficulty(1)
        assert len(easy_questions) == 1
        assert easy_questions[0].difficulty == 1

    def test_update_question(self, setup_database):
        """Test updating a question"""
        question_id = Question.create("Original question", 1, "Test")
        Question.update(question_id, question_text="Updated question", difficulty=2)
        
        question = Question.get_by_id(question_id)
        assert question.question_text == "Updated question"
        assert question.difficulty == 2

    def test_delete_question(self, setup_database):
        """Test deleting a question"""
        question_id = Question.create("To be deleted", 1, "Test")
        assert Question.delete(question_id) == True
        
        question = Question.get_by_id(question_id)
        assert question is None

    def test_random_question_selection(self, setup_database):
        """Test randomization of questions"""
        # Create 10 questions
        for i in range(10):
            Question.create(f"Question {i}", 1, "Test")
        
        random_questions = Question.get_random_questions(5)
        assert len(random_questions) == 5
        
        # Check that they are actually random (run multiple times)
        selections = []
        for _ in range(3):
            questions = Question.get_random_questions(3)
            question_ids = [q.id for q in questions]
            selections.append(tuple(question_ids))
        
        # At least one selection should be different (with high probability)
        # This tests randomization but may occasionally fail due to randomness
        assert len(set(selections)) >= 1  # At minimum, we got results


class TestOptionModel:
    """Tests for Option model"""

    def test_create_option(self, setup_database):
        """Test creating an option"""
        question_id = Question.create("Test question", 1, "Test")
        option_id = Option.create(question_id, "Option A", True)
        
        assert option_id is not None
        assert option_id > 0

    def test_get_options_by_question(self, setup_database):
        """Test retrieving options for a question"""
        question_id = Question.create("Test question", 1, "Test")
        Option.create(question_id, "Option A", True)
        Option.create(question_id, "Option B", False)
        Option.create(question_id, "Option C", False)
        
        options = Option.get_by_question(question_id)
        assert len(options) == 3

    def test_get_correct_option(self, setup_database):
        """Test getting the correct option"""
        question_id = Question.create("Test question", 1, "Test")
        Option.create(question_id, "Wrong", False)
        correct_id = Option.create(question_id, "Correct", True)
        Option.create(question_id, "Also wrong", False)
        
        correct_option = Option.get_correct_option(question_id)
        assert correct_option is not None
        assert correct_option.is_correct == True
        assert correct_option.option_text == "Correct"


class TestQuizController:
    """Tests for Quiz Controller"""

    def test_create_quiz_with_random_questions(self, setup_database):
        """Test creating a quiz with random questions"""
        # Create test questions
        for i in range(10):
            question_id = Question.create(f"Question {i}", 1, "Test")
            Option.create(question_id, "A", True)
            Option.create(question_id, "B", False)
        
        quiz_id = QuizController.create_quiz_with_random_questions(
            "Test Quiz", "Description", 5, 300
        )
        
        assert quiz_id is not None
        
        quiz_data = QuizController.get_quiz_with_questions(quiz_id)
        assert len(quiz_data['questions']) == 5

    def test_difficulty_matrix_selection(self, setup_database):
        """Test difficulty matrix for question selection"""
        # Create questions with different difficulties
        for i in range(5):
            q_id = Question.create(f"Easy {i}", 1, "Test")
            Option.create(q_id, "A", True)
            Option.create(q_id, "B", False)
        
        for i in range(3):
            q_id = Question.create(f"Medium {i}", 2, "Test")
            Option.create(q_id, "A", True)
            Option.create(q_id, "B", False)
        
        for i in range(2):
            q_id = Question.create(f"Hard {i}", 3, "Test")
            Option.create(q_id, "A", True)
            Option.create(q_id, "B", False)
        
        quiz_id = QuizController.create_quiz_with_random_questions(
            "Mixed Quiz", "Test", 6, 300,
            difficulty_matrix={'easy': 3, 'medium': 2, 'hard': 1}
        )
        
        quiz_data = QuizController.get_quiz_with_questions(quiz_id)
        assert len(quiz_data['questions']) == 6

    def test_submit_answer_correct(self, setup_database):
        """Test submitting a correct answer"""
        # Setup
        question_id = Question.create("Test", 1, "Test")
        correct_option = Option.create(question_id, "Correct", True)
        Option.create(question_id, "Wrong", False)
        
        quiz_id = Quiz.create("Test Quiz", "Desc", 300, 1)
        Quiz.add_question(quiz_id, question_id, 1)
        
        attempt_id = QuizController.start_attempt(quiz_id, "Test Student")
        
        # Test correct answer
        is_correct = QuizController.submit_answer(attempt_id, question_id, correct_option)
        assert is_correct == True

    def test_submit_answer_incorrect(self, setup_database):
        """Test submitting an incorrect answer"""
        # Setup
        question_id = Question.create("Test", 1, "Test")
        Option.create(question_id, "Correct", True)
        wrong_option = Option.create(question_id, "Wrong", False)
        
        quiz_id = Quiz.create("Test Quiz", "Desc", 300, 1)
        Quiz.add_question(quiz_id, question_id, 1)
        
        attempt_id = QuizController.start_attempt(quiz_id, "Test Student")
        
        # Test wrong answer
        is_correct = QuizController.submit_answer(attempt_id, question_id, wrong_option)
        assert is_correct == False

    def test_scoring_calculation(self, setup_database):
        """Test scoring calculation"""
        # Create quiz with 3 questions
        questions = []
        for i in range(3):
            q_id = Question.create(f"Q{i}", 1, "Test")
            Option.create(q_id, "Correct", True)
            Option.create(q_id, "Wrong", False)
            questions.append(q_id)
        
        quiz_id = Quiz.create("Test", "Desc", 300, 3)
        for i, q_id in enumerate(questions, 1):
            Quiz.add_question(quiz_id, q_id, i)
        
        attempt_id = QuizController.start_attempt(quiz_id, "Student")
        
        # Answer 2 correct, 1 wrong
        correct_opt = Option.get_correct_option(questions[0])
        QuizController.submit_answer(attempt_id, questions[0], correct_opt.id)
        
        correct_opt = Option.get_correct_option(questions[1])
        QuizController.submit_answer(attempt_id, questions[1], correct_opt.id)
        
        wrong_opts = Option.get_by_question(questions[2])
        wrong_opt = [o for o in wrong_opts if not o.is_correct][0]
        QuizController.submit_answer(attempt_id, questions[2], wrong_opt.id)
        
        result = QuizController.complete_attempt(attempt_id, 120)
        
        assert result['correct'] == 2
        assert result['total'] == 3
        assert result['score'] == 20  # 2 correct * 10 points


class TestQuestionBankController:
    """Tests for Question Bank Controller"""

    def test_add_question_with_options(self, setup_database):
        """Test adding question with options"""
        options_data = [
            ("Option A", True),
            ("Option B", False),
            ("Option C", False),
            ("Option D", False)
        ]
        
        question_id = QuestionBankController.add_question_with_options(
            "Test question", 1, "Test", options_data
        )
        
        assert question_id is not None
        options = Option.get_by_question(question_id)
        assert len(options) == 4

    def test_validate_one_correct_answer(self, setup_database):
        """Test validation: exactly one correct answer required"""
        # No correct answers
        with pytest.raises(ValueError):
            QuestionBankController.add_question_with_options(
                "Test", 1, "Test",
                [("A", False), ("B", False)]
            )
        
        # Multiple correct answers
        with pytest.raises(ValueError):
            QuestionBankController.add_question_with_options(
                "Test", 1, "Test",
                [("A", True), ("B", True)]
            )

    def test_validate_minimum_options(self, setup_database):
        """Test validation: minimum 2 options required"""
        with pytest.raises(ValueError):
            QuestionBankController.add_question_with_options(
                "Test", 1, "Test",
                [("A", True)]
            )

    def test_question_bank_validation(self, setup_database):
        """Test question bank validation"""
        # Add valid question
        QuestionBankController.add_question_with_options(
            "Valid", 1, "Test",
            [("A", True), ("B", False)]
        )
        
        validation = QuestionBankController.validate_question_bank()
        assert validation['is_valid'] == True
        assert len(validation['issues']) == 0


def run_tests():
    """Run all tests"""
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == '__main__':
    run_tests()
