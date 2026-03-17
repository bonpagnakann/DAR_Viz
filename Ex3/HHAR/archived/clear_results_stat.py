import os
import shutil

def remove_stat_folders(root_directory):
    # Iterate over all directories and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_directory):
        # Check if 'stat' folder exists in the current directory
        if 'stat' in dirnames:
            stat_folder_path = os.path.join(dirpath, 'stat')
            # Remove the 'stat' folder and its contents
            shutil.rmtree(stat_folder_path)
            print(f"Removed folder: {stat_folder_path}")

# Specify the root directory
#root_dirs = ['2_2_2_2','2_3_1_1_1','3_2_1_1_1','4_1_1_1_1','4_2_1_1','5_3']
root_dirs = ['222', '21111','231','3111','321','33','42']

# Call the function
for root_dir in root_dirs:
    remove_stat_folders(root_dir)

