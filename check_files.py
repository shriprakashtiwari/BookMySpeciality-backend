import os

# Define the path to the backend directory
backend_dir = os.path.join(os.getcwd())

# List of important folders and files to check
required_folders = ['accounts', 'bookings', 'templates', 'static']
required_files = ['manage.py', 'settings.py']

# Check if the required folders exist
print("Checking required folders...\n")
for folder in required_folders:
    folder_path = os.path.join(backend_dir, folder)
    if os.path.isdir(folder_path):
        print(f"Folder found: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")

# Check if the required files exist
print("\nChecking required files...\n")
for file in required_files:
    file_path = os.path.join(backend_dir, file)
    if os.path.isfile(file_path):
        print(f"File found: {file_path}")
    else:
        print(f"File not found: {file_path}")
