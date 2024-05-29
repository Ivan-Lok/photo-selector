import tkinter as tk
from PIL import Image, ImageTk
import json
import os

def load_people_photos(file_path):
    with open(file_path, "r") as file:
        people_photos = json.load(file)
    return people_photos

# def get_folder_path():
#     folder_path = tk.filedialog.askdirectory()
#     return folder_path

def show_people_list(people_photos, people_list):
    selected_person = tk.StringVar()

    def show_photos(event):
        person = selected_person.get()
        if person:
            show_photo_viewer(people_photos[person])

    people_frame = tk.Frame(root)
    people_frame.pack(pady=10)

    people_label = tk.Label(people_frame, text="Select a person:")
    people_label.pack(side=tk.LEFT)

    people_dropdown = tk.OptionMenu(people_frame, selected_person, *people_list)
    people_dropdown.pack(side=tk.LEFT)

    select_button = tk.Button(people_frame, text="Select", command=lambda: show_photos(None))
    select_button.pack(side=tk.LEFT, padx=10)

    selected_person.trace("w", show_photos)

def show_photo_viewer(photo_list):
    photo_viewer = tk.Toplevel(root)
    photo_viewer.title("Photo Viewer")

    current_photo_index = 0

    def show_photo(index):
        nonlocal current_photo_index
        current_photo_index = index
        photo_path = os.path.join(folder_path, photo_list[index])
        image = Image.open(photo_path)
        photo = ImageTk.PhotoImage(image)
        photo_label.configure(image=photo)
        photo_label.image = photo
        filename_label.configure(text=f"File: {photo_list[index]}")

    photo_label = tk.Label(photo_viewer)
    photo_label.pack(pady=10)

    filename_label = tk.Label(photo_viewer)
    filename_label.pack()

    button_frame = tk.Frame(photo_viewer)
    button_frame.pack(pady=10)

    prev_button = tk.Button(button_frame, text="Previous", command=lambda: show_photo((current_photo_index - 1) % len(photo_list)))
    prev_button.pack(side=tk.LEFT, padx=5)

    next_button = tk.Button(button_frame, text="Next", command=lambda: show_photo((current_photo_index + 1) % len(photo_list)))
    next_button.pack(side=tk.LEFT, padx=5)

    show_photo(0)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Photo Viewer")

    folder_path = "C:/Users/ivanl/Downloads/2024 robogames export"
    if folder_path:
        people_photos_file = "people_photos.json"
        if os.path.isfile(people_photos_file):
            people_photos = load_people_photos(people_photos_file)
            people_list = list(people_photos.keys())
            show_people_list(people_photos, people_list)
        else:
            tk.messagebox.showerror("Error", "people_photos.json file not found in the selected folder.")
    else:
        tk.messagebox.showerror("Error", "No folder selected.")

    root.mainloop()