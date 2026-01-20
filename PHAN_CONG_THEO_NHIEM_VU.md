# PHÂN CÔNG THEO NHIỆM VỤ - QUIZ APPLICATION

## Mỗi người chịu trách nhiệm 1 LAYER hoàn chỉnh

> **💡 Nguyên tắc phân công:**
>
> - Mỗi người = 1 nhiệm vụ chính rõ ràng
> - Ai làm xong phần mình = có 1 module hoàn chỉnh
> - Đánh giá theo CHẤT LƯỢNG, không phải số dòng code
> - Công bằng về MỨC ĐỘ KHÓ và TRÁCH NHIỆM

---

## 👥 PHÂN CÔNG 5 THÀNH VIÊN

| STT   | Thành viên       | Nhiệm vụ chính                      | Layer          | Độ khó     |
| ----- | ---------------- | ----------------------------------- | -------------- | ---------- |
| **1** | **CƯỜNG** | **DATABASE + ALL MODELS** + BÁO CÁO          | Data Layer     | ⭐⭐⭐⭐⭐ |
| **2** | **KHIÊM** | **ALL CONTROLLERS**   + CHIA VIỆC              | Business Logic | ⭐⭐⭐⭐⭐ |
| **3** | **NHUNG** | **QUIZ VIEW** + SLIDE                      | Presentation   | ⭐⭐⭐⭐   |
| **4** | **LỢI** | **QUESTION BANK VIEW** + STATISTICS             | Presentation   | 
| **5** | **ENGLISH** |  **MAIN APP  + TESTING** + THUYẾT TRÌNH | Integration    | ⭐⭐⭐⭐⭐ |

---

## 📋 CHI TIẾT TỪNG NGƯỜI

### 👤 THÀNH VIÊN A - DATABASE + ALL MODELS

**🎯 Nhiệm vụ:** Chịu trách nhiệm toàn bộ DATA LAYER

#### 📦 Files phụ trách:

```
database/
├── __init__.py
└── connection.py          # Database schema, 6 tables, indexes

models/
├── __init__.py
├── question.py           # Question CRUD + random selection
├── option.py             # Option CRUD + validation
├── quiz.py               # Quiz CRUD + management
└── attempt.py            # Attempt tracking + statistics
```

#### 🎯 Nhiệm vụ cụ thể:

1. **Thiết kế Database Schema**

   - 6 bảng: questions, options, quizzes, quiz_questions, attempts, attempt_answers
   - Ràng buộc toàn vẹn: CHECK, UNIQUE, NOT NULL
   - Foreign keys với CASCADE
   - Indexes cho performance
   - Vẽ ERD diagram

2. **4 Models hoàn chỉnh**

   - **Question Model:** CRUD, get_by_difficulty, get_by_category, get_random_questions, count
   - **Option Model:** CRUD, get_by_question, get_correct_option, validation
   - **Quiz Model:** CRUD, add_question, remove_question, get_questions
   - **Attempt Model:** create, save_answer, get_answers, complete_attempt, get_statistics

3. **Data Integrity**
   - Đảm bảo mỗi question có đúng 1 correct option
   - Đảm bảo mỗi question có ít nhất 2 options
   - Validation trước khi insert/update

#### ✅ Deliverables:

- [ ] ERD diagram
- [ ] Database schema với đầy đủ constraints
- [ ] 4 Models với tổng ~30 methods
- [ ] Unit tests cho tất cả models (8 tests)
- [ ] Documentation cho data layer

#### ⏱️ Timeline: 7-10 ngày

**Độ khó:** ⭐⭐⭐⭐⭐ (Nền tảng quan trọng nhất, cần chính xác 100%)

---

### 👤 THÀNH VIÊN B - ALL CONTROLLERS

**🎯 Nhiệm vụ:** Chịu trách nhiệm toàn bộ BUSINESS LOGIC

#### 📦 Files phụ trách:

```
controllers/
├── __init__.py
├── quiz_controller.py              # Quiz business logic
└── question_bank_controller.py     # Question management logic

utils/
├── __init__.py
└── sample_data.py                  # Demo data generator
```

#### 🎯 Nhiệm vụ cụ thể:

1. **Quiz Controller** (Core business logic)

   - `create_quiz_with_random_questions()` với ma trận độ khó
   - `get_quiz_with_questions()` với shuffle options
   - `start_attempt()` khởi tạo lượt thi
   - `submit_answer()` lưu câu trả lời
   - `complete_attempt()` tính điểm (max 10)
   - `get_attempt_review()` review chi tiết
   - `get_question_statistics()` thống kê câu hỏi
   - `analyze_difficulty()` phân tích độ khó thực tế

2. **Question Bank Controller**

   - `add_question_with_options()` thêm câu hỏi + options
   - `update_question_with_options()` cập nhật
   - `delete_question_with_options()` xóa cascade
   - `validate_question_options()` validation logic
   - `search_questions()` tìm kiếm
   - `filter_questions()` lọc theo difficulty/category

3. **Sample Data Generator**

   - Tạo 30+ câu hỏi mẫu đa dạng
   - Tạo quiz mẫu để demo
   - Populate database cho testing

4. **Business Rules**
   - Scoring algorithm: max 10 points
   - Random selection với distribution
   - Validation rules
   - Statistics calculation

#### ✅ Deliverables:

- [ ] Quiz Controller với 9+ methods
- [ ] Question Bank Controller với 6+ methods
- [ ] Sample data với 30+ questions
- [ ] Unit tests cho controllers (6 tests)
- [ ] Business logic documentation

#### ⏱️ Timeline: 7-10 ngày

**Độ khó:** ⭐⭐⭐⭐⭐ (Logic phức tạp, cần test kỹ)

---

### 👤 THÀNH VIÊN C - QUIZ VIEW

**🎯 Nhiệm vụ:** Giao diện LÀM BÀI THI hoàn chỉnh

#### 📦 Files phụ trách:

```
views/
└── quiz_view.py           # Toàn bộ quiz interface
```

#### 🎯 Nhiệm vụ cụ thể:

1. **Quiz List Screen**

   - Hiển thị danh sách bài thi
   - Button "Tạo bài thi mẫu"
   - Chọn quiz để bắt đầu

2. **Quiz Selection Screen**

   - Nhập tên thí sinh
   - Hiển thị thông tin quiz (time, questions count)
   - Button "Bắt đầu thi"

3. **Quiz Taking Screen** (Màn hình chính - phức tạp nhất)

   - **Display:**

     - Question text với số thứ tự
     - 4 options với radio buttons
     - Question navigation (Previous/Next)

   - **Timer:**

     - Countdown từ time_limit
     - Color coding:
       - 🟢 Xanh: > 5 phút
       - 🟠 Cam: 1-5 phút
       - 🔴 Đỏ: < 1 phút
     - Auto-submit khi hết giờ

   - **Navigation:**
     - Previous question
     - Next question
     - Jump to question (optional)
     - Submit quiz

4. **Results Screen**

   - Hiển thị điểm số (X/10)
   - Số câu đúng/tổng số câu
   - Thời gian làm bài
   - Button "Xem đáp án chi tiết"

5. **Review Screen**
   - Hiển thị từng câu hỏi
   - Đáp án đã chọn (highlight màu)
   - Đáp án đúng (highlight xanh)
   - Đáp án sai (highlight đỏ)
   - Giải thích (nếu có)

#### ✅ Deliverables:

- [ ] Quiz View với 5 screens
- [ ] Timer countdown chính xác
- [ ] Auto-submit functionality
- [ ] Review answers với colors
- [ ] UI/UX mượt mà với ttkbootstrap
- [ ] Error handling (quiz not found, etc.)

#### ⏱️ Timeline: 7-10 ngày

**Độ khó:** ⭐⭐⭐⭐ (UI phức tạp, nhiều states)

---

### 👤 THÀNH VIÊN D - QUESTION BANK VIEW

**🎯 Nhiệm vụ:** Giao diện QUẢN LÝ CÂU HỎI hoàn chỉnh

#### 📦 Files phụ trách:

```
views/
└── question_bank_view.py  # Toàn bộ question management UI
```

#### 🎯 Nhiệm vụ cụ thể:

1. **Question List Screen**

   - TreeView/Table hiển thị tất cả câu hỏi
   - Columns: ID, Question Text (truncated), Difficulty, Category
   - Sorting by columns
   - Toolbar với buttons: Add, Edit, Delete, Refresh

2. **Add Question Form** (Form phức tạp)

   - Input fields:
     - Question text (multiline)
     - Difficulty dropdown (Easy/Medium/Hard)
     - Category input
   - **4 Options section:**
     - 4 text inputs cho options
     - 4 radio buttons để chọn đáp án đúng
     - Validation: ít nhất 2 options có text
     - Validation: phải chọn 1 đáp án đúng
   - Buttons: Save, Cancel
   - Error messages rõ ràng

3. **Edit Question Form**

   - Load câu hỏi hiện tại từ database
   - Pre-fill tất cả fields
   - Load options + radio button đúng
   - Update functionality
   - Buttons: Update, Cancel

4. **Delete Question**

   - Confirmation dialog
   - Hiển thị question text để xác nhận
   - Cascade delete options
   - Success/error notification

5. **Search & Filter**

   - **Search box:** Tìm theo question text
   - **Filter dropdown 1:** All / Easy / Medium / Hard
   - **Filter dropdown 2:** All Categories / Specific
   - Real-time filtering
   - Clear filters button

6. **Question Details (Optional)**
   - Click vào question → hiển thị popup
   - Full question text
   - All 4 options
   - Correct answer highlighted
   - Statistics: times used, success rate

#### ✅ Deliverables:

- [ ] Question List với CRUD operations
- [ ] Add/Edit forms với validation
- [ ] Search & filter functionality
- [ ] Delete với confirmation
- [ ] Error handling & user feedback
- [ ] UI/UX intuitive

#### ⏱️ Timeline: 7-10 ngày

**Độ khó:** ⭐⭐⭐⭐ (Form validation phức tạp, CRUD đầy đủ)

---

### 👤 THÀNH VIÊN E - MAIN APP + STATISTICS + TESTING

**🎯 Nhiệm vụ:** INTEGRATION + TESTING + STATISTICS

#### 📦 Files phụ trách:

```
main.py                    # Application entry point
config.py                  # Configuration settings

views/
└── statistics_view.py     # Statistics & analytics

tests/
├── __init__.py
└── test_quiz_app.py      # All unit tests

requirements.txt
README.md
```

#### 🎯 Nhiệm vụ cụ thể:

1. **Main Application** (`main.py`)

   - QuizApp class với ttkbootstrap window
   - **Sidebar navigation:**
     - 🏠 Trang chủ
     - 📝 Làm bài thi
     - 📚 Ngân hàng câu hỏi
     - 📊 Thống kê
     - ❌ Thoát
   - **Content area:** Dynamic switching
   - **Home screen:** Welcome message, quick actions
   - **Exit confirmation:** Dialog trước khi quit
   - Initialize database on startup

2. **Statistics View** (`statistics_view.py`)

   - **Tab 1 - Quiz Statistics:**

     - Danh sách tất cả quizzes
     - Mỗi quiz: tên, attempts count, avg score
     - Click vào quiz → xem chi tiết attempts
     - Attempts list: student name, score, time, date

   - **Tab 2 - Question Analysis:**

     - Danh sách tất cả questions
     - Mỗi question:
       - Question text
       - Times answered
       - Success rate (%)
       - Option distribution (pie chart/bars)
     - Identify câu khó nhất/dễ nhất

   - **Tab 3 - Difficulty Analysis:**
     - So sánh labeled difficulty vs actual difficulty
     - Table: Question | Labeled | Actual | Success Rate
     - Color coding:
       - Đúng: xanh
       - Sai 1 level: vàng
       - Sai 2+ levels: đỏ

3. **Testing** (`tests/test_quiz_app.py`)

   - **Model Tests (8 tests):**

     - test_create_question
     - test_get_question_by_id
     - test_get_questions_by_difficulty
     - test_update_question
     - test_delete_question
     - test_create_option
     - test_get_options_by_question
     - test_get_correct_option

   - **Controller Tests (6 tests):**

     - test_create_quiz_with_random_questions
     - test_difficulty_matrix_selection
     - test_submit_answer_correct
     - test_submit_answer_incorrect
     - test_scoring_calculation
     - test_random_question_selection

   - **Validation Tests (4+ tests):**

     - test_validate_one_correct_answer
     - test_validate_minimum_options
     - test_add_question_with_options
     - test_question_bank_validation

   - **Integration Tests:**
     - test_full_workflow (add question → create quiz → take quiz → review)

4. **Configuration** (`config.py`)

   - Database path
   - Window dimensions
   - Font settings
   - Theme configuration
   - Scoring constants

5. **Documentation**
   - README.md với:
     - Project overview
     - Installation guide
     - Usage guide
     - Testing guide
     - Screenshots (optional)

#### ✅ Deliverables:

- [ ] Main application với navigation
- [ ] Statistics View với 3 tabs đầy đủ
- [ ] 18+ unit tests (pytest)
- [ ] Test coverage ≥80%
- [ ] Config file
- [ ] README.md documentation
- [ ] Integration testing successful

#### ⏱️ Timeline: 10-14 ngày

**Độ khó:** ⭐⭐⭐⭐⭐ (Integration phức tạp, testing toàn diện)

---

## 🔄 DEPENDENCIES & WORKFLOW

```
┌────────────────────────────────────────────────────────┐
│                   WEEK 1 (Setup)                       │
└────────────────────────────────────────────────────────┘

Day 1-3:
  [A] ━━━━━━━━━► Database schema + ERD
                   ↓
Day 4-7:           ↓
  [A] ━━━━━━━━━► Models (Question, Option)
  [E] ━━━━━━━━━► Setup tests, test Models

┌────────────────────────────────────────────────────────┐
│                  WEEK 2 (Core Dev)                     │
└────────────────────────────────────────────────────────┘

Day 8-10:
  [A] ━━━━━━━━━► Models (Quiz, Attempt)
                   ↓
Day 11-14:         ↓
  [B] ━━━━━━━━━► Controllers (chờ A xong Models)
  [E] ━━━━━━━━━► Test Controllers

┌────────────────────────────────────────────────────────┐
│                 WEEK 3 (UI Layer)                      │
└────────────────────────────────────────────────────────┘

Day 15-21:
  [C] ━━━━━━━━━► Quiz View (SONG SONG)
  [D] ━━━━━━━━━► Question Bank View (SONG SONG)
  [E] ━━━━━━━━━► Main App + Statistics View

┌────────────────────────────────────────────────────────┐
│              WEEK 4 (Integration)                      │
└────────────────────────────────────────────────────────┘

Day 22-28:
  [E] ━━━━━━━━━► Integration testing
  [ALL] ━━━━━━━► Bug fixes, polish
  [ALL] ━━━━━━━► Code review
  [E] ━━━━━━━━━► Documentation
  [ALL] ━━━━━━━► Presentation prep
```

### ⚡ Critical Path:

1. **A (Models)** → BLOCK toàn bộ
2. **B (Controllers)** → BLOCK C, D, E
3. **C, D (Views)** → Có thể song song
4. **E (Integration)** → Cuối cùng

### 🤝 Collaboration Points:

- **A & B:** Họp đầu tuần 2 về data structure
- **B & C,D:** Họp đầu tuần 3 về API calls
- **E với All:** Daily testing updates

---

## ⚖️ TẠI SAO PHÂN CÔNG NÀY CÔNG BẰNG?

### So sánh độ khó và trách nhiệm:

| Tiêu chí              | A           | B           | C           | D           | E              |
| --------------------- | ----------- | ----------- | ----------- | ----------- | -------------- |
| **Khối lượng code**   | 613         | 507         | 512         | 370         | 848            |
| **Số components**     | 5 files     | 3 files     | 1 file      | 1 file      | 5 files        |
| **Độ phức tạp logic** | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐    | ⭐⭐⭐⭐    | ⭐⭐⭐⭐⭐     |
| **Độ phụ thuộc**      | 0 (bắt đầu) | 1 (chờ A)   | 2 (chờ A,B) | 2 (chờ A,B) | 3 (chờ tất cả) |
| **Testing burden**    | Self-test   | Self-test   | Manual      | Manual      | Toàn bộ        |
| **Impact nếu fail**   | ⚠️ CRITICAL | ⚠️ CRITICAL | ⚠️ HIGH     | ⚠️ MEDIUM   | ⚠️ CRITICAL    |

### Điểm cân bằng:

✅ **Thành viên A:** Code ít nhưng nền tảng, sai = toàn bộ fail  
✅ **Thành viên B:** Logic phức tạp, business rules nhiều  
✅ **Thành viên C:** UI phức tạp (timer, states), code nhiều  
✅ **Thành viên D:** CRUD đầy đủ, validation UI, code ít nhất  
✅ **Thành viên E:** Code nhiều nhất nhưng:

- Làm cuối (có time)
- Nhiều công việc parallel (main + stats + tests)
- Tổng hợp từ work của người khác

---

## 📊 ĐÁNH GIÁ RIÊNG TỪNG NGƯỜI

### Thành viên A - Data Layer:

**Điểm mạnh cần có:**

- Giỏi SQL, hiểu database design
- Tỉ mỉ, cẩn thận với constraints
- Hiểu data integrity

**Đánh giá dựa trên:**

- ERD có logic không?
- Constraints đầy đủ chưa?
- Models có bug không?
- Code có clean không?

---

### Thành viên B - Business Logic:

**Điểm mạnh cần có:**

- Tư duy logic tốt
- Hiểu thuật toán (scoring, random)
- Biết xử lý edge cases

**Đánh giá dựa trên:**

- Business logic có đúng không?
- Scoring chính xác chưa?
- Random có fair không?
- Validation có đầy đủ không?

---

### Thành viên C - Quiz UI:

**Điểm mạnh cần có:**

- Giỏi UI/UX design
- Hiểu state management
- Biết làm timer

**Đánh giá dựa trên:**

- UI có đẹp không?
- Timer có chính xác không?
- Navigation mượt mà chưa?
- Error handling tốt không?

---

### Thành viên D - Question Bank UI:

**Điểm mạnh cần có:**

- Giỏi forms & validation
- Hiểu CRUD patterns
- Biết làm search/filter

**Đánh giá dựa trên:**

- CRUD có đầy đủ không?
- Validation UI có tốt không?
- Search/filter có work không?
- User-friendly không?

---

### Thành viên E - Integration:

**Điểm mạnh cần có:**

- Tư duy tổng thể
- Giỏi testing & debugging
- Biết viết documentation

**Đánh giá dựa trên:**

- Tests có pass không?
- Coverage có đủ không?
- Integration có smooth không?
- Documentation có đầy đủ không?

---

## ✅ CHECKLIST HOÀN THÀNH

### ☑️ Thành viên A - Data Layer

- [ ] ERD diagram hoàn chỉnh
- [ ] Database schema với 6 bảng
- [ ] Question model (10+ methods)
- [ ] Option model (6+ methods)
- [ ] Quiz model (8+ methods)
- [ ] Attempt model (7+ methods)
- [ ] 8 unit tests cho models
- [ ] Data layer documentation

### ☑️ Thành viên B - Business Logic

- [ ] Quiz controller (9+ methods)
- [ ] Question bank controller (6+ methods)
- [ ] Sample data (30+ questions)
- [ ] Scoring algorithm implemented
- [ ] Difficulty matrix working
- [ ] 6 unit tests cho controllers
- [ ] Business logic documentation

### ☑️ Thành viên C - Quiz UI

- [ ] Quiz list screen
- [ ] Quiz selection screen
- [ ] Quiz taking screen với timer
- [ ] Results screen
- [ ] Review screen với highlights
- [ ] Timer color coding working
- [ ] Auto-submit on timeout
- [ ] All error handling

### ☑️ Thành viên D - Question Bank UI

- [ ] Question list với TreeView
- [ ] Add question form
- [ ] Edit question form
- [ ] Delete với confirmation
- [ ] Search functionality
- [ ] Filter by difficulty
- [ ] Filter by category
- [ ] All validation working

### ☑️ Thành viên E - Integration

- [ ] Main app với navigation
- [ ] Statistics view với 3 tabs
- [ ] 18+ unit tests
- [ ] Integration tests
- [ ] Test coverage ≥80%
- [ ] config.py
- [ ] requirements.txt
- [ ] README.md
- [ ] All tests passing

---

## 🎯 MỤC TIÊU CHUNG

**Functional:**

- ✅ Đầy đủ chức năng theo yêu cầu
- ✅ UI/UX dễ sử dụng
- ✅ Không có bug critical

**Technical:**

- ✅ MVC pattern rõ ràng
- ✅ Code clean, có comments
- ✅ Test coverage ≥80%

**Team:**

- ✅ Ai cũng hiểu toàn bộ project
- ✅ Code review lẫn nhau
- ✅ Documentation đầy đủ

---

## 📞 COMMUNICATION

### Daily Standup (10 phút):

- Hôm qua làm gì?
- Hôm nay làm gì?
- Có vấn đề gì cần help?

### Weekly Demo (30 phút):

- Mỗi người demo phần của mình
- Feedback từ team
- Điều chỉnh nếu cần

### Code Review:

- Mỗi PR cần 1 reviewer
- Review trong 24h
- Constructive feedback

### Git Workflow:

```bash
# Branch naming
feature/database-schema         # A
feature/quiz-controller         # B
feature/quiz-view              # C
feature/question-bank-view     # D
feature/integration-testing    # E

# Commit format
git commit -m "[A] Add question model with CRUD"
git commit -m "[B] Implement scoring algorithm"
git commit -m "[C] Add timer countdown feature"
```

---

## 🚀 SUCCESS METRICS

### Individual:

- Hoàn thành đúng timeline
- Code quality tốt
- Ít bug trong phần của mình

### Team:

- Integration smooth
- All tests pass
- Demo thành công

---

## 💡 TIPS

**Cho Thành viên A:**

- Tham khảo các DB schema samples online
- Vẽ ERD trước khi code
- Test constraints kỹ

**Cho Thành viên B:**

- Viết unit tests trước (TDD)
- Handle edge cases
- Document business rules

**Cho Thành viên C:**

- Sketch UI trên giấy trước
- Test timer thoroughly
- Handle all user actions

**Cho Thành viên D:**

- Validation trước khi submit
- Clear error messages
- Test với invalid inputs

**Cho Thành viên E:**

- Start testing early
- Automate as much as possible
- Keep documentation updated

---

**Phân công này đảm bảo:**

1. ✅ Mỗi người có 1 NHIỆM VỤ RÕ RÀNG
2. ✅ Ai cũng có thể làm SONG SONG một phần
3. ✅ Độ khó & trách nhiệm TƯƠNG ĐƯƠNG
4. ✅ Dễ ĐÁNH GIÁ đóng góp cá nhân
5. ✅ CÔNG BẰNG về workload và impact

**Chúc team thành công! 🎉**
