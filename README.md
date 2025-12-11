# To-Do List Manager


Pequeña aplicación de línea de comandos para gestionar una lista de tareas.

Archivos principales:
- [todo_list.py](todo_list.py): Lógica principal (importable).
- [main.py](main.py): Punto de entrada; ejecutar `python main.py`.

Instalación y uso rápido:

```bash
python -m pip install --user -r requirements.txt  # si necesita paquetes
```

CLI ejemplos:

```bash
python main.py add "Buy groceries"
python main.py list
python main.py complete "Buy groceries"
python main.py remove "Buy groceries"
python main.py clear
```
# Acceptance-Testing