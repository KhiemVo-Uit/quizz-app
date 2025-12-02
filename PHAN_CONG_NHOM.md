# PHÂN CÔNG CÔNG VIỆC - QUIZ APPLICATION

## Dự án: Hệ thống thi trắc nghiệm trực tuyến

---

## 👥 THÀNH VIÊN NHÓM

| STT | Họ tên           | Vai trò                       | Phần việc chính               |
| --- | ---------------- | ----------------------------- | ----------------------------- |
| 1   | **Thành viên A** | Team Leader + Database Design | Database, Models, Testing     |
| 2   | **Thành viên B** | Backend Developer             | Controllers, Business Logic   |
| 3   | **Thành viên C** | Frontend Developer            | Views - Quiz & Statistics     |
| 4   | **Thành viên D** | Frontend Developer            | Views - Question Bank         |
| 5   | **Thành viên E** | Testing & Integration         | Testing, Utils, Documentation |

---

## 📋 CHI TIẾT PHÂN CÔNG

### 👤 THÀNH VIÊN A - Team Leader + Database Design

**Trách nhiệm:** Thiết kế database, xây dựng Models, kiểm thử

#### Công việc cụ thể:

1. **Database Layer** (`database/`)

   - ✅ `connection.py`: Kết nối database, khởi tạo schema
   - ✅ Thiết kế 6 bảng với đầy đủ ràng buộc (CHECK, UNIQUE, FK)
   - ✅ Tạo indexes cho hiệu suất
   - ✅ Foreign keys với CASCADE

2. **Models Layer** (`models/`)

   - ✅ `question.py`: CRUD cho câu hỏi, random selection
   - ✅ `option.py`: CRUD cho đáp án, validation
   - ✅ `quiz.py`: CRUD cho bài thi
   - ✅ `attempt.py`: Lưu lượt thi, câu trả lời

3. **Testing Models**
   - ✅ Tests cho từng model (CRUD operations)
   - ✅ Test random question selection
   - ✅ Test data integrity constraints

#### Deliverables:

- [ ] Schema database hoàn chỉnh với ERD diagram
- [ ] 4 file models với đầy đủ methods
- [ ] 8-10 unit tests cho models
- [ ] Documentation cho database structure

#### Thời gian: 7-10 ngày

---

### 👤 THÀNH VIÊN B - Backend Developer

**Trách nhiệm:** Business logic, Controllers, API xử lý

#### Công việc cụ thể:

1. **Controllers** (`controllers/`)

   - ✅ `quiz_controller.py`:

     - Tạo bài thi với random questions
     - Ma trận độ khó (easy/medium/hard)
     - Start/Complete attempt
     - Submit answer & scoring
     - Review đáp án
     - Statistics & analysis

   - ✅ `question_bank_controller.py`:
     - Quản lý ngân hàng câu hỏi
     - Thêm/Sửa/Xóa câu hỏi + options
     - Validation (1 đáp án đúng, min 2 options)
     - Filter by difficulty/category
     - Search functionality

2. **Business Logic**

   - ✅ Tính điểm (max 10 điểm)
   - ✅ Random selection với ma trận độ khó
   - ✅ Validation logic
   - ✅ Statistics queries

3. **Sample Data** (`utils/sample_data.py`)
   - ✅ Tạo dữ liệu mẫu cho demo
   - ✅ Populate database với câu hỏi test

#### Deliverables:

- [ ] 2 file controllers hoàn chỉnh
- [ ] Sample data generator
- [ ] Unit tests cho controllers (6-8 tests)
- [ ] API documentation

#### Thời gian: 7-10 ngày

---

### 👤 THÀNH VIÊN C - Frontend Developer (Quiz & Statistics)

**Trách nhiệm:** Giao diện làm bài thi và thống kê

#### Công việc cụ thể:

1. **Quiz View** (`views/quiz_view.py`)

   - ✅ Danh sách bài thi có sẵn
   - ✅ Chọn bài thi và nhập tên
   - ✅ Giao diện làm bài:
     - Hiển thị câu hỏi và 4 đáp án
     - Radio buttons cho chọn đáp án
     - Navigation giữa các câu (Next/Previous)
     - Timer đếm ngược với màu cảnh báo:
       - Xanh: > 5 phút
       - Cam: 1-5 phút
       - Đỏ: < 1 phút
     - Auto-submit khi hết giờ
   - ✅ Review đáp án sau khi submit:
     - Hiển thị đáp án đã chọn
     - Highlight đúng/sai
     - Hiển thị đáp án đúng
     - Tổng điểm, số câu đúng

2. **Statistics View** (`views/statistics_view.py`)
   - ✅ Tab "Thống kê bài thi":
     - Danh sách attempts
     - Điểm cao nhất/thấp nhất/trung bình
     - Thời gian làm bài
   - ✅ Tab "Phân tích câu hỏi":
     - Tỷ lệ chọn từng đáp án
     - Câu hỏi khó nhất/dễ nhất
   - ✅ Tab "Độ khó":
     - So sánh độ khó gán vs thực tế
     - Charts/graphs visualization

#### Deliverables:

- [ ] `quiz_view.py` với đầy đủ chức năng
- [ ] `statistics_view.py` với 3 tabs
- [ ] Timer logic hoàn chỉnh
- [ ] UI/UX responsive và đẹp mắt

#### Thời gian: 7-10 ngày

---

### 👤 THÀNH VIÊN D - Frontend Developer (Question Bank)

**Trách nhiệm:** Giao diện quản lý ngân hàng câu hỏi

#### Công việc cụ thể:

1. **Question Bank View** (`views/question_bank_view.py`)

   - ✅ Danh sách tất cả câu hỏi:

     - TreeView/Table hiển thị câu hỏi
     - Cột: ID, Question Text, Difficulty, Category
     - Sorting và filtering

   - ✅ Thêm câu hỏi mới:

     - Form nhập câu hỏi
     - Chọn độ khó (Easy/Medium/Hard)
     - Nhập category
     - Nhập 4 đáp án
     - Radio button chọn đáp án đúng
     - Validation trước khi save

   - ✅ Sửa câu hỏi:

     - Load dữ liệu câu hỏi hiện tại
     - Edit form tương tự thêm mới
     - Update câu hỏi + options

   - ✅ Xóa câu hỏi:

     - Confirm dialog
     - Cascade delete options

   - ✅ Tìm kiếm & Filter:
     - Search by text
     - Filter by difficulty
     - Filter by category

2. **Integration với Controllers**
   - ✅ Gọi `question_bank_controller` methods
   - ✅ Handle errors và validation
   - ✅ Refresh view sau mỗi thao tác

#### Deliverables:

- [ ] `question_bank_view.py` hoàn chỉnh
- [ ] CRUD UI cho câu hỏi
- [ ] Search & filter functionality
- [ ] Error handling và user feedback

#### Thời gian: 7-10 ngày

---

### 👤 THÀNH VIÊN E - Testing & Integration

**Trách nhiệm:** Testing toàn diện, Integration, Documentation

#### Công việc cụ thể:

1. **Testing** (`tests/test_quiz_app.py`)

   - ✅ Unit tests cho Models (6 tests)
   - ✅ Unit tests cho Controllers (6 tests)
   - ✅ Integration tests (4 tests)
   - ✅ Randomization tests
   - ✅ Validation tests
   - ✅ Scoring calculation tests
   - **Tổng: 18+ tests** (yêu cầu ≥12)

2. **Main Application** (`main.py`)

   - ✅ Setup main window với ttkbootstrap
   - ✅ Sidebar navigation
   - ✅ Route giữa các views
   - ✅ Home screen
   - ✅ Exit confirmation

3. **Configuration** (`config.py`)

   - ✅ Database path
   - ✅ Window settings
   - ✅ Font configurations
   - ✅ Scoring constants

4. **Documentation**

   - ✅ `README.md`: Hướng dẫn sử dụng
   - ✅ Installation guide
   - ✅ Testing guide
   - ✅ Code comments

5. **Integration Testing**
   - ✅ Test toàn bộ workflow:
     - Thêm câu hỏi → Tạo bài thi → Làm bài → Xem kết quả
   - ✅ Test edge cases
   - ✅ Performance testing

#### Deliverables:

- [ ] 18+ unit tests passing
- [ ] `main.py` hoàn chỉnh
- [ ] `config.py` với settings
- [ ] README.md chi tiết
- [ ] Test coverage report

#### Thời gian: 7-10 ngày

---

## 🔄 QUY TRÌNH LÀM VIỆC

### Week 1: Setup & Core Development

- **Day 1-2**: Team meeting, setup environment, create repository
- **Day 3-7**:
  - A: Database + Models
  - B: Controllers logic
  - C, D, E: Study ttkbootstrap, prototype UI

### Week 2: Integration & Testing

- **Day 8-10**:
  - A: Finish Models, support others
  - B: Complete Controllers
  - C: Complete Quiz & Statistics views
  - D: Complete Question Bank view
  - E: Write tests continuously
- **Day 11-12**:
  - E: Integration testing
  - All: Bug fixes
  - All: Code review

### Week 3: Polish & Documentation

- **Day 13-14**:
  - All: Testing, bug fixes
  - E: Documentation
  - All: Prepare presentation

---

## 📊 TIÊU CHÍ ĐÁNH GIÁ

### Chức năng (40%)

- ✅ Ngân hàng câu hỏi CRUD
- ✅ Random selection với ma trận độ khó
- ✅ Timer và auto-submit
- ✅ Review đáp án
- ✅ Statistics & analysis

### Database (20%)

- ✅ 6 bảng với đầy đủ ràng buộc
- ✅ Foreign keys, indexes
- ✅ Data integrity

### Giao diện (15%)

- ✅ GUI đẹp, dễ sử dụng
- ✅ Navigation mượt mà
- ✅ Error handling tốt

### Testing (15%)

- ✅ ≥12 unit tests (đã có 18)
- ✅ Coverage tốt
- ✅ Pass all tests

### Code Quality (10%)

- ✅ MVC pattern rõ ràng
- ✅ Code clean, có comments
- ✅ Error handling

---

## 📁 CẤU TRÚC FILE THEO NGƯỜI

```
Thành viên A:
├── database/
│   ├── __init__.py
│   └── connection.py
└── models/
    ├── __init__.py
    ├── question.py
    ├── option.py
    ├── quiz.py
    └── attempt.py

Thành viên B:
├── controllers/
│   ├── __init__.py
│   ├── quiz_controller.py
│   └── question_bank_controller.py
└── utils/
    ├── __init__.py
    └── sample_data.py

Thành viên C:
└── views/
    ├── quiz_view.py
    └── statistics_view.py

Thành viên D:
└── views/
    ├── __init__.py
    └── question_bank_view.py

Thành viên E:
├── main.py
├── config.py
├── requirements.txt
├── README.md
└── tests/
    ├── __init__.py
    └── test_quiz_app.py
```

---

## 🔗 DEPENDENCIES GIỮA CÁC MODULES

```
A (Models) → B (Controllers) → C, D (Views) → E (Integration)
     ↓              ↓              ↓              ↓
  Database    Business Logic    UI/UX         Testing
```

**Lưu ý:**

- Thành viên A phải hoàn thành Models trước
- Thành viên B cần Models để implement Controllers
- Thành viên C, D cần Controllers để implement Views
- Thành viên E test liên tục trong suốt quá trình

---

## 📞 COMMUNICATION

- **Daily standup**: 15 phút mỗi ngày
- **Code review**: Peer review trước khi merge
- **Git workflow**: Feature branches, pull requests
- **Documentation**: Comment code, update README

---

## ✅ CHECKLIST HOÀN THÀNH

### Thành viên A

- [ ] Database schema hoàn chỉnh
- [ ] 4 Models với CRUD đầy đủ
- [ ] 8 unit tests cho models
- [ ] ERD diagram

### Thành viên B

- [ ] 2 Controllers hoàn chỉnh
- [ ] Sample data generator
- [ ] 6 unit tests cho controllers
- [ ] Business logic documentation

### Thành viên C

- [ ] Quiz View hoàn chỉnh
- [ ] Statistics View với 3 tabs
- [ ] Timer với color coding
- [ ] Review đáp án UI

### Thành viên D

- [ ] Question Bank View hoàn chỉnh
- [ ] CRUD UI cho câu hỏi
- [ ] Search & filter
- [ ] Validation UI

### Thành viên E

- [ ] Main application setup
- [ ] 18+ unit tests
- [ ] Integration tests
- [ ] README.md chi tiết
- [ ] Test coverage ≥80%

---

## 🎯 MỤC TIÊU CHUNG

- ✅ Hoàn thành đúng deadline
- ✅ Code quality cao
- ✅ Đầy đủ chức năng theo yêu cầu
- ✅ UI/UX đẹp và dễ dùng
- ✅ Testing coverage tốt
- ✅ Documentation đầy đủ

**Chúc team thành công! 🚀**
