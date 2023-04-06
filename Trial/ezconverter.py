import csv
import os
import hashlib
import gzip
import tkinter as tk
from tkinter import filedialog

class LogConverterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Log Converter")


        # Create input file selection button
        self.input_files_button = tk.Button(master, text="Select input files", command=self.select_input_files)
        self.input_files_button.pack(padx=100, pady=50)

        # Create output file selection button
        self.output_file_button = tk.Button(master, text="Select output file", command=self.select_output_file)
        self.output_file_button.pack(padx=100, pady=50)

        # Create conversion button
        self.convert_button = tk.Button(master, text="Convert", command=self.convert)
        self.convert_button.pack(padx=100, pady=50)

        # Initialize file selection variables
        self.input_files = []
        self.output_file = ""

    def select_input_files(self):
        # Open file dialog to select input files
        filenames = filedialog.askopenfilenames(title="Select input files", filetypes=(("Gzip files", "*.gz"), ("All files", "*.*")))

        # Update input file list
        self.input_files = list(filenames)

    def select_output_file(self):
        # Open file dialog to select output file
        filename = filedialog.asksaveasfilename(title="Select output file", defaultextension=".csv", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

        # Update output file
        self.output_file = filename

    def convert(self):
        # Convert each input file to the output file
        if len(self.input_files) == 0:
            tk.messagebox.showerror("Error", "Please select at least one input file.")
            return

        if self.output_file == "":
            tk.messagebox.showerror("Error", "Please select an output file.")
            return

        header_written = False 
        processed_rows = set()

        if os.path.exists(self.output_file):
            mode = 'a' # append if file exists
            header_written = True
        
            with open(self.output_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    processed_rows.add(hash_row(row))

        else:
            mode = 'w' # write if file does not exist

        with open(self.output_file, mode, newline='') as f_output:
            csv_writer = csv.writer(f_output, delimiter=',')

            if not header_written:
                csv_writer.writerow(["timestamp","timezone", "request size", "source ip", "cache status", "status code", "request method", "url","empty", "hierarchy destination ip", "mime"])
                header_written = True

            for input_file in self.input_files:
                with gzip.open(input_file, 'rt') as f_input:
                    for line in f_input:
                        data = []
                        for item in line.split(" "):
                            if item != "":
                                data.append(item)
                        row_hash = hash_row(data) 
                        if row_hash not in processed_rows:
                            csv_writer.writerow(data)
                            processed_rows.add(row_hash)

        tk.messagebox.showinfo("Success", "Conversion complete.")

def hash_row(row):
    return hashlib.sha1(str(row).encode()).hexdigest()

root = tk.Tk()
app = LogConverterGUI(root)
root.mainloop()



# I'm not sure if this is the best way to do this, but it works. I'm open to suggestions.