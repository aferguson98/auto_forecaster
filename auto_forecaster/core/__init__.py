import math


class FileLoader:
    def __init__(self, total_files, current_pos=0):
        self.total_files = total_files
        self.current_pos = current_pos
        if self.total_files != 0:
            self.print_progress()

    def adjust(self, loaded=0, total=0):
        self.current_pos += loaded
        self.total_files += total
        if self.total_files != 0:
            self.print_progress()

    def print_progress(self):
        progress = math.floor(self.current_pos / self.total_files * 100)
        progress_left = 100 - progress
        print("\r\tLoading: |" + "#" * progress + "-" * progress_left + "|",
              self.current_pos, "out of", self.total_files, "files", end="")
