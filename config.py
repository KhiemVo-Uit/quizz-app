"""Configuration settings for Quiz App"""
import os

# Database settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'quiz_app.db')

# Quiz settings
DEFAULT_QUIZ_TIME = 600  # 10 minutes in seconds
MIN_QUESTIONS_PER_QUIZ = 5
MAX_QUESTIONS_PER_QUIZ = 50

# Difficulty levels
DIFFICULTY_LEVELS = {
    'easy': 1,
    'medium': 2,
    'hard': 3
}

# Scoring settings
CORRECT_ANSWER_POINTS = 10
WRONG_ANSWER_PENALTY = 0
TIME_BONUS_ENABLED = False

# GUI settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FONT_FAMILY = 'Arial'
FONT_SIZE_TITLE = 16
FONT_SIZE_NORMAL = 12
FONT_SIZE_SMALL = 10

# Colors
COLOR_PRIMARY = '#2196F3'
COLOR_SUCCESS = '#4CAF50'
COLOR_DANGER = '#F44336'
COLOR_WARNING = '#FF9800'
COLOR_BACKGROUND = '#F5F5F5'
COLOR_TEXT = '#212121'
