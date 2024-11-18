from flask import Flask, jsonify, render_template, request, send_file, session, redirect, url_for, flash
import psycopg2
import os
import threading
import time
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime, timedelta
from fpdf import FPDF
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Global variables to hold monitored files and event logs
monitored_files = {}
events_log = []  # List to hold events for real-time updates

# Supported file extensions
SUPPORTED_EXTENSIONS = {'.pdf', '.pptx', '.pub', '.rar', '.xlsx', '.bmp', '.docx', '.accdb', '.txt'}

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
    def __init__(self):
        super().__init__()

    def log_event(self, message):
        timestamped_event = {
            'message': message,
            'timestamp': datetime.now()
        }
        events_log.append(timestamped_event)
        self.cleanup_old_events()

    def cleanup_old_events(self):
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        global events_log
        events_log = [event for event in events_log if event['timestamp'] > twenty_four_hours_ago]

    def on_created(self, event):
        if any(event.src_path.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
            print(f'Created: {event.src_path}')
            if event.src_path not in monitored_files:
                new_hash = file_hash(event.src_path)
                if new_hash is not None:
                    monitored_files[event.src_path] = new_hash
                    self.log_event(f'File created: {event.src_path}')

    def on_modified(self, event):
        if event.src_path in monitored_files:
            print(f'Modified: {event.src_path}')
            new_hash = file_hash(event.src_path)
            if new_hash is None:
                print(f'Permission denied: {event.src_path}')
            elif new_hash != monitored_files[event.src_path]:
                print(f'Integrity violation detected in {event.src_path}')
                monitored_files[event.src_path] = new_hash
                self.log_event(f'File modified: {event.src_path}')

    def on_deleted(self, event):
        if event.src_path in monitored_files:
            print(f'Deleted: {event.src_path}')
            del monitored_files[event.src_path]
            self.log_event(f'File deleted: {event.src_path}')

    def on_moved(self, event):
        if event.src_path in monitored_files:
            print(f'Renamed: {event.src_path} to {event.dest_path}')
            monitored_files[event.dest_path] = monitored_files[event.src_path]
            del monitored_files[event.src_path]
            self.log_event(f'File renamed: {event.src_path} to {event.dest_path}')

def start_monitoring(directory):
    observer = Observer()
    event_handler = FIMEventHandler()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if any(filepath.endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                new_hash = file_hash(filepath)
                if new_hash is not None:
                    monitored_files[filepath] = new_hash

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

@app.route('/')
def index():
    # Check if user is logged in
    if 'admin' in session:
        return render_template('index.html')  # Serve the index page
    return redirect(url_for('login'))  # Redirect to login if not logged in

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admin_credentials WHERE username = %s AND password_hash = %s", (username, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin:
            session['admin'] = username
            return redirect(url_for('index'))  # Redirect to the index page
        else:
            flash('Invalid username or password. Please try again.')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
       

        # Connect to the database and insert the new user
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        try:
            # Insert the new user into the admin_credentials table
            cursor.execute("INSERT INTO admin_credentials (username, password_hash) VALUES (%s, %s)", (username, password))
            conn.commit()  # Commit the transaction

            # Show a success message and redirect to the login page
            flash("Registration successful! Please log in.")
            return redirect('/login')

        except psycopg2.IntegrityError:
            # Handle duplicate username errors
            flash("Username already exists. Please choose another one.")
            conn.rollback()

        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('admin', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/monitored-files', methods=['GET'])
def monitored_files_page():
    if 'admin' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    base_directory = r'C:\Users\HP PAVILION AERO'  # Adjust as necessary
    monitored_files_list = [f for f in monitored_files if os.path.isfile(f)]
    return render_template('monitored-files.html', files=monitored_files_list)

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')

@app.route('/api/events', methods=['GET'])
def get_events():
    global events_log
    events_to_return = [{'message': event['message'], 'timestamp': event['timestamp'].isoformat()} for event in reversed(events_log)]
    return jsonify(events_to_return)

@app.route('/api/start-monitoring', methods=['POST'])
def start_monitoring_route():
    directory = request.json.get('sub_directory')
    if not directory:
        return jsonify({"error": "No directory provided."}), 400

    base_directory = r'C:\Users\HP PAVILION AERO'  # Adjust as necessary
    full_directory_path = os.path.join(base_directory, directory)

    if not os.path.isdir(full_directory_path):
        return jsonify({"error": "Invalid directory provided."}), 400

    # Clear previously monitored files
    monitored_files.clear()

    thread = threading.Thread(target=start_monitoring, args=(full_directory_path,))
    thread.start()
    return jsonify({"message": f"Started monitoring: {full_directory_path}"}), 200

@app.route('/api/download-report', methods=['GET'])
def download_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="File Integrity Monitoring Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Event Log:", ln=True)
    pdf.ln(5)

    for event in events_log:
        message = event['message']
        timestamp = event['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        pdf.multi_cell(0, 10, txt=f"{message} at {timestamp}", border=0)

    report_path = "event_report.pdf"
    pdf.output(report_path)
    
    return send_file(report_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
