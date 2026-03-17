import os
import pandas as pd
import numpy as np
from exemplar_size_list import *

def average_all_classes(dataset, scenario):
    # Base directory structure
    person = ['0','1','2']

    # Define methods with different calculation requirements
    non_vae_methods = ['EWC_Replay', 'Random', 'iCaRL', 'LUCIR']
    vae_methods = ['VAE_Adapt', 'VAE_BBox', 'VAE_Filter', 'VAE_GMM']

    acc_list = ['All_Acc','New_Acc','Old_Acc']

    for p in person:
        exemplar_size = calculate_exemp_size(dataset, scenario[1:], p)
        base_dir = scenario + '/Person_' + p
        output_dir = scenario + '/Person_' + p + '/Scenario Analysis/P' + p + '_Results/Materials/All/'
        os.makedirs(output_dir, exist_ok=True)

        for acc in acc_list:
            output_file = output_dir + dataset + '_' + scenario + '_P' + p + '_' + acc +'.csv'
            results = []
            # Process non-VAE methods
            for method_name in non_vae_methods:
                print(f'Processing non-VAE method: {method_name}')

                # Iterate over 5 iterations for the current method
                methods = [f'{method_name}_{i}' for i in range(5)]

                for sample in exemplar_size:
                    exemplar_data = []

                    for method in methods:
                        method_dir = os.path.join(base_dir, method, 'stat')
                        if acc == 'All_Acc':
                            file_name = f'accuracy_by_task{sample}.txt'
                            file_path = os.path.join(method_dir, 'all_classes', file_name)
                        elif acc == 'New_Acc':
                            file_name = f'new_classes_accuracy_by_task{sample}.txt'
                            file_path = os.path.join(method_dir, 'new_classes', file_name)
                        elif acc == 'Old_Acc':
                            file_name = f'old_classes_accuracy_by_task{sample}.txt'
                            file_path = os.path.join(method_dir, 'old_classes', file_name)

                        if os.path.exists(file_path):
                            try:
                                data = pd.read_csv(file_path, header=None)
                                exemplar_data.append(data.values)
                            except Exception as e:
                                print(f'Error processing file {file_path}: {e}')
                        else:
                            print(f'File {file_path} does not exist. Skipping...')

                    if len(exemplar_data) == 5:
                        try:
                            stacked_data = np.stack(exemplar_data, axis=0)  # Shape: (5, 30, 3)
                            mean_data = np.mean(stacked_data, axis=0)  # Shape: (30, 3)

                            for row in mean_data:
                                task_values = row.tolist()  # Convert row to list
                                results.append([sample, *task_values, method_name])
                        except Exception as e:
                            print(f'Error computing mean for exemplar size {sample}: {e}')
                    else:
                        print(
                            f'Insufficient files for exemplar size {sample} in {method_name}.')

            # Process VAE methods
            for vae_method in vae_methods:
                print(f'Processing VAE method: {vae_method}')

                vae_dir = os.path.join(base_dir, vae_method, 'stat')
                exemplar_data = []

                for sample in exemplar_size:
                    if acc == 'All_Acc':
                        file_name = f'accuracy_by_task{sample}.txt'
                        file_path = os.path.join(vae_dir, 'all_classes', file_name)
                    elif acc == 'New_Acc':
                        file_name = f'new_classes_accuracy_by_task{sample}.txt'
                        file_path = os.path.join(vae_dir, 'new_classes', file_name)
                    elif acc == 'Old_Acc':
                        file_name = f'old_classes_accuracy_by_task{sample}.txt'
                        file_path = os.path.join(vae_dir, 'old_classes', file_name)

                    if os.path.exists(file_path):
                        try:
                            data = pd.read_csv(file_path, header=None)
                            exemplar_data.append(data.values)
                        except Exception as e:
                            print(f'Error processing file {file_path}: {e}')
                    else:
                        print(f'File {file_path} does not exist. Skipping...')

                if len(exemplar_data) == 5:
                    try:
                        stacked_data = np.stack(exemplar_data, axis=0)  # Shape: (5, 30, 3)
                        mean_data = np.mean(stacked_data, axis=0)  # Shape: (30, 3)

                        for row in mean_data:
                            task_values = row.tolist()  # Convert row to list
                            results.append(['All Exemplars', *task_values, vae_method])
                    except Exception as e:
                        print(f'Error computing mean for {vae_method}: {e}')
                else:
                    print(f'Insufficient files for {vae_method}.')

            # Dynamically generate task column names based on the number of columns in the exemplar data
            print('len(results[0]):', len(results[0]))
            num_tasks = len(results[0]) - 2  # Exclude 'Exemplar_Size' and 'Method' columns

            if acc == 'All_Acc':
                task_columns = [f'Task {i + 1}' for i in range(num_tasks)]
            elif acc == 'New_Acc' or acc =='Old_Acc':
                task_columns = [f'Task {i + 2}' for i in range(num_tasks)]
            print('num_tasks:', num_tasks)
            columns = ['Exemplar_Size'] + task_columns + ['Method']

            # Create a DataFrame from the results
            output_df = pd.DataFrame(results, columns=columns)

            # Save to a CSV file
            output_df.to_csv(output_file, index=False)

            print(f'Results saved to {output_file}')
