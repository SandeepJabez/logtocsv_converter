import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.master.geometry("500x200")
        #title of the window
        self.master.title("File Deletion Tool")

    def create_widgets(self):
        # Add input folder button
        self.input_folder = None
        self.input_folder_label = tk.Label(self, text="No input folder selected.")
        self.input_folder_label.pack(side="top")
        self.add_input_button = tk.Button(self, text="Select input folder", command=self.select_input_folder)
        self.add_input_button.pack(side="top")

        # Add date entry
        self.date_label = tk.Label(self, text="Enter date (YYYY-MM-DD):")
        self.date_label.pack(side="top")
        self.date_entry = tk.Entry(self)
        self.date_entry.pack(side="top")

        # Add delete option button
        self.delete_option = tk.IntVar()
        self.delete_before = tk.Radiobutton(self, text="Delete files before the specified date", variable=self.delete_option, value=0)
        self.delete_before.pack(side="top")
        self.delete_after = tk.Radiobutton(self, text="Delete files after the specified date", variable=self.delete_option, value=1)
        self.delete_after.pack(side="top")

        # Delete button
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_files)
        self.delete_button.pack(side="top")

        # Add completion message label
        self.completion_message_label = tk.Label(self, text="")
        self.completion_message_label.pack(side="top")

        # Quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="bottom")

    def select_input_folder(self):
        # Select input folder
        folderpath = filedialog.askdirectory(title="Select input folder")
        
        if folderpath:
            self.input_folder = folderpath
            self.input_folder_label.config(text=folderpath)

    def delete_files(self):
        if not self.input_folder:
            tk.messagebox.showerror("Error", "No input folder selected.")
            return

        # Get date from entry
        date_str = self.date_entry.get()

        # Parse date string into datetime object
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Check whether to delete files before or after the specified date
        if self.delete_option.get() == 0:
            file_condition = lambda f: os.path.getmtime(os.path.join(self.input_folder, f)) < datetime.timestamp(date)
        else:
            file_condition = lambda f: os.path.getmtime(os.path.join(self.input_folder, f)) > datetime.timestamp(date)

        # Delete files
        files_to_delete = [f for f in os.listdir(self.input_folder) if file_condition(f)]
        for f in files_to_delete:
            os.remove(os.path.join(self.input_folder, f))

        # Clear date entry and show completion message
        self.date_entry.delete(0, tk.END)
        self.completion_message_label.config(text="Task completed.")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
