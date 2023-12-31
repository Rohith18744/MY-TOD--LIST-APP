
import functions
import PySimpleGUI as sg
import time
import os

if not os.path.exists("todos.txt"):
    with open("todos.txt","w") as file:
        pass
sg.theme("voilet")
clock=sg.Text('',key="clock")
label = sg.Text("Type in a TODO-LIST")
input_box = sg.InputText(key='todo', tooltip="Enter todo")
add_button = sg.Button("Add")
list_box = sg.Listbox(values=functions.get_todos('todos.txt'), key='todos', enable_events=True, size=[45, 10])
edit_button = sg.Button("Edit")
complete_button=sg.Button("Complete")
exit_button=sg.Button("Exit")
window = sg.Window('TODO-LIST APP',
                    layout=[[clock],[label],
                    [input_box, add_button], [list_box, edit_button,complete_button],[exit_button]]
                    , font=('Helvetica', 20))

while True:
    event, values = window.read(timeout=10)
    window["clock"].update(value=time.strftime("%b %d,%Y %H:%M:%S"))
    if event == "Add":
        new_todo = values['todo'] + "\n"
        if new_todo.strip():  # Check if the input is not empty or contains only whitespaces
            todos = functions.get_todos('todos.txt')
            todos.append(new_todo)
            functions.write_todos('todos.txt', todos)
            window['todos'].update(values=todos)

    if event == "Edit":
        try:
            todo_to_edit = values['todos'][0]
            new_todo = values['todo'] + "\n"
            todos = functions.get_todos('todos.txt')
            index = todos.index(todo_to_edit)
            todos[index] = new_todo
            functions.write_todos('todos.txt', todos)
            window['todos'].update(values=todos)
        except IndexError:
            sg.popup("Please select an index",font=('Helvetica', 20))
            
    if event == "Complete":
        try:
            todo_to_complete=values['todos'][0]
            todos=functions.get_todos('todos.txt')
            todos.remove(todo_to_complete)
            functions.write_todos('todos.txt',todos)
            window['todos'].update(values=todos)
            window['todo'].update(value=' ')
        except IndexError:
            sg.popup("Please select an index",font=('Helvetica', 20))
    if event == "Exit":
        break
    if event == "todos":
        window['todo'].update(value=values['todos'][0])

    if event == sg.WIN_CLOSED:
        break

window.close()
