from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional
import argparse
import os


@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str
    created_at: str


class TodoList:
    def __init__(self, data_file: str = "todo_data.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                    self.tasks = [Task(**t) for t in raw]
            except Exception:
                self.tasks = []
        else:
            self.tasks = []

    def _save(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in self.tasks], f, ensure_ascii=False, indent=2)

    def _next_id(self) -> int:
        return max((t.id for t in self.tasks), default=0) + 1

    def add_task(self, title: str, description: str = "") -> Task:
        t = Task(
            id=self._next_id(),
            title=title,
            description=description,
            status="Pending",
            created_at=datetime.utcnow().isoformat(),
        )
        self.tasks.append(t)
        self._save()
        return t

    def list_tasks(self) -> str:
        if not self.tasks:
            return "Tasks:\n"
        lines = ["Tasks:"]
        for t in self.tasks:
            lines.append(f"- {t.title} [{t.status}]")
        return "\n".join(lines) + "\n"

    def complete_task(self, title: Optional[str] = None, task_id: Optional[int] = None) -> bool:
        for t in self.tasks:
            if (title and t.title == title) or (task_id and t.id == task_id):
                t.status = "Completed"
                self._save()
                return True
        return False

    def remove_task(self, title: Optional[str] = None, task_id: Optional[int] = None) -> bool:
        for i, t in enumerate(self.tasks):
            if (title and t.title == title) or (task_id and t.id == task_id):
                del self.tasks[i]
                self._save()
                return True
        return False

    def clear(self):
        self.tasks = []
        self._save()


def main():
    parser = argparse.ArgumentParser(description="To-Do List Manager")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add")
    p_add.add_argument("title")
    p_add.add_argument("--desc", default="")

    p_list = sub.add_parser("list")

    p_complete = sub.add_parser("complete")
    p_complete.add_argument("title")

    p_remove = sub.add_parser("remove")
    p_remove.add_argument("title")

    p_clear = sub.add_parser("clear")

    parser.add_argument("--data", default="todo_data.json")

    args = parser.parse_args()
    todo = TodoList(data_file=args.data)

    if args.cmd == "add":
        t = todo.add_task(args.title, args.desc)
        print(f"Added: {t.title} (id={t.id})")
    elif args.cmd == "list":
        print(todo.list_tasks())
    elif args.cmd == "complete":
        ok = todo.complete_task(title=args.title)
        print("Completed" if ok else "Task not found")
    elif args.cmd == "remove":
        ok = todo.remove_task(title=args.title)
        print("Removed" if ok else "Task not found")
    elif args.cmd == "clear":
        todo.clear()
        print("Cleared all tasks")
    else:
        parser.print_help()
