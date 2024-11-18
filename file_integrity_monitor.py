import os
import time
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Function to calculate the hash of a file
def file_hash(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None  # Return None if we can't access the file

# Event handler for file system changes
class FIMEventHandler(FileSystemEventHandler):
    def __init__(self, monitored_files):
        self.monitored_files = monitored_files
    
    def on_created(self, event):
        print(f'Created: {event.src_path}')
        if event.src_path not in self.monitored_files:
            new_hash = file_hash(event.src_path)
            if new_hash is not None:
                self.monitored_files[event.src_path] = new_hash

    def on_modified(self, event):
        print(f'Modified: {event.src_path}')
        if event.src_path in self.monitored_files:
            new_hash = file_hash(event.src_path)
            if new_hash is None:
                print(f'Permission denied: {event.src_path}')
            elif new_hash != self.monitored_files[event.src_path]:
                print(f'Integrity violation detected in {event.src_path}')
                self.monitored_files[event.src_path] = new_hash  # Update the hash if modified

    def on_deleted(self, event):
        print(f'Deleted: {event.src_path}')
        if event.src_path in self.monitored_files:
            del self.monitored_files[event.src_path]

    def on_moved(self, event):
        print(f'Renamed: {event.src_path} to {event.dest_path}')
        if event.src_path in self.monitored_files:
            self.monitored_files[event.dest_path] = self.monitored_files[event.src_path]
            del self.monitored_files[event.src_path]

# Main function to set up monitoring
def main():
    base_directory = r'C:\Users\HP PAVILION AERO'  # Base directory to monitor
    
    # Prompt user for a subdirectory name
    while True:
        sub_directory_name = input("Enter the name of the subdirectory to monitor: ").strip()
        path_to_monitor = os.path.join(base_directory, sub_directory_name)
        
        # Check if the directory is valid and exists
        if os.path.isdir(path_to_monitor):
            break
        else:
            print(f"Invalid directory. Please enter a valid subdirectory name within {base_directory}.")
    
    monitored_files = {}
    
    # Calculate initial hashes
    for root, dirs, files in os.walk(path_to_monitor):
        for filename in files:
            filepath = os.path.join(root, filename)
            new_hash = file_hash(filepath)
            if new_hash is not None:
                monitored_files[filepath] = new_hash

    event_handler = FIMEventHandler(monitored_files)
    observer = Observer()
    observer.schedule(event_handler, path_to_monitor, recursive=True)
    observer.start()
    
    print("Monitoring started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    main()
