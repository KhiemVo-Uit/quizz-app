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
        
        # Questions container with scroll
        container = ttk.Frame(self.parent)
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        self.questions_container = ttk.Frame(container)
        self.questions_container.pack(fill=tk.BOTH, expand=True)
        
        self.display_questions()

    def filter_questions(self):
        """Filter questions by difficulty"""
        self.display_questions()

    def display_questions(self):
        """Display filtered questions"""
        for widget in self.questions_container.winfo_children():
            widget.destroy()
        
        # Get questions
        difficulty = self.difficulty_var.get()
        if difficulty == "all":
            questions_data = QuestionBankController.get_all_questions_with_options()
        else:
            questions = Question.get_by_difficulty(int(difficulty))
            questions_data = []
            for q in questions:
                from models.option import Option
                options = Option.get_by_question(q.id)
                questions_data.append({'question': q, 'options': options})
        
        if not questions_data:
            empty_frame = ttk.Frame(self.questions_container)
            empty_frame.pack(expand=True)
            
            ttk.Label(empty_frame, text="📋",
                     font=(FONT_FAMILY, 48)).pack(pady=20)
            ttk.Label(empty_frame,
                     text="Không có câu hỏi nào",
                     font=(FONT_FAMILY, 14)).pack(pady=10)
            return
        
        # Create scrollable frame
        canvas = tk.Canvas(self.questions_container)
        scrollbar = ttk.Scrollbar(self.questions_container, orient=tk.VERTICAL, command=canvas.yview)
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
        
        # Display each question
        for data in questions_data:
            self.create_question_card(scrollable_frame, data)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

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

    def add_question(self):
        """Open dialog to add new question"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Thêm câu hỏi")
        dialog.geometry("600x500")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Question text
        ttk.Label(dialog, text="Câu hỏi:", font=(FONT_FAMILY, 11, 'bold')).pack(pady=5)
        question_text = tk.Text(dialog, height=3, font=(FONT_FAMILY, 10))
        question_text.pack(fill=tk.X, padx=20, pady=5)
        
        # Category
        cat_frame = ttk.Frame(dialog)
        cat_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(cat_frame, text="Danh mục:").pack(side=tk.LEFT)
        category_entry = ttk.Entry(cat_frame)
        category_entry.insert(0, "General")
        category_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Difficulty
        diff_frame = ttk.Frame(dialog)
        diff_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(diff_frame, text="Độ khó:").pack(side=tk.LEFT)
        
        difficulty_var = tk.IntVar(value=1)
        ttk.Radiobutton(diff_frame, text="Dễ", variable=difficulty_var, value=1).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(diff_frame, text="Trung bình", variable=difficulty_var, value=2).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(diff_frame, text="Khó", variable=difficulty_var, value=3).pack(side=tk.LEFT, padx=5)
        
        # Options
        ttk.Label(dialog, text="Đáp án (chọn đáp án đúng):", font=(FONT_FAMILY, 11, 'bold')).pack(pady=10)
        
        options_frame = ttk.Frame(dialog)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        correct_var = tk.IntVar(value=0)
        option_entries = []
        
        for i in range(4):
            opt_frame = ttk.Frame(options_frame)
            opt_frame.pack(fill=tk.X, pady=5)
            
            ttk.Radiobutton(opt_frame, variable=correct_var, value=i).pack(side=tk.LEFT)
            entry = ttk.Entry(opt_frame, font=(FONT_FAMILY, 10))
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
                QuestionBankController.add_question_with_options(
                    q_text, difficulty, category, options_data
                )
                messagebox.showinfo("Thành công", "Đã thêm câu hỏi!")
                dialog.destroy()
                self.show_question_list()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        
        ttk.Button(dialog, text="Thêm câu hỏi", command=submit).pack(pady=10)

    def edit_question(self, question):
        """Edit existing question"""
        from models.option import Option
        options = Option.get_by_question(question.id)
        
        dialog = tk.Toplevel(self.parent)
        dialog.title("Sửa câu hỏi")
        dialog.geometry("600x500")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Question text
        ttk.Label(dialog, text="Câu hỏi:", font=(FONT_FAMILY, 11, 'bold')).pack(pady=5)
        question_text = tk.Text(dialog, height=3, font=(FONT_FAMILY, 10))
        question_text.insert("1.0", question.question_text)
        question_text.pack(fill=tk.X, padx=20, pady=5)
        
        # Category
        cat_frame = ttk.Frame(dialog)
        cat_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(cat_frame, text="Danh mục:").pack(side=tk.LEFT)
        category_entry = ttk.Entry(cat_frame)
        category_entry.insert(0, question.category)
        category_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Difficulty
        diff_frame = ttk.Frame(dialog)
        diff_frame.pack(fill=tk.X, padx=20, pady=5)
        ttk.Label(diff_frame, text="Độ khó:").pack(side=tk.LEFT)
        
        difficulty_var = tk.IntVar(value=question.difficulty)
        ttk.Radiobutton(diff_frame, text="Dễ", variable=difficulty_var, value=1).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(diff_frame, text="Trung bình", variable=difficulty_var, value=2).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(diff_frame, text="Khó", variable=difficulty_var, value=3).pack(side=tk.LEFT, padx=5)
        
        # Options
        ttk.Label(dialog, text="Đáp án:", font=(FONT_FAMILY, 11, 'bold')).pack(pady=10)
        
        options_frame = ttk.Frame(dialog)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        correct_var = tk.IntVar(value=0)
        option_entries = []
        
        for i, option in enumerate(options[:4]):
            opt_frame = ttk.Frame(options_frame)
            opt_frame.pack(fill=tk.X, pady=5)
            
            if option.is_correct:
                correct_var.set(i)
            
            ttk.Radiobutton(opt_frame, variable=correct_var, value=i).pack(side=tk.LEFT)
            entry = ttk.Entry(opt_frame, font=(FONT_FAMILY, 10))
            entry.insert(0, option.option_text)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            option_entries.append(entry)
        
        # Submit button
        def submit():
            q_text = question_text.get("1.0", tk.END).strip()
            category = category_entry.get().strip()
            difficulty = difficulty_var.get()
            
            options_data = []
            for i, entry in enumerate(option_entries):
                opt_text = entry.get().strip()
                if opt_text:
                    options_data.append((opt_text, i == correct_var.get()))
            
            try:
                QuestionBankController.update_question_with_options(
                    question.id, q_text, difficulty, category, options_data
                )
                messagebox.showinfo("Thành công", "Đã cập nhật câu hỏi!")
                dialog.destroy()
                self.show_question_list()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        
        ttk.Button(dialog, text="Cập nhật", command=submit).pack(pady=10)

    def delete_question(self, question):
        """Delete a question"""
        if messagebox.askyesno("Xác nhận", 
                              f"Bạn có chắc muốn xóa câu hỏi này?\n\n{question.question_text}"):
            QuestionBankController.delete_question(question.id)
            messagebox.showinfo("Thành công", "Đã xóa câu hỏi!")
            self.show_question_list()
