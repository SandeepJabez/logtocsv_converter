import csv
import os
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Add input file button
        self.input_files = []
        self.add_input_button = tk.Button(self, text="Add input file", command=self.add_input)
        self.add_input_button.pack(side="top")

        # Add output file button
        self.output_file = None
        self.add_output_button = tk.Button(self, text="Choose output file", command=self.choose_output)
        self.add_output_button.pack(side="top")

        # Convert button
        self.convert_button = tk.Button(self, text="Convert", command=self.convert)
        self.convert_button.pack(side="top")

        # Exit button
        self.quit = tk.Button(self, text="Exit", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def add_input(self):
        # Add one or more input files
        filepaths = filedialog.askopenfilenames(title="Select input file", filetypes=[("Log files", "*.log")])
        self.input_files.extend(filepaths)

    def choose_output(self):
        # Choose output file
        filepath = filedialog.asksaveasfilename(title="Save as", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        self.output_file = filepath

    def convert(self):
        if not self.input_files:
            messagebox.showerror("Error", "No input files selected.")
            return
        if not self.output_file:
            messagebox.showerror("Error", "No output file selected.")
            return

        # Convert all input files
        header_written = False
        temp_file = "temp.txt"
        saved_hash = ""

        with open(self.output_file, 'a', newline='') as f_output:
            csv_writer = csv.writer(f_output, delimiter=',')

            for input_file in self.input_files:
                with open(input_file, 'r') as f_input:
                    for line in f_input:
                        data = []
                        for item in line.split(" "):
                            if item != "":
                                data.append(item)

                        # Check if data is already in the CSV
                        current_hash = hashlib.md5(str(data).encode('utf-8')).hexdigest()
                        if current_hash == saved_hash:
                            continue

                        saved_hash = current_hash

                        # Write header if not already written
                        if not header_written:
                            csv_writer.writerow(["timestamp","timezone", "request size", "source ip", "cache status", "status code", "request method", "url","empty", "hierarchy destination ip", "mime"])
                            header_written = True

                        # Write data to CSV
                        csv_writer.writerow(data)

        # Write saved hash to temp file
        with open(temp_file, "w") as f:
            f.write(saved_hash)

        messagebox.showinfo("Success", "Conversion complete.")


root = tk.Tk()
root.title("Log Converter")
app = Application(master=root)
app.mainloop()
