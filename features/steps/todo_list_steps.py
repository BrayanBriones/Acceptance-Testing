from behave import given, when, then
import tempfile
import os
from todo_list import TodoList


@given("the to-do list is empty")
def step_given_empty(context):
    # Creo un archivo temporal para simular la base de datos de la lista
    fd, path = tempfile.mkstemp(prefix="behave_todo_", text=True)
    os.close(fd)
    context.data_file = path
    context.todo = TodoList(data_file=path)
    context.todo.clear()


@given('the to-do list contains tasks:')
def step_given_contains(context):
     # Si aún no existe la lista, la creo igual que el step anterior
    if not getattr(context, "data_file", None):
        fd, path = tempfile.mkstemp(prefix="behave_todo_", text=True)
        os.close(fd)
        context.data_file = path
        context.todo = TodoList(data_file=path)
        context.todo.clear()
    # Agrego cada tarea de la tabla del feature
    for row in context.table:
        title = row.get("Task") or row.get("task")
        status = row.get("Status") if "Status" in context.table.headings else None
        t = context.todo.add_task(title)
        # Si viene marcada como completada desde el feature, la marco aquí
        if status and status.lower() == "completed":
            context.todo.complete_task(task_id=t.id)


@when('the user adds a task "{title}"')
def step_when_add(context, title):
    # Agrego la tarea directamente
    context.todo.add_task(title)


@when('the user lists all tasks')
def step_when_list(context):
    # Guardo el output para validarlo luego
    context.output = context.todo.list_tasks()


@when('the user marks task "{title}" as completed')
def step_when_complete(context, title):
    # Marco la tarea como completada usando el título
    context.todo.complete_task(title=title)


@when('the user clears the to-do list')
def step_when_clear(context):
    # Limpio toda la lista
    context.todo.clear()


@when('the user removes task "{title}"')
def step_when_remove(context, title):
    # Elimino la tarea según el título
    context.todo.remove_task(title=title)


@then('the to-do list should contain "{title}"')
def step_then_contains(context, title):
    out = context.todo.list_tasks()
    # Verifico que el título sí esté en el listado
    assert title in out, f"Expected '{title}' in output: {out}"


@then('the output should contain:')
def step_then_output_contains(context):
    expected = context.text.strip()
    actual = context.output.strip()
    # Comparación exacta del output
    assert expected == actual, f"Expected exact output:\n{expected}\nGot:\n{actual}"


@then('the to-do list should show task "{title}" as completed')
def step_then_completed(context, title):
    out = context.todo.list_tasks()
    # Verifico que salga con el formato de completado
    assert f"- {title} [Completed]" in out, f"Task not marked completed: {out}"


@then('the to-do list should be empty')
def step_then_empty(context):
    out = context.todo.list_tasks()
    # La lista vacía debe mostrar solo el encabezado
    assert out.strip() == "Tasks:", f"Expected empty tasks, got: {out}"


@then('the to-do list should not contain "{title}"')
def step_then_not_contains(context, title):
    out = context.todo.list_tasks()
    # La tarea no debería aparecer después de eliminarla
    assert title not in out, f"Task '{title}' still present: {out}"
