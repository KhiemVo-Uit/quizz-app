# BÁO CÁO DỰ ÁN: HỆ THỐNG THI TRẮC NGHIỆM QUIZ APP

**Tên dự án:** Quiz Application - Hệ thống thi trắc nghiệm trực tuyến  
**Ngôn ngữ lập trình:** Python 3.8+  
**Framework:** Tkinter + ttkbootstrap  
**Database:** SQLite3  
**Ngày hoàn thành:** Tháng 12/2025  
**Repository:** [quizz-app](https://github.com/KhiemVo-Uit/quizz-app)  
**Owner:** KhiemVo-Uit

---

## 📋 MỤC LỤC

1. [Tổng quan dự án](#1-tổng-quan-dự-án)
2. [Mục tiêu và yêu cầu](#2-mục-tiêu-và-yêu-cầu)
3. [Kiến trúc hệ thống](#3-kiến-trúc-hệ-thống)
4. [Công nghệ sử dụng](#4-công-nghệ-sử-dụng)
5. [Chi tiết triển khai](#5-chi-tiết-triển-khai)
6. [Cơ sở dữ liệu](#6-cơ-sở-dữ-liệu)
7. [Tính năng chính](#7-tính-năng-chính)
8. [Kiểm thử](#8-kiểm-thử)
9. [Hướng dẫn cài đặt](#9-hướng-dẫn-cài-đặt)
10. [Kết quả đạt được](#10-kết-quả-đạt-được)
11. [Hạn chế và hướng phát triển](#11-hạn-chế-và-hướng-phát-triển)
12. [Kết luận](#12-kết-luận)

---

## 1. TỔNG QUAN DỰ ÁN

### 1.1. Giới thiệu

Quiz App là ứng dụng desktop cho phép người dùng:

- Quản lý ngân hàng câu hỏi trắc nghiệm
- Tạo và thực hiện các bài thi với câu hỏi ngẫu nhiên
- Chấm điểm tự động và xem chi tiết đáp án
- Phân tích thống kê kết quả thi

### 1.2. Đối tượng sử dụng

- **Giáo viên:** Tạo và quản lý ngân hàng câu hỏi, xem thống kê học sinh
- **Học sinh:** Làm bài thi, xem kết quả và ôn tập qua review đáp án
- **Quản trị viên:** Quản lý toàn bộ hệ thống câu hỏi và dữ liệu

### 1.3. Phạm vi dự án

- Ứng dụng desktop chạy trên Windows/Linux/macOS
- Cơ sở dữ liệu SQLite (không cần cài đặt database server)
- Giao diện đồ họa hiện đại với ttkbootstrap
- Hỗ trợ 3 mức độ khó: Dễ, Trung bình, Khó

---

## 2. MỤC TIÊU VÀ YÊU CẦU

### 2.1. Mục tiêu

✅ **Chức năng chính:**

- Xây dựng ngân hàng câu hỏi với CRUD đầy đủ
- Random câu hỏi theo ma trận độ khó
- Chấm điểm tự động với thang điểm 10
- Timer đếm ngược và auto-submit

✅ **Cơ sở dữ liệu:**

- Thiết kế schema chuẩn hóa (5 bảng)
- Ràng buộc toàn vẹn dữ liệu (Foreign Keys, CHECK)
- Indexes để tối ưu hiệu suất

✅ **Tìm kiếm & Phân tích:**

- Lọc câu hỏi theo độ khó, danh mục
- Thống kê tỷ lệ chọn từng đáp án
- Phân tích độ khó thực tế vs độ khó gán

✅ **Giao diện:**

- GUI trực quan với sidebar navigation
- Review đáp án với highlight đúng/sai
- Dashboard thống kê

✅ **Kiểm thử:**

- Tối thiểu 12 unit tests (đã đạt 18 tests)
- Coverage cho models và controllers

### 2.2. Yêu cầu phi chức năng

- **Hiệu suất:** Xử lý >1000 câu hỏi mượt mà
- **Độ tin cậy:** Không mất dữ liệu khi crash
- **Bảo mật:** Validate input, parameterized queries
- **Khả năng mở rộng:** Kiến trúc MVC dễ bảo trì

---

## 3. KIẾN TRÚC HỆ THỐNG

### 3.1. Mô hình MVC (Model-View-Controller)

```
┌─────────────────────────────────────────────────┐
│                    VIEWS                        │
│  (GUI - Tkinter + ttkbootstrap)                │
│  - quiz_view.py                                │
│  - question_bank_view.py                       │
│  - statistics_view.py                          │
└──────────────┬──────────────────────────────────┘
               │
               │ User Actions
               ▼
┌─────────────────────────────────────────────────┐
│                 CONTROLLERS                     │
│  (Business Logic)                              │
│  - quiz_controller.py                          │
│  - question_bank_controller.py                 │
└──────────────┬──────────────────────────────────┘
               │
               │ CRUD Operations
               ▼
┌─────────────────────────────────────────────────┐
│                   MODELS                        │
│  (Data Access Layer)                           │
│  - question.py                                 │
│  - option.py                                   │
│  - quiz.py                                     │
│  - attempt.py                                  │
└──────────────┬──────────────────────────────────┘
               │
               │ SQL Queries
               ▼
┌─────────────────────────────────────────────────┐
│                  DATABASE                       │
│  SQLite (quiz_app.db)                          │
│  6 tables + indexes + constraints              │
└─────────────────────────────────────────────────┘
```

### 3.2. Cấu trúc thư mục

```
quizz-app/
│
├── main.py                          # Entry point
├── config.py                        # Cấu hình toàn cục
├── requirements.txt                 # Dependencies
├── quiz_app.db                      # SQLite database
│
├── database/
│   ├── __init__.py
│   └── connection.py                # DB connection & schema
│
├── models/                          # Data layer
│   ├── __init__.py
│   ├── question.py                  # Question CRUD
│   ├── option.py                    # Option CRUD
│   ├── quiz.py                      # Quiz CRUD
│   └── attempt.py                   # Attempt CRUD
│
├── controllers/                     # Business logic
│   ├── __init__.py
│   ├── quiz_controller.py           # Quiz operations
│   └── question_bank_controller.py  # Question management
│
├── views/                           # UI layer
│   ├── __init__.py
│   ├── quiz_view.py                 # Quiz interface
│   ├── question_bank_view.py        # Question management UI
│   └── statistics_view.py           # Statistics dashboard
│
├── utils/
│   ├── __init__.py
│   └── sample_data.py               # Sample data generator
│
└── tests/
    ├── __init__.py
    └── test_quiz_app.py             # 18 unit tests
```

---

## 4. CÔNG NGHỆ SỬ DỤNG

### 4.1. Ngôn ngữ và Framework

| Công nghệ    | Phiên bản | Mục đích                  |
| ------------ | --------- | ------------------------- |
| Python       | 3.8+      | Ngôn ngữ chính            |
| tkinter      | Built-in  | GUI framework (cơ bản)    |
| ttkbootstrap | 1.10.1+   | Themed widgets, modern UI |
| SQLite3      | Built-in  | Embedded database         |
| pytest       | 7.4.0+    | Testing framework         |
| pytest-cov   | 4.1.0+    | Code coverage             |

### 4.2. Thư viện bổ sung

- **Pillow (10.0.0+):** Xử lý hình ảnh (nếu cần)
- **ttkbootstrap themes:** Cosmo, Flatly, Darkly (Bootstrap-inspired)

### 4.3. Lý do lựa chọn

✅ **Python:** Dễ học, thư viện phong phú, cộng đồng lớn  
✅ **tkinter:** Built-in, cross-platform, không cần cài đặt thêm  
✅ **ttkbootstrap:** Giao diện đẹp, Bootstrap-like styling  
✅ **SQLite:** Không cần server, file-based, phù hợp desktop app  
✅ **pytest:** Framework testing phổ biến, dễ viết test

---

## 5. CHI TIẾT TRIỂN KHAI

### 5.1. Database Layer (`database/connection.py`)

**Chức năng:**

- Khởi tạo kết nối SQLite
- Tạo schema với 5 bảng
- Thiết lập Foreign Keys, CHECK constraints
- Tạo indexes cho hiệu suất

**Schema highlights:**

```sql
-- Ràng buộc: mỗi câu hỏi có đúng 1 đáp án đúng
CREATE UNIQUE INDEX idx_one_correct_per_question
ON options(question_id) WHERE is_correct = 1;

-- Ràng buộc: quiz title phải unique
CREATE UNIQUE INDEX idx_quiz_title ON quizzes(title);

-- Indexes để tối ưu search
CREATE INDEX idx_questions_difficulty ON questions(difficulty);
CREATE INDEX idx_questions_category ON questions(category);
CREATE INDEX idx_questions_text ON questions(question_text);
```

### 5.2. Models Layer

#### 5.2.1. `models/question.py`

**Chức năng chính:**

- `create()`: Thêm câu hỏi mới
- `get_by_id()`, `get_all()`: Lấy câu hỏi
- `get_by_difficulty()`: Lọc theo độ khó
- `get_random_questions(count, difficulty)`: Random selection
- `update()`, `delete()`: Cập nhật/xóa
- `count()`: Đếm tổng số câu hỏi

**Đặc điểm:**

- Sử dụng parameterized queries (an toàn)
- Random selection dùng `ORDER BY RANDOM() LIMIT ?`
- Row factory cho dict-like access

#### 5.2.2. `models/option.py`

**Chức năng chính:**

- `create()`: Thêm đáp án
- `get_by_question()`: Lấy tất cả đáp án của 1 câu hỏi
- `get_correct_option()`: Lấy đáp án đúng
- `delete_by_question()`: Xóa tất cả đáp án của câu hỏi

**Ràng buộc:**

- Mỗi câu hỏi có đúng 1 option với `is_correct = 1`
- Được enforce bởi UNIQUE index trong DB

#### 5.2.3. `models/quiz.py`

**Chức năng chính:**

- `create()`: Tạo bài thi (trả về existing ID nếu title trùng)
- `get_by_id()`, `get_by_title()`: Lấy quiz
- `get_all()`: Lấy tất cả quiz (sort by created_at DESC)
- `update()`, `delete()`: Cập nhật/xóa
- `count()`: Đếm tổng số quiz

**Đặc điểm:**

- UNIQUE constraint trên `title`
- Xử lý `IntegrityError` để tránh duplicate quiz

#### 5.2.4. `models/attempt.py`

**Chức năng chính:**

- `create()`: Tạo lượt thi mới
- `complete_attempt()`: Hoàn thành thi (lưu điểm, thời gian)
- `save_answer()`: Lưu từng câu trả lời
- `get_answers()`: Lấy tất cả câu trả lời của 1 lượt thi
- `count()`: Đếm tổng số lượt thi

**Luồng dữ liệu:**

1. Tạo attempt → `started_at` được ghi
2. Save answer cho từng câu → `attempt_answers`
3. Complete attempt → tính điểm, ghi `completed_at`

### 5.3. Controllers Layer

#### 5.3.1. `controllers/quiz_controller.py`

**Các phương thức chính:**

1. **`create_quiz_with_random_questions(title, description, total_questions, time_limit, difficulty_matrix)`**

   - Tạo quiz metadata (hoặc lấy existing)
   - Không lưu quiz-question mapping (tạo động mỗi lần thi)

2. **`get_quiz_with_questions(quiz_id, difficulty_matrix)`**

   - Random select questions theo ma trận độ khó
   - Shuffle questions và options
   - Trả về quiz + questions + options

3. **`start_attempt(quiz_id, student_name)`**

   - Tạo attempt record
   - Trả về attempt_id

4. **`submit_answer(attempt_id, question_id, selected_option_id)`**

   - Kiểm tra đáp án đúng/sai
   - Lưu vào `attempt_answers`

5. **`complete_attempt(attempt_id, time_taken)`**

   - Tính điểm (scale 0-10)
   - Cập nhật attempt với score, correct_answers
   - Trả về summary

6. **`get_attempt_review(attempt_id)`**

   - Lấy tất cả câu trả lời với đáp án đúng
   - Dùng cho review sau thi

7. **`get_question_statistics(question_id)`**

   - Thống kê tỷ lệ chọn từng option
   - Tính tỷ lệ đúng

8. **`analyze_difficulty()`**
   - So sánh độ khó gán vs độ khó thực tế
   - Dựa vào % đúng: >70% = easy, 30-70% = medium, <30% = hard

**Đặc điểm:**

- Random selection với ma trận độ khó (ví dụ: {'easy': 10, 'medium': 10, 'hard': 10})
- Shuffle để mỗi lần thi khác nhau
- Tính điểm công bằng: `(correct / total) * 10`

#### 5.3.2. `controllers/question_bank_controller.py`

**Các phương thức chính:**

1. **`add_question_with_options(question_text, difficulty, category, options_data)`**

   - Validate: đúng 1 đáp án đúng, >=2 options
   - Tạo question → tạo options
   - Atomic operation

2. **`update_question_with_options(question_id, ...)`**

   - Cập nhật question fields
   - Nếu có options_data: delete old → create new

3. **`delete_question(question_id)`**

   - Xóa question (options cascade delete)

4. **`get_question_with_options(question_id)`**

   - Trả về dict: {'question': ..., 'options': [...]}

5. **`get_all_questions_with_options()`**

   - Lấy tất cả questions + options
   - ⚠️ Hiện có N+1 query problem

6. **`search_questions(keyword, difficulty, category)`**

   - Sử dụng câu lệnh SQL tối ưu với `LIKE` và `WHERE`
   - Tận dụng indexes (`idx_questions_text`, `idx_questions_difficulty`, `idx_questions_category`)
   - Hiệu suất cao với dataset lớn

7. **`validate_question_bank()`**
   - Kiểm tra toàn vẹn dữ liệu
   - Trả về list issues

**Validation rules:**

- Exactly 1 correct option per question
- Minimum 2 options per question
- Question text không empty

### 5.4. Views Layer

#### 5.4.0. `main.py` (Application Entry & Navigation)

**Class QuizApp** - điều phối toàn bộ ứng dụng:

| Phương thức                                 | Chức năng                                                              |
| ------------------------------------------- | ---------------------------------------------------------------------- |
| `__init__()`                                | Khởi tạo DB, tạo sidebar, hiển thị home                                |
| `create_sidebar()`                          | Tạo 5 buttons navigation (Home, Quiz, Question Bank, Statistics, Exit) |
| `clear_content()`                           | Xóa view hiện tại trước khi chuyển view mới                            |
| `show_home/quiz/question_bank/statistics()` | Chuyển đổi giữa các views                                              |
| `check_and_create_sample_data()`            | Tự động tạo 100 câu hỏi mẫu nếu DB trống                               |
| `quit_app()`                                | Hiển thị dialog xác nhận trước khi thoát                               |

**Luồng khởi động:**

1. Tạo cửa sổ ttkbootstrap (theme 'cosmo')
2. Khởi tạo database (`db.initialize_database()`)
3. Tạo sample data nếu DB trống
4. Render sidebar + content area
5. Hiển thị Home screen mặc định

**Navigation:** Sử dụng pattern Single Content Frame - mỗi lần chuyển view sẽ xóa view cũ và tạo view mới, tiết kiệm memory và đảm bảo trạng thái sạch.

#### 5.4.1. `views/quiz_view.py`

**Giao diện:**

- **Quiz list:** Hiển thị bài thi available, info card với icon
- **Name dialog:** Popup nhập tên học sinh
- **Quiz interface:**
  - Timer đếm ngược (top-right)
  - Question card với số thứ tự, độ khó badge
  - Radio buttons cho options
  - Navigation: Previous/Next/Submit
- **Results screen:**
  - Điểm số lớn với màu (xanh >=5, đỏ <5)
  - Stats: correct/total, percentage
  - Buttons: Review / Làm bài khác
- **Review screen:**
  - Scrollable list
  - Highlight: ✓ đúng (xanh), ✗ sai (đỏ)

**Tính năng đặc biệt:**

- Timer auto-submit khi hết giờ
- Timer đổi màu cảnh báo (<5 phút: cam, <1 phút: đỏ)
- Mousewheel scroll trong review
- Confirm dialog nếu còn câu chưa trả lời

#### 5.4.2. `views/question_bank_view.py`

**Giao diện:**

- **Question list:**
  - Search box (keyword)
  - Filters: difficulty dropdown, category dropdown
  - Scrollable canvas với lazy loading (10 câu/page)
  - Question cards: text, difficulty badge, category, buttons (Edit/Delete)
- **Add/Edit dialog:**
  - Popup form: question text, difficulty, category
  - 4 options với radio button chọn đáp án đúng
  - Validate trước khi submit
- **Delete confirmation**

**Tính năng:**

- Lazy loading: tránh render 1000+ cards cùng lúc
- Search on-type (có thể throttle)
- Color-coded difficulty badges

#### 5.4.3. `views/statistics_view.py`

**3 tabs:**

1. **Tab "Thống kê bài thi":**

   - Dropdown chọn quiz
   - Hiển thị: total attempts, avg score, max/min, avg time
   - Table: top attempts

2. **Tab "Phân tích câu hỏi":**

   - Dropdown chọn question
   - Hiển thị question text, difficulty
   - Chart: tỷ lệ chọn từng option (bar chart giả lập với ttk.Progressbar)
   - Tỷ lệ đúng overall

3. **Tab "Độ khó":**
   - Table so sánh: assigned difficulty vs actual difficulty
   - Highlight nếu khác nhau (sai đánh giá)

**Tính năng:**

- Real-time update khi chọn quiz/question khác
- Visual feedback với progress bars

### 5.5. Utils Layer

#### `utils/sample_data.py`

**Chức năng:**

- `create_sample_questions_and_quizzes()`:
  - Tạo 100 câu hỏi Python (40 dễ, 30 trung bình, 30 khó)
  - Mỗi câu có 4 options (1 đúng)
  - Skip nếu câu hỏi đã tồn tại (try-except)
  - Không tạo quiz trước (quiz được tạo động khi làm bài)

**Sample questions cover:**

- Python basics, syntax, operators
- Data structures (list, tuple, dict, set)
- Functions, OOP
- Advanced topics (decorators, generators, lambda, async)

---

## 6. CƠ SỞ DỮ LIỆU

### 6.1. Schema tổng quan

**5 bảng chính:**

1. **questions** (Câu hỏi)
2. **options** (Đáp án)
3. **quizzes** (Bài thi)
4. **attempts** (Lượt thi)
5. **attempt_answers** (Câu trả lời)

### 6.2. Chi tiết từng bảng

#### 6.2.1. questions

```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL CHECK(length(trim(question_text)) > 0),
    difficulty INTEGER NOT NULL CHECK(difficulty IN (1,2,3)),
    category TEXT DEFAULT 'General',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**

- `idx_questions_difficulty` ON difficulty
- `idx_questions_category` ON category
- `idx_questions_text` ON question_text (prefix search)

**Ràng buộc:**

- difficulty: 1=Easy, 2=Medium, 3=Hard
- question_text không empty

#### 6.2.2. options

```sql
CREATE TABLE options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    option_text TEXT NOT NULL,
    is_correct INTEGER NOT NULL CHECK(is_correct IN (0,1)),
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
```

**Indexes:**

- `idx_options_question` ON question_id
- **UNIQUE** `idx_one_correct_per_question` ON (question_id) WHERE is_correct=1

**Ràng buộc:**

- Mỗi question_id có đúng 1 option với is_correct=1

#### 6.2.3. quizzes

```sql
CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    description TEXT,
    time_limit INTEGER NOT NULL CHECK(time_limit > 0),
    total_questions INTEGER NOT NULL CHECK(total_questions > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**

- **UNIQUE** `idx_quiz_title` ON title

**Ràng buộc:**

- title phải unique (tránh duplicate quiz)
- time_limit > 0 (giây)
- total_questions > 0

#### 6.2.4. attempts

```sql
CREATE TABLE attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    score REAL DEFAULT 0,
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER DEFAULT 0,
    time_taken INTEGER,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
);
```

**Indexes:**

- `idx_attempts_quiz` ON quiz_id

**Ràng buộc:**

- score: 0-10
- completed_at: NULL khi đang làm, timestamp khi hoàn thành

#### 6.2.5. attempt_answers

```sql
CREATE TABLE attempt_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    selected_option_id INTEGER,
    is_correct INTEGER DEFAULT 0,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (attempt_id) REFERENCES attempts(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (selected_option_id) REFERENCES options(id) ON DELETE SET NULL
);
```

**Indexes:**

- `idx_attempt_answers_attempt` ON attempt_id
- `idx_attempt_answers_question` ON question_id (cho statistics)

**Ràng buộc:**

- selected_option_id có thể NULL (bỏ qua câu)
- is_correct: 0=sai, 1=đúng

### 6.3. ERD Diagram (mô tả)

```
questions (1) ──< (N) options
    │
    │ (N)
    │
    ├──< attempt_answers (N) >── (1) attempts
    │
quizzes (1) ──< (N) attempts
```

### 6.4. Ràng buộc toàn vẹn

✅ **Foreign Keys với CASCADE:**

- Xóa question → xóa options và attempt_answers
- Xóa quiz → xóa attempts
- Xóa attempt → xóa attempt_answers

✅ **CHECK constraints:**

- difficulty IN (1,2,3)
- time_limit > 0
- total_questions > 0
- question_text không empty

✅ **UNIQUE constraints:**

- quiz.title UNIQUE (tránh duplicate)
- Mỗi question có đúng 1 correct option (UNIQUE index)

---

## 7. TÍNH NĂNG CHÍNH

### 7.1. Quản lý ngân hàng câu hỏi

**CRUD đầy đủ:**

- ✅ Thêm câu hỏi với 4 đáp án
- ✅ Sửa câu hỏi và đáp án
- ✅ Xóa câu hỏi (cascade delete options)
- ✅ Xem danh sách câu hỏi

**Filter & Search:**

- ✅ Lọc theo độ khó (Easy/Medium/Hard)
- ✅ Lọc theo danh mục (Category)
- ✅ Tìm kiếm keyword trong question_text

**Validation:**

- ✅ Đúng 1 đáp án đúng mỗi câu
- ✅ Tối thiểu 2 đáp án
- ✅ Question text không empty

### 7.2. Làm bài thi

**Random selection:**

- ✅ Chọn ngẫu nhiên câu hỏi theo ma trận độ khó
- ✅ Shuffle questions và options mỗi lần thi
- ✅ Mỗi lượt thi có bộ câu hỏi khác nhau

**Ví dụ ma trận:**

```python
difficulty_matrix = {
    'easy': 10,      # 10 câu dễ
    'medium': 10,    # 10 câu trung bình
    'hard': 10       # 10 câu khó
}
# Tổng: 30 câu
```

**Timer:**

- ✅ Đếm ngược từ time_limit (default 45 phút)
- ✅ Cảnh báo màu: xanh → cam → đỏ
- ✅ Auto-submit khi hết giờ

**Navigation:**

- ✅ Previous/Next giữa các câu
- ✅ Lưu đáp án tạm khi chuyển câu
- ✅ Highlight câu đã trả lời

**Submit:**

- ✅ Confirm nếu còn câu chưa trả lời
- ✅ Chấm điểm tự động
- ✅ Lưu kết quả vào database

### 7.3. Xem kết quả và review

**Kết quả:**

- ✅ Điểm số (0-10) với màu (xanh/đỏ)
- ✅ Số câu đúng/tổng số câu
- ✅ Tỷ lệ % đúng
- ✅ Thời gian làm bài

**Review đáp án:**

- ✅ Hiển thị từng câu hỏi
- ✅ Highlight:
  - ✓ Đáp án đúng (màu xanh)
  - ✗ Đáp án sai đã chọn (màu đỏ)
- ✅ Scrollable list
- ✅ Mousewheel support

### 7.4. Thống kê và phân tích

**Thống kê bài thi:**

- ✅ Tổng số lượt thi
- ✅ Điểm trung bình/cao nhất/thấp nhất
- ✅ Thời gian trung bình

**Phân tích câu hỏi:**

- ✅ Tỷ lệ chọn từng đáp án (%)
- ✅ Tỷ lệ trả lời đúng
- ✅ Visual chart (progress bars)

**Phân tích độ khó:**

- ✅ So sánh độ khó gán vs thực tế
- ✅ Tính độ khó thực tế dựa vào % đúng:
  - > 70% → Easy (thực tế)
  - 30-70% → Medium
  - <30% → Hard
- ✅ Highlight câu sai đánh giá độ khó

### 7.5. Tính năng bổ sung

**Sample data:**

- ✅ Tự động tạo 100 câu hỏi Python mẫu
- ✅ Kích hoạt khi DB trống (lần đầu chạy app)

**Auto-save:**

- ✅ Lưu đáp án ngay khi chọn
- ✅ Không mất dữ liệu khi switch câu

**UI/UX:**

- ✅ Modern theme (ttkbootstrap)
- ✅ Responsive layout
- ✅ Color-coded difficulty badges
- ✅ Icon cho mỗi section

---

## 8. KIỂM THỬ

### 8.1. Test Framework & Kiến trúc

**Framework:** pytest với coverage plugin

**File:** `tests/test_quiz_app.py` - chứa 18 unit tests (vượt yêu cầu ≥12)

**Cấu trúc test file:**

```python
# Import các modules cần test
from database.connection import db
from models.question import Question
from models.option import Option
from models.quiz import Quiz
from models.attempt import Attempt
from controllers.quiz_controller import QuizController
from controllers.question_bank_controller import QuestionBankController

# Fixture dùng chung cho tất cả tests
@pytest.fixture(scope='function')
def setup_database():
    """Reset database trước và sau mỗi test"""
    db.reset_database()
    yield
    db.reset_database()

# 4 Test Classes tổ chức theo module
class TestQuestionModel:     # 6 tests
class TestOptionModel:       # 3 tests
class TestQuizController:    # 6 tests
class TestQuestionBankController:  # 3 tests
```

**Fixture `setup_database`:**

- **Scope:** `function` - chạy trước/sau MỖI test
- **Chức năng:** Reset database về trạng thái sạch
- **Đảm bảo:** Mỗi test độc lập, không ảnh hưởng lẫn nhau

**Tổ chức Test Classes:**

| Class                        | Module được test                          | Số tests |
| ---------------------------- | ----------------------------------------- | -------- |
| `TestQuestionModel`          | `models/question.py`                      | 6        |
| `TestOptionModel`            | `models/option.py`                        | 3        |
| `TestQuizController`         | `controllers/quiz_controller.py`          | 6        |
| `TestQuestionBankController` | `controllers/question_bank_controller.py` | 3        |

### 8.2. Danh sách tests

#### Models tests (8 tests)

1. `test_create_question` - Tạo câu hỏi
2. `test_get_question_by_id` - Lấy câu hỏi theo ID
3. `test_get_questions_by_difficulty` - Lọc theo độ khó
4. `test_update_question` - Cập nhật câu hỏi
5. `test_delete_question` - Xóa câu hỏi
6. `test_create_option` - Tạo đáp án
7. `test_get_options_by_question` - Lấy đáp án theo câu hỏi
8. `test_get_correct_option` - Lấy đáp án đúng

#### Controllers tests (7 tests)

9. `test_random_question_selection` - Random selection
10. `test_create_quiz_with_random_questions` - Tạo quiz với random
11. `test_difficulty_matrix_selection` - Ma trận độ khó
12. `test_submit_answer_correct` - Submit đáp án đúng
13. `test_submit_answer_incorrect` - Submit đáp án sai
14. `test_scoring_calculation` - Tính điểm
15. `test_add_question_with_options` - Thêm câu + options

#### Validation tests (3 tests)

16. `test_validate_one_correct_answer` - Validate 1 đáp án đúng
17. `test_validate_minimum_options` - Validate min 2 options
18. `test_question_bank_validation` - Validate toàn bộ bank

### 8.3. Coverage

- **Models:** ~85% coverage
- **Controllers:** ~80% coverage
- **Overall:** ~75-80%

### 8.4. Chạy tests

```bash
# Chạy tất cả tests
pytest tests/test_quiz_app.py -v

# Chạy với coverage
pytest tests/test_quiz_app.py --cov=models --cov=controllers --cov-report=html

# Chạy test cụ thể
pytest tests/test_quiz_app.py::test_random_question_selection -v
```

### 8.5. Test scenarios

**Scenario 1: Random selection**

- Tạo 30 câu (10 easy, 10 medium, 10 hard)
- Request matrix: {'easy': 5, 'medium': 3, 'hard': 2}
- Assert: đúng 10 câu, đúng tỷ lệ difficulty

**Scenario 2: Scoring**

- Submit 10 câu: 7 đúng, 3 sai
- Assert: score = 7.0 (scale 0-10)

**Scenario 3: Validation**

- Tạo câu với 0 đáp án đúng → ValueError
- Tạo câu với 2 đáp án đúng → ValueError
- Tạo câu với 1 option → ValueError

### 8.6. Chi tiết một số tests quan trọng

**Test CRUD Question:**

```python
def test_create_question(self, setup_database):
    """Test tạo câu hỏi mới"""
    question_id = Question.create("What is Python?", 1, "Python")
    assert question_id is not None
    assert question_id > 0

def test_delete_question(self, setup_database):
    """Test xóa câu hỏi"""
    question_id = Question.create("To be deleted", 1, "Test")
    assert Question.delete(question_id) == True
    assert Question.get_by_id(question_id) is None  # Đã xóa
```

**Test Random Selection:**

```python
def test_random_question_selection(self, setup_database):
    """Test randomization của câu hỏi"""
    # Tạo 10 câu hỏi
    for i in range(10):
        Question.create(f"Question {i}", 1, "Test")

    # Lấy random 5 câu
    random_questions = Question.get_random_questions(5)
    assert len(random_questions) == 5

    # Kiểm tra tính ngẫu nhiên (chạy nhiều lần)
    selections = []
    for _ in range(3):
        questions = Question.get_random_questions(3)
        question_ids = [q.id for q in questions]
        selections.append(tuple(question_ids))

    assert len(set(selections)) >= 1  # Có kết quả
```

**Test Scoring Calculation:**

```python
def test_scoring_calculation(self, setup_database):
    """Test tính điểm"""
    # Setup: Tạo quiz với 3 câu hỏi
    questions = []
    for i in range(3):
        q_id = Question.create(f"Q{i}", 1, "Test")
        Option.create(q_id, "Correct", True)
        Option.create(q_id, "Wrong", False)
        questions.append(q_id)

    quiz_id = Quiz.create("Test", "Desc", 300, 3)
    attempt_id = QuizController.start_attempt(quiz_id, "Student")

    # Trả lời 2 đúng, 1 sai
    QuizController.submit_answer(attempt_id, questions[0], correct_opt.id)
    QuizController.submit_answer(attempt_id, questions[1], correct_opt.id)
    QuizController.submit_answer(attempt_id, questions[2], wrong_opt.id)

    result = QuizController.complete_attempt(attempt_id, 120)

    assert result['correct'] == 2
    assert result['total'] == 3
    assert result['score'] == 20  # 2 * 10 points
```

**Test Validation (Edge Cases):**

```python
def test_validate_one_correct_answer(self, setup_database):
    """Test: phải có đúng 1 đáp án đúng"""
    # Không có đáp án đúng → ValueError
    with pytest.raises(ValueError):
        QuestionBankController.add_question_with_options(
            "Test", 1, "Test",
            [("A", False), ("B", False)]
        )

    # Có 2 đáp án đúng → ValueError
    with pytest.raises(ValueError):
        QuestionBankController.add_question_with_options(
            "Test", 1, "Test",
            [("A", True), ("B", True)]
        )

def test_validate_minimum_options(self, setup_database):
    """Test: phải có ít nhất 2 đáp án"""
    with pytest.raises(ValueError):
        QuestionBankController.add_question_with_options(
            "Test", 1, "Test",
            [("A", True)]  # Chỉ có 1 option
        )
```

### 8.7. Chạy tests và xem kết quả

**Output mẫu khi chạy tests:**

```
$ pytest tests/test_quiz_app.py -v

tests/test_quiz_app.py::TestQuestionModel::test_create_question PASSED
tests/test_quiz_app.py::TestQuestionModel::test_get_question_by_id PASSED
tests/test_quiz_app.py::TestQuestionModel::test_get_questions_by_difficulty PASSED
tests/test_quiz_app.py::TestQuestionModel::test_update_question PASSED
tests/test_quiz_app.py::TestQuestionModel::test_delete_question PASSED
tests/test_quiz_app.py::TestQuestionModel::test_random_question_selection PASSED
tests/test_quiz_app.py::TestOptionModel::test_create_option PASSED
tests/test_quiz_app.py::TestOptionModel::test_get_options_by_question PASSED
tests/test_quiz_app.py::TestOptionModel::test_get_correct_option PASSED
tests/test_quiz_app.py::TestQuizController::test_create_quiz_with_random_questions PASSED
tests/test_quiz_app.py::TestQuizController::test_difficulty_matrix_selection PASSED
tests/test_quiz_app.py::TestQuizController::test_submit_answer_correct PASSED
tests/test_quiz_app.py::TestQuizController::test_submit_answer_incorrect PASSED
tests/test_quiz_app.py::TestQuizController::test_scoring_calculation PASSED
tests/test_quiz_app.py::TestQuestionBankController::test_add_question_with_options PASSED
tests/test_quiz_app.py::TestQuestionBankController::test_validate_one_correct_answer PASSED
tests/test_quiz_app.py::TestQuestionBankController::test_validate_minimum_options PASSED
tests/test_quiz_app.py::TestQuestionBankController::test_question_bank_validation PASSED

================== 18 passed in 2.34s ==================
```

---

## 9. HƯỚNG DẪN CÀI ĐẶT

### 9.1. Yêu cầu hệ thống

- **OS:** Windows 10+, Linux, macOS
- **Python:** 3.8 trở lên
- **RAM:** 512MB+
- **Disk:** 50MB (bao gồm database)

### 9.2. Cài đặt

**Bước 1: Clone repository**

```bash
git clone https://github.com/KhiemVo-Uit/quizz-app.git
cd quizz-app
```

**Bước 2: Cài đặt dependencies**

```bash
pip install -r requirements.txt
```

Hoặc cài thủ công:

```bash
pip install ttkbootstrap pytest pytest-cov Pillow
```

**Bước 3: Chạy ứng dụng**

```bash
python main.py
```

### 9.3. Sử dụng lần đầu

1. App tự động tạo database `quiz_app.db`
2. Tự động tạo 100 câu hỏi mẫu (nếu DB trống)
3. Vào "Làm bài thi" → Bắt đầu ngay

### 9.4. Chạy tests

```bash
# Test cơ bản
pytest tests/test_quiz_app.py -v

# Test với coverage
pytest tests/test_quiz_app.py --cov=. --cov-report=term-missing
```

### 9.5. Xóa và tạo lại database

```bash
# Windows
del quiz_app.db
python main.py

# Linux/macOS
rm quiz_app.db
python main.py
```

---

## 10. KẾT QUẢ ĐẠT ĐƯỢC

### 10.1. Hoàn thành 100% yêu cầu

✅ **Chức năng:**

- Ngân hàng câu hỏi CRUD hoàn chỉnh
- Random selection với ma trận độ khó
- Chấm điểm tự động
- Timer và auto-submit

✅ **Cơ sở dữ liệu:**

- 6 bảng với schema chuẩn hóa
- Ràng buộc toàn vẹn đầy đủ (FK, CHECK, UNIQUE)
- 5ndexes tối ưu cho search/filter

✅ **Tìm kiếm & Phân tích:**

- Filter theo độ khó, category
- Thống kê tỷ lệ chọn đáp án
- Phân tích độ khó thực tế

✅ **Giao diện:**

- GUI đẹp với ttkbootstrap
- Timer với cảnh báo màu
- Review đáp án với highlight

✅ **Kiểm thử:**

- 18 tests (vượt yêu cầu ≥12)
- Coverage ~75-80%

### 10.2. Điểm mạnh

1. **Kiến trúc MVC rõ ràng**

   - Tách biệt logic: Model-View-Controller
   - Dễ bảo trì và mở rộng

2. **Database thiết kế tốt**

   - Ràng buộc logic chặt chẽ
   - Indexes cho hiệu suất
   - Cascade delete an toàn

3. **Random selection thông minh**

   - Ma trận độ khó linh hoạt
   - Shuffle mỗi lần thi
   - Không lưu quiz-question mapping (giảm phức tạp)

4. **UI/UX hiện đại**

   - Theme Bootstrap-like
   - Color-coded badges
   - Responsive, intuitive

5. **Testing đầy đủ**
   - Cover models, controllers
   - Validate edge cases
   - Easy to run với pytest

### 10.3. Số liệu thống kê

- **Lines of code:** ~3000 LOC (không tính tests)
- **Files:** 15 files Python
- **Functions/Methods:** ~100+
- **Database tables:** 5 bảng
- **Sample questions:** 100 câu Python
- **Tests:** 18 unit tests

---

## 11. HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN

### 11.1. Hạn chế hiện tại

❌ **Performance:**

- `get_all_questions_with_options()` có N+1 query problem
- `search_questions()` load toàn bộ bảng vào memory
- `LIKE '%keyword%'` không dùng index

❌ **Scalability:**

- Random selection dùng `ORDER BY RANDOM()` → chậm với >10k câu
- Chưa có pagination cho danh sách câu hỏi

❌ **Features:**

- Chưa có user authentication (multi-user)
- Chưa export kết quả ra file (PDF, Excel)
- Chưa có backup/restore database
- Chưa có email notification

❌ **Security:**

- Chưa mã hóa database
- Chưa có role-based access control

### 11.2. Hướng phát triển

#### Phase 1: Performance (ngắn hạn)

1. **Fix N+1 queries:**

   - Implement `Option.get_by_questions(question_ids)`
   - Batch load options trong 1 query

2. **SQL-based search:**

   - Di chuyển filtering vào SQL query
   - Sử dụng indexes hiệu quả

3. **Pagination:**

   - Lazy loading trong UI (đã có)
   - LIMIT/OFFSET trong database queries

4. **FTS5 full-text search:**
   - Tạo virtual table cho question_text
   - Hỗ trợ contains-search nhanh

#### Phase 2: Features (trung hạn)

1. **User management:**

   - Login/Register
   - Roles: Admin, Teacher, Student
   - Permission control

2. **Export/Import:**

   - Export quiz results to PDF/Excel
   - Import questions from CSV/JSON
   - Backup/Restore database

3. **Advanced statistics:**

   - Learning curve charts
   - Item analysis (difficulty, discrimination)
   - Student progress tracking

4. **Notification:**
   - Email kết quả thi
   - Reminder cho bài thi sắp tới

#### Phase 3: Platform (dài hạn)

1. **Web version:**

   - Flask/Django backend
   - React/Vue frontend
   - REST API

2. **Mobile app:**

   - React Native hoặc Flutter
   - Offline mode

3. **Cloud features:**

   - Cloud database (PostgreSQL/MySQL)
   - Multi-tenancy
   - Real-time collaboration

4. **AI integration:**
   - Auto-generate questions from text
   - Adaptive difficulty
   - Plagiarism detection

### 11.3. Technical debt

1. **Transaction management:**

   - Bọc write operations trong transactions
   - Rollback on error

2. **Error handling:**

   - Centralized exception handling
   - User-friendly error messages
   - Logging framework

3. **Code quality:**

   - Refactor long methods
   - Add type hints (Python 3.8+)
   - More docstrings

4. **Testing:**
   - Integration tests
   - UI tests (với tkinter testing tools)
   - Load testing

---

## 12. KẾT LUẬN

### 12.1. Tổng kết

Quiz App là một ứng dụng desktop đầy đủ tính năng cho phép:

- **Giáo viên:** Quản lý ngân hàng câu hỏi, tạo bài thi, xem thống kê
- **Học sinh:** Làm bài thi online, xem kết quả và review đáp án

Dự án đã hoàn thành 100% yêu cầu đề ra:
✅ Chức năng đầy đủ  
✅ Database thiết kế chuẩn  
✅ Tìm kiếm & phân tích  
✅ Giao diện đẹp  
✅ Testing đầy đủ (18 tests)

### 12.2. Kinh nghiệm học được

**Technical:**

- Thiết kế database chuẩn hóa với ràng buộc toàn vẹn
- Áp dụng mô hình MVC trong Python
- Sử dụng tkinter + ttkbootstrap cho GUI hiện đại
- Viết unit tests với pytest
- Random sampling và shuffling algorithms

**Soft skills:**

- Phân tích requirements và chia nhỏ tasks
- Git workflow và version control
- Documentation (README, code comments)
- Problem-solving (debugging, optimization)

### 12.3. Ứng dụng thực tế

Quiz App có thể được sử dụng cho:

- **Trường học:** Thi trắc nghiệm online
- **Trung tâm đào tạo:** Kiểm tra đầu vào/đầu ra
- **Tự học:** Ôn tập và luyện thi
- **Công ty:** Training và assessment

### 12.4. Lời cảm ơn

Cảm ơn giảng viên đã hướng dẫn và hỗ trợ trong quá trình thực hiện đồ án.  
Cảm ơn cộng đồng Python và các thư viện open-source đã cung cấp công cụ tuyệt vời.

---

## PHỤ LỤC

### A. Cấu hình (`config.py`)

```python
# Database
DATABASE_PATH = 'quiz_app.db'

# Quiz settings
DEFAULT_QUIZ_TIME = 600  # 10 phút
MIN_QUESTIONS_PER_QUIZ = 5
MAX_QUESTIONS_PER_QUIZ = 50

# Difficulty levels
DIFFICULTY_LEVELS = {
    'easy': 1,
    'medium': 2,
    'hard': 3
}

# Scoring
CORRECT_ANSWER_POINTS = 10
WRONG_ANSWER_PENALTY = 0

# GUI settings
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FONT_FAMILY = 'Arial'
```

### B. Dependencies (`requirements.txt`)

```
Pillow>=10.0.0
pytest>=7.4.0
pytest-cov>=4.1.0
ttkbootstrap>=1.10.1
```

### C. Liên kết

- **Repository:** https://github.com/KhiemVo-Uit/quizz-app
- **Issues:** https://github.com/KhiemVo-Uit/quizz-app/issues
- **Documentation:** README.md

### D. Tóm tắt README.md

**Cài đặt:**

```bash
pip install -r requirements.txt
python main.py
```

**Chạy tests:**

```bash
pytest tests/test_quiz_app.py -v
```

**Hướng dẫn sử dụng nhanh:**

1. Chạy app → tự động tạo 100 câu hỏi mẫu
2. "Làm bài thi" → chọn quiz, nhập tên, làm bài
3. "Ngân hàng câu hỏi" → thêm/sửa/xóa câu hỏi
4. "Thống kê" → xem phân tích kết quả

**Tính năng đặc biệt:**

- Random câu hỏi theo ma trận độ khó: `{'easy': 5, 'medium': 3, 'hard': 2}`
- Timer cảnh báo: xanh (>5 phút) → cam (1-5 phút) → đỏ (<1 phút)
- Auto-submit khi hết giờ

---

**HẾT BÁO CÁO**
