import os
import psutil
import subprocess
import platform
from datetime import datetime
from utils.logger import get_logger

class SystemController:
    def __init__(self):
        self.logger = get_logger(__name__)
        
    def get_system_info(self):
        """Get system information"""
        try:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Get memory info
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Get disk info
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            info = f"System Status: CPU usage is {cpu_percent}%, "
            info += f"Memory usage is {memory_percent}%, "
            info += f"Disk usage is {disk_percent}%"
            
            return info
            
        except Exception as e:
            self.logger.error(f"Error getting system info: {e}")
            return "Unable to retrieve system information."
    
    def open_application(self, app_name):
        """Open an application"""
        try:
            app_name = app_name.lower()
            
            # Common application mappings
            app_map = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "chrome": "chrome.exe",
                "firefox": "firefox.exe",
                "explorer": "explorer.exe",
                "cmd": "cmd.exe",
                "terminal": "cmd.exe"
            }
            
            if app_name in app_map:
                subprocess.Popen(app_map[app_name])
                return f"Opening {app_name}"
            else:
                # Try to open directly
                subprocess.Popen(app_name)
                return f"Attempting to open {app_name}"
                
        except Exception as e:
            self.logger.error(f"Error opening application {app_name}: {e}")
            return f"Unable to open {app_name}"
    
    def get_current_time(self):
        """Get current time"""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The current time is {time_str}"
    
    def shutdown_system(self):
        """Shutdown the system"""
        try:
            system = platform.system()
            if system == "Windows":
                os.system("shutdown /s /t 60")
                return "System will shutdown in 60 seconds"
            elif system == "Linux" or system == "Darwin":
                os.system("shutdown -h +1")
                return "System will shutdown in 1 minute"
        except Exception as e:
            self.logger.error(f"Error shutting down system: {e}")
            return "Unable to shutdown system"