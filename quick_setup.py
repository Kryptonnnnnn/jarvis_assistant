# quick_setup.py - Run this ONCE to set up JARVIS GUI
import os
import subprocess
import sys

def install_packages():
    """Install GUI packages"""
    packages = ['flask', 'flask-socketio', 'fuzzywuzzy']
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        except:
            print(f"❌ Failed to install {package}")

def create_gui_server():
    """Create gui_server.py"""
    content = '''# gui_server.py - GUI server for JARVIS
from flask import Flask
from flask_socketio import SocketIO, emit
import threading
import webbrowser
import time
import os

class SimpleJarvisGUI:
    def __init__(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.jarvis_instance = None
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/')
        def index():
            if os.path.exists('jarvis_gui.html'):
                with open('jarvis_gui.html', 'r', encoding='utf-8') as f:
                    return f.read()
            return "<h1>JARVIS GUI</h1><p>HTML file missing</p>"
        
        @self.socketio.on('connect')
        def handle_connect():
            emit('jarvis_update', {'type': 'SYSTEM', 'message': 'Connected to JARVIS'})
        
        @self.socketio.on('toggle_voice')
        def handle_toggle():
            if self.jarvis_instance:
                self.jarvis_instance.is_active = not getattr(self.jarvis_instance, 'is_active', False)
                status = "enabled" if self.jarvis_instance.is_active else "disabled"
                emit('jarvis_update', {'type': 'AUDIO', 'message': f'Voice {status}'})
        
        @self.socketio.on('test_command')  
        def handle_test():
            if self.jarvis_instance:
                emit('jarvis_update', {'type': 'TEST', 'message': 'Test command sent'})
                try:
                    response = self.jarvis_instance.process_text_command("what time is it")
                    emit('jarvis_update', {'type': 'RESPONSE', 'message': response})
                except:
                    emit('jarvis_update', {'type': 'RESPONSE', 'message': 'Test completed'})
        
        @self.socketio.on('get_status')
        def handle_status():
            if self.jarvis_instance:
                try:
                    status = self.jarvis_instance.get_system_status()
                    emit('system_status', status)
                except:
                    emit('jarvis_update', {'type': 'SYSTEM', 'message': 'Status updated'})
        
        @self.socketio.on('send_command')
        def handle_command(data):
            command = data.get('command', '')
            if command and self.jarvis_instance:
                try:
                    response = self.jarvis_instance.process_text_command(command)
                    emit('jarvis_update', {'type': 'TEXT_RESPONSE', 'message': response})
                except:
                    emit('jarvis_update', {'type': 'RESPONSE', 'message': 'Command processed'})
    
    def start_gui(self, jarvis_instance=None):
        self.jarvis_instance = jarvis_instance
        
        def run_server():
            self.socketio.run(self.app, host='127.0.0.1', port=5555, debug=False, use_reloader=False, log_output=False)
        
        threading.Thread(target=run_server, daemon=True).start()
        time.sleep(2)
        
        try:
            webbrowser.open('http://127.0.0.1:5555')
            print("🌐 GUI: http://127.0.0.1:5555")
        except:
            print("Open: http://127.0.0.1:5555")
        
        return self.socketio
    
    def send_update(self, update_type, message):
        try:
            self.socketio.emit('jarvis_update', {'type': update_type, 'message': message})
        except:
            pass

gui = SimpleJarvisGUI()
'''
    
    with open('gui_server.py', 'w') as f:
        f.write(content)
    print("✅ Created gui_server.py")

def create_gui_html():
    """Create the beautiful HTML interface"""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>JARVIS AI Assistant</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #0c0c0c, #1a1a2e, #16213e);
            color: #00d4ff; min-height: 100vh; overflow-x: hidden;
        }
        .container {
            display: flex; flex-direction: column; justify-content: center;
            align-items: center; min-height: 100vh; padding: 20px;
            background: rgba(0, 0, 0, 0.3);
        }
        .avatar {
            width: 150px; height: 150px; border: 3px solid #00d4ff;
            border-radius: 50%; margin-bottom: 20px; position: relative;
            animation: pulse 2s infinite;
        }
        .avatar::before {
            content: ''; position: absolute; top: 50%; left: 50%;
            transform: translate(-50%, -50%); width: 80px; height: 80px;
            background: linear-gradient(45deg, #00d4ff, #00ffff);
            border-radius: 50%; animation: glow 1.5s ease-in-out infinite alternate;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0.7); }
            70% { box-shadow: 0 0 0 20px rgba(0, 212, 255, 0); }
        }
        @keyframes glow {
            from { box-shadow: 0 0 20px #00d4ff; }
            to { box-shadow: 0 0 40px #00ffff; }
        }
        .title {
            font-size: 3rem; font-weight: bold; margin-bottom: 10px; color: #00ffff;
        }
        .status {
            font-size: 1.2rem; margin-bottom: 20px; padding: 15px 30px;
            background: rgba(0, 20, 40, 0.8); border: 1px solid #00d4ff;
            border-radius: 15px; text-align: center;
        }
        .controls {
            display: flex; gap: 15px; margin-bottom: 20px; flex-wrap: wrap;
            justify-content: center;
        }
        .btn {
            background: rgba(0, 212, 255, 0.2); border: 1px solid #00d4ff;
            color: #00ffff; padding: 10px 20px; border-radius: 25px;
            cursor: pointer; font-family: inherit; transition: all 0.3s;
        }
        .btn:hover {
            background: rgba(0, 212, 255, 0.4); transform: translateY(-2px);
        }
        .command-input {
            margin: 20px 0; display: flex; gap: 10px; width: 100%; max-width: 500px;
        }
        .command-input input {
            flex: 1; background: rgba(0, 20, 40, 0.8); border: 1px solid #00d4ff;
            color: #00ffff; padding: 10px 15px; border-radius: 25px;
            font-family: inherit; outline: none;
        }
        .command-input button {
            background: #00d4ff; color: #000; border: none; padding: 10px 20px;
            border-radius: 25px; cursor: pointer; font-family: inherit; font-weight: bold;
        }
        .logs {
            background: rgba(0, 20, 40, 0.6); border: 1px solid #00d4ff;
            border-radius: 10px; padding: 20px; width: 100%; max-width: 700px;
            height: 300px; overflow-y: auto;
        }
        .log-entry {
            padding: 5px 0; color: #a0e7ff; border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        }
        .log-type { color: #00d4ff; font-weight: bold; }
        .system-stats {
            position: fixed; top: 20px; right: 20px;
            background: rgba(0, 20, 40, 0.8); border: 1px solid #00d4ff;
            border-radius: 10px; padding: 15px; font-size: 0.8rem; min-width: 180px;
        }
        .stat-item {
            display: flex; justify-content: space-between; margin-bottom: 5px;
        }
        .stat-value { color: #00ffff; font-weight: bold; }
        @media (max-width: 768px) {
            .title { font-size: 2rem; }
            .system-stats { position: relative; top: 0; right: 0; margin-top: 20px; }
        }
    </style>
</head>
<body>
    <div class="system-stats">
        <div class="stat-item"><span>Status:</span><span class="stat-value" id="system-status">OFFLINE</span></div>
        <div class="stat-item"><span>CPU:</span><span class="stat-value" id="cpu-usage">0%</span></div>
        <div class="stat-item"><span>Memory:</span><span class="stat-value" id="memory-usage">0%</span></div>
        <div class="stat-item"><span>Uptime:</span><span class="stat-value" id="uptime">00:00:00</span></div>
    </div>

    <div class="container">
        <div class="avatar"></div>
        <h1 class="title">J.A.R.V.I.S</h1>
        <div class="status" id="status">Connecting to JARVIS...</div>
        
        <div class="controls">
            <button class="btn" onclick="toggleVoice()">🎤 Toggle Voice</button>
            <button class="btn" onclick="testCommand()">🧪 Test Command</button>
            <button class="btn" onclick="getStatus()">📊 System Status</button>
            <button class="btn" onclick="clearLogs()">🗑️ Clear Logs</button>
        </div>
        
        <div class="command-input">
            <input type="text" id="commandInput" placeholder="Type a command for JARVIS..." onkeypress="if(event.key==='Enter') sendCommand()">
            <button onclick="sendCommand()">Send</button>
        </div>
        
        <div class="logs">
            <h3 style="color: #00ffff; margin-bottom: 15px; text-align: center;">ACTIVITY LOG</h3>
            <div id="log-container">
                <div class="log-entry"><span class="log-type">[SYSTEM]</span> GUI initialized</div>
            </div>
        </div>
    </div>

    <script>
        const socket = io();

        socket.on('connect', () => {
            document.getElementById('status').textContent = 'JARVIS ONLINE - READY';
            document.getElementById('system-status').textContent = 'ACTIVE';
            addLog('SYSTEM', 'Connected to JARVIS');
        });

        socket.on('jarvis_update', (data) => {
            addLog(data.type, data.message);
            if (data.type === 'WAKE') {
                document.getElementById('status').textContent = 'WAKE WORD DETECTED';
            } else if (data.type === 'READY') {
                document.getElementById('status').textContent = 'READY FOR COMMANDS';
            }
        });

        socket.on('system_status', (data) => {
            document.getElementById('cpu-usage').textContent = data.cpu || '0%';
            document.getElementById('memory-usage').textContent = data.memory || '0%';
            document.getElementById('uptime').textContent = data.uptime || '00:00:00';
        });

        function toggleVoice() {
            socket.emit('toggle_voice');
            addLog('USER', 'Voice toggle requested');
        }

        function testCommand() {
            socket.emit('test_command');
            addLog('USER', 'Test command sent');
        }

        function getStatus() {
            socket.emit('get_status');
            addLog('USER', 'Status requested');
        }

        function sendCommand() {
            const input = document.getElementById('commandInput');
            const command = input.value.trim();
            if (command) {
                socket.emit('send_command', {command: command});
                addLog('TEXT_CMD', `Sent: ${command}`);
                input.value = '';
            }
        }

        function clearLogs() {
            document.getElementById('log-container').innerHTML = '';
            addLog('USER', 'Logs cleared');
        }

        function addLog(type, message) {
            const container = document.getElementById('log-container');
            const time = new Date().toLocaleTimeString();
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `<span class="log-type">[${type}]</span> ${message} <small>(${time})</small>`;
            container.insertBefore(entry, container.firstChild);
            if (container.children.length > 30) container.removeChild(container.lastChild);
        }

        setInterval(() => socket.emit('get_status'), 10000);
    </script>
</body>
</html>'''
    
    with open('jarvis_gui.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ Created jarvis_gui.html")

def main():
    print("🚀 JARVIS GUI Quick Setup")
    print("=" * 30)
    
    print("📦 Installing packages...")
    install_packages()
    
    print("📝 Creating GUI files...")
    create_gui_server()
    create_gui_html()
    
    print("\n✅ Setup Complete!")
    print("\nNow replace your main.py with the new version and run:")
    print("python main.py")

if __name__ == "__main__":
    main()