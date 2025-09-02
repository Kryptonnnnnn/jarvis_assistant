import os
import shutil
import subprocess
from pathlib import Path
from utils.logger import get_logger

class FileManager:
    def __init__(self):
        self.logger = get_logger(__name__)
        
    def open_file(self, filename):
        """Open a file"""
        try:
            if os.path.exists(filename):
                os.startfile(filename)  # Windows
                return f"Opening {filename}"
            else:
                return f"File {filename} not found."
        except Exception as e:
            self.logger.error(f"Error opening file {filename}: {e}")
            return f"Unable to open {filename}"