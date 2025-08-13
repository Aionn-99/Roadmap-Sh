import sys 
import json
import os
from datetime import datetime

FILENAME =  "tasks.json"
# --------------- File Handling ---------------
def load_tasks():
    # kenapa ? untuk cek apakah file exist atau tidak
    if not os.path.exists(FILENAME):
        # kenapa ?
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

# --------------- Helper ---------------
def get_valid_task_id(arg_index):
    if len(sys.argv) <= arg_index:
        print("Harap masukkan ID tugas.")
        sys.exit(1)
    
    if not sys.argv[arg_index].isdigit():
        print("ID harus berupa angka.")
        sys.exit(1)

    return int(sys.argv[arg_index])

# --------------- Core Features ---------------
def add_task(description):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
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
            save_tasks(tasks)
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

def main():


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

        if not sys.argv[2].isdigit():
            print("ID tugas harus berupa angka.")
            sys.exit()

        mark_status(int(sys.argv[2]), "done")

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Harap masukkan ID tugas.")
            sys.exit(1)

        if not sys.argv[2].isdigit():
            print("ID tugas harus berupa angka.")
            sys.exit(1)

        mark_status(int(sys.argv[2]), "in-progress")

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Harap masukkan ID tugas.")
            sys.exit(1)
        
        if not sys.argv[2].isdigit():
            print("ID tugas harus berupa angka.")
            sys.exit(1)
        
        delete_task(int(sys.argv[2]))

    elif command == "update":
        if len(sys.argv) < 4:
            print("Harap masukkan ID tugas dan deskripsi baru.")
            sys.exit(1)

        if not sys.argv[2].isdigit():
            print("ID tugas harus berupa angka.")
            sys.exit(1)

        new_description = ' '.join(sys.argv[3:])
        update_task(int(sys.argv[2]), new_description)


    else:
        print("Perintah tidak dikenal:", command)


if __name__=="__main__":
    main()
