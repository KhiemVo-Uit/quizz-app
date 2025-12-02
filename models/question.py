"""Question model"""
from database.connection import db


class Question:
    """Question model for quiz app"""

    def __init__(self, id=None, question_text='', difficulty=1, category='', created_at=None):
        self.id = id
        self.question_text = question_text
        self.difficulty = difficulty
        self.category = category
        self.created_at = created_at

    @staticmethod
    def create(question_text, difficulty, category='General'):
        """Create a new question"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO questions (question_text, difficulty, category)
            VALUES (?, ?, ?)
        ''', (question_text, difficulty, category))

        conn.commit()
        return cursor.lastrowid

    @staticmethod
    def get_by_id(question_id):
        """Get question by ID"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
        row = cursor.fetchone()

        if row:
            return Question(
                id=row['id'],
                question_text=row['question_text'],
                difficulty=row['difficulty'],
                category=row['category'],
                created_at=row['created_at']
            )
        return None

    @staticmethod
    def get_all():
        """Get all questions"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM questions ORDER BY id ASC')
        rows = cursor.fetchall()

        return [Question(
            id=row['id'],
            question_text=row['question_text'],
            difficulty=row['difficulty'],
            category=row['category'],
            created_at=row['created_at']
        ) for row in rows]

    @staticmethod
    def get_by_difficulty(difficulty):
        """Get questions by difficulty level"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM questions WHERE difficulty = ?', (difficulty,))
        rows = cursor.fetchall()

        return [Question(
            id=row['id'],
            question_text=row['question_text'],
            difficulty=row['difficulty'],
            category=row['category'],
            created_at=row['created_at']
        ) for row in rows]

    @staticmethod
    def get_by_category(category):
        """Get questions by category"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM questions WHERE category = ?', (category,))
        rows = cursor.fetchall()

        return [Question(
            id=row['id'],
            question_text=row['question_text'],
            difficulty=row['difficulty'],
            category=row['category'],
            created_at=row['created_at']
        ) for row in rows]

    @staticmethod
    def update(question_id, question_text=None, difficulty=None, category=None):
        """Update question"""
        conn = db.get_connection()
        cursor = conn.cursor()

        updates = []
        params = []

        if question_text is not None:
            updates.append('question_text = ?')
            params.append(question_text)
        if difficulty is not None:
            updates.append('difficulty = ?')
            params.append(difficulty)
        if category is not None:
            updates.append('category = ?')
            params.append(category)

        if updates:
            params.append(question_id)
            query = f"UPDATE questions SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
        return False

    @staticmethod
    def delete(question_id):
        """Delete question"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def count():
        """Count total questions"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) as count FROM questions')
        return cursor.fetchone()['count']

    @staticmethod
    def get_random_questions(count, difficulty=None):
        """Get random questions, optionally filtered by difficulty"""
        conn = db.get_connection()
        cursor = conn.cursor()

        if difficulty:
            cursor.execute('''
                SELECT * FROM questions 
                WHERE difficulty = ?
                ORDER BY RANDOM() 
                LIMIT ?
            ''', (difficulty, count))
        else:
            cursor.execute('''
                SELECT * FROM questions 
                ORDER BY RANDOM() 
                LIMIT ?
            ''', (count,))

        rows = cursor.fetchall()

        return [Question(
            id=row['id'],
            question_text=row['question_text'],
            difficulty=row['difficulty'],
            category=row['category'],
            created_at=row['created_at']
        ) for row in rows]
