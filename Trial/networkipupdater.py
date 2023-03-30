import pandas as pd
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.master.geometry("500x200")
        #title of the window
        self.master.title("Network Ip Address updater")

    def create_widgets(self):
        # Add input file button
        self.input_file = None
        self.input_file_label = tk.Label(self, text="No input file selected.")
        self.input_file_label.pack(side="top")
        self.add_input_button = tk.Button(self, text="Select input file", command=self.select_input_file)
        self.add_input_button.pack(side="top")

        # Add date entry
        self.date_label = tk.Label(self, text="Enter date (YYYY-MM-DD):")
        self.date_label.pack(side="top")
        self.date_entry = tk.Entry(self)
        self.date_entry.pack(side="top")

        # Convert button
        self.convert_button = tk.Button(self, text="Convert", command=self.convert)
        self.convert_button.pack(side="top")

        # Add completion message label
        self.completion_message_label = tk.Label(self, text="")
        self.completion_message_label.pack(side="top")

        # Quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="bottom")

    def select_input_file(self):
        # Select input file
        filepath = filedialog.askopenfilename(title="Select input file", filetypes=[("CSV files", "*.csv")])
        
        if filepath:
            self.input_file = filepath
            self.input_file_label.config(text=filepath)

    def convert(self):
        if not self.input_file:
            tk.messagebox.showerror("Error", "No input file selected.")
            return

        # Read in CSV file
        df = pd.read_csv(self.input_file)

        # Get date from entry
        date_str = self.date_entry.get()

        # Parse date string into datetime object
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Add new column with given date
        df['Date'] = date

        # Write out updated data to new or existing CSV file
        output_file = filedialog.asksaveasfilename(title="Save as", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        
        if output_file:
            try:
                existing_df = pd.read_csv(output_file)
                merged_df = pd.concat([existing_df, df], ignore_index=True)
                merged_df.to_csv(output_file, index=False)
            except FileNotFoundError:
                df.to_csv(output_file, index=False)

            # Clear date entry and show completion message
            self.date_entry.delete(0, tk.END)
            self.completion_message_label.config(text="Task completed.")

root = tk.Tk()
app = Application(master=root)
app.mainloop()