"""Attempt model"""
from models.base_model import BaseModel
from datetime import datetime


class Attempt(BaseModel):
    """Attempt model for quiz attempts"""

    def __init__(self, id=None, quiz_id=None, student_name='', score=0, 
                 total_questions=0, correct_answers=0, time_taken=None,
                 started_at=None, completed_at=None):
        self.id = id
        self.quiz_id = quiz_id
        self.student_name = student_name
        self.score = score
        self.total_questions = total_questions
        self.correct_answers = correct_answers
        self.time_taken = time_taken
        self.started_at = started_at
        self.completed_at = completed_at

    @classmethod
    def _from_row(cls, row):
        """Create Attempt instance from database row"""
        if not row:
            return None
        return cls(
            id=row['id'],
            quiz_id=row['quiz_id'],
            student_name=row['student_name'],
            score=float(row['score']) if row['score'] else 0,
            total_questions=row['total_questions'],
            correct_answers=row['correct_answers'],
            time_taken=row['time_taken'],
            started_at=row['started_at'],
            completed_at=row['completed_at']
        )

    @classmethod
    def _from_rows(cls, rows):
        """Create list of Attempt instances from database rows"""
        return [cls._from_row(row) for row in rows]

    @staticmethod
    def create(quiz_id, student_name, total_questions):
        """Create a new attempt"""
        Attempt.cleanup_abandoned_attempts()
        return BaseModel.execute_insert(
            'INSERT INTO attempts (quiz_id, student_name, total_questions) VALUES (%s, %s, %s)',
            (quiz_id, student_name, total_questions)
        )

    @classmethod
    def get_by_id(cls, attempt_id):
        """Get attempt by ID"""
        row = BaseModel.execute_query_one(
            'SELECT * FROM attempts WHERE id = %s',
            (attempt_id,)
        )
        return cls._from_row(row)

    @classmethod
    def get_by_quiz(cls, quiz_id):
        """Get all attempts for a quiz"""
        rows = BaseModel.execute_query(
            'SELECT * FROM attempts WHERE quiz_id = %s ORDER BY started_at DESC',
            (quiz_id,)
        )
        return cls._from_rows(rows)

    @staticmethod
    def complete_attempt(attempt_id, score, correct_answers, time_taken):
        """Complete an attempt with results"""
        return BaseModel.execute_update(
            'UPDATE attempts SET score = %s, correct_answers = %s, time_taken = %s, completed_at = %s WHERE id = %s',
            (score, correct_answers, time_taken, datetime.now(), attempt_id)
        )

    @staticmethod
    def save_answer(attempt_id, question_id, selected_option_id, is_correct):
        """Save an answer for an attempt"""
        return BaseModel.execute_insert(
            'INSERT INTO attempt_answers (attempt_id, question_id, selected_option_id, is_correct) VALUES (%s, %s, %s, %s)',
            (attempt_id, question_id, selected_option_id, is_correct)
        )

    @staticmethod
    def get_answers(attempt_id):
        """Get all answers for an attempt"""
        return BaseModel.execute_query('''
            SELECT aa.*, q.question_text, o.option_text as selected_text
            FROM attempt_answers aa
            INNER JOIN questions q ON aa.question_id = q.id
            LEFT JOIN options o ON aa.selected_option_id = o.id
            WHERE aa.attempt_id = %s
            ORDER BY aa.answered_at
        ''', (attempt_id,))

    @staticmethod
    def get_statistics(quiz_id):
        """Get statistics for a quiz"""
        return BaseModel.execute_query_one('''
            SELECT 
                COUNT(*) as total_attempts,
                AVG(score) as avg_score,
                MAX(score) as max_score,
                MIN(score) as min_score,
                AVG(time_taken) as avg_time
            FROM attempts
            WHERE quiz_id = %s AND completed_at IS NOT NULL
        ''', (quiz_id,))

    @staticmethod
    def delete(attempt_id):
        """Delete attempt"""
        return BaseModel.execute_update(
            'DELETE FROM attempts WHERE id = %s',
            (attempt_id,)
        )

    @staticmethod
    def cleanup_abandoned_attempts(hours_threshold=24):
        """Delete abandoned attempts that were started but not completed within the threshold hours"""
        with BaseModel.get_cursor() as cursor:
            cursor.execute(
                'DELETE FROM attempts WHERE completed_at IS NULL AND started_at < DATE_SUB(NOW(), INTERVAL %s HOUR)',
                (hours_threshold,)
            )
            return cursor.rowcount
