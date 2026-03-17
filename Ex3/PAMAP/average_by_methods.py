import pandas as pd
import os
from exemplar_size_list import *

def average_by_methods(dataset, scenario):

    # Base directory structure
    person = ['0','1','2']

    acc_list = ['All_Acc','New_Acc','Old_Acc']

    for p in person:
        exemplar_size = calculate_exemp_size(dataset, scenario[1:], p)
        exemplar_size = [str(i) for i in exemplar_size]
        base_dir = scenario + '/Person_' + p + '/Scenario Analysis/P' + p + '_Results/Materials/All/'
        result_dir = scenario + '/Person_' + p + '/Scenario Analysis/P' + p + '_Results/Materials/Average/'
        os.makedirs(result_dir, exist_ok=True)

        for acc in acc_list:
            # Input and output file paths
            input_file = base_dir + dataset + '_' + scenario + '_P' + p + '_' + acc +'.csv'
            output_file = result_dir + dataset + '_Avg_' + scenario + '_P' + p + '_' + acc + '.csv'  # Final output file

            # Read the CSV
            data = pd.read_csv(input_file)

            # Identify task columns dynamically
            task_columns = [col for col in data.columns if col.startswith('Task ')]

            # Group by Exemplar_Size and Method to calculate the mean accuracy for all tasks
            grouped_data = (
                data.groupby(['Exemplar_Size', 'Method'], as_index=False)
                .agg({task: 'mean' for task in task_columns})
            )

            # Define the desired order of methods and exemplar sizes
            desired_method_order = [
                'Random', 'EWC_Replay', 'iCaRL', 'LUCIR',
                'VAE_Adapt', 'VAE_BBox', 'VAE_Filter', 'VAE_GMM'
            ]

            # VAE methods
            vae_methods = ['VAE_Adapt', 'VAE_BBox', 'VAE_Filter', 'VAE_GMM']

            # Process the data
            rows_to_append = []

            for vae_method in vae_methods:
                # Find rows with 'All Exemplars' in the Exemplar_Size column and specific VAE method
                vae_rows = grouped_data[
                    (grouped_data['Exemplar_Size'] == 'All Exemplars')
                    & (grouped_data['Method'] == vae_method)
                ]
                for _, row in vae_rows.iterrows():
                    for size in exemplar_size:
                        # Duplicate the row for each exemplar size
                        new_row = row.copy()
                        new_row['Exemplar_Size'] = size
                        rows_to_append.append(new_row)

            # Create a DataFrame for the new rows
            new_rows_df = pd.DataFrame(rows_to_append)

            # Append the new rows to the original grouped data
            updated_data = pd.concat([grouped_data, new_rows_df], ignore_index=True)

            # Remove 'All Exemplars' rows for VAE methods
            updated_data = updated_data[~(
                (updated_data['Exemplar_Size'] == 'All Exemplars')
                & (updated_data['Method'].isin(vae_methods))
            )]

            # Sort the data by Method and Exemplar_Size
            updated_data['Method'] = pd.Categorical(updated_data['Method'], categories=desired_method_order, ordered=True)
            updated_data['Exemplar_Size'] = pd.Categorical(updated_data['Exemplar_Size'], categories=exemplar_size, ordered=True)

            updated_data = updated_data.sort_values(by=['Method', 'Exemplar_Size'])

            # Save the updated data to a new CSV file
            updated_data.to_csv(output_file, index=False)

            print('Final updated CSV file has been saved as', output_file, '.')
