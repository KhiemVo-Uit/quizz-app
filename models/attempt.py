"""Attempt model"""
from database.connection import db
from datetime import datetime


class Attempt:
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

    @staticmethod
    def create(quiz_id, student_name, total_questions):
        """Create a new attempt"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO attempts (quiz_id, student_name, total_questions)
            VALUES (?, ?, ?)
        ''', (quiz_id, student_name, total_questions))

        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_id(attempt_id):
        """Get attempt by ID"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM attempts WHERE id = ?', (attempt_id,))
        row = cursor.fetchone()

        if row:
            return Attempt(
                id=row['id'],
                quiz_id=row['quiz_id'],
                student_name=row['student_name'],
                score=row['score'],
                total_questions=row['total_questions'],
                correct_answers=row['correct_answers'],
                time_taken=row['time_taken'],
                started_at=row['started_at'],
                completed_at=row['completed_at']
            )
        return None

    @staticmethod
    def get_by_quiz(quiz_id):
        """Get all attempts for a quiz"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM attempts 
            WHERE quiz_id = ? 
            ORDER BY started_at DESC
        ''', (quiz_id,))
        rows = cursor.fetchall()

        return [Attempt(
            id=row['id'],
            quiz_id=row['quiz_id'],
            student_name=row['student_name'],
            score=row['score'],
            total_questions=row['total_questions'],
            correct_answers=row['correct_answers'],
            time_taken=row['time_taken'],
            started_at=row['started_at'],
            completed_at=row['completed_at']
        ) for row in rows]

    @staticmethod
    def complete_attempt(attempt_id, score, correct_answers, time_taken):
        """Complete an attempt with results"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE attempts 
            SET score = ?, correct_answers = ?, time_taken = ?, completed_at = ?
            WHERE id = ?
        ''', (score, correct_answers, time_taken, datetime.now(), attempt_id))

        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def save_answer(attempt_id, question_id, selected_option_id, is_correct):
        """Save an answer for an attempt"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO attempt_answers (attempt_id, question_id, selected_option_id, is_correct)
            VALUES (?, ?, ?, ?)
        ''', (attempt_id, question_id, selected_option_id, is_correct))

        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def get_answers(attempt_id):
        """Get all answers for an attempt"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT aa.*, q.question_text, o.option_text as selected_text
            FROM attempt_answers aa
            INNER JOIN questions q ON aa.question_id = q.id
            LEFT JOIN options o ON aa.selected_option_id = o.id
            WHERE aa.attempt_id = ?
            ORDER BY aa.answered_at
        ''', (attempt_id,))

        return cursor.fetchall()

    @staticmethod
    def get_statistics(quiz_id):
        """Get statistics for a quiz"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                COUNT(*) as total_attempts,
                AVG(score) as avg_score,
                MAX(score) as max_score,
                MIN(score) as min_score,
                AVG(time_taken) as avg_time
            FROM attempts
            WHERE quiz_id = ? AND completed_at IS NOT NULL
        ''', (quiz_id,))

        return cursor.fetchone()

    @staticmethod
    def delete(attempt_id):
        """Delete attempt"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM attempts WHERE id = ?', (attempt_id,))
        conn.commit()
        return cursor.rowcount > 0
