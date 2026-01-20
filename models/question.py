"""Question model"""
from models.base_model import BaseModel


class Question(BaseModel):
    """Question model for quiz app"""

    def __init__(self, id=None, question_text='', difficulty=1, category='', created_at=None):
        self.id = id
        self.question_text = question_text
        self.difficulty = difficulty
        self.category = category
        self.created_at = created_at

    @classmethod
    def _from_row(cls, row):
        """Create Question instance from database row"""
        if not row:
            return None
        return cls(
            id=row['id'],
            question_text=row['question_text'],
            difficulty=row['difficulty'],
            category=row['category'],
            created_at=row['created_at']
        )

    @classmethod
    def _from_rows(cls, rows):
        """Create list of Question instances from database rows"""
        return [cls._from_row(row) for row in rows]

    @staticmethod
    def create(question_text, difficulty, category='General'):
        """Create a new question"""
        return BaseModel.execute_insert(
            'INSERT INTO questions (question_text, difficulty, category) VALUES (%s, %s, %s)',
            (question_text, difficulty, category)
        )

    @classmethod
    def get_by_id(cls, question_id):
        """Get question by ID"""
        row = BaseModel.execute_query_one(
            'SELECT * FROM questions WHERE id = %s',
            (question_id,)
        )
        return cls._from_row(row)

    @classmethod
    def get_all(cls):
        """Get all questions"""
        rows = BaseModel.execute_query('SELECT * FROM questions ORDER BY id ASC')
        return cls._from_rows(rows)

    @classmethod
    def get_by_difficulty(cls, difficulty):
        """Get questions by difficulty level"""
        rows = BaseModel.execute_query(
            'SELECT * FROM questions WHERE difficulty = %s',
            (difficulty,)
        )
        return cls._from_rows(rows)

    @classmethod
    def get_by_category(cls, category):
        """Get questions by category"""
        rows = BaseModel.execute_query(
            'SELECT * FROM questions WHERE category = %s',
            (category,)
        )
        return cls._from_rows(rows)

    @staticmethod
    def update(question_id, question_text=None, difficulty=None, category=None):
        """Update question"""
        query, params = BaseModel.build_update_query(
            'questions',
            {'question_text': question_text, 'difficulty': difficulty, 'category': category}
        )
        if query:
            params.append(question_id)
            return BaseModel.execute_update(query, params)
        return False

    @staticmethod
    def delete(question_id):
        """Delete question"""
        return BaseModel.execute_update(
            'DELETE FROM questions WHERE id = %s',
            (question_id,)
        )

    @staticmethod
    def count():
        """Count total questions"""
        return BaseModel.execute_count('SELECT COUNT(*) as count FROM questions')

    @classmethod
    def get_random_questions(cls, count, difficulty=None):
        """Get random questions, optionally filtered by difficulty"""
        if difficulty:
            rows = BaseModel.execute_query(
                'SELECT * FROM questions WHERE difficulty = %s ORDER BY RAND() LIMIT %s',
                (difficulty, count)
            )
        else:
            rows = BaseModel.execute_query(
                'SELECT * FROM questions ORDER BY RAND() LIMIT %s',
                (count,)
            )
        return cls._from_rows(rows)

    @staticmethod
    def get_statistics(question_id):
        """Get statistics for a specific question"""
        # Total times answered
        total_answers = BaseModel.execute_count(
            'SELECT COUNT(*) as count FROM attempt_answers WHERE question_id = %s',
            (question_id,)
        )

        # Correct answer count
        correct_count = BaseModel.execute_count(
            'SELECT COUNT(*) as count FROM attempt_answers WHERE question_id = %s AND is_correct = 1',
            (question_id,)
        )

        # Option selection distribution
        option_stats = BaseModel.execute_query('''
            SELECT 
                o.id,
                o.option_text,
                o.is_correct,
                COUNT(aa.id) as selection_count
            FROM options o
            LEFT JOIN attempt_answers aa ON o.id = aa.selected_option_id
            WHERE o.question_id = %s
            GROUP BY o.id, o.option_text, o.is_correct
        ''', (question_id,))

        return {
            'total_answers': total_answers,
            'correct_count': correct_count,
            'correct_rate': (correct_count / total_answers * 100) if total_answers > 0 else 0,
            'option_distribution': option_stats
        }

    @staticmethod
    def analyze_difficulty():
        """Analyze actual difficulty based on answer statistics"""
        return BaseModel.execute_query('''
            SELECT 
                q.id,
                q.question_text,
                q.difficulty as labeled_difficulty,
                COUNT(aa.id) as total_answers,
                SUM(CASE WHEN aa.is_correct = 1 THEN 1 ELSE 0 END) as correct_answers,
                CAST(SUM(CASE WHEN aa.is_correct = 1 THEN 1 ELSE 0 END) AS DECIMAL(10,2)) / 
                    COUNT(aa.id) * 100 as success_rate
            FROM questions q
            LEFT JOIN attempt_answers aa ON q.id = aa.question_id
            GROUP BY q.id, q.question_text, q.difficulty
            HAVING COUNT(aa.id) > 0
            ORDER BY success_rate ASC
        ''')
