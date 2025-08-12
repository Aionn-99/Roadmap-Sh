import sys 
import json
import os
from datetime import datetime

FILENAME =  "tasks.json"

def load_tasks():
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            json.dump([], f)
    with open(FILENAME, "r") as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(FILENAME, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updateAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added succesfully (ID: {new_id})")

def list_tasks(status_filter=None):
    tasks = load_tasks()
    if status_filter:
        tasks = [t for t in tasks if t["status"] == status_filter]

    if not tasks:
        print("Tidak ada tugas yang ditemukan.")
        return
    
    for t in tasks:
        print(f"[{t['id']}] {t['description']} - {t['status']}")

def mark_status(task_id, new_status):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = new_status
            t["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} tidak ditemukan.")


if len(sys.argv) < 2:
    print("Harap masukkan perintah. Contoh: python task_cli.py add 'Belajar Python' ")
    sys.exit(1)

command = sys.argv[1]

if command == "add":
    if len(sys.argv) < 3:
        print("Deskripsi tugas harus diisi.")
        sys.exit(1)
    add_task(sys.argv[2])

elif command == "list":
    if len(sys.argv) > 2:
        status = sys.argv[2]
        if status not in ["todo", "done", "in-progress"]:
            print("Status filter tidak valid. Gunakan: todo, done, in-progress")
            sys.exit(1)
        list_tasks(status)
    else:
        list_tasks()

elif command == "mark-done":
    if len(sys.argv) < 3:
        print("Harap masukkan ID tugas.")
        sys.exit(1)
    mark_status(int(sys.argv[2]), "done")

elif command == "mark-in-progress":
    if len(sys.argv) < 3:
        print("Harap masukkan ID tugas.")
        sys.exit(1)
    mark_status(int(sys.argv[2]), "in-progress")

else:
    print("Perintah tidak dikenal:", command)
