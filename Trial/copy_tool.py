import tkinter as tk
import os
import shutil

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Input Path Label and Entry
        self.input_path_label = tk.Label(self)
        self.input_path_label["text"] = "Input Path:"
        self.input_path_label.pack(side="top")

        self.input_path_entry = tk.Entry(self)
        self.input_path_entry.pack(side="top")

        # Output Path Label and Entry
        self.output_path_label = tk.Label(self)
        self.output_path_label["text"] = "Output Path:"
        self.output_path_label.pack(side="top")

        self.output_path_entry = tk.Entry(self)
        self.output_path_entry.pack(side="top")

        # Copy Button
        self.copy_button = tk.Button(self)
        self.copy_button["text"] = "Copy"
        self.copy_button["command"] = self.copy_files
        self.copy_button.pack(side="top")

        # Completion Message Label
        self.completion_message_label = tk.Label(self, fg="green")
        self.completion_message_label.pack(side="bottom")

    def copy_files(self):
        # Get input and output paths
        input_path = self.input_path_entry.get()
        output_path = self.output_path_entry.get()

        # Check if input path exists
        if not os.path.exists(input_path):
            self.completion_message_label.config(text="Input path does not exist.")
            return

        # Create output path if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Copy files
        copied_files = []
        for item in os.listdir(input_path):
            s = os.path.join(input_path, item)
            d = os.path.join(output_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
                copied_files.append(d)
            else:
                if os.path.exists(d):
                    if os.path.getsize(s) != os.path.getsize(d) or os.path.getmtime(s) != os.path.getmtime(d):
                        base, extension = os.path.splitext(d)
                        counter = 1
                        while os.path.exists(d):
                            d = f"{base}{counter}{extension}"
                            counter += 1
                        shutil.copy2(s, d)
                        copied_files.append(d)
                else:
                    shutil.copy2(s, d)
                    copied_files.append(d)

        # Show completion message
        if copied_files:
            with open("copied_files.txt", "w") as f:
                f.write("\n".join(copied_files))
            self.completion_message_label.config(text=f"Task completed. Copied files saved to copied_files.txt.")
        else:
            self.completion_message_label.config(text="No files copied.")  

root = tk.Tk()
app = Application(master=root)
app.mainloop()
