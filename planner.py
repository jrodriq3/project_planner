import csv
import tkinter
from tkinter.filedialog import askopenfilename
from collections import namedtuple
Task = namedtuple("Task", ["title", "duration", "prerequisites"])

def read_tasks(filename):
    tasks = {}
    for row in csv.reader(open(filename)):
        number = int(row[0])
        title = row[1]
        duration = float(row[2])
        prerequisites = set(map(int, row[3].split()))
        tasks[number] = Task(title, duration, prerequisites)
    return tasks

def order_tasks(tasks):
    incomplete = set(tasks)
    completed = set()
    start_weeks = {}
    while incomplete:
        for task_number in incomplete:
            task = tasks[task_number]
            if task.prerequisites.issubset(completed):
                earliest_start_day = 0
                for prereq_number in task.prerequisites:
                    prereq_end_day = start_weeks[prereq_number] + \
                                     tasks[prereq_number].duration
                    if prereq_end_day > earliest_start_day:
                        earliest_start_day = prereq_end_day
                start_weeks[task_number] = earliest_start_day
                incomplete.remove(task_number)
                completed.add(task_number)
                break
    return start_weeks

def draw_chart(tasks, canvas, row_height=40, title_width=300, line_height=40, \
                        day_width=20, bar_height=20, title_indent=20, font_size=-16):
    height = canvas["height"]
    width = canvas["width"]
    week_width = 5 * day_width
    canvas.create_line(0, row_height, width, line_height, \
                        fill="red", width="5")
    canvas.create_line(0, row_height * 2, width, line_height * 2, \
                        fill="red", width="5")
    canvas.create_line(0, row_height * 3, width, line_height * 3, \
                        fill="red", width="5")
    canvas.create_line(0, row_height * 4, width, line_height * 4, \
                        fill="purple", width="5")
    canvas.create_line(0, row_height * 5, width, line_height * 5, \
                        fill="red", width="5")
    canvas.create_line(0, row_height * 6, width, line_height * 6, \
                        fill="red", width="5")
    canvas.create_line(0, row_height * 7, width, line_height * 7, \
                        fill="red", width="5")
    canvas.create_line(0, row_height * 8, width, line_height * 8, \
                        fill="red", width="5")
    canvas.create_line(0, row_height * 9, width, line_height * 9, \
                        fill="red", width="5")
    
    for month_number in range(5):
        x = title_width + month_number * week_width
        canvas.create_line(x, 0, x,height, fill="blue", width="5")
        canvas.create_text(x + week_width / 2, row_height / 2, \
            text=f"Month {month_number +1}", \
                font=("Helvetica", font_size, "bold"))
        start_weeks = order_tasks(tasks)
        y = row_height
        for task_number in start_weeks:
                task = tasks[task_number]
                canvas.create_text(title_indent, y + row_height / 2, \
                    text=task.title, anchor=tkinter.W, \
                        font=("Helvetica", font_size))
                bar_x = title_width + start_weeks[task_number] \
                    * day_width
                bar_y = y + (row_height - bar_height) / 2
                bar_width = task.duration * day_width
                canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, \
                                bar_y + bar_height, fill="blue")
                y += row_height

def open_project():
    filename = askopenfilename(title="Open Project", initialdir=".", \
                                filetypes=[("CSV Document", "*.csv")])
    tasks = read_tasks(filename)
    draw_chart(tasks, canvas)

root = tkinter.Tk()
root.title("My Project Planner")
root.resizable(width=False, height=False)
button_frame = tkinter.Frame(root, padx=5, pady=5)
button_frame.pack(side="top", fill="x")
open_button = tkinter.Button(button_frame, text="Open project...", \
                            command = open_project)
open_button.pack(side="left")
canvas = tkinter.Canvas(root, width=800, height=400, bg="white")
canvas.pack(side="bottom")
tkinter.mainloop()

    
