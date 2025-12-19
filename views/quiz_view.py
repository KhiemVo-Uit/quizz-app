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

    def show_quiz_list(self):
        """Show list of available quizzes"""
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Header with title and action button
        header = ttk.Frame(self.parent)
        header.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Label(header, text="📝 Bài thi Kỹ thuật lập trình Python", 
                 font=(FONT_FAMILY, 24, 'bold'),
                 bootstyle="primary").pack(side=tk.LEFT)
        
        # Main container with centered content
        container = ttk.Frame(self.parent)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Center frame
        center_frame = ttk.Frame(container)
        center_frame.pack(expand=True)
        
        # Quiz card
        card = ttk.Frame(center_frame, bootstyle="light")
        card.pack(fill=tk.BOTH, expand=True, pady=20, padx=40)
        
        inner = ttk.Frame(card, relief=tk.SOLID, borderwidth=2)
        inner.pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.Frame(inner)
        info_frame.pack(padx=60, pady=50, fill=tk.BOTH, expand=True)
        
        # Icon
        ttk.Label(info_frame, text="📚",
                 font=(FONT_FAMILY, 56)).pack(pady=(0, 15))
        
        # Title
        ttk.Label(info_frame, text="Kỹ thuật lập trình Python",
                 font=(FONT_FAMILY, 22, 'bold'),
                 bootstyle="primary").pack(pady=(0, 15))
        
        # Description
        ttk.Label(info_frame, text="Bài thi gồm 30 câu hỏi ngẫu nhiên",
                 font=(FONT_FAMILY, 14),
                 bootstyle="secondary").pack(pady=8)
        
        ttk.Label(info_frame, text="10 câu dễ • 10 câu trung bình • 10 câu khó",
                 font=(FONT_FAMILY, 13),
                 bootstyle="info").pack(pady=8)
        
        ttk.Separator(info_frame).pack(fill=tk.X, padx=80, pady=20)
        
        # Info badges
        info_container = ttk.Frame(info_frame)
        info_container.pack(pady=(10, 25))
        
        badge1 = ttk.Frame(info_container, bootstyle="light", padding=(20, 12))
        badge1.pack(side=tk.LEFT, padx=12)
        ttk.Label(badge1, text="⏱ 45 phút",
                 font=(FONT_FAMILY, 14, 'bold'),
                 bootstyle="info").pack()
        
        badge2 = ttk.Frame(info_container, bootstyle="light", padding=(20, 12))
        badge2.pack(side=tk.LEFT, padx=12)
        ttk.Label(badge2, text="📝 30 câu",
                 font=(FONT_FAMILY, 14, 'bold'),
                 bootstyle="info").pack()
        
        # Start button
        ttk.Button(info_frame, text="🚀 Bắt đầu làm bài",
                  command=self.start_dynamic_quiz,
                  bootstyle="success",
                  width=22,
                  padding=(20, 12)).pack(pady=15)

    def start_dynamic_quiz(self):
        """Start quiz by creating new random questions each time"""
        # Check if enough questions exist in database
        from models.question import Question
        
        total_questions = Question.count()
        easy_count = len(Question.get_by_difficulty(1))
        medium_count = len(Question.get_by_difficulty(2))
        hard_count = len(Question.get_by_difficulty(3))
        
        # If not enough questions, create sample questions automatically
        if easy_count < 10 or medium_count < 10 or hard_count < 10:
            try:
                from utils.sample_data import create_sample_questions_and_quizzes
                create_sample_questions_and_quizzes()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo câu hỏi mẫu: {str(e)}")
                return
        
        # Get student name first
        name_dialog = tk.Toplevel(self.parent)
        name_dialog.title("Thông tin sinh viên")
        name_dialog.geometry("400x200")
        name_dialog.transient(self.parent)
        name_dialog.grab_set()
        
        # Center the dialog
        name_dialog.update_idletasks()
        x = (name_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (name_dialog.winfo_screenheight() // 2) - (250 // 2)
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
            
            # Create or get existing quiz (UNIQUE title constraint ensures no duplicates)
            try:
                quiz_id = QuizController.create_quiz_with_random_questions(
                    "Kỹ thuật lập trình Python",
                    "Bài thi về lập trình Python - 30 câu hỏi (10 dễ, 10 trung bình, 10 khó)",
                    30,
                    2700,  # 45 phút
                    {'easy': 10, 'medium': 10, 'hard': 10}
                )
                
                # Get the quiz
                quiz = Quiz.get_by_id(quiz_id)
                if quiz:
                    self.initialize_quiz(quiz, student_name)
                else:
                    messagebox.showerror("Lỗi", "Không thể tạo bài thi!")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tạo bài thi: {str(e)}")
        
        ttk.Button(container, text="🚀 Bắt đầu làm bài",
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
        for widget in self.parent.winfo_children():
            widget.destroy()
        
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
            rb.config(font=(FONT_FAMILY, 13))
        
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
        for widget in self.parent.winfo_children():
            widget.destroy()
        
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
        
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Title
        ttk.Label(self.parent, text="Xem lại đáp án",
                 font=(FONT_FAMILY, 16, 'bold')).pack(pady=20)
        
        # Scrollable frame
        canvas = tk.Canvas(self.parent)
        scrollbar = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mousewheel scrolling only when hovering over canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind("<Enter>", _bind_mousewheel)
        canvas.bind("<Leave>", _unbind_mousewheel)
        
        # Show each answer
        for i, answer in enumerate(review_data['answers'], 1):
            self.create_review_item(scrollable_frame, i, answer)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
