import os
import shutil

# Define the source directories and their corresponding new target paths


source_to_target = {
    "VAE_adaptive_boundary_none/": "VAE_Adapt/log/",
    "VAE_boundary_box_none/": "VAE_BBox/log/",
    "VAE_boundary_box_probability/": "VAE_Filter/log/",
    "VAE_gmm_none/": "VAE_GMM/log/",
}
'''
source_to_target = {
    "VAE_Adapt/log/log/": "VAE_adaptive_boundary_none/",
    "VAE_BBox/log/log/": "VAE_boundary_box_none/",
    "VAE_Filter/log/log/": "VAE_boundary_box_probability/",
    "VAE_GMM/log/log/": "VAE_gmm_none/",
}
'''

scenarios = ['21111/','222/','231/','3111/','321/','33/','42/']
person = ['Person_0','Person_1','Person_2']
for scenario in scenarios:
    for p in person:
        # Create new directory structure and move the contents
        origin_base_dir = scenario + p
        destination_base_dir = scenario + p

        for source, target in source_to_target.items():

            origin_dir = os.path.join(origin_base_dir, source)
            destination_dir = os.path.join(destination_base_dir, target)

            # Create the target directory structure
            os.makedirs(destination_dir, exist_ok=True)

            # Get all items in the source directory
            if os.path.exists(origin_dir):
                items = os.listdir(origin_dir)

                # Move each item from source to the target directory
                for item in items:
                    item_path = os.path.join(origin_dir, item)
                    if os.path.isdir(item_path) or os.path.isfile(item_path):
                        shutil.move(item_path, destination_dir)

                # Delete the now-empty source directory
                shutil.rmtree(origin_dir)
                print(f"Deleted source folder: {origin_dir}")
            else:
                print(f"Source directory {origin_dir} does not exist. Skipping...")

print("Folders and files have been reorganized successfully!")
