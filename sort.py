import os
import shutil
import sys
import re
from unidecode import unidecode

# Dictionary with file categories
file_categories = {
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "archives": [".zip", ".gz", ".tar"]
}

# Function to normalize file names
def normalize(file_name):
    normalized_name = unidecode(file_name)
    normalized_name = re.sub(r'[^\w\s]', '_', normalized_name)
    return normalized_name

# Function to process the folder and organize files
def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            normalized_name = normalize(file_name)
            new_file_name = normalized_name + file_extension
            file_path = os.path.join(root, file)
            new_file_path = os.path.join(root, new_file_name)

            os.rename(file_path, new_file_path)

            for category, extensions in file_categories.items():
                if file_extension.lower() in extensions:
                    category_folder = os.path.join(root, category)
                    os.makedirs(category_folder, exist_ok=True)
                    shutil.move(new_file_path, os.path.join(category_folder, new_file_name))
                    break
            else:
                unknown_folder = os.path.join(root, "unknown")
                os.makedirs(unknown_folder, exist_ok=True)
                shutil.move(new_file_path, os.path.join(unknown_folder, new_file_name))

        for folder in os.listdir(root):
            folder_path = os.path.join(root, folder)
            if os.path.isdir(folder_path) and not os.listdir(folder_path):
                os.rmdir(folder_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Wrong number of args, provide target folder.")
    else:
        target_folder = sys.argv[1]
        process_folder(target_folder)
        print("Sorting and organizing completed.")