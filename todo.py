import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json

# Task Class
class Task:
    def __init__(self, title, description, category, completed=False):
        self.title = title
        self.description = description
        self.category = category
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def __repr__(self):
        return f"{self.title} - {self.category} ({'Completed' if self.completed else 'Pending'})"

# File Handling Functions
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)

def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return [Task(**data) for data in json.load(f)]
    except FileNotFoundError:
        return []

# Task Manager GUI Class
class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Personal To-Do List")
        self.root.geometry("600x500")
        self.root.config(bg="#dfe6e9")  # Background color

        self.tasks = load_tasks()

        # Style setup for buttons and tasks
        self.setup_styles()

        # Widgets Setup
        self.create_widgets()
        self.update_task_list()
        self.update_status()

    def setup_styles(self):
        """Set up custom styles for widgets."""
        self.root.option_add("*TButton*Font", "Helvetica 12")
        self.root.option_add("*TLabel*Font", "Helvetica 12")
        self.root.option_add("*TEntry*Font", "Helvetica 12")

    def create_widgets(self):
        # Frame for input and task operations
        input_frame = tk.Frame(self.root, bg="#74b9ff", pady=10, padx=10)  # Blue frame
        input_frame.pack(side="top", fill="x")

        # Button to add tasks with a pop-up window
        self.add_task_btn = tk.Button(input_frame, text="Add Task", command=self.show_add_task_dialog,
                                      bg="#55efc4", fg="black", activebackground="#00b894", font=("Arial", 12, "bold"))
        self.add_task_btn.grid(row=0, column=0, padx=10, pady=5)

        # Task Listbox with scrollbar
        listbox_frame = tk.Frame(self.root, bg="#dfe6e9")  # Light grey background
        listbox_frame.pack(side="top", fill="both", expand=True)

        self.task_listbox = tk.Listbox(listbox_frame, width=70, height=10, font="Helvetica 12", selectmode='SINGLE',
                                       bg="white", fg="black", selectbackground="#fdcb6e", selectforeground="black")
        self.task_listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Buttons for task operations
        button_frame = tk.Frame(self.root, bg="#74b9ff", pady=10, padx=10)  # Blue frame
        button_frame.pack(side="bottom", fill="x")

        self.complete_task_btn = tk.Button(button_frame, text="Mark Completed", command=self.mark_task_completed,
                                           bg="#fab1a0", fg="black", activebackground="#e17055", font=("Arial", 12, "bold"))
        self.complete_task_btn.grid(row=0, column=0, padx=10, pady=5)

        self.delete_task_btn = tk.Button(button_frame, text="Delete Task", command=self.delete_task,
                                         bg="#ff7675", fg="black", activebackground="#d63031", font=("Arial", 12, "bold"))
        self.delete_task_btn.grid(row=0, column=1, padx=10, pady=5)

        self.exit_btn = tk.Button(button_frame, text="Exit", command=self.exit_app,
                                  bg="#74b9ff", fg="black", activebackground="#0984e3", font=("Arial", 12, "bold"))
        self.exit_btn.grid(row=0, column=2, padx=10, pady=5)

        # Status bar
        self.status_label = tk.Label(self.root, text="Total Tasks: 0 | Completed Tasks: 0", anchor="w", bg="#dfe6e9", font=("Arial", 10))
        self.status_label.pack(side="bottom", fill="x")

    def show_add_task_dialog(self):
        """Show a pop-up dialog to add a new task."""
        title = simpledialog.askstring("Task Title", "Enter the task title:")
        description = simpledialog.askstring("Task Description", "Enter the task description:")
        category = simpledialog.askstring("Task Category", "Enter the task category (e.g., Work, Personal, Urgent):")

        if not title or not description or not category:
            messagebox.showerror("Error", "All fields are required.")
            return

        task = Task(title, description, category)
        self.tasks.append(task)
        self.update_task_list()
        save_tasks(self.tasks)
        self.update_status()

    def update_task_list(self):
        """Update the task listbox with all tasks."""
        self.task_listbox.delete(0, 'end')
        for task in self.tasks:
            display_text = self.get_display_text(task)
            self.task_listbox.insert('end', display_text)

    def get_display_text(self, task):
        """Return the display text for a task, with special formatting for completed tasks."""
        if task.completed:
            return f"{task.title} - {task.category} (✔ Completed)"
        else:
            return f"{task.title} - {task.category} (Pending)"

    def mark_task_completed(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No task selected.")
            return

        task = self.tasks[selected[0]]
        task.mark_completed()
        self.update_task_list()
        save_tasks(self.tasks)
        self.update_status()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No task selected.")
            return

        del self.tasks[selected[0]]
        self.update_task_list()
        save_tasks(self.tasks)
        self.update_status()

    def update_status(self):
        """Update the status bar with total and completed task counts."""
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task.completed])
        self.status_label.config(text=f"Total Tasks: {total_tasks} | Completed Tasks: {completed_tasks}")

    def exit_app(self):
        save_tasks(self.tasks)
        self.root.quit()


# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
