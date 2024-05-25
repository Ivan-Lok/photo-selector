import os
import random
import tkinter as tk
from PIL import Image, ImageTk

# Path to the folder containing the photos
print("Please enter the file path, correct format: C:/folder path")
folder_path = input("Folder Path: ")

# Get the list of photo file names in the folder
photo_file_names = os.listdir(folder_path)

# Shuffle the photo file names randomly
random.shuffle(photo_file_names)

# Create the main window
window = tk.Tk()

# Create a frame for the main content area
main_frame = tk.Frame(window)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a label to display the photos
photo_label = tk.Label(main_frame)
photo_label.pack(padx=20, pady=20)

# Variable to keep track of the current photo index
current_photo_index = -1

# Function to display the next photo
def display_next_photo():
    global current_photo_index

    if current_photo_index < len(photo_file_names) - 1:
        # Retrieve the next photo file name from the list
        current_photo_index += 1
    else:
        # Loop back to the first photo
        current_photo_index = 0

    display_current_photo()

# Function to display the previous photo
def display_previous_photo():
    global current_photo_index

    if current_photo_index > 0:
        # Retrieve the previous photo file name from the list
        current_photo_index -= 1
    else:
        # Loop back to the last photo
        current_photo_index = len(photo_file_names) - 1

    display_current_photo()

# Function to display the current photo
def display_current_photo():
    photo_file_name = photo_file_names[current_photo_index]

    # Construct the full path to the photo
    photo_path = os.path.join(folder_path, photo_file_name)

    # Open the image using Pillow
    image = Image.open(photo_path)


    # Resize the image to fit within the window
    image = image.resize((500, 500), resample=Image.BICUBIC)

    # Convert the image to Tkinter-compatible format
    photo = ImageTk.PhotoImage(image)

    # Update the label with the new photo
    photo_label.configure(image=photo)
    photo_label.image = photo

    # Update the counter label
    counter_label.config(text=f"{current_photo_index + 1} / {len(photo_file_names)}")

    # Update the people count in the right panel
    update_people_count()

def update_people_count():
    global current_name_frame
    # Destroy all existing name labels
    for label_tuple in name_labels.values():
        for label in label_tuple:
            label.destroy()
    name_labels.clear()

    # Create new name labels with buttons
    for name, count in people_count.items():
        frame = tk.Frame(right_panel)
        frame.pack(pady=5)
       
        name_label = tk.Label(frame, text=f"{name}: {count}")
        name_label.pack(side=tk.LEFT)

        dec_button = tk.Button(frame, text="-", command=lambda name=name: update_count(name, -1))
        dec_button.pack(side=tk.LEFT, padx=5)

        inc_button = tk.Button(frame, text="+", command=lambda name=name: update_count(name, 1))
        inc_button.pack(side=tk.LEFT, padx=5)

        name_labels[name] = (frame, name_label, dec_button, inc_button)

# Function to update the count for a specific person
def update_count(name, delta):
    if name in people_count:
        people_count[name] += delta
        people_count[name] = max(people_count[name], 0)
        flame,name_label, dec_button, inc_button = name_labels[name]
        name_label.config(text=f"{name}: {people_count[name]}")
    else:
        people_count[name] = 0
        update_people_count()

# Function to add a new person
def add_new_person():
    new_name = new_person_entry.get().strip()
    if new_name:
        update_count(new_name, 1)
        new_person_entry.delete(0, tk.END)

def save_state():
    with open("saved_state.txt", "w") as file:
        file.write(f"Current Photo Index: {current_photo_index}\n")
        file.write(",".join(photo_file_names) + "\n")  # Save the shuffled photo file names
        for name, count in people_count.items():
            file.write(f"{name}: {count}\n")

def load_state():
    global current_photo_index
    global photo_file_names
    saved_state_file = "saved_state.txt"
    if os.path.isfile(saved_state_file):
            with open(saved_state_file, "r") as file:
                lines = file.readlines()
                current_photo_index = int(lines[0].split(": ")[1].strip()) - 1
                photo_file_names = lines[1].strip().split(",")
                for line in lines[2:]:
                    name, count = line.strip().split(": ")
                    people_count[name] = int(count)
                    update_people_count()

def check_new_photos():
    global photo_file_names
    new_photos = [f for f in os.listdir(folder_path) if f not in photo_file_names]
    if new_photos:
        random.shuffle(new_photos)
        photo_file_names.extend(new_photos)
        update_people_count()
        display_next_photo()

# Create a frame for the bottom bar
bottom_bar = tk.Frame(main_frame)
bottom_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Create a label to display the photo count
counter_label = tk.Label(bottom_bar, text="0 / 0")
counter_label.pack(side=tk.LEFT)

# Create a button to display the previous photo
previous_photo_button = tk.Button(bottom_bar, text="Previous", command=display_previous_photo)
previous_photo_button.pack(side=tk.LEFT)

# Create a button to display the next photo
next_photo_button = tk.Button(bottom_bar, text="Next", command=display_next_photo)
next_photo_button.pack(side=tk.LEFT)

# Create a button to save the current state
save_button = tk.Button(bottom_bar, text="Save", command=save_state)
save_button.pack(side=tk.LEFT, padx=10)

# Create a button to check for new photos
check_new_photos_button = tk.Button(bottom_bar, text="Check New Photo", command=check_new_photos)
check_new_photos_button.pack(side=tk.LEFT, padx=10)

# Create a frame for the right-hand side panel
right_panel = tk.Frame(window)
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH)

# Dictionary to store the name labels
name_labels = {}

# Dictionary to store the people count
people_count = {}

# Create a frame for the new person input
new_person_frame = tk.Frame(right_panel)
new_person_frame.pack(pady=10)

new_person_label = tk.Label(new_person_frame, text="Add New Person:")
new_person_label.pack(side=tk.LEFT)

new_person_entry = tk.Entry(new_person_frame)
new_person_entry.pack(side=tk.LEFT, padx=5)

add_person_button = tk.Button(new_person_frame, text="Add", command=add_new_person)
add_person_button.pack(side=tk.LEFT)

current_name_frame=0

load_state()

# Initially display the first photo
display_next_photo()

# Start the main event loop
window.mainloop()