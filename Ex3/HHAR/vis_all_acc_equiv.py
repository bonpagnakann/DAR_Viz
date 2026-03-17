import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import os
from exemplar_size_list import *

def vis_bar_accuracy(dataset, scenario, equivalent):

    person = ['0','1','2'] #people = ['0','1','2']

    acc_list = ['All_Acc','New_Acc','Old_Acc']

    for p in person:
        base_dir = scenario + '/P' + p + '_Results/Materials/Average/'
        for acc in acc_list:
            result_dir = scenario + '/P' + p + '_Results/Figures/' + acc
            os.makedirs(result_dir, exist_ok=True)

            # Read the CSV file
            file_path = base_dir + dataset + "_Avg_" + scenario + "_P" + p + "_" + acc + ".csv"

            dataset_name_map = {
                'MS': 'MotionSense',
                'HHAR': 'HHAR',
                'UCI': 'UCI',
                'RW': 'RealWorld',
                'PM': 'PAMAP',

            }

            output_fig = result_dir + "/" + dataset_name_map[dataset] + "_P" + p + "_" + acc + ".png"  # Replace with the correct path to your file
            df = pd.read_csv(file_path)

            # Clean column names
            df.columns = df.columns.str.strip()
            df["Method"] = df["Method"].replace("VAE_Filter", "TaskVAE")
            df["Method"] = df["Method"].replace("VAE_GMM", "DAR")

            # Process the data manually for each task
            if acc == 'All_Acc':
                tasks = [f"Task {i + 1}" for i in range(len(scenario))]
            elif acc == 'New_Acc' or acc == 'Old_Acc':
                tasks = [f"Task {i + 2}" for i in range(len(scenario)-1)]

            #methods = df["Method"].unique()
            methods = [method for method in df["Method"].unique() if method not in ['VAE_Adapt', 'VAE_BBox']]
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
            fig, axes = plt.subplots(nrows=1, ncols=n_cols, figsize=(20, 8), sharey=True, sharex=True)  # Increased figure size

            if n_cols == 1:
                axes = [axes]
            center_idx = n_cols // 2  # Index of the center subplot

            for i, (task, ax) in enumerate(zip(tasks, axes)):
                # Plot bars for each method
                for j, method in enumerate(methods):
                    ax.bar(
                        x_positions + j * (bar_width + gap_between_methods),  # Offset bars for each method with gap
                        task_data[task][j],
                        width=bar_width,
                        color=colors[j],
                        label=method if i == 0 else ""  # Add legend label only for the first subplot
                    )
                ax.set_title(f"{task}", fontsize=20)  # Increase title font size

                if i == 0:
                    ax.set_ylabel("Accuracy", fontsize=20)  # Increase Y-axis label font size
                ax.set_ylim(0, 1)
                ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
                ax.grid(axis="y", linestyle="--", alpha=0.7)
                ax.tick_params(axis="y", labelsize=20)  # Increase Y-axis tick label font size

                ax.set_xticklabels([])


                #ax.set_xticks(x_positions + (len(methods) * (bar_width + gap_between_methods) - gap_between_methods) / 2)  # Center the ticks
                #ax.set_xlabel("Exemplar Size", fontsize=14)  # Increase X-axis label font size
                #ax.set_xticklabels(exemplar_size, fontsize=14)  # Increase X-axis tick label font size
            # Add a single centered x-axis label below all subplots
            #fig.text(0.45, 0, f"Exemplar Size = {exemplar_size[0]}", ha='center', fontsize=20)

            # Add a legend to the figure
            #if acc == 'All_Acc':
            #axes[-1].legend(
            fig.legend(
                title="Methods",
                labels=methods,  # Use unique values from the 'Method' column directly
                bbox_to_anchor=(0.85, 0.5),  # Move legend closer to the graph
                loc="center left",
                borderaxespad=0.1,  # Reduce padding around the legend
                fontsize=14,  # Increase legend font size
                title_fontsize=16  # Increase legend title font size
            )

            # Customize the plot
            if acc == 'All_Acc':
                fig_name = "Task Accuracy for All Classes by Methods"
            elif acc == 'New_Acc':
                fig_name = "Task Accuracy for New Classes by Methods"
            elif acc == 'Old_Acc':
                fig_name = "Task Accuracy for Old Classes by Methods"

            # Add a shared title and adjust layout
            fig.suptitle(fig_name, fontsize=20)  # Increase overall title font size
            plt.tight_layout(rect=[0, 0, 0.85, 1])  # Adjust layout to fit legend

            # Save the plot to a file
            plt.savefig(output_fig, dpi=300, bbox_inches="tight")  # Save with high resolution

            # Close the plot to avoid displaying it in interactive environments
            plt.close()

            print('Scenario', scenario, ', Person', p, ',', acc, ' Bar Chart is completed.')