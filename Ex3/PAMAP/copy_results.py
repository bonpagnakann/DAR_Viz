import os
import shutil

def copy_results(scenarios):
    for source_base_dir in scenarios:
        destination_base_dir = "results/" + source_base_dir

        # Ensure the destination base directory exists
        os.makedirs(destination_base_dir, exist_ok=True)

        # Loop through the Person_{i} folders and copy their Scenario Analysis folders
        for person_id in os.listdir(source_base_dir):
            person_path = os.path.join(source_base_dir, person_id)

            # Skip if it's not a directory
            if not os.path.isdir(person_path):
                continue

            # Path to the Scenario Analysis directory
            scenario_analysis_path = os.path.join(person_path, "Scenario Analysis")

            # Ensure Scenario Analysis exists
            if not os.path.exists(scenario_analysis_path):
                print(f"Scenario Analysis folder not found in {person_path}. Skipping...")
                continue

            # Path to the P{i}_Results folder
            for scenario_folder in os.listdir(scenario_analysis_path):
                folder_path = os.path.join(scenario_analysis_path, scenario_folder)

                # Skip if it's not a directory
                if not os.path.isdir(folder_path):
                    continue

                # Define the destination path
                destination_path = os.path.join(destination_base_dir, scenario_folder)

                # Copy the folder
                shutil.copytree(folder_path, destination_path, dirs_exist_ok=True)
                print(f"Copied {folder_path} to {destination_path}")

        print("Copying completed.")
