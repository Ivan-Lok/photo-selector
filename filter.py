import json
import os

def load_state():
    saved_state_file = "saved_state.json"
    if os.path.isfile(saved_state_file):
        with open(saved_state_file, "r") as file:
            app_state = json.load(file)
            return app_state
    else:
        print("No saved state found.")
        return None

def filter_photos_by_person(app_state):
    photo_people = app_state["photo_people"]
    photo_file_names = app_state["photo_file_names"]
    people_photos = {}

    for person_name in app_state["people_count"].keys():
        filtered_photos = []
        for photo_file_name, people_list in photo_people.items():
            if person_name in people_list:
                filtered_photos.append(photo_file_name)
        people_photos[person_name] = filtered_photos

    return people_photos

def save_people_photos(people_photos, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(people_photos, file, ensure_ascii=False, indent=2)

def main():
    app_state = load_state()
    if app_state:
        people_photos = filter_photos_by_person(app_state)
        output_file = "people_photos.json"
        save_people_photos(people_photos, output_file)
        print(f"People and their photos saved to {output_file}")
    else:
        print("No saved state found.")

if __name__ == "__main__":
    main()