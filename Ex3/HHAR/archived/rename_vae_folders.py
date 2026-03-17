import os
import shutil


def rename_vae_folders(dataset, scenario):

    old_base_dirs = ['VAE_adaptive_boundary_none/', 'VAE_boundary_box_none/', 'VAE_boundary_box_probability/', 'VAE_gmm_none/']
    source_to_target = {
        "/VAE_adaptive_boundary_none/log/": "/VAE_Adapt/log/",
        "/VAE_boundary_box_none/log/": "/VAE_BBox/log/",
        "/VAE_boundary_box_probability/log/": "/VAE_Filter/log/",
        "/VAE_gmm_none/log/": "/VAE_GMM/log/",
    }
    '''
    old_base_dirs = ['VAE_Adapt/', 'VAE_BBox/', 'VAE_Filter/', 'VAE_GMM/']
    source_to_target = {
    "/VAE_Adapt/log/": "/VAE_adaptive_boundary_none/log/",
    "/VAE_BBox/log/": "/VAE_boundary_box_none/log/",
    "/VAE_Filter/log/": "/VAE_boundary_box_probability/log/",
    "/VAE_GMM/log/": "/VAE_gmm_none/log/",
    }
    '''
    #scenarios = ['222/','321/','231/','3111/','21111/','33/','42/']
    person = ['Person_0','Person_1','Person_2']
    #for scenario in scenarios:
    for p in person:
        # Create new directory structure and move the contents
        origin_base_dir = os.path.join(scenario, p)

        for source, target in source_to_target.items():

            origin_dir = origin_base_dir + source
            destination_dir = origin_base_dir + target

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

        for old_dir in old_base_dirs:
            old_dir = os.path.join(origin_base_dir, old_dir)
            shutil.rmtree(old_dir)
            print(f"Deleted source folder: {old_dir}")


    print("Folders and files have been reorganized successfully!")

