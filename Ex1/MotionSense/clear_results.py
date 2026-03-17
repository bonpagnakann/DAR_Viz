import os
import shutil
from coefficients import *

def clear_folder(folder_path):
    """
    Remove all directories and files in the specified folder.

    Args:
    - folder_path (str): Path to the folder to be cleared.
    """
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return

    try:
        # Iterate over each item in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            # Remove files
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Removed file: {item_path}")

            # Remove directories
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Removed directory: {item_path}")

        print(f"All contents in '{folder_path}' have been removed.")
    except Exception as e:
        print(f"Error clearing folder '{folder_path}': {e}")

def remove_file(file_path):
    """
    Remove a file at the specified path.

    Args:
    - file_path (str): Path to the file to be removed.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been removed.")
        else:
            print(f"File '{file_path}' does not exist.")
    except Exception as e:
        print(f"Error removing file '{file_path}': {e}")


# Specify the root directory
person = ['0','1','2']
dataset = 'HHAR'
params = get_params(dataset)

for s in list(params.keys()):
    for p in person:

        root_dir = s + '/P' + p + '_Results/Figures'
        #root_dir = s + '/Person_' + p + '/Scenario Analysis/P' + p + '_Results'
        #file = s + '/Person_' + p + '/Scenario Analysis/MS_' + s + '_P' + p + '_All_Acc.csv'

        # Call the function
        clear_folder(root_dir)
        #remove_file(root_dir)