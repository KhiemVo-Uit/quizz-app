"""Question Bank Management View"""
import tkinter as tk
from tkinter import messagebox, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controllers.question_bank_controller import QuestionBankController
from models.question import Question
from config import FONT_FAMILY


class QuestionBankView:
    """View for managing question bank"""

    def __init__(self, parent):
        self.parent = parent
        self.current_offset = 0
        self.batch_size = 10
        self.loading = False
        self.all_loaded = False
        self.show_question_list()

    def show_question_list(self):
        """Show list of all questions"""
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Header with better styling
        header = ttk.Frame(self.parent)
        header.pack(fill=tk.X, padx=30, pady=20)
        
        ttk.Label(header, text="📚 Ngân hàng câu hỏi",
                 font=(FONT_FAMILY, 20, 'bold'),
                 bootstyle="primary").pack(side=tk.LEFT)
        
        ttk.Button(header, text="➕ Thêm câu hỏi mới",
                  command=self.add_question,
                  bootstyle="success",
                  width=18).pack(side=tk.RIGHT)
        
        # Filter card
        filter_card = ttk.Frame(self.parent, bootstyle="light")
        filter_card.pack(fill=tk.X, padx=30, pady=(0, 15))
        
        filter_frame = ttk.Frame(filter_card)
        filter_frame.pack(fill=tk.X, padx=20, pady=15)
        
        ttk.Label(filter_frame, text="🎯 Lọc theo độ khó:",
                 font=(FONT_FAMILY, 11, 'bold')).pack(side=tk.LEFT, padx=(0, 15))
        
        self.difficulty_var = tk.StringVar(value="all")
        difficulties = [("Tất cả", "all"), ("Dễ", "1"), ("Trung bình", "2"), ("Khó", "3")]
        
        for text, value in difficulties:
            ttk.Radiobutton(filter_frame, text=text,
                           variable=self.difficulty_var,
                           value=value,
                           bootstyle="primary",
                           command=self.filter_questions).pack(side=tk.LEFT, padx=8)

        # Search box
        search_frame = ttk.Frame(filter_card)
        search_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        ttk.Label(search_frame, text="🔍 Tìm kiếm câu hỏi:",
                 font=(FONT_FAMILY, 11, 'bold')).pack(side=tk.LEFT, padx=(0, 10))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)

        # Tìm kiếm khi nhấn Enter
        search_entry.bind("<Return>", lambda event: self.filter_questions())

        ttk.Button(search_frame, text="Tìm",
                  command=self.filter_questions,
                  bootstyle="secondary-outline").pack(side=tk.LEFT)
        
        # Questions container with scroll
        container = ttk.Frame(self.parent)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        self.questions_container = ttk.Frame(container)
        self.questions_container.pack(fill=tk.BOTH, expand=True)
        
        self.display_questions()

    def filter_questions(self):
        """Filter questions by difficulty"""
        self.current_offset = 0
        self.all_loaded = False
        self.display_questions()

    def display_questions(self, load_more=False):
        """Display filtered questions with lazy loading"""
        if not load_more:
            # Clear container for fresh display
            for widget in self.questions_container.winfo_children():
                widget.destroy()
            self.current_offset = 0
            self.all_loaded = False
        
        # Get questions theo bộ lọc (độ khó + từ khóa)
        difficulty_value = self.difficulty_var.get()
        keyword = self.search_var.get().strip() if hasattr(self, 'search_var') else ''

        difficulty = None
        if difficulty_value != "all":
            try:
                difficulty = int(difficulty_value)
            except ValueError:
                difficulty = None

        # Check count before loading if first load
        if not load_more:
            if not keyword and difficulty is None:
                total_count = Question.count()
            else:
                total_count = QuestionBankController.count_questions(
                    keyword=keyword or None, difficulty=difficulty, category=None
                )
            
            if total_count == 0:
                self.show_empty_state()
                return
        
        # Get paginated questions
        questions_data = QuestionBankController.search_questions(
            keyword=keyword or None, difficulty=difficulty, category=None,
            offset=self.current_offset, limit=self.batch_size
        )
        
        if not questions_data:
            if not load_more:
                self.show_empty_state()
            else:
                self.all_loaded = True
            return
        
        # Mark if we loaded less than batch_size (means no more data)
        if len(questions_data) < self.batch_size:
            self.all_loaded = True
        
        # Create scrollable frame on first load
        if not load_more:
            canvas = tk.Canvas(self.questions_container)
            scrollbar = ttk.Scrollbar(self.questions_container, orient=tk.VERTICAL, command=canvas.yview)
            self.scrollable_frame = ttk.Frame(canvas)
            
            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Detect scroll to bottom
            def _on_scroll(*args):
                scrollbar.set(*args)
                # Check if scrolled near bottom
                if float(args[1]) > 0.8 and not self.loading and not self.all_loaded:
                    self.load_more_questions()
            
            canvas.configure(yscrollcommand=_on_scroll)
            
            # Enable mousewheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            def _bind_mousewheel(event):
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            def _unbind_mousewheel(event):
                canvas.unbind_all("<MouseWheel>")
            
            canvas.bind("<Enter>", _bind_mousewheel)
            canvas.bind("<Leave>", _unbind_mousewheel)
            
            self.canvas = canvas
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Display each question
        for data in questions_data:
            self.create_question_card(self.scrollable_frame, data)
        
        # Update offset for next batch
        self.current_offset += len(questions_data)
        self.loading = False

    def load_more_questions(self):
        """Load more questions when scrolling down"""
        if self.loading or self.all_loaded:
            return
        
        self.loading = True
        self.display_questions(load_more=True)

    def show_empty_state(self):
        """Show empty state when no questions found"""
        empty_frame = ttk.Frame(self.questions_container)
        empty_frame.pack(expand=True)
        ttk.Label(empty_frame, text="📋", font=(FONT_FAMILY, 48)).pack(pady=20)
        ttk.Label(empty_frame, text="Không có câu hỏi nào", font=(FONT_FAMILY, 14)).pack(pady=10)

    def create_question_card(self, parent, data):
        """Create card for a question"""
        question = data['question']
        options = data['options']
        
        # Card with better styling
        card = ttk.Frame(parent, bootstyle="light")
        card.pack(fill=tk.X, pady=8, padx=5)
        
        inner = ttk.Frame(card, relief=tk.SOLID, borderwidth=1)
        inner.pack(fill=tk.BOTH, expand=True)
        
        # Question header with badges
        header = ttk.Frame(inner)
        header.pack(fill=tk.X, padx=15, pady=10)
        
        # ID badge
        ttk.Label(header, text=f"#{question.id}",
                 font=(FONT_FAMILY, 10, 'bold'),
                 bootstyle="secondary").pack(side=tk.LEFT, padx=(0, 10))
        
        # Difficulty badge
        difficulty_text = {1: "Dễ", 2: "Trung bình", 3: "Khó"}
        difficulty_style = {1: "success", 2: "warning", 3: "danger"}
        ttk.Label(header, text=difficulty_text.get(question.difficulty, ""),
                 font=(FONT_FAMILY, 9),
                 bootstyle=difficulty_style.get(question.difficulty, "secondary")).pack(side=tk.LEFT, padx=5)
        
        # Category badge
        ttk.Label(header, text=f"📁 {question.category}",
                 font=(FONT_FAMILY, 9),
                 bootstyle="info").pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        btn_frame = ttk.Frame(header)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Sửa",
                  command=lambda q=question: self.edit_question(q),
                  bootstyle="info-outline",
                  width=10).pack(side=tk.LEFT, padx=3)
        
        ttk.Button(btn_frame, text="Xóa",
                  command=lambda q=question: self.delete_question(q),
                  bootstyle="danger-outline",
                  width=10).pack(side=tk.LEFT, padx=3)
        
        # Question text
        text_frame = ttk.Frame(inner)
        text_frame.pack(fill=tk.X, padx=15, pady=10)
        
        ttk.Label(text_frame, text=question.question_text,
                 font=(FONT_FAMILY, 11),
                 wraplength=800).pack(anchor=tk.W)
        
        # Options with better display
        options_frame = ttk.Frame(inner)
        options_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        for i, option in enumerate(options, 1):
            opt_frame = ttk.Frame(options_frame)
            opt_frame.pack(fill=tk.X, pady=2)
            
            if option.is_correct:
                ttk.Label(opt_frame, text=f"{chr(64+i)}. ✓ {option.option_text}",
                         font=(FONT_FAMILY, 10, 'bold'),
                         bootstyle="success").pack(anchor=tk.W, padx=20)
            else:
                ttk.Label(opt_frame, text=f"{chr(64+i)}. {option.option_text}",
                         font=(FONT_FAMILY, 10),
                         bootstyle="secondary").pack(anchor=tk.W, padx=20)

    def create_question_dialog(self, question=None, options=None):
        """Create dialog for add/edit question (DRY principle)"""
        is_edit = question is not None
        
        dialog = tk.Toplevel(self.parent)
        dialog.title("Sửa câu hỏi" if is_edit else "Thêm câu hỏi")
        dialog.geometry("700x600")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog on screen
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Question text
        ttk.Label(dialog, text="Câu hỏi:", font=(FONT_FAMILY, 11, 'bold')).pack(pady=5)
        question_text = tk.Text(dialog, height=3, font=(FONT_FAMILY, 10))
        if is_edit:
            question_text.insert("1.0", question.question_text)
        question_text.pack(fill=tk.X, padx=20, pady=5)
        
        # Category
        cat_frame = ttk.Frame(dialog)
        cat_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(cat_frame, text="Danh mục:").pack(side=tk.LEFT)
        category_entry = ttk.Entry(cat_frame)
        category_entry.insert(0, question.category if is_edit else "General")
        category_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Difficulty
        diff_frame = ttk.Frame(dialog)
        diff_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(diff_frame, text="Độ khó:").pack(side=tk.LEFT)
        
        difficulty_var = tk.IntVar(value=question.difficulty if is_edit else 1)
        for text, value in [("Dễ", 1), ("Trung bình", 2), ("Khó", 3)]:
            ttk.Radiobutton(diff_frame, text=text, variable=difficulty_var, value=value).pack(side=tk.LEFT, padx=5)
        
        # Options
        ttk.Label(dialog, text="Đáp án (chọn đáp án đúng):" if not is_edit else "Đáp án:", 
                 font=(FONT_FAMILY, 11, 'bold')).pack(pady=10)
        
        options_frame = ttk.Frame(dialog)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        correct_var = tk.IntVar(value=0)
        option_entries = []
        
        for i in range(4):
            opt_frame = ttk.Frame(options_frame)
            opt_frame.pack(fill=tk.X, pady=5)
            
            ttk.Radiobutton(opt_frame, variable=correct_var, value=i).pack(side=tk.LEFT)
            entry = ttk.Entry(opt_frame, font=(FONT_FAMILY, 10))
            
            if is_edit and i < len(options):
                entry.insert(0, options[i].option_text)
                if options[i].is_correct:
                    correct_var.set(i)
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            option_entries.append(entry)
        
        # Submit button
        def submit():
            q_text = question_text.get("1.0", tk.END).strip()
            category = category_entry.get().strip()
            difficulty = difficulty_var.get()
            
            if not q_text:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập câu hỏi!")
                return
            
            options_data = []
            for i, entry in enumerate(option_entries):
                opt_text = entry.get().strip()
                if opt_text:
                    options_data.append((opt_text, i == correct_var.get()))
            
            if len(options_data) < 2:
                messagebox.showwarning("Cảnh báo", "Cần ít nhất 2 đáp án!")
                return
            
            try:
                if is_edit:
                    QuestionBankController.update_question_with_options(
                        question.id, q_text, difficulty, category, options_data
                    )
                    messagebox.showinfo("Thành công", "Đã cập nhật câu hỏi!")
                else:
                    QuestionBankController.add_question_with_options(
                        q_text, difficulty, category, options_data
                    )
                    messagebox.showinfo("Thành công", "Đã thêm câu hỏi!")
                
                dialog.destroy()
                self.show_question_list()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        
        btn_text = "Cập nhật" if is_edit else "Thêm câu hỏi"
        ttk.Button(dialog, text=btn_text, command=submit).pack(pady=10)

    def add_question(self):
        """Open dialog to add new question"""
        self.create_question_dialog()

    def edit_question(self, question):
        """Edit existing question"""
        from models.option import Option
        options = Option.get_by_question(question.id)
        self.create_question_dialog(question, options)

    def delete_question(self, question):
        """Delete a question"""
        if messagebox.askyesno("Xác nhận", 
                              f"Bạn có chắc muốn xóa câu hỏi này?\n\n{question.question_text}"):
            QuestionBankController.delete_question(question.id)
            messagebox.showinfo("Thành công", "Đã xóa câu hỏi!")
            self.show_question_list()
