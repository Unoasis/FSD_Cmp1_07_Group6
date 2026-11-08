# University Application - Group6-Cmp1-07

32555 Fundamentals of Software Development

Sheyda Niaparast - 26496772

Huilin Zeng - 26310336

Chengfeng Yang - 26642759

Sihan Yin - 26151769

## 1. Project Overview

This project is a University Management Application written in Python. It has two parts, CLIUniApp and GUIUniApp.

In CLIUniApp, students can register, log in and manage their enrolled subjects, and admins can manage student records. GUIUniApp gives registered students a graphical interface to log in, enrol in subjects and view their subject information.

Both applications share the same backend classes and store student and enrolment information as JSON in `students.data`.

## 2. Project Structure

<pre>
UniApp/
├── __pycache__/           # Python-generated cache files
├── admin_system.py        # Admin management functions
├── CLIUniApp.py           # CLI entry point and University menu
├── database.py            # JSON data storage and retrieval
├── gui_enrolment.py       # GUI enrolment window
├── gui_errors.py          # GUI exception window
├── gui_subjects.py        # GUI subject window
├── GUIUniApp.py           # GUI entry point and Login window
├── person.py              # Base Person class
├── README.md              # Project documentation
├── student_system.py      # Student registration and login
├── student.py             # Student model
├── students.data          # Application data (JSON)
├── subject_controller.py  # Subject enrolment operations
├── subject.py             # Subject model, marks and grades
├── test_students.data     # Development and testing data
└── validator.py           # Input validation and student ID generation
</pre>

## 3. Team Contributions

| Team Member | Main Contributions |
|---|---|
| Huilin Zeng | Student System, Database and JSON data management, GUIUniApp (Login Window and Exception Window). |
| Sheyda Niaparast |  |
| Chengfeng Yang |  |
| Sihan Yin |  |

## 4. Implementation Details

This section follows the Assessment 1 Part 2 marking scheme.

### a. The University System (Chengfeng Yang)

*To be completed by the responsible team member.*

### b. The Student System (Huilin Zeng)

#### Implementation and Main Functions

I was responsible for the Student System: registration, login, input validation and database operations. I also wrote the basic Person and Student classes and connected the Student Menu to the University System and the Subject Enrolment System.

**1. Student Registration and Login**

In `student_system.py`, I implemented `student_menu()`, `register_account()` and `login_account()`.

Registration validates the email and password, checks whether the student already exists, generates a unique student ID and saves the new student to the database.

Login checks the input format, then calls `find_student_by_email()` and `Student.login()` to verify the credentials. After a successful login, the Student object is passed to the Subject Enrolment System.

Student inherits name, email and password from Person, so these attributes are not repeated across classes.

**2. Input Validation**

In `validator.py`, I used regular expressions (RegEx) to check email and password formats, so that registration and login follow the required input rules. I made these methods static because they do not depend on a specific Student object.

`generate_ID()` uses `random.randint()` to produce a number and `zfill(6)` to format it as a six-digit student ID. It compares the new ID with the existing ones and generates another if there is a duplicate. The Database also checks for duplicate IDs before adding a student.

**3. Database and File Management**

In `database.py`, I implemented methods for adding, finding, updating, saving and loading student records.

I chose JSON for storage because it is simple, readable and supported by Python. `save_to_file()` converts Student and Subject objects into dictionaries before writing, and `load_from_file()` reads the JSON and restores the objects.

During development, I found that previously enrolled subjects were lost when the file was loaded. The original Subject constructor generates random IDs and marks, so it could not restore saved records. I added `Subject.from_saved_data()`, which restores the original subject ID, mark and grade without generating new values.

I also changed `save_to_file()` to write to a temporary file first and then replace the original, which reduces the risk of data loss if writing fails.

#### Testing and Integration

I tested valid and invalid registration details, duplicate emails, login failures, unique student ID generation and JSON read/write operations. I also checked that Student and Subject information stayed the same after saving and reloading, and tested the connection between the University Menu, Student Menu and Subject Enrolment System.

### c. The Subject Enrolment System (Sihan Yin)

*To be completed by the responsible team member.*

### d. The Admin System (Sheyda Niaparast)

*To be completed by the responsible team member.*

### e. GUIUniApp (Huilin Zeng, Chengfeng Yang)

#### 1. Login Window (Huilin Zeng)

I built the Login Window with Python Tkinter. It has email and password fields and a Login button.

When the user clicks Login, the program reads the input with `Entry.get()`, validates the format through the Validator class and checks the credentials through the Database and Student methods. After a successful login, it calls `show_enrolment_window(root, student, database)` to open the Enrolment Window.

I reused the existing backend classes instead of writing separate login and database functions for the GUI. This keeps the CLI and GUI consistent and avoids duplicated code.

#### 2. Enrolment Window (Chengfeng Yang)

*To be completed by Chengfeng Yang.*

#### 3. Subject Window (Chengfeng Yang)

*To be completed by Chengfeng Yang.*

#### 4. Exception Window (Huilin Zeng)

I implemented the Exception Window in `gui_errors.py` using Tkinter's `Toplevel` widget. The `show_error()` function displays error messages in a separate window for empty login fields, invalid input formats and incorrect login credentials. The Enrolment Window can reuse it when a student tries to enrol in more than four subjects, which keeps error messages consistent across the GUI.

## 5. Program Execution Instructions

During integration testing, group members ran the complete application on their own computers. We found that launching the program from different working directories could create or read `students.data` in the wrong place, so stored data was not always the same when retrieved.

To fix this, we changed the Database to build the path to `students.data` from the location of `database.py` instead of the current working directory. The CLI and GUI applications now read the same data file wherever the program is launched.

Users can still go to the `FSD_Cmp1_07_Group6/UniApp` directory and start the applications with these commands.

CLI application:

```powershell
python CLIUniApp.py
```

GUI application:

```powershell
python GUIUniApp.py
```

The GUI is for registered students, so new students need to register through CLIUniApp before logging in to GUIUniApp.

## 6. Testing Data

The project uses two data files:

- `students.data` holds the student and enrolment data the application uses.
- `test_students.data` holds sample records for development and testing.

We used the test file to check database operations without touching the main application data. The tests covered student registration, searching, updating records, saving and loading enrolled subjects, and data consistency after reloading. Both files are in JSON format.

## 7. Project Notes

The team developed the application on GitHub. Each member worked on assigned modules, which were then integrated into one application.

Student data, validation, file management and the user interfaces each live in their own modules, so the CLI and GUI can reuse the same backend functions and the system is easier to maintain and test.
