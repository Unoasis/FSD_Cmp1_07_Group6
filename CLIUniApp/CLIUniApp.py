from database import Database


class CLIUniApp:
    CYAN = "\033[36m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    RESET = "\033[0m"

    def __init__(self, student_handler=None, admin_handler=None, database=None):
        self._database = database if database is not None else Database()
        self._current_student = None
        self._student_handler = student_handler
        self._admin_handler = admin_handler

    def run(self):
        """Show the one-line University menu until the user exits."""
        while True:
            try:
                choice = input(
                    f"{self.CYAN}University System: (A)dmin, (S)tudent, or X : "
                    f"{self.RESET}"
                ).strip().lower()
            except (EOFError, KeyboardInterrupt):
                # Move to the next line if Ctrl+D or Ctrl+C interrupts input.
                print()
                self._say_goodbye()
                return

            if choice == "a":
                self.admin_menu()
            elif choice == "s":
                self.student_menu()
            elif choice == "x":
                self._say_goodbye()
                return
            else:
                print(f"{self.RED}Invalid option. Please enter A, S or X.{self.RESET}")

    def _say_goodbye(self):
        print(f"{self.YELLOW}Thank You{self.RESET}")

    def student_menu(self):
        if self._student_handler is not None:
            self._student_handler(self._database)
            return

        try:
            import student_system
        except ModuleNotFoundError as exc:
            if exc.name != "student_system":
                raise
            print("Student System is not connected yet.")
            return

        handler = getattr(student_system, "student_menu", None)
        if not callable(handler):
            print("student_system.py needs a student_menu(database) function.")
            return
        handler(self._database)

    def admin_menu(self):
        if self._admin_handler is not None:
            self._admin_handler(self._database)
            return

        try:
            import admin_system
        except ModuleNotFoundError as exc:
            if exc.name != "admin_system":
                raise
            print("Admin System is not connected yet.")
            return

        handler = getattr(admin_system, "admin_menu", None)
        if not callable(handler):
            print("admin_system.py needs an admin_menu(database) function.")
            return
        handler(self._database)


if __name__ == "__main__":
    CLIUniApp().run()
