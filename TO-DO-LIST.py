import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import os

tasks = []

def save_tasks():
    with open("tasks.txt", "w") as file:
        for task, priority, deadline in tasks:
            file.write(f"{task},{priority},{deadline}\n")
      

def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    task, priority, deadline = parts
                    try:
                        datetime.strptime(deadline, "%Y-%m-%d %H:%M")
                        tasks.append((task, priority, deadline))
                        display_task(task, priority, deadline)
                    except ValueError:
                        print(f"Skipping invalid deadline format: {deadline}")
                else:
                    print(f"Skipping invalid line: {line.strip()}")


def display_task(task, priority, deadline):
    task_with_details = f"{task} ({priority}) - Due: {deadline}"
    task_list.insert(tk.END, task_with_details)
  

def clear_placeholder(event):
    if deadline_entry.get() == "YYYY-MM-DD HH:MM":
        deadline_entry.delete(0, tk.END)
  

def add_task():
    task = task_entry.get().strip()
    priority = priority_var.get()
    deadline = deadline_entry.get().strip()
  
    if task and deadline:
        try:
            datetime.strptime(deadline, "%Y-%m-%d %H:%M")
            tasks.append((task, priority, deadline))
            tasks.sort(key=lambda x: (["High Medium Low"].split().index(x[1]), x[2]))
            task_list.delete(0, tk.END)
      
            refresh_task_list()
            task_entry.delete(0, tk.END)
            deadline_entry.delete(0, tk.END)
            save_tasks()
        except ValueError:
            messagebox.showwarning("Input Error" "Please enter the deadline in format YYYY-MM-DD HH:MM.")
    else:
        messagebox.showwarning("Input Error", "Please enter a task and a deadline")
    
    
def delete_task():
    try:
        selected_task_index = task_list.curselection()[0]
        removed_task = tasks.pop(selected_task_index)
        refresh_task_list()
        save_tasks()
        messagebox.showinfo("Task Deleted", f"Deleted task: {removed_task[0]}")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select aa task to delete.")
    

def save_changes(task_index):
        new_task_name = task_entry.get().strip()
        new_priority = priority_var.get()
        new_deadline = deadline_entry.get().strip()
      
        if new_task_name and new_deadline:
            try:
                datetime.strptime(new_deadline, "%Y-%m-%d %H:%M")
          
                tasks[task_index] = (new_task_name, new_priority, new_deadline)
          
          
                refresh_task_list()
            
                save_tasks()
                task_entry.delete(0, tk.END)
                deadline_entry.delete(0, tk.END)
                priority_var.set("Medium")
          
                add_button.config(text="Add Task", command="add_task")
            except ValueError:
                messagebox.showwarning("Input Error", "please enter the deadline in format YYYY-MM-DD HH:MM.")
          
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields")   
      
    
def edit_task():
    try:
        selected_task_index = task_list.curselection()[0]
        selected_task = tasks[selected_task_index]
    
        task_entry.delete(0, tk.END)
        task_entry.insert(0, selected_task[0])
    
        priority_var.set(selected_task[1])
    
        deadline_entry.delete(0, tk.END)
        deadline_entry.insert(0, selected_task[2])

        add_button.config(text="Save Changes", command=lambda: save_changes(selected_task_index))
    
    
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to edit.")
    
    
def refresh_task_list():
    task_list.delete(0, tk.END)
    for t, p, d in tasks:
        display_task(t, p, d)
      
  

    

root = tk.Tk()
root.title("Task Manager with Priorities")

frame = tk.Frame(root)
frame.pack(pady=10)

task_entry = tk.Entry(frame, width=40)
task_entry.pack(side=tk.LEFT, padx=5)

priority_var = tk.StringVar(value="Medium")
priority_menu = tk.OptionMenu(frame,priority_var, "High", "Medium", "Low")
priority_menu.pack(side=tk.LEFT, padx=5)

deadline_entry = tk.Entry(frame, width=20)
deadline_entry.pack(side=tk.LEFT, padx=5)
deadline_entry.insert(0, "YYYY-MM-DD HH:MM")
deadline_entry.bind("<FocusIn>", clear_placeholder)

task_list = tk.Listbox(root, width=50, height=15)
task_list.pack(pady=10)

add_button = tk.Button(frame, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)

edit_button = tk.Button(root, text="Edit Task", command=edit_task)
edit_button.pack(pady=5)

load_tasks()

root.mainloop()