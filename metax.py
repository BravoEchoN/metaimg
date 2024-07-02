import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import exifread
import os

def extract_metadata(file_path):
    with open(file_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
    
    metadata = {
        'DateTime': tags.get('EXIF DateTimeOriginal', 'N/A'),
        'GPSInfo': {
            'Latitude': tags.get('GPS GPSLatitude', 'N/A'),
            'Longitude': tags.get('GPS GPSLongitude', 'N/A')
        }
    }
    return metadata

def convert_to_degrees(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degrees in float format
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)

def save_metadata(file_path, metadata):
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    output_file = f"{name}_metadata.txt"
    
    with open(output_file, 'w') as f:
        f.write(f"Date and Time: {metadata['DateTime']}\n")
        
        if metadata['GPSInfo']['Latitude'] != 'N/A' and metadata['GPSInfo']['Longitude'] != 'N/A':
            lat = convert_to_degrees(metadata['GPSInfo']['Latitude'])
            lon = convert_to_degrees(metadata['GPSInfo']['Longitude'])
            f.write(f"Location: Latitude: {lat}, Longitude: {lon}\n")
        else:
            f.write("Location: N/A\n")
    
    messagebox.showinfo("Success", f"Metadata saved to {output_file}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        metadata = extract_metadata(file_path)
        save_metadata(file_path, metadata)

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# Set up the GUI
root = tk.Tk()
root.title("Image Metadata Extractor")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

browse_button = tk.Button(frame, text="Browse Image", command=browse_file)
browse_button.pack()

root.update_idletasks()  # Update "requested size" from geometry manager
center_window(root)

root.mainloop()
