
---

# Real-Time File Integrity Monitoring System  

A **Real-Time File Integrity Monitoring System** designed to detect and alert on unauthorized changes to critical files. The system uses cryptographic hashing to monitor file integrity, providing instant notifications, detailed logs, and customizable file or directory tracking.  

This Python-based system leverages cryptographic hashing (SHA-256) and file system event monitoring to detect unauthorized changes, additions, deletions, or renames in real time and provides alerts for integrity violations.  

## Features  
- **Real-Time Monitoring**: Automatically detects file creation, modification, deletion, and renaming events.  
- **Integrity Checks**: Uses SHA-256 cryptographic hashing to verify file integrity.  
- **Customizable Monitoring**: Users can specify a subdirectory within a base directory to monitor.  
- **User-Friendly Alerts**: Provides instant notifications of any detected changes or integrity violations.  
- **Robust Error Handling**: Gracefully handles inaccessible files due to permission issues or file absence.  

## Technologies Used  
### Backend:  
- **Python (Flask)**: A powerful backend framework for server-side logic and APIs.  
- **Watchdog**: Library for monitoring real-time file system events.  
- **Hashlib**: Built-in Python module for cryptographic operations.  

### Frontend:  
- **HTML5, CSS3, JavaScript**: Used to craft an intuitive, responsive, and interactive user interface.  
- **Bootstrap**: Ensures mobile responsiveness and device optimization.  

### Database:  
- **PostgreSQL**: A robust, open-source relational database for user authentication and secure credential storage.  

## How It Works  
1. **Initial Setup**: Computes and stores hashes of all files in the monitored directory at startup.  
2. **Continuous Monitoring**: Watches the directory for events like file creation, modification, deletion, or renaming.  
3. **Integrity Validation**: Compares new file hashes to stored hashes to detect unauthorized changes.  
4. **Real-Time Alerts**: Notifies users of events like file tampering or unauthorized deletions in real time.  

## Usage  
### Clone the Repository:  
```bash
git clone https://github.com/yourusername/Real-Time-File-Integrity-Monitoring-System.git  
cd Real-Time-File-Integrity-Monitoring-System  
```  

### Run the Script:  
```bash
python app.py  
```  

### Example:  
If the base directory is `C:\Users\HP PAVILION AERO`, and you want to monitor the subdirectory `Documents`, enter `Documents` when prompted.  

## Configuration  
- **Base Directory**: Modify the `base_directory` variable in the script to change the default directory.  
- **Monitoring Scope**: The script monitors all subdirectories and files within the specified path recursively.  

## Output  
- **Event Logging**: Prints real-time notifications for file events (created, modified, deleted, renamed).  
- **Integrity Alerts**: Notifies of detected integrity violations.  
- **Report Generation**: Supports exporting event logs into a PDF file.  


---

