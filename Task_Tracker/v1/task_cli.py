import argparse
import json
import os
from datetime import datetime

FILENAME =  "tasks.json"
# --------------- File Handling ---------------
def load_tasks():
    # kenapa ? untuk cek apakah file exist atau tidak
    if not os.path.exists(FILENAME):
        # kenapa ? membuat file json baru dengan awal list kosong
        save_tasks([])
    try:
        with open(FILENAME, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("File tasks.json corrupt, membuat ulang file baru.")
        save_tasks([])
        return []

def save_tasks(tasks):
    with open(FILENAME, "w") as f:
        json.dump(tasks, f, indent=4)

# --------------- Core Features ---------------
def add_task(description):
    # kenapa ? memuat task dari task.json
    tasks = load_tasks()
    # kenapa ? membuat id baru untuk tugas baru
    new_id = max([t["id"] for t in tasks], default=0) + 1
    """
    kenapa ? membuat dictionary untuk tugas baru dengan id baru , 
    description, dan status awal todo
    """
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
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
    task_found = False

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = new_status
            t["updatedAt"] = datetime.now().isoformat()
            task_found = True
            break
    
    if task_found:
        save_tasks(tasks) 
        print(f"Task {task_id} diperbarui menjadi {new_status}.")
    else:
        print(f"Task {task_id} tidak ditemukan.")

def delete_task(task_id):
    tasks = load_tasks()
    if any(t["id"] == task_id for t in tasks):
        tasks = [t for t in tasks if t["id"] != task_id]
        save_tasks(tasks)
        print(f"Berhasil menghapus task {task_id}")
    else:
        print(f"Task {task_id} tidak ditemukan")


def update_task(task_id, new_description):
    tasks = load_tasks()
    task_found = False

    for t in tasks:
        if t["id"] == task_id:
            t["description"] = new_description
            t["updatedAt"] = datetime.now().isoformat()
            task_found = True
            break

    if task_found:
        save_tasks(tasks)
        print(f"Task {task_id} berhasil diperbarui.")

    else:
        print(f"Task {task_id} tidak ditemukan.")

# --------------- CLI Setup ---------------
def main():
    parser = argparse.ArgumentParser(description="Simple Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Tambah task baru")
    add_parser.add_argument("description", help="Deskripsi task")

    # list
    list_parser = subparsers.add_parser("list", help="List semua task")
    list_parser.add_argument("--status", choices=["todo", "done", "in-progress"], help="Filter berdasarkan status")

    # mark-in-progress
    progress_parser = subparsers.add_parser("mark-in-progress", help="Tandai task sedang dikerjakan")
    progress_parser.add_argument("id", type=int, help="ID task")
    
    # PERBAIKAN 2: Menambahkan parser untuk "mark-done" yang hilang
    done_parser = subparsers.add_parser("mark-done", help="Tandai task telah selesai")
    done_parser.add_argument("id", type=int, help="ID task")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Hapus task")
    delete_parser.add_argument("id", type=int, help="ID task")

    # update
    update_parser = subparsers.add_parser("update", help="Perbarui deskripsi task")
    update_parser.add_argument("id", type=int, help="ID task")
    update_parser.add_argument("description", help="Deskripsi baru task")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks(args.status)
    elif args.command == "mark-done":
        mark_status(args.id, "done")
    elif args.command == "mark-in-progress":
        mark_status(args.id, "in-progress")
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "update":
        update_task(args.id, args.description)

if __name__ == "__main__":
    main()
