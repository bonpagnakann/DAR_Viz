import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from exemplar_size_list import *

def split_into_task_files(input_csv, output_dir):
    """
    Split the Average Accuracy Results CSV into individual task files.
    """
    # Load the input CSV
    data = pd.read_csv(input_csv)

    # Extract task columns
    task_columns = [col for col in data.columns if col.startswith("Task")]

    # Remove the smallest exemplar size from the data (e.g., 100 if it's in the file)
    columns_to_keep = [col for col in data.columns if not col.endswith("- 100")]

    # Save each task column as a separate CSV file
    task_files = []
    for task in task_columns:
        task_data = data[columns_to_keep].drop(task_columns, axis=1)  # Exclude other task columns
        task_data[task] = data[task]  # Include only the current task column
        output_file = os.path.join(output_dir, f"{task.replace(' ', '_')}.csv")
        task_data.to_csv(output_file, index=False)
        task_files.append(output_file)

    return task_files

def process_task_file(input_file, output_file):
    """
    Process individual task files to remove rows with the smallest exemplar size and
    format column names.
    """
    # Load the task file
    task_data = pd.read_csv(input_file)

    # Rename methods to match the method order
    rename_mapping = {
        "EWC_Replay": "EWC Replay",
        "VAE_Adapt": "VAE - Adapt",
        "VAE_BBox": "VAE - BBox",
        "VAE_Filter": "TaskVAE",
        "VAE_GMM": "DAR"
    }
    task_data['Method'] = task_data['Method'].replace(rename_mapping)

    # Remove rows with Exemplar_Size = 100
    task_data = task_data[task_data['Exemplar_Size'] != '100']

    # Create a new DataFrame for the output
    output_data = pd.DataFrame()
    methods = [method for method in task_data["Method"].unique() if method not in ['VAE - Adapt', 'VAE_BBox']]
    # Loop through the unique methods and format column names
    for method in methods:
        method_data = task_data[task_data['Method'] == method]
        if method in ['VAE - Adapt', 'VAE - BBox', 'TaskVAE', 'DAR']:  # For VAE-based methods, use only the method name
            if method not in output_data.columns:
                output_data[method] = method_data.iloc[:, 2].values  # Accuracy values
        else:  # For non-VAE methods, concatenate method and exemplar size
            for exemplar_size in sorted(method_data['Exemplar_Size'].unique()):
                col_name = f"{method} - {int(exemplar_size)}"
                output_data[col_name] = method_data[method_data['Exemplar_Size'] == exemplar_size].iloc[:, 2].values

    # Save the processed file
    output_data.to_csv(output_file, index=False)
    return output_file

def plot_boxplot(input_csv, output_image, task_name, method_order, exemplar_size_order, acc_type):
    """
    Create a box plot for the task with exemplar sizes grouped by method.
    """
    # Load the processed task file
    data = pd.read_csv(input_csv)

    # Melt the data for easier plotting
    melted_data = data.melt(var_name="Method", value_name="Accuracy")

    # Generate the sorted categories for box plot order
    ordered_methods = []
    for method in method_order:
        if method in ['VAE - Adapt', 'VAE - BBox', 'TaskVAE', 'DAR']:  # VAE-based methods have no exemplar size
            ordered_methods.append(method)
        else:  # Non-VAE methods include exemplar sizes
            ordered_methods.extend(
                [f"{method} - {size}" for size in exemplar_size_order if f"{method} - {size}" in data.columns]
            )

    # Enforce the custom order
    melted_data["Method"] = pd.Categorical(melted_data["Method"], categories=ordered_methods, ordered=True)
    

    # Create the box plot
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=melted_data, x="Method", y="Accuracy", hue="Method", palette="Set3", dodge=False)

    # Customize the plot
    if acc_type == 'All_Acc':
        fig_name = f"Box Plot of Accuracy for All Classes in {task_name[:-2]} {task_name[-1]}"
    elif acc_type == 'New_Acc':
        fig_name = f"Box Plot of Accuracy for New Classes in {task_name[:-2]} {int(task_name[-1])}"
    elif acc_type == 'Old_Acc':
        fig_name = f"Box Plot of Accuracy for Old Classes in {task_name[:-2]} {int(task_name[-1])}"

    # Add horizontal dashed lines every 0.1 on the y-axis
    plt.ylim(0, 1.0)
    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(0.1))  # Add ticks every 0.1
    plt.grid(axis='y', linestyle=':', linewidth=0.7, alpha=0.7)  # Dotted lines for y-axis
    plt.title(fig_name, fontsize=20)
    plt.xlabel("Method", fontsize=18)
    plt.ylabel("Accuracy", fontsize=18)
    plt.xticks([])
    plt.yticks(fontsize=18)
    plt.legend(fontsize=14, title_fontsize=16)
    # Save the plot
    plt.tight_layout()
    plt.savefig(output_image)
    plt.close()


def accuracy_histogram(dataset, scenario, equivalence):

    person = ['0','1','2'] #people = ['0','1','2']
    acc_list = ['All_Acc', 'New_Acc', 'Old_Acc']

    for p in person:
        for acc in acc_list:
            exemplar_size = calculate_exemp_size(dataset, scenario[1:], p)
            base_dir = scenario + '/P' + p + '_Results/Materials/All/'
            output_dir = base_dir + "/Box_plot/" + acc
            result_dir = scenario + '/P' + p + '_Results/Figures/' + acc

            input_csv = base_dir + dataset + '_' + scenario + '_P' + p + '_' + acc +'.csv'  # Replace with the actual input CSV file
            os.makedirs(output_dir, exist_ok=True)
            os.makedirs(result_dir, exist_ok=True)
            # Step 1: Split the Average Accuracy Results file into individual task files
            task_files = split_into_task_files(input_csv, output_dir)

            # Step 2: Process each task file and generate box plots
            method_order = [
                "Random", "EWC Replay", "iCaRL", "LUCIR",
                "TaskVAE", "DAR"
            ]

            exemplar_size_order = [equivalence]

            dataset_name_map = {
                'MS': 'MotionSense',
                'HHAR': 'HHAR',
                'UCI': 'UCI',
                'RW': 'RealWorld',
                'PM': 'PAMAP',

            }

            for task_file in task_files:
                # Process the task file
                task_name = os.path.splitext(os.path.basename(task_file))[0]
                processed_file = os.path.join(output_dir, f"Processed_{task_name}.csv")
                process_task_file(task_file, processed_file)

                # Generate the box plot
                if acc == 'All_Acc':
                    output_image = os.path.join(result_dir, f"{dataset_name_map[dataset]}_Box_plot_Acc_{task_name}.png")
                elif acc == 'New_Acc':
                    output_image = os.path.join(result_dir, f"{dataset_name_map[dataset]}_Box_plot_of_Acc_{task_name[:-1]}{int(task_name[-1])}.png")
                elif acc == 'Old_Acc':
                    output_image = os.path.join(result_dir, f"{dataset_name_map[dataset]}_Box_plot_of_Acc_{task_name[:-1]}{int(task_name[-1])}.png")

                plot_boxplot(processed_file, output_image, task_name, method_order, exemplar_size_order, acc)

            print('Scenario', scenario, ', Person', p, ',', acc, ': All task files processed and box plots generated.')

