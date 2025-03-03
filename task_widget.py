import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class TaskWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Widget")
        self.tasks = []

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        tk.Label(self.frame, text="Task:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.task_entry = tk.Entry(self.frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Priority:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.priority_entry = tk.Entry(self.frame, width=30)
        self.priority_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Due Date:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.due_date_entry = tk.Entry(self.frame, width=30)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Reminder:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.reminder_entry = tk.Entry(self.frame, width=30)
        self.reminder_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.task_listbox.grid(row=5, column=0, columnspan=2, pady=10)

        self.modify_button = tk.Button(self.frame, text="Modify Task", command=self.modify_task)
        self.modify_button.grid(row=6, column=0, pady=5)

        self.remove_button = tk.Button(self.frame, text="Remove Task", command=self.remove_task)
        self.remove_button.grid(row=6, column=1, pady=5)

        self.link_button = tk.Button(self.frame, text="Link Tasks", command=self.link_tasks)
        self.link_button.grid(row=7, column=0, pady=5)

        self.search_entry = tk.Entry(self.frame, width=30)
        self.search_entry.grid(row=8, column=0, padx=5, pady=5)
        self.search_button = tk.Button(self.frame, text="Search Tasks", command=self.search_tasks)
        self.search_button.grid(row=8, column=1, padx=5, pady=5)

        self.filter_button = tk.Button(self.frame, text="Filter Tasks", command=self.filter_tasks)
        self.filter_button.grid(row=9, column=0, columnspan=2, pady=5)

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_entry.get()
        due_date = self.due_date_entry.get()
        reminder = self.reminder_entry.get()

        if task:
            try:
                if due_date:
                    datetime.strptime(due_date, "%Y-%m-%d")
                if reminder:
                    datetime.strptime(reminder, "%Y-%m-%d %H:%M")
                self.tasks.append({"task": task, "priority": priority if priority else None, "due_date": due_date if due_date else None, "reminder": reminder if reminder else None, "linked_tasks": []})
                self.update_task_listbox()
                self.task_entry.delete(0, tk.END)
                self.priority_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
                self.reminder_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date format. Please enter date as YYYY-MM-DD and time as YYYY-MM-DD HH:MM.")
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def modify_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            new_task = simpledialog.askstring("Modify Task", "Enter new task:")
            if new_task:
                self.tasks[selected_task_index[0]]["task"] = new_task
                self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task to modify.")

    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.tasks.pop(selected_task_index[0])
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task to remove.")

    def link_tasks(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            link_index = simpledialog.askinteger("Link Tasks", "Enter index of task to link:")
            if link_index is not None and 0 <= link_index < len(self.tasks):
                self.tasks[selected_task_index[0]]["linked_tasks"].append(link_index)
                self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "You must select a task to link.")

    def search_tasks(self):
        search_term = self.search_entry.get()
        if search_term:
            search_results = [task for task in self.tasks if search_term.lower() in task["task"].lower()]
            self.update_task_listbox(search_results)
        else:
            messagebox.showwarning("Warning", "You must enter a search term.")

    def filter_tasks(self):
        filter_term = simpledialog.askstring("Filter Tasks", "Enter filter (priority, due_date, status):")
        if filter_term:
            if filter_term in ["High", "Medium", "Low"]:
                filter_results = [task for task in self.tasks if task["priority"] == filter_term]
            elif filter_term == "due_date":
                filter_results = [task for task in self.tasks if task["due_date"] is not None]
            elif filter_term == "status":
                filter_results = [task for task in self.tasks if task["reminder"] is not None and datetime.strptime(task["reminder"], "%Y-%m-%d %H:%M") < datetime.now()]
            else:
                messagebox.showwarning("Warning", "Invalid filter. Please enter priority (High, Medium, Low), due date, or status.")
                return
            self.update_task_listbox(filter_results)
        else:
            messagebox.showwarning("Warning", "You must enter a filter term.")

    def update_task_listbox(self, tasks=None):
        self.task_listbox.delete(0, tk.END)
        tasks = tasks if tasks is not None else self.tasks
        for task in tasks:
            task_str = task["task"]
            if task["priority"]:
                task_str += f" [Priority: {task['priority']}]"
            if task["due_date"]:
                task_str += f" [Due: {task['due_date']}]"
            if task["reminder"]:
                task_str += f" [Reminder: {task['reminder']}]"
            if task["linked_tasks"]:
                linked_tasks_str = ", ".join(str(i) for i in task["linked_tasks"])
                task_str += f" [Linked: {linked_tasks_str}]"
            self.task_listbox.insert(tk.END, task_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskWidget(root)
    root.mainloop()