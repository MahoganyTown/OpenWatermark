import os


class File:
    def __init__(self, filepath: str) -> None:
        # Extension of file
        self.extension = os.path.splitext(filepath)[1]
        # Name of file without extension
        self.filename = os.path.basename(filepath)
        # Full path of file
        self.path = filepath
        
    
    def exists(self) -> bool:
        return os.path.exists(self.path)


    def is_image(self) -> bool:
        return self.extension != '.pdf'