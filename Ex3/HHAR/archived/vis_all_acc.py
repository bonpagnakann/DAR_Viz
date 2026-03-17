import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import os
from exemplar_size_list import *

def vis_bar_accuracy(dataset, scenario):

    person = ['0', '1', '2']

    acc_list = ['All_Acc','New_Acc','Old_Acc']

    for p in person:
        base_dir = scenario + '/Person_' + p + '/Scenario Analysis/P' + p + '_Results/Materials/Average/'
        for acc in acc_list:
            result_dir = scenario + "/Person_" + p + "/Scenario Analysis/P" + p + "_Results/Figures/" + acc
            os.makedirs(result_dir, exist_ok=True)

            # Read the CSV file
            file_path = base_dir + dataset + "_Avg_" + scenario + "_P" + p + "_" + acc + ".csv"
            output_fig = result_dir + "/P" + p + "_" + acc + ".png"  # Replace with the correct path to your file
            df = pd.read_csv(file_path)

            # Rename methods to match the method order
            rename_mapping = {
                "VAE_Adapt": "VAE - Adapt",
                "VAE_BBox": "VAE - BBox",
                "VAE_Filter": "VAE - Filter",
                "VAE_GMM": "VAE - GMM"
            }

            df["Method"] = df["Method"].replace(rename_mapping)

            # Clean column names
            df.columns = df.columns.str.strip()

            # Process the data manually for each task
            if acc == 'All_Acc':
                tasks = [f"Task {i + 1}" for i in range(len(scenario))]
            elif acc == 'New_Acc' or acc == 'Old_Acc':
                tasks = [f"Task {i + 2}" for i in range(len(scenario)-1)]

            methods = df["Method"].unique()
            exemplar_size = df["Exemplar_Size"].unique()

            # Create a dictionary to hold data for each task
            task_data = {task: [] for task in tasks}

            for task in tasks:
                for method in methods:
                    method_data = df[df["Method"] == method][task].values
                    task_data[task].append(method_data)

            # Generate positions for the bars
            x_positions = np.arange(len(exemplar_size))  # Positions for exemplar size groups
            gap_between_methods = 0.05  # Small gap between methods
            bar_width = (0.8 - gap_between_methods * (len(methods) - 1)) / len(methods)  # Adjust bar width to include gaps

            # Use a more vibrant Seaborn color palette
            colors = ['#1f77b4', '#ff7f0e', '#9467bd', '#2ca02c']

            if acc == 'All_Acc':
                n_cols = len(scenario)
            elif acc == 'New_Acc' or acc == 'Old_Acc':
                n_cols = len(scenario) - 1

            # Plotting
            fig, axes = plt.subplots(nrows=1, ncols=n_cols, figsize=(20, 8), sharey=True)  # Increased figure size

            if n_cols == 1:
                axes = [axes]

            for i, (task, ax) in enumerate(zip(tasks, axes)):
                method_labels = []
                # Plot bars for each method
                for j, method in enumerate(methods):
                    ax.bar(
                        x_positions + j * (bar_width + gap_between_methods),  # Offset bars for each method with gap
                        task_data[task][j],
                        width=bar_width,
                        color=colors[j],
                        label=method if i == 0 else ""  # Add legend label only for the first subplot
                    )

                    method_labels.append(method)  # Collect method names for x-ticks

                ax.set_title(f"{task} Accuracy", fontsize=18)  # Increase title font size

                if i == 0:
                    ax.set_ylabel("Accuracy", fontsize=14)  # Increase Y-axis label font size
                ax.set_ylim(0, 1)
                ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
                ax.grid(axis="y", linestyle="--", alpha=0.7)
                # Set the x-ticks to the center of the grouped bars
                # Generate the x-tick positions to center the method names
                tick_positions = x_positions + np.linspace(0, (len(methods) - 1) * (bar_width + gap_between_methods),
                                                           len(methods))

                # Set x-ticks to match the methods
                ax.set_xticks(tick_positions)
                ax.set_xticklabels(methods, fontsize=12, rotation=45)
                ax.tick_params(axis="y", labelsize=14)  # Increase Y-axis tick label font size

            fig.supxlabel("Methods", fontsize=14, y=0.03)
            # Add a shared title and adjust layout
            fig.suptitle("Task Accuracy by Generative Methods", fontsize=22)  # Increase overall title font size
            plt.tight_layout()  # Adjust layout to fit legend

            # Save the plot to a file
            plt.savefig(output_fig, dpi=300, bbox_inches="tight")  # Save with high resolution

            # Close the plot to avoid displaying it in interactive environments
            plt.close()

            print('Scenario', scenario, ', Person', p, ',', acc, ' Bar Chart is completed.')
