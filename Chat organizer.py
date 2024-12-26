import os
import shutil


source_folder = r"Chats"  
destination_folder = r"Chat names"  

# Kreirajte ciljni folder ako ne postoji
os.makedirs(destination_folder, exist_ok=True)


for subfolder in os.listdir(source_folder):
    subfolder_path = os.path.join(source_folder, subfolder)
    
    
    if os.path.isdir(subfolder_path):
        
        for file_name in os.listdir(subfolder_path):
            if file_name.endswith(".txt"):
                original_file_path = os.path.join(subfolder_path, file_name)
                
                new_file_name = f"{subfolder}.txt"
                new_file_path = os.path.join(destination_folder, new_file_name)
                
                
                shutil.move(original_file_path, new_file_path)
                print(f"File transfered: {original_file_path} -> {new_file_path}")

print("All files trasfered.")
