import csv
import os
import tkinter as tk
from tkinter import filedialog

def convert_to_csv(input_file, output_file):
    header_written = False
    if os.path.exists(output_file):
        mode = 'a' # append if file exists
        header_written = True
    else:
        mode = 'w' # write if file does not exist

    with open(input_file, 'r') as f_input, open(output_file, mode, newline='') as f_output:
        csv_writer = csv.writer(f_output, delimiter=',')

        if not header_written:
            csv_writer.writerow(["timestamp","timezone", "request size", "source ip", "cache status", "status code", "request method", "url","empty", "hierarchy destination ip", "mime"])
            header_written = True

        for line in f_input:
            data = []
            for item in line.split(" "):
                if item != "":
                    data.append(item)
            csv_writer.writerow(data)

def browse_input_file():
    filename = filedialog.askopenfilename(filetypes=[('Log files', '*.log')])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, filename)

def browse_output_file():
    filename = filedialog.asksaveasfilename(defaultextension='.csv')
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, filename)

def convert():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()
    convert_to_csv(input_file, output_file)
    status_label.config(text='Conversion complete!')

# Create the main window
window = tk.Tk()
window.title('Log File Converter')

# Create the input file section
input_frame = tk.Frame(window)
input_label = tk.Label(input_frame, text='Input file:')
input_label.pack(side=tk.LEFT)
input_file_entry = tk.Entry(input_frame)
input_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
input_browse_button = tk.Button(input_frame, text='Browse', command=browse_input_file)
input_browse_button.pack(side=tk.LEFT)
input_frame.pack(fill=tk.X, padx=10, pady=10)

# Create the output file section
output_frame = tk.Frame(window)
output_label = tk.Label(output_frame, text='Output file:')
output_label.pack(side=tk.LEFT)
output_file_entry = tk.Entry(output_frame)
output_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
output_browse_button = tk.Button(output_frame, text='Browse', command=browse_output_file)
output_browse_button.pack(side=tk.LEFT)
output_frame.pack(fill=tk.X, padx=10, pady=10)

# Create the convert button
convert_button = tk.Button(window, text='Convert', command=convert)
convert_button.pack(padx=10, pady=10)

# Create the status label
status_label = tk.Label(window, text='')
status_label.pack(padx=10, pady=10)

# Run the main loop
window.mainloop()
