import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.master.geometry("600x300")
        self.master.title("File Deleter")

    def create_widgets(self):
        # Add input path label and entry
        self.input_path_label = tk.Label(self, text="Enter file paths (separated by comma):")
        self.input_path_label.pack(side="top")
        self.input_path_entry = tk.Entry(self, width=50)
        self.input_path_entry.pack(side="top")

        # Add date entry
        self.date_label = tk.Label(self, text="Enter date (YYYY-MM-DD HH:MM:SS):")
        self.date_label.pack(side="top")
        self.date_entry = tk.Entry(self)
        self.date_entry.pack(side="top")

        # Add before/after radio buttons
        self.before_after_var = tk.StringVar(value="before")
        self.before_radio = tk.Radiobutton(self, text="Before", variable=self.before_after_var, value="before")
        self.before_radio.pack(side="left")
        self.after_radio = tk.Radiobutton(self, text="After", variable=self.before_after_var, value="after")
        self.after_radio.pack(side="left")

        # Add delete button
        self.delete_button = tk.Button(self, text="Delete Files", command=self.delete_files)
        
        self.delete_button.pack(side="top")

        # Add completion message label
        self.completion_message_label = tk.Label(self, text="")
        self.completion_message_label.pack(side="top")

        # Quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="bottom")

    def delete_files(self):
        # Get file paths from entry
        paths_str = self.input_path_entry.get()
        if not paths_str:
            tk.messagebox.showerror("Error", "No file paths entered.")
            return
        paths = [p.strip() for p in paths_str.split(",")]

        # Get date from entry
        date_str = self.date_entry.get()
        if not date_str:
            tk.messagebox.showerror("Error", "No date entered.")
            return
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")
            return

        # Get before/after value
        before_after = self.before_after_var.get()

        # Delete files
        deleted_files = []
        for path in paths:
            if not os.path.exists(path):
                tk.messagebox.showerror("Error", f"File path {path} does not exist.")
                return
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if before_after == "before" and file_time <= date:
                        os.remove(file_path)
                        deleted_files.append(file_path)
                    elif before_after == "after" and file_time >= date:
                        os.remove(file_path)
                        deleted_files.append(file_path)

        # Show completion message
        if deleted_files:
            with open("deleted_files.txt", "w") as f:
                f.write("\n".join(deleted_files))
            self.completion_message_label.config(text=f"Task completed. Deleted files saved to deleted_files.txt.")
        else:
            self.completion_message_label.config(text="No files deleted.")  

root = tk.Tk()
app = Application(master=root)
app.mainloop()

