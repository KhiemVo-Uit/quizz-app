"""Quiz Taking View"""
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import time
from controllers.quiz_controller import QuizController
from models.quiz import Quiz
from config import FONT_FAMILY, COLOR_SUCCESS, COLOR_DANGER, COLOR_PRIMARY


class QuizView:
    """View for taking quizzes"""

    def __init__(self, parent):
        self.parent = parent
        self.current_quiz = None
        self.current_attempt = None
        self.current_question_index = 0
        self.answers = {}
        self.start_time = None
        self.timer_running = False
        self.time_remaining = 0
        
        self.show_quiz_list()
    def _clear_widgets(self):
        """Helper: Clear all widgets (DRY)"""
        for widget in self.parent.winfo_children():
            widget.destroy()

    def _create_info_badge(self, parent, text, style="info"):
        """Helper: Create info badge (DRY)"""
        badge = ttk.Frame(parent, bootstyle="light", padding=(20, 12))
        badge.pack(side=tk.LEFT, padx=12)
        ttk.Label(badge, text=text, font=(FONT_FAMILY, 14, 'bold'), bootstyle=style).pack()

    def _setup_scrollable_canvas(self, parent):
        """Helper: Create scrollable canvas with mousewheel (DRY)"""
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        return scrollable_frame

    def show_quiz_list(self):
        """Show list of available quizzes"""
        self._clear_widgets()
        
        # Header
        header = ttk.Frame(self.parent)
        header.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Label(header, text="📝 Danh sách bài thi", 
                 font=(FONT_FAMILY, 24, 'bold'),
                 bootstyle="primary").pack(side=tk.LEFT)
        
        # Get all quizzes from database
        quizzes = Quiz.get_all()
        
        if not quizzes:
            # No quizzes available
            container = ttk.Frame(self.parent)
            container.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(container, text="Chưa có bài thi nào",
                     font=(FONT_FAMILY, 16),
                     bootstyle="secondary").pack(expand=True)
            return
        
        # Scrollable container for quiz list
        scrollable_frame = self._setup_scrollable_canvas(self.parent)
        
        # Display each quiz as a card
        for quiz in quizzes:
            self._create_quiz_card(scrollable_frame, quiz)
    
    def _create_quiz_card(self, parent, quiz):
        """Create a quiz card"""
        card = ttk.Frame(parent, bootstyle="light")
        card.pack(fill=tk.X, pady=10, padx=20)
        
        inner = ttk.Frame(card, relief=tk.SOLID, borderwidth=1)
        inner.pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.Frame(inner)
        info_frame.pack(padx=30, pady=25, fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(info_frame, text=quiz.title,
                 font=(FONT_FAMILY, 18, 'bold'),
                 bootstyle="primary").pack(anchor=tk.W, pady=(0, 10))
        
        # Description
        ttk.Label(info_frame, text=quiz.description,
                 font=(FONT_FAMILY, 12),
                 bootstyle="secondary").pack(anchor=tk.W, pady=5)
        
        # Info badges
        info_container = ttk.Frame(info_frame)
        info_container.pack(anchor=tk.W, pady=(15, 10))
        
        time_minutes = quiz.time_limit // 60
        self._create_info_badge(info_container, f"⏱ {time_minutes} phút")
        self._create_info_badge(info_container, f"📝 {quiz.total_questions} câu")
        
        # Start button
        ttk.Button(info_frame, text="🚀 Bắt đầu làm bài",
                  command=lambda q=quiz: self.start_quiz_with_name(q),
                  bootstyle="success",
                  width=20).pack(anchor=tk.W, pady=(10, 0))

    def start_quiz_with_name(self, quiz):
        """Start quiz after getting student name"""
        # Get student name first
        name_dialog = tk.Toplevel(self.parent)
        name_dialog.title("Thông tin sinh viên")
        name_dialog.geometry("400x200")
        name_dialog.transient(self.parent)
        name_dialog.grab_set()
        
        # Center the dialog
        name_dialog.update_idletasks()
        x = (name_dialog.winfo_screenwidth() // 2) - (200)
        y = (name_dialog.winfo_screenheight() // 2) - (125)
        name_dialog.geometry(f"400x250+{x}+{y}")
        
        container = ttk.Frame(name_dialog)
        container.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
        
        ttk.Label(container, text="👤 Nhập tên của bạn:",
                 font=(FONT_FAMILY, 13, 'bold'),
                 bootstyle="primary").pack(pady=(0, 15))
        
        name_entry = ttk.Entry(container, font=(FONT_FAMILY, 12), width=30)
        name_entry.pack(pady=10)
        name_entry.focus()
        
        def submit_name():
            student_name = name_entry.get().strip()
            if not student_name:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên!")
                return
            
            name_dialog.destroy()
            self.initialize_quiz(quiz, student_name)
        
        ttk.Button(container, text="🚀 Bắt đầu",
                  command=submit_name,
                  bootstyle="success",
                  width=20).pack(pady=15)
        name_entry.bind('<Return>', lambda e: submit_name())

    def initialize_quiz(self, quiz, student_name):
        """Initialize quiz session"""
        # Get quiz data with randomly selected questions
        difficulty_matrix = {'easy': 10, 'medium': 10, 'hard': 10}
        quiz_data = QuizController.get_quiz_with_questions(quiz.id, difficulty_matrix)
        if not quiz_data:
            messagebox.showerror("Lỗi", "Không thể tải bài thi!")
            return
        
        # Start attempt
        attempt_id = QuizController.start_attempt(quiz.id, student_name)
        
        self.current_quiz = quiz_data
        self.current_attempt = attempt_id
        self.current_question_index = 0
        self.answers = {}
        self.start_time = time.time()
        self.time_remaining = quiz.time_limit
        
        self.show_quiz_interface()

    def show_quiz_interface(self):
        """Show quiz taking interface"""
        self._clear_widgets()
        
        # Header with gradient-like styling
        header = ttk.Frame(self.parent, bootstyle="primary")
        header.pack(fill=tk.X, padx=20, pady=(15, 12))
        
        header_inner = ttk.Frame(header)
        header_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=18)
        
        ttk.Label(header_inner, text=f"📝 {self.current_quiz['quiz'].title}",
                 font=(FONT_FAMILY, 20, 'bold'),
                 bootstyle="inverse-primary").pack(side=tk.LEFT)
        
        self.timer_label = ttk.Label(header_inner, text="",
                                     font=(FONT_FAMILY, 20, 'bold'),
                                     bootstyle="inverse-primary")
        self.timer_label.pack(side=tk.RIGHT)
        
        # Question container with card styling
        container_outer = ttk.Frame(self.parent)
        container_outer.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.question_container = ttk.Frame(container_outer, bootstyle="light")
        self.question_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        # Navigation buttons with better styling
        nav_frame = ttk.Frame(self.parent)
        nav_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        self.prev_btn = ttk.Button(nav_frame, text="◀ Câu trước",
                                   command=self.previous_question,
                                   bootstyle="secondary-outline",
                                   width=18,
                                   padding=(15, 10))
        self.prev_btn.pack(side=tk.LEFT)
        
        self.next_btn = ttk.Button(nav_frame, text="Câu sau ▶",
                                   command=self.next_question,
                                   bootstyle="primary",
                                   width=18,
                                   padding=(15, 10))
        self.next_btn.pack(side=tk.RIGHT)
        
        self.submit_btn = ttk.Button(nav_frame, text="✅ Nộp bài",
                                     command=self.submit_quiz,
                                     bootstyle="success",
                                     width=18,
                                     padding=(15, 10))
        
        # Show first question
        self.show_question()
        
        # Start timer
        self.timer_running = True
        self.update_timer()

    def show_question(self):
        """Display current question"""
        for widget in self.question_container.winfo_children():
            widget.destroy()
        
        question_data = self.current_quiz['questions'][self.current_question_index]
        question = question_data['question']
        options = question_data['options']
        
        # Question card
        q_card = ttk.Frame(self.question_container)
        q_card.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Question header
        header = ttk.Frame(q_card)
        header.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header,
                 text=f"📝 Câu {self.current_question_index + 1}/{len(self.current_quiz['questions'])}",
                 font=(FONT_FAMILY, 18, 'bold'),
                 bootstyle="primary").pack(side=tk.LEFT)
        
        # Difficulty badge
        difficulty_text = {1: "Dễ", 2: "Trung bình", 3: "Khó"}
        difficulty_style = {1: "success", 2: "warning", 3: "danger"}
        badge = ttk.Frame(header, bootstyle="light", padding=(12, 6))
        badge.pack(side=tk.RIGHT)
        ttk.Label(badge,
                 text=difficulty_text.get(question.difficulty, 'N/A'),
                 font=(FONT_FAMILY, 11, 'bold'),
                 bootstyle=difficulty_style.get(question.difficulty, "secondary")).pack()
        
        # Question text
        ttk.Label(q_card,
                 text=question.question_text,
                 font=(FONT_FAMILY, 15),
                 wraplength=900).pack(anchor=tk.W, pady=(0, 25))
        
        # Options with better styling
        options_label = ttk.Label(q_card, text="Chọn đáp án:",
                                 font=(FONT_FAMILY, 13, 'bold'),
                                 bootstyle="secondary")
        options_label.pack(anchor=tk.W, pady=(0, 15))
        
        self.selected_option = tk.IntVar(value=self.answers.get(question.id, -1))
        
        for i, option in enumerate(options, 1):
            option_frame = ttk.Frame(q_card, bootstyle="light", padding=(5, 5))
            option_frame.pack(fill=tk.X, pady=6, padx=15)
            
            rb = ttk.Radiobutton(option_frame,
                                text=f"{chr(64+i)}. {option.option_text}",
                                variable=self.selected_option,
                                value=option.id,
                                bootstyle="primary",
                                command=lambda q=question.id, o=option.id: self.save_answer(q, o))
            rb.pack(anchor=tk.W, pady=10, padx=20)
        
        # Update navigation buttons
        self.prev_btn.config(state=tk.NORMAL if self.current_question_index > 0 else tk.DISABLED)
        
        if self.current_question_index == len(self.current_quiz['questions']) - 1:
            self.next_btn.pack_forget()
            self.submit_btn.pack(side=tk.RIGHT)
        else:
            self.submit_btn.pack_forget()
            self.next_btn.pack(side=tk.RIGHT)

    def save_answer(self, question_id, option_id):
        """Save selected answer"""
        self.answers[question_id] = option_id

    def previous_question(self):
        """Go to previous question"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def next_question(self):
        """Go to next question"""
        if self.current_question_index < len(self.current_quiz['questions']) - 1:
            self.current_question_index += 1
            self.show_question()

    def update_timer(self):
        """Update countdown timer"""
        if not self.timer_running:
            return
        
        # Check if timer_label still exists
        if not hasattr(self, 'timer_label') or not self.timer_label.winfo_exists():
            self.timer_running = False
            return
        
        self.time_remaining -= 1
        
        if self.time_remaining <= 0:
            self.timer_running = False
            messagebox.showinfo("Hết giờ", "Đã hết thời gian làm bài!")
            self.submit_quiz()
            return
        
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        
        try:
            self.timer_label.config(text=f"⏱ {minutes:02d}:{seconds:02d}")
            
            # Change color when time is running out
            if self.time_remaining < 60:
                self.timer_label.config(foreground=COLOR_DANGER)
            elif self.time_remaining < 300:
                self.timer_label.config(foreground='orange')
            
            self.parent.after(1000, self.update_timer)
        except tk.TclError:
            # Widget was destroyed, stop timer
            self.timer_running = False

    def submit_quiz(self):
        """Submit quiz answers"""
        if len(self.answers) < len(self.current_quiz['questions']):
            unanswered = len(self.current_quiz['questions']) - len(self.answers)
            if not messagebox.askyesno("Xác nhận",
                                       f"Bạn còn {unanswered} câu chưa trả lời.\nBạn có chắc muốn nộp bài?"):
                return
        
        self.timer_running = False
        
        # Submit all answers
        for question_data in self.current_quiz['questions']:
            question_id = question_data['question'].id
            selected_option = self.answers.get(question_id)
            QuizController.submit_answer(self.current_attempt, question_id, selected_option)
        
        # Calculate time taken
        time_taken = int(time.time() - self.start_time)
        
        # Complete attempt
        result = QuizController.complete_attempt(self.current_attempt, time_taken)
        
        # Show results
        self.show_results(result)

    def show_results(self, result):
        """Show quiz results"""
        self._clear_widgets()
        
        container = ttk.Frame(self.parent)
        container.pack(expand=True)
        
        ttk.Label(container, text="🎉",
                 font=(FONT_FAMILY, 56)).pack(pady=(20, 10))
        
        ttk.Label(container, text="Kết quả bài thi",
                 font=(FONT_FAMILY, 24, 'bold'),
                 bootstyle="primary").pack(pady=(0, 20))
        
        # Score card
        score_card = ttk.Frame(container, bootstyle="light")
        score_card.pack(pady=15, padx=50)
        
        score_inner = ttk.Frame(score_card)
        score_inner.pack(padx=60, pady=40)
        
        # Score with color based on percentage
        percentage = result['correct'] / result['total'] * 100
        score_color = COLOR_SUCCESS if percentage >= 50 else COLOR_DANGER
        score_style = "success" if percentage >= 50 else "danger"
        
        score_label = tk.Label(score_inner,
                              text=f"{result['score']}/10",
                              font=(FONT_FAMILY, 64, 'bold'),
                              fg=score_color)
        score_label.pack(pady=12)
        
        ttk.Label(score_inner, text="điểm",
                 font=(FONT_FAMILY, 18),
                 bootstyle="secondary").pack()
        
        ttk.Separator(container).pack(fill=tk.X, padx=120, pady=20)
        
        # Stats
        stats_frame = ttk.Frame(container)
        stats_frame.pack(pady=20)
        
        ttk.Label(stats_frame,
                 text=f"✓ Số câu đúng: {result['correct']}/{result['total']}",
                 font=(FONT_FAMILY, 16),
                 bootstyle=score_style).pack(pady=8)
        
        ttk.Label(stats_frame,
                 text=f"📊 Tỷ lệ đúng: {percentage:.1f}%",
                 font=(FONT_FAMILY, 16),
                 bootstyle="info").pack(pady=8)
        
        # Action buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=35)
        
        ttk.Button(btn_frame, text="📋 Xem chi tiết",
                  command=lambda: self.show_review(),
                  bootstyle="info",
                  width=18,
                  padding=(15, 10)).pack(side=tk.LEFT, padx=12)
        
        ttk.Button(btn_frame, text="📝 Làm bài khác",
                  bootstyle="success-outline",
                  width=18,
                  padding=(15, 10),
                  command=self.show_quiz_list).pack(side=tk.LEFT, padx=12)

    def show_review(self):
        """Show detailed answer review"""
        review_data = QuizController.get_attempt_review(self.current_attempt)
        
        self._clear_widgets()
        
        # Title
        ttk.Label(self.parent, text="Xem lại đáp án",
                 font=(FONT_FAMILY, 16, 'bold')).pack(pady=20)
        
        scrollable_frame = self._setup_scrollable_canvas(self.parent)
        
        # Show each answer
        for i, answer in enumerate(review_data['answers'], 1):
            self.create_review_item(scrollable_frame, i, answer)
        
        # Back button
        ttk.Button(self.parent, text="Quay lại",
                  command=self.show_quiz_list).pack(pady=10)

    def create_review_item(self, parent, number, answer):
        """Create review item for one question"""
        frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
        frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Question
        status = "✓" if answer['is_correct'] else "✗"
        color = COLOR_SUCCESS if answer['is_correct'] else COLOR_DANGER
        
        header = tk.Label(frame, text=f"{status} Câu {number}",
                         font=(FONT_FAMILY, 12, 'bold'),
                         fg=color)
        header.pack(anchor=tk.W, padx=10, pady=5)
        
        ttk.Label(frame, text=answer['question'].question_text,
                 wraplength=700).pack(anchor=tk.W, padx=20, pady=5)
        
        # Options
        for option in answer['all_options']:
            option_frame = ttk.Frame(frame)
            option_frame.pack(fill=tk.X, padx=30, pady=2)
            
            prefix = ""
            fg_color = 'black'
            
            if option.id == answer['correct_option_id']:
                prefix = "✓ "
                fg_color = COLOR_SUCCESS
            elif option.id == answer['selected_option_id'] and not answer['is_correct']:
                prefix = "✗ "
                fg_color = COLOR_DANGER
            
            tk.Label(option_frame, text=f"{prefix}{option.option_text}",
                    fg=fg_color).pack(anchor=tk.W)

    def create_sample_quiz(self):
        """Create sample quiz with sample questions"""
        from utils.sample_data import create_sample_questions_and_quizzes
        
        result = create_sample_questions_and_quizzes()
       
        self.show_quiz_list()
