import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import functions

app = dash.Dash(__name__)
server=app.server

todos = functions.get_todos("todos.txt")

app.layout = html.Div([
    html.H1("MY TODO APP"),
    html.H2("This is my todo app"),
    html.P("This app is used to increase your productivity."),

    # Display todos and checkboxes
    html.Div([
        dcc.Checklist(
            id=f"checkbox-{index}",
            options=[{'label': todo, 'value': todo} for index, todo in enumerate(todos)],
            inline=True
        )
        for index, todo in enumerate(todos)
    ]),

    # Input for adding new todo
    dcc.Input(id='new-todo', type='text', placeholder='Add new todo...'),
    html.Button('Add', id='add-button'),
])


@app.callback(
    Output('checkbox-container', 'children'),
    [Input(f'checkbox-{index}', 'value') for index in range(len(todos))],
    prevent_initial_call=True
)
def update_todos(*checkbox_values):
    global todos
    todos = [todo for todo, value in zip(todos, checkbox_values) if value]

    # Update the todos in the file
    functions.write_todos(todos)

    return [
        dcc.Checklist(
            id=f"checkbox-{index}",
            options=[{'label': todo, 'value': todo} for index, todo in enumerate(todos)],
            inline=True
        )
        for index, todo in enumerate(todos)
    ]


@app.callback(
    Output('new-todo', 'value'),
    [Input('add-button', 'n_clicks')],
    [State('new-todo', 'value')],
    prevent_initial_call=True
)
def add_todo(n_clicks, new_todo):
    global todos
    if new_todo:
        todos.append(new_todo)
        functions.write_todos(todos)
    return ''


if __name__ == '__main__':
    app.run_server(debug=True)
