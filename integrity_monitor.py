import hashlib
import json
import os
 
folder = "subfolder"
baseline_file = "baseline.json"
 
 
def get_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
 
 
def scan_folder():
    files = {}
 
    # os.walk recurses into nested folders too — os.listdir would not.
    for root, _dirs, filenames in os.walk(folder):
    
        for name in filenames:
            full_path = os.path.join(root, name)
            #root="subfolder/nested", name="file3.txt" → "subfolder/nested/file3.txt". os.path.join handles the slash correctly on any OS
            rel_path = os.path.relpath(full_path, folder) #converts #"subfolder/nested/file3.txt" → "nested/file3.txt"
 
            try:
                files[rel_path] = get_hash(full_path)
            except (PermissionError, FileNotFoundError) as e:
                print(f"Skipped {rel_path}: {e}")
 
    return files
 
 
print("===== FILE INTEGRITY MONITOR =====")
print("1. Create Baseline")
print("2. Check for Changes")
 
choice = input("Enter choice: ")
 
 
if choice == "1":
 
    if not os.path.isdir(folder):
        print(f"\nFolder '{folder}' does not exist.")
    else:
        files = scan_folder()
 
        with open(baseline_file, "w") as f:
            json.dump(files, f, indent=4)
 
        print("\nBaseline created successfully!")
        print("Files scanned:", len(files))
 
 
elif choice == "2":
 
    if not os.path.exists(baseline_file):
        print("\nPlease create a baseline first.")
    else:
        try:
            with open(baseline_file, "r") as f:
                old_files = json.load(f)
        except json.JSONDecodeError:
            print("\nbaseline.json is corrupted or empty. Recreate the baseline.")
            old_files = None
 
        if old_files is not None:
            new_files = scan_folder()
 
            changes = False
 
            print("\n===== INTEGRITY REPORT =====")
 
            # Check deleted and modified files
            for file in old_files:
 
                if file not in new_files:
                    print("DELETED :", file)
                    changes = True
 
                elif old_files[file] != new_files[file]:
                    print("MODIFIED:", file)
                    changes = True
 
            # Check added files
            for file in new_files:
 
                if file not in old_files:
                    print("ADDED   :", file)
                    changes = True
 
            if not changes:
                print("No changes detected.")
 
else:
    print("Invalid choice.")
 
