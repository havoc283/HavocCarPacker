import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path

class CarPackOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Havoc's FiveM Car Pack Organizer")
        self.geometry("600x400")
        self.resizable(False, False)

        # Variables
        self.source_dir = tk.StringVar(value=str(Path.home() / "Desktop" / "HavocCarPacker" / "Car Files"))
        self.target_dir = tk.StringVar(value=str(Path.home() / "Desktop" / "HavocCarPacker" / "[OUTPUT]"))

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        # Source folder
        tk.Label(self, text="Source Folder:").pack(anchor="w", padx=10, pady=(10, 0))
        source_frame = tk.Frame(self)
        source_frame.pack(fill="x", padx=10)
        self.source_entry = tk.Entry(source_frame, textvariable=self.source_dir, width=60)
        self.source_entry.pack(side="left", fill="x", expand=True)
        tk.Button(source_frame, text="Browse", command=self.browse_source).pack(side="left", padx=5)

        # Target folder
        tk.Label(self, text="Target Folder:").pack(anchor="w", padx=10, pady=(10, 0))
        target_frame = tk.Frame(self)
        target_frame.pack(fill="x", padx=10)
        self.target_entry = tk.Entry(target_frame, textvariable=self.target_dir, width=60)
        self.target_entry.pack(side="left", fill="x", expand=True)
        tk.Button(target_frame, text="Browse", command=self.browse_target).pack(side="left", padx=5)

        # Run button
        tk.Button(self, text="Organize Car Pack", command=self.run_organizer, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=15)

        # Status log
        tk.Label(self, text="Status:").pack(anchor="w", padx=10)
        self.log_area = scrolledtext.ScrolledText(self, height=10, state="disabled")
        self.log_area.pack(fill="both", expand=True, padx=10, pady=(0,10))

    def browse_source(self):
        folder = filedialog.askdirectory(title="Select Source Folder")
        if folder:
            self.source_dir.set(folder)

    def browse_target(self):
        folder = filedialog.askdirectory(title="Select Target Folder")
        if folder:
            self.target_dir.set(folder)

    def log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state="disabled")

    def run_organizer(self):
        source = self.source_dir.get()
        target = self.target_dir.get()
        if not os.path.isdir(source):
            messagebox.showerror("Error", "Source folder does not exist.")
            return
        if not os.path.isdir(target):
            try:
                os.makedirs(target)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create target folder: {e}")
                return

        self.log("Starting organization...")
        # Run in separate thread to keep UI responsive
        threading.Thread(target=self.organize_cars, args=(source, target), daemon=True).start()

    def organize_cars(self, source_dir, target_dir):
        RESOURCE_CONTENT = """\
-- Created by Havoc

fx_version 'cerulean'
game 'gta5'

name 'FiveM Car Pack'
author 'Havoc'

files {
    '**/data/**/*.meta',
    '**/data/**/*.dat',
    '**/data/**/*.rel',
}

data_file 'HANDLING_FILE' '**/data/**/handling.meta'
data_file 'VEHICLE_METADATA_FILE' '**/data/**/vehicles.meta'
data_file 'CARCOLS_FILE' '**/data/**/carcols.meta'
data_file 'CAR_VARIATION_FILE' '**/data/**/carvariations.meta'
data_file 'VEHICLE_VARIATION_FILE' '**/data/**/vehiclelayouts.meta'
data_file 'CLIP_SETS_FILE' '**/data/**/clip_sets.meta'
data_file 'DLC_TEXT_FILE' '**/data/**/dlctext.meta'
data_file 'AUDIO_GAMEDATA' '**/data/**/game.dat151.rel'
data_file 'AUDIO_SOUNDDATA' '**/data/**/sounds.dat54.rel'
data_file 'AUDIO_WAVEPACK' '**/data/**/dlc_*.awc'
data_file 'AUDIO_FILE' '**/data/**/audioconfig/*.dat54.rel'
"""

        def ensure_dir(path):
            if not os.path.exists(path):
                os.makedirs(path)

        def delete_resource_file(folder_path):
            resource_file = os.path.join(folder_path, '__resource.lua')
            if os.path.isfile(resource_file):
                os.remove(resource_file)

        try:
            ensure_dir(target_dir)
            self.log(f"Target folder set to: {target_dir}")

            car_folders = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]
            if not car_folders:
                self.log("No car folders found in source.")
                return

            for car_folder in car_folders:
                car_path = os.path.join(source_dir, car_folder)
                self.log(f"Processing: {car_folder}")

                delete_resource_file(car_path)

                target_data = os.path.join(target_dir, 'data', car_folder)
                target_stream = os.path.join(target_dir, 'stream', car_folder)
                ensure_dir(target_stream)

                # Copy stream files
                stream_path = os.path.join(car_path, 'stream')
                if os.path.exists(stream_path):
                    for file in os.listdir(stream_path):
                        src_file = os.path.join(stream_path, file)
                        dst_file = os.path.join(target_stream, file)
                        shutil.copy2(src_file, dst_file)
                    self.log(f"  Stream files copied.")

                # Gather data files (.meta, .dat, .rel) from 'data/' folder or root
                meta_files = []

                data_folder = os.path.join(car_path, 'data')
                if os.path.isdir(data_folder):
                    for f in os.listdir(data_folder):
                        if f.endswith(('.meta', '.rel', '.dat')):
                            meta_files.append(os.path.join(data_folder, f))

                for f in os.listdir(car_path):
                    full_path = os.path.join(car_path, f)
                    if f.endswith(('.meta', '.rel', '.dat')) and os.path.isfile(full_path):
                        meta_files.append(full_path)

                # Copy meta files
                if meta_files:
                    ensure_dir(target_data)
                    for file_path in meta_files:
                        dst_file = os.path.join(target_data, os.path.basename(file_path))
                        shutil.copy2(file_path, dst_file)
                    self.log(f"  Meta/data files copied.")

            # Write __resource.lua
            with open(os.path.join(target_dir, '__resource.lua'), 'w') as f:
                f.write(RESOURCE_CONTENT)

            self.log("✅ Organization complete!")

        except Exception as e:
            self.log(f"❌ Error: {e}")

if __name__ == "__main__":
    app = CarPackOrganizerApp()
    app.mainloop()
