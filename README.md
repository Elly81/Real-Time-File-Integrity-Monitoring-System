Real-Time-File-Integrity-Monitoring-System
A Real-Time File Integrity Monitoring System designed to detect and alert on unauthorized changes to critical files. The system uses cryptographic hashing to monitor file integrity, providing instant notifications, detailed logs, and customizable file or directory tracking.

This project is a Python-based Real-Time File Integrity Monitoring System that tracks changes to files and directories within a specified path. By leveraging cryptographic hashing (SHA-256) and file system event monitoring, the system detects unauthorized changes, additions, deletions, or renames in real time and provides alerts for integrity violations.
Features

 # Real-Time Monitoring: Automatically detects file creation, modification, deletion, and renaming events.
 # Integrity Checks: Uses SHA-256 cryptographic hashing to verify file integrity.
 # Customizable Monitoring: Users can specify the subdirectory within a base directory to monitor.
 # User-Friendly Alerts: Provides instant notifications of any detected changes or integrity violations.
 # Robust Error Handling: Gracefully handles inaccessible files due to permission issues or file absence.

 Technologies Used
 Python (Flask) - A powerful backend framework used for building the server-side logic and APIs.
 HTML5, CSS3, JavaScript: Used for crafting an intuitive, responsive, and interactive user interface.
 Bootstrap: A front-end framework that ensures the app is mobile-responsive and optimized for various devices.
 PostgreSQL: A robust, open-source relational database used to manage user authentication and store secure login credentials.
 
  How It Works

  Initial Setup: The system computes and stores hashes of all files in the monitored directory at startup.
  Continuous Monitoring: Watches the directory for events like file creation, modification, deletion, or renaming.
  Integrity Validation: When a file changes, its new hash is compared to the stored hash to detect unauthorized alterations.
  Real-Time Alerts: Notifies users of events like file tampering or unauthorized deletions in real time.

  Usage

  Clone the repository:
  git clone https://github.com/yourusername/Real-Time-File-Integrity-Monitoring-System.git
  cd Real-Time-File-Integrity-Monitoring-System
  
  Run the script:
  python app.py

  Example:
  If the base directory is C:\Users\HP PAVILION AERO, and you want to monitor the subdirectory Documents, enter Documents      when prompted.
  Configuration

  Base Directory: Modify the base_directory variable in the script to change the default directory.
  Monitoring Scope: The script monitors all subdirectories and files within the specified path recursively.

  Output

  Event Logging: Prints real-time notifications for file events (created, modified, deleted, renamed).
  Integrity Alerts: Notifies of detected integrity violations.
  Reporting Generation: It supports you to print event logs in a pdf file.
  

