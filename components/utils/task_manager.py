import json
import os

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

    def save_tasks(self):
        """Save tasks to JSON file."""
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, title, description="", priority="Medium"):
        """Add a new task."""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "priority": priority,
            "completed": False
        }
        self.tasks.append(task)
        self.save_tasks()

    def get_tasks(self):
        """Return all tasks."""
        return self.tasks

    def complete_task(self, task_id):
        """Mark a task as completed."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                break
        self.save_tasks()

    def delete_task(self, task_id):
        """Delete a task by id."""
        self.tasks = [task for task in self.tasks if task["id"] != task_id]
        self.save_tasks()
