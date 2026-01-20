"""Quiz model"""
from mysql.connector import Error as MySQLError
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
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute('''
                INSERT INTO quizzes (title, description, time_limit, total_questions)
                VALUES (%s, %s, %s, %s)
            ''', (title, description, time_limit, total_questions))
            conn.commit()
            quiz_id = cursor.lastrowid
            db.close_connection(conn)
            return quiz_id
        except MySQLError:
            # Title already exists, return existing quiz ID
            cursor.execute('SELECT id FROM quizzes WHERE title = %s', (title,))
            row = cursor.fetchone()
            db.close_connection(conn)
            return row['id'] if row else None

    @staticmethod
    def get_by_id(quiz_id):
        """Get quiz by ID"""
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM quizzes WHERE id = %s', (quiz_id,))
        row = cursor.fetchone()
        db.close_connection(conn)

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
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM quizzes WHERE title = %s', (title,))
        row = cursor.fetchone()
        db.close_connection(conn)

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
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM quizzes ORDER BY created_at DESC')
        rows = cursor.fetchall()
        db.close_connection(conn)

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
            updates.append('title = %s')
            params.append(title)
        if description is not None:
            updates.append('description = %s')
            params.append(description)
        if time_limit is not None:
            updates.append('time_limit = %s')
            params.append(time_limit)
        if total_questions is not None:
            updates.append('total_questions = %s')
            params.append(total_questions)

        if updates:
            params.append(quiz_id)
            query = f"UPDATE quizzes SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, params)
            conn.commit()
            result = cursor.rowcount > 0
            db.close_connection(conn)
            return result
        db.close_connection(conn)
        return False

    @staticmethod
    def delete(quiz_id):
        """Delete quiz"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM quizzes WHERE id = %s', (quiz_id,))
        conn.commit()
        result = cursor.rowcount > 0
        db.close_connection(conn)
        return result

    # Quiz questions are now generated randomly at attempt time
    # No need to store quiz-question mapping

    @staticmethod
    def count():
        """Count total quizzes"""
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT COUNT(*) as count FROM quizzes')
        result = cursor.fetchone()['count']
        db.close_connection(conn)
        return result
