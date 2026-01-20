"""Quiz model"""
import sqlite3
from database.connection import db


class Quiz:
    """Quiz model"""

    def __init__(self, id=None, title='', description='', time_limit=600, 
                 total_questions=0, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.time_limit = time_limit
        self.total_questions = total_questions
        self.created_at = created_at

    @staticmethod
    def create(title, description='', time_limit=600, total_questions=10):
        """Create a new quiz (returns existing quiz_id if title already exists)"""
        conn = db.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO quizzes (title, description, time_limit, total_questions)
                VALUES (?, ?, ?, ?)
            ''', (title, description, time_limit, total_questions))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Title already exists, return existing quiz ID
            cursor.execute('SELECT id FROM quizzes WHERE title = ?', (title,))
            row = cursor.fetchone()
            return row['id'] if row else None

    @staticmethod
    def get_by_id(quiz_id):
        """Get quiz by ID"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM quizzes WHERE id = ?', (quiz_id,))
        row = cursor.fetchone()

        if row:
            return Quiz(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                time_limit=row['time_limit'],
                total_questions=row['total_questions'],
                created_at=row['created_at']
            )
        return None

    @staticmethod
    def get_by_title(title):
        """Get quiz by title"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM quizzes WHERE title = ?', (title,))
        row = cursor.fetchone()

        if row:
            return Quiz(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                time_limit=row['time_limit'],
                total_questions=row['total_questions'],
                created_at=row['created_at']
            )
        return None

    @staticmethod
    def get_all():
        """Get all quizzes"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM quizzes ORDER BY created_at DESC')
        rows = cursor.fetchall()

        return [Quiz(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            time_limit=row['time_limit'],
            total_questions=row['total_questions'],
            created_at=row['created_at']
        ) for row in rows]

    @staticmethod
    def update(quiz_id, title=None, description=None, time_limit=None, total_questions=None):
        """Update quiz"""
        conn = db.get_connection()
        cursor = conn.cursor()

        updates = []
        params = []

        if title is not None:
            updates.append('title = ?')
            params.append(title)
        if description is not None:
            updates.append('description = ?')
            params.append(description)
        if time_limit is not None:
            updates.append('time_limit = ?')
            params.append(time_limit)
        if total_questions is not None:
            updates.append('total_questions = ?')
            params.append(total_questions)

        if updates:
            params.append(quiz_id)
            query = f"UPDATE quizzes SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        return False

    @staticmethod
    def delete(quiz_id):
        """Delete quiz"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM quizzes WHERE id = ?', (quiz_id,))
        conn.commit()
        return cursor.rowcount > 0

    # Quiz questions are now generated randomly at attempt time
    # No need to store quiz-question mapping

    @staticmethod
    def count():
        """Count total quizzes"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) as count FROM quizzes')
        return cursor.fetchone()['count']
