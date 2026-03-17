import os
import shutil

# Sub-folders to move
folders_to_move = ["log", "time_log"]

scenarios = ['21111/','222/','231/','3111/','321/','33/','42/']
person = ['0','1','2']
for scenario in scenarios:
    for p in person:
        # Define the source directory and the target directory
        source_dir = scenario + '/Person_' + p + "/DDGR"
        temp_folder = os.path.join(source_dir, "log_new")  # Temporary folder
        final_folder = os.path.join(source_dir, "log")  # Final folder name

        # Step 1: Create the temporary folder
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
            print(f"Created temporary folder: {temp_folder}")
        else:
            print(f"Temporary folder already exists: {temp_folder}")

        # Step 2: Move subfolders into the temporary folder
        for folder_name in folders_to_move:
            old_path = os.path.join(source_dir, folder_name)  # Original path
            new_path = os.path.join(temp_folder, folder_name)  # Destination path

            # Check for self-move and skip
            if os.path.abspath(old_path) == os.path.abspath(temp_folder):
                print(f"Skipping move: '{old_path}' cannot be moved into itself.")
                continue

            if os.path.exists(old_path):
                shutil.move(old_path, new_path)
                print(f"Moved '{folder_name}' to '{temp_folder}'")
            else:
                print(f"Folder '{folder_name}' does not exist in '{source_dir}'")

        # Step 3: Rename the temporary folder back to 'log'
        if os.path.exists(temp_folder):
            if os.path.exists(final_folder):
                print(f"Removing existing '{final_folder}' folder...")
                shutil.rmtree(final_folder)  # Remove existing 'log' folder if it exists

            os.rename(temp_folder, final_folder)
            print(f"Renamed '{temp_folder}' to '{final_folder}'")
