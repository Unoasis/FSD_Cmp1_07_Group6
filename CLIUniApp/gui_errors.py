import tkinter as tk


def show_error(parent, message):
    """Display an error window for GUIUniApp."""

    error_window = tk.Toplevel(parent)
    error_window.title("Error")
    error_window.geometry("350x160")
    error_window.resizable(False, False)

    # Keep the error window associated with its parent.
    error_window.transient(parent)

    # Display the error message.
    tk.Label(
        error_window,
        text=message,
        fg="red",
        wraplength=300
    ).pack(pady=25)

    # Close the error window when OK is clicked.
    tk.Button(
        error_window,
        text="OK",
        width=10,
        command=error_window.destroy
    ).pack(pady=5)

    # Modal error window.
    error_window.grab_set()
    error_window.focus_set()



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Exception Test")
    root.geometry("300x150")

    tk.Button(
        root,
        text="Test Error",
        command=lambda: show_error(root, "Invalid email format")
    ).pack(pady=40)

    root.mainloop()

