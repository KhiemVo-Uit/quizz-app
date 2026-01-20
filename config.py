"""Configuration settings for Quiz App"""
import os

# Database settings (MySQL)
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'quiz_app',
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': False,
    'pool_name': 'quiz_pool',
    
    'pool_size': 5
}

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
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
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

# Score/Difficulty colors (for legends and indicators)
COLOR_GREEN = '#28a745'      # Easy/Good
COLOR_YELLOW = '#ffc107'     # Medium
COLOR_RED = "#dc35ad"        # Hard/Low

# Table row colors
COLOR_ROW_HIGH_BG = '#d4edda'
COLOR_ROW_HIGH_FG = '#155724'
COLOR_ROW_MEDIUM_BG = '#fff3cd'
COLOR_ROW_MEDIUM_FG = '#856404'
COLOR_ROW_LOW_BG = '#f8d7da'
COLOR_ROW_LOW_FG = '#721c24'
COLOR_ROW_ODD = '#f8f9fa'
COLOR_ROW_EVEN = '#ffffff'
