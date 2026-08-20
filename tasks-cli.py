import datetime
import json
import os
import sys

count = 0
listoftasks = []

if os.path.exists('tasks.json'):
    with open('tasks.json', 'r') as file:
        try:
            listoftasks = json.load(file)
            if listoftasks:
                count = max(task['id'] for task in listoftasks)
        except json.JSONDecodeError:
            listoftasks = []
        except OSError:
            print("Could not access the tasks.json file.")

class Task:
    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.status = 'todo'
        self.createdAt = datetime.datetime.now().isoformat()
        self.updatedAt = self.createdAt
        task = {'id' : self.id, 
                'description' : self.description, 
                'status' : self.status, 
                'createdAt' : self.createdAt, 
                'updatedAt' : self.updatedAt}
        listoftasks.append(task)

    @staticmethod
    def _save():
        with open('tasks.json', 'w') as file:
            json.dump(listoftasks, file, indent=4)

    @staticmethod
    def update(id, new_description):
        for task in listoftasks:
            if task['id'] == id:
                task['description'] = new_description
                task['updatedAt'] = datetime.datetime.now().isoformat()
                print(f"Task {id} updated to '{new_description}'")
                Task._save()
                return
        print(f"Task ID {id} does not exist.")


    @staticmethod
    def delete(id):
        for task in listoftasks:
            if task['id'] == id:
                listoftasks.remove(task)
                print(f"Deleted task {id} '{task['description']}'")
                Task._save()
                return
        print(f"Task ID {id} does not exist.")


    @staticmethod
    def mark_in_progress(id):
        for task in listoftasks:
            if task['id'] == id:
                task['status'] = 'in-progress'
                task['updatedAt'] = datetime.datetime.now().isoformat()
                print(f"Task {id} '{task['description']}' marked 'in-progress'")
                Task._save()
                return
        print(f"Task ID {id} does not exist.")
            
    @staticmethod
    def mark_done(id):
        for task in listoftasks:
            if task['id'] == id:
                task['status'] = 'done'
                task['updatedAt'] = datetime.datetime.now().isoformat()
                print(f"Task {id} '{task['description']}' marked 'done'")
                Task._save()
                return
        print(f"Task ID {id} does not exist. ")

    @staticmethod
    def clear():
        global listoftasks, count
        listoftasks.clear()
        count = 0
        Task._save()
        print("All tasks have been cleared!")

    @staticmethod
    def list(status = None):
        if status == None:
            print("--- LIST OF ALL TASKS ---")
            for task in listoftasks:
                print(f"Task ID: {task['id']}, Task: {task['description']}")
        elif status == 'todo':
            print("--- LIST OF ALL TASKS THAT ARE NOT DONE ---")
            for task in listoftasks:
                if task['status'] == 'todo':
                    print(f"Task ID: {task['id']}, Task: {task['description']}")
        elif status == 'in-progress':
            print("--- LIST OF ALL TASKS THAT ARE IN PROGRESS ---")
            for task in listoftasks:
                if task['status'] == 'in-progress':
                    print(f"Task ID: {task['id']}, Task: {task['description']}")
        elif status == 'done':
            print("--- LIST OF ALL TASKS THAT ARE DONE ---")
            for task in listoftasks:
                if task['status'] == 'done':
                    print(f"Task ID: {task['id']}, Task: {task['description']}")
        else:
            print(f"Invalid status: '{status}'. Use 'todo', 'in-progress', or 'done'.") 


def add(description):
    global count
    count += 1
    Task(count, description)
    Task._save()
    print(f"NEW TASK ADDED \nTask ID: {count} \nTask: {description}")


try:
    if len(sys.argv) < 2:
        print('Please provide a command')
    elif sys.argv[1] == 'add':
        add(sys.argv[2])
    elif sys.argv[1] == 'update':
        Task.update(int(sys.argv[2]), sys.argv[3])
    elif sys.argv[1] == 'delete':
        Task.delete(int(sys.argv[2]))
    elif sys.argv[1] == 'mark-in-progress':
        Task.mark_in_progress(int(sys.argv[2]))
    elif sys.argv[1] == 'mark-done':
        Task.mark_done(int(sys.argv[2]))
    elif sys.argv[1] == 'list':
        if len(sys.argv) > 2:
            Task.list(sys.argv[2])
        else:
            Task.list()
    elif sys.argv[1] == 'clear':
        Task.clear()
    else:
        print('Invalid command!')
except IndexError:
    print("Missing argument.")
except ValueError:
    print("Task ID must be a number.")