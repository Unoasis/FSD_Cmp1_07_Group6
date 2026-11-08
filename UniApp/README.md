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
├── admin.py               # Admin model (view, group, partition, remove, clear)
├── admin_controller.py    # Admin menu and output
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
| Sheyda Niaparast | Admin System: `Admin` model and `AdminController` (show, group, partition, remove and clear students), error handling, sample I/O formatting and integration with `CLIUniApp`. |
| Chengfeng Yang | University System (CLIUniApp entry point, menu routing and the shared Database), GUIUniApp (Enrolment Window and Subject Window). |
| Sihan Yin |  |

## 4. Implementation Details

This section follows the Assessment 1 Part 2 marking scheme.

### a. The University System (Chengfeng Yang)

#### Implementation and Main Functions

I was responsible for the University System in `CLIUniApp.py`, the entry point of the CLI application. It shows the main menu, sends the user to the Admin System or the Student System, and creates the Database that every menu shares.

**1. Main Menu and Navigation**

`run()` shows `University System: (A)dmin, (S)tudent, or X :` in cyan and reads the user's choice in a loop. The input is stripped and converted to lower case, so `A`, `a` and ` a ` are all accepted. `A` calls `admin_menu()`, `S` calls `student_menu()`, and `X` prints `Thank You` in yellow and ends the program. Any other input shows a red error message and the menu appears again.

When the user leaves a submenu with `x`, that function returns and control goes back to the loop in `run()`. This is how users move back and forth between the menus.

**2. Shared Database**

The constructor creates one `Database` object and stores it in the private attribute `_database`, which matches the composition relationship between CLIUniApp and Database in our Part 1 class diagram. The same object is passed to `student_system.student_menu(database)` and `admin_system.admin_menu(database)`.

During integration testing we found that two separate Database objects overwrote each other's changes, because each one keeps its own list of students in memory and saves that list over the file. With one shared object, a student registered in the Student System appears straight away in the Admin System, and a student removed by the admin can no longer log in.

**3. Connecting the Submenus**

`student_menu()` and `admin_menu()` import the teammates' modules inside the method rather than at the top of the file. While the other systems were still being written, the University System could still run and print "not connected yet" instead of crashing. The method checks `exc.name`, so only a missing submenu file is treated this way; if a submenu file exists but a module it needs is missing, the error is raised again so real problems stay visible.

The constructor also accepts optional `student_handler` and `admin_handler` functions. I used them to test the menu routing with simple stand-in functions before the real submenus were finished. In the final program they are not passed, so the real modules are used.

**4. Error Handling and Output**

The `input()` call in the main menu is wrapped in `try/except` for `EOFError` and `KeyboardInterrupt`, so pressing Ctrl+D or Ctrl+C at the main menu prints `Thank You` and exits cleanly instead of showing a traceback.

Colours use ANSI escape codes: cyan (36) for the menu prompt, yellow (33) for `Thank You`, red (31) for errors, and 0 to reset. The reset code at the end of the prompt keeps the user's typing in the normal colour. The prompt text, colours and indentation follow the sample I/O.

#### Testing and Integration

Before the other systems were ready, I tested the routing with stand-in submenus: upper- and lower-case options, extra spaces, invalid options, empty input, and Ctrl+C and Ctrl+D at the main menu.

After the Student, Subject Enrolment and Admin Systems were finished, I ran the full sample I/O scenario from `CLIUniApp.py`, covering registration, login, enrolment, admin actions and exit, and compared the text, colours and indentation with the sample line by line. I also checked that all menus received the same Database object and that changes made in one menu were visible in the others.

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

#### Implementation and Main Functions

I was responsible for the Admin System. Admins already exist, so there is no login: from the University menu an admin goes straight to the Admin System and can show all students, group them by grade, partition them into PASS/FAIL, remove a student by ID, or clear the database. I split the work into `admin.py` (the `Admin` model) and `admin_controller.py` (the `AdminController`), following the Model and Controller structure recommended in the brief.

**1. Admin Model (`admin.py`)**

`Admin` inherits from `Person` and has no printing or input. The `Database` is passed into each method rather than stored, so `Admin` only depends on `Database`, as in our Part 1 class diagram.

- `view_all_students()` reloads `students.data` and returns the students, so the admin always sees the latest saved data.
- `group_by_grade()` returns `{grade: [Student, ...]}`. The grade comes from `Subject.grade_from_mark()` using the student's average mark, so the grade rules are only defined in one place.
- `categorise_pass_fail()` returns the passed and failed students. A student passes when the average mark is at least `PASS_MARK` (50).
- `remove_student()` finds the student by ID, saves the remaining students and returns the removed one, or `None` if the ID does not exist. It also accepts a short ID such as `12345` for `012345`.
- `clear_all_students()` saves an empty list to empty the file.
- `admin_access()` always returns `True`, because admins do not log in.

**2. Admin Controller (`admin_controller.py`)**

`AdminController.run()` shows the `Admin System (c/g/p/r/s/x)` menu and calls one method per option until the admin enters `x`. It reads the input, calls `Admin`, and prints the results with the same wording, colours, tab indentation and two-decimal marks as the sample I/O. Show and group print `< Nothing to Display >` when there are no students, while partition prints `FAIL --> []` and `PASS --> []`, as in the sample. Clearing asks for a `(Y)ES/(N)O` confirmation first. `admin_menu(database)` is the entry point that `CLIUniApp.py` calls.

**3. File Management**

The Admin System never opens `students.data` directly. It reads with `Database.load_from_file()` and writes with `Database.save_to_file()`. `Database` has no remove or clear method, so `Admin.save_students()` replaces the student list held by the `Database` and then saves it. A cleaner version would add `remove_student()` and `clear()` to `Database`.

**4. Error Handling**

Invalid menu options, empty or non-numeric IDs, and IDs that do not exist all show an error message. Clearing only happens on `Y`. File write errors show a message instead of crashing, and Ctrl+C or Ctrl+D returns to the previous menu.

#### Testing and Integration

I tested the Admin System through the University menu with students in different grade bands. I checked show, group and partition output, removing an existing, missing, empty and non-numeric ID, clearing with `N`, an invalid answer and `Y`, all views on an empty database, and that a removed student stays removed after restarting. The Admin System shares one `Database` with the Student System, so newly registered or enrolled students appear straight away in the admin views, and a removed student can no longer log in.

### e. GUIUniApp (Huilin Zeng, Chengfeng Yang)

#### 1. Login Window (Huilin Zeng)

I built the Login Window with Python Tkinter. It has email and password fields and a Login button.

When the user clicks Login, the program reads the input with `Entry.get()`, validates the format through the Validator class and checks the credentials through the Database and Student methods. After a successful login, it calls `show_enrolment_window(root, student, database)` to open the Enrolment Window.

I reused the existing backend classes instead of writing separate login and database functions for the GUI. This keeps the CLI and GUI consistent and avoids duplicated code.

#### 2. Enrolment Window (Chengfeng Yang)

I built the Enrolment Window in `gui_enrolment.py` as an `EnrolmentWindow` class. After a successful login, the Login Window hides itself with `withdraw()` and calls `show_enrolment_window(root, student, database)`, which creates this class. The window is a `Toplevel` of the root window, because a Tkinter program should have only one `Tk()` root and one event loop.

The window shows the student's name and ID, the number of enrolled subjects ("Currently enrolled: n / 4 subjects", updated through a `StringVar`) and a `ttk.Progressbar`. It has three buttons: Enrol, Show Subjects and Logout.

When the student clicks Enrol, the window calls `student.enrol_subject()`. The four-subject limit is checked inside the Student class rather than in the GUI, so the CLI and GUI follow the same rule. If the student already has four subjects, the method returns `None` and the window calls `show_error()` to open the Exception Window with "Students are allowed to enrol in 4 subjects only." The Enrol button stays active on purpose, so the Exception Window appears when a student tries to enrol in a fifth subject.

Otherwise the new subject is saved straight away with `database.update_student()`. If saving fails, the window removes the new subject again and shows an error, so the window and `students.data` never disagree.

Error windows use the Enrolment Window as their parent, not the root. After login the root window is withdrawn, and we found during testing that an error window attached to it would stay hidden while still blocking input, making the program look frozen.

The Logout button and the window's close button (bound with `protocol("WM_DELETE_WINDOW", ...)`) both call `close_window()`. It closes the Subject Window if it is open, destroys the Enrolment Window and shows the Login Window again with `deiconify()`, so another student can log in.

#### 3. Subject Window (Chengfeng Yang)

I built the Subject Window in `gui_subjects.py` as a `SubjectWindow` class. It lists the logged-in student's enrolled subjects in a `ttk.Treeview` table with three columns: Subject ID, Mark and Grade. Below the table it shows the number of subjects and the average mark, or "No subjects enrolled yet." when the list is empty.

`refresh()` deletes every row and inserts one row for each subject in `student.get_enrolment_list()`, so rows are never duplicated. The data comes from the same Student object that the Enrolment Window has just saved, so the table always matches `students.data`.

The Enrolment Window keeps a reference to the open Subject Window. Clicking Show Subjects again refreshes and raises the existing window instead of opening a second one, and the table refreshes automatically after each successful enrolment. When the Subject Window is closed, an `on_close` callback tells the Enrolment Window. Its parent is the Enrolment Window, so it also closes when the student logs out.

I tested both windows by enrolling one to four subjects, attempting a fifth, refreshing the table while it was open, logging in with a student who already had four subjects, and logging out and back in as another student. I also checked that the IDs, marks and grades shown in the GUI matched `students.data` and the CLI's subject list.

#### 4. Exception Window (Huilin Zeng)

I implemented the Exception Window in `gui_errors.py` using Tkinter's `Toplevel` widget. The `show_error()` function displays error messages in a separate window for empty login fields, invalid input formats and incorrect login credentials. The Enrolment Window can reuse it when a student tries to enrol in more than four subjects, which keeps error messages consistent across the GUI.

## 5. Program Execution Instructions

**Requirements:** Python 3 with Tkinter, which is included with the standard Python installer. The project only uses the Python standard library, so no extra libraries need to be installed.

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

We used the test file to check database operations without touching the main application data. The tests covered student registration, searching, updating records, saving and loading enrolled subjects, and data consistency after reloading. The Admin System was also tested through the University menu using students in different grade bands (see section 4d). Both files are in JSON format.

## 7. Project Notes

The code follows the Model, View and Controller structure recommended in the brief:

- **Model:** `Person`, `Student`, `Subject`, `Database` and `Admin` hold the data and the rules.
- **Controller:** `AdminController`, `SubjectController` and the functions in `student_system.py` handle the menus and call the model classes.
- **View:** the CLI menus and output in `CLIUniApp.py` and the controllers, and the Tkinter windows in `GUIUniApp.py`, `gui_enrolment.py`, `gui_subjects.py` and `gui_errors.py`.

`Validator` provides input validation and student ID generation for both interfaces.

The team developed the application on GitHub. Each member worked on assigned modules, which were then integrated into one application.

Student data, validation, file management and the user interfaces each live in their own modules, so the CLI and GUI can reuse the same backend functions and the system is easier to maintain and test.
