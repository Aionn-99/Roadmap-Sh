import subprocess
import os
import json

FILENAME = "tasks.json"

def run_cmd(cmd):
    print(f"> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout.strip())
    if result.stderr:
        print("Error:", result.stderr.strip())
    print("-" * 50)

# Bersihkan file tasks.json sebelum tes
if os.path.exists(FILENAME):
    os.remove(FILENAME)

print("=== MULAI PENGUJIAN TASK CLI ===\n")

# 1. Tambah task
run_cmd("python3 task_cli.py add Belajar Python CLI")
run_cmd("python3 task_cli.py add Membaca dokumentasi Python")
run_cmd("python3 task_cli.py add Mengerjakan latihan coding")

# 2. List semua task
run_cmd("python3 task_cli.py list")

# 3. Update task ID 2
run_cmd('python3 task_cli.py update 2 Membaca dokumentasi resmi Python')

# 4. Tandai task ID 1 sebagai in-progress
run_cmd("python3 task_cli.py mark-in-progress 1")

# 5. Tandai task ID 3 sebagai done
run_cmd("python3 task_cli.py mark-done 3")

# 6. List berdasarkan status
run_cmd("python3 task_cli.py list todo")
run_cmd("python3 task_cli.py list in-progress")
run_cmd("python3 task_cli.py list done")

# 7. Hapus task ID 2
run_cmd("python3 task_cli.py delete 2")

# 8. List semua task lagi untuk cek hasil
run_cmd("python3 task_cli.py list")

# 9. Coba hapus task yang tidak ada
run_cmd("python3 task_cli.py delete 99")

print("\n=== PENGUJIAN SELESAI ===")
