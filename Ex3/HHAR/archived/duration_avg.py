import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Concatenate files
def concatenate_files(base_dir, concat_file, method_file_map, columns):
    concatenated_data = pd.DataFrame()
    for method, file_name in method_file_map.items():
        if "VAE" in method or method == 'FeTrIL' or method == 'DDGR':
            method_dir = os.path.join(base_dir, method, "log/time_log")
            file_path = os.path.join(method_dir, file_name)
            if os.path.exists(file_path):
                data = pd.read_csv(file_path, header=None, sep=",")
                concatenated_data = pd.concat([concatenated_data, data], ignore_index=True)
        else:
            for i in range(5):
                method_dir = os.path.join(base_dir, f"{method}_{i}", "log/time_log")
                file_path = os.path.join(method_dir, file_name)
                if os.path.exists(file_path):
                    data = pd.read_csv(file_path, header=None, sep=",")
                    concatenated_data = pd.concat([concatenated_data, data], ignore_index=True)

    concatenated_data.columns = columns
    concatenated_data.to_csv(concat_file, index=False, sep=",")
    return concatenated_data

# Step 2: Calculate averages and rename methods
def calculate_averages(data, avg_file, vae_mapping):
    # Ensure clean column names and data
    data.columns = [col.strip() for col in data.columns]
    data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Rename VAE-related methods
    for (vae_method, vae_sampling, vae_filter), new_name in vae_mapping.items():
        mask = (
            (data["method"] == vae_method) &
            (data["vae_sampling"] == vae_sampling) &
            (data["filter"] == vae_filter)
        )
        data.loc[mask, "method"] = new_name

    # Drop unnecessary columns for VAE-related methods
    data = data.drop(columns=["vae_sampling", "filter"])

    # Separate `ce_vae` and other methods
    ce_vae_data = data[(data["method"].str.startswith("VAE")) | (data["method"].str.startswith("FeTrIL")) | (data["method"].str.startswith("DDGR"))]

    # Group `ce_vae` by [method]
    ce_vae_grouped = (
        ce_vae_data.groupby(["method"], as_index=False)[
            ["each_exemplar_time", "whole_exemplar_time", "each_task_time", "whole_task_time"]
        ]
        .mean()
    )

    # Combine the results
    grouped_data = ce_vae_grouped

    #print("grouped_data: ",grouped_data)

    # Reorder columns
    grouped_data = grouped_data[
        ["method", "each_exemplar_time", "whole_exemplar_time", "each_task_time", "whole_task_time"]
    ]

    grouped_data['total_time'] = grouped_data['whole_exemplar_time'] + grouped_data['whole_task_time']

    # Save the grouped data to the output file
    grouped_data.to_csv(avg_file, index=False)
    print(f"Grouped and averaged data saved to {avg_file}")
    return grouped_data

# Step 3: Plot the graphs
def plot_graphs(data, output_fig):
    # Define the method order for consistent plotting
    method_order = ["FeTrIL", "DDGR", "VAE - Adapt", "VAE - BBox", "VAE - Filter", "VAE - GMM"]
    data["method"] = pd.Categorical(data["method"], categories=method_order, ordered=True)
    data = data.sort_values(by=["method"])
    #print('data["method"]: ', data["method"])

    # Define colors for each method
    colors = plt.cm.tab10(np.linspace(0, 1, len(method_order)))

    # Metrics to visualize
    metrics = ["whole_exemplar_time", "whole_task_time", "total_time"]
    metric_titles = {
        "whole_exemplar_time": "Generating/Selecting Exemplar Duration (s)",
        "whole_task_time": "Model Training Task Time (s)",
        "total_time": "Total Training Time (s)"
    }

    # Determine the maximum value for the y-axis across all metrics
    max_y_value = data[metrics].max().max()

    # Create the plot with an extra subplot for the legend
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(22, 8))
    axes = axes.flatten()

    for i, (metric, ax) in enumerate(zip(metrics, axes)):  # Use only the first 3 axes for the plots
        # Pivot the data for the current metric
        metric_data = data.pivot(columns="method", values=metric).reindex(columns=method_order)

        # Plot settings
        bar_width = 0.5

        # Plot each method
        for j, method in enumerate(method_order):
            ax.bar(
                j,
                metric_data[method],
                width=bar_width,
                label=method if i == 0 else None,  # Add legend only in the first subplot
                color=colors[j]
            )

        # Set labels and title
        ax.set_title(metric_titles[metric], fontsize=18)
        if i == 0:
            ax.set_ylabel("Time (s)", fontsize=12)
        ax.set_xticks(range(len(method_order)))
        ax.set_xticklabels(method_order, fontsize=12, rotation=45)
        ax.set_ylim(0, max_y_value + 1)  # Set consistent y-axis limit
        ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Adjust layout
    plt.tight_layout(rect=[0, 0, 0, 0])  # Adjust to leave space for the legend subplot
    fig.suptitle("Training Duration Comparison", fontsize=22, y=0.98)
    #fig.supxlabel("Methods", fontsize=14, y=0.03)
    # Save and display the plot
    plt.savefig(output_fig, bbox_inches="tight")
    plt.close()
    print("Bar chart saved as", output_fig, '.')

def duration_vis(scenario):

    person = ['0', '1', '2']

    # Column names for the output file
    columns = [
        "dataset", "scenario", "person", "method", "vae_sampling", "filter",
        "iteration", "exemplar_size", "each_exemplar_time",
        "whole_exemplar_time", "each_task_time", "whole_task_time"
    ]

    vae_mapping = {
        ("ce_fetril", "none", "none"): "FeTrIL",
        ("ce_ddgr", "none", "none"): "DDGR",
        ("ce_vae", "adaptive_boundary", "none"): "VAE - Adapt",
        ("ce_vae", "boundary_box", "none"): "VAE - BBox",
        ("ce_vae", "boundary_box", "probability"): "VAE - Filter",
        ("ce_vae", "gmm", "none"): "VAE - GMM"
    }

    for p in person:
        # Define directories, file mappings, and output paths
        base_dir = scenario + "/Person_" + p

        method_file_map = {
            "FeTrIL": "t_" + p + "_ce_fetril.txt",
            "DDGR": "t_" + p + "_ce_ddgr.txt",
            "VAE_Adapt": "t_" + p + "_ce_vae_adaptive_boundary_none.txt",
            "VAE_BBox": "t_" + p + "_ce_vae_boundary_box_none.txt",
            "VAE_Filter": "t_" + p + "_ce_vae_boundary_box_probability.txt",
            "VAE_GMM": "t_" + p + "_ce_vae_gmm_none.txt",
        }
        output_dir = os.path.join(base_dir, 'Scenario Analysis/P' + p + '_Results/Materials/Duration')
        concat_file = os.path.join(output_dir, "output_combined.csv")
        avg_file = os.path.join(output_dir, "avg_duration_combined.csv")
        output_path = os.path.join(base_dir, "Scenario Analysis/P" + p + "_Results/Figures/Duration/")
        output_fig = os.path.join(output_path, "Training Duration Comparison.png")

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(output_path, exist_ok=True)

        concatenated_data = concatenate_files(base_dir, concat_file, method_file_map, columns)
        averaged_data = calculate_averages(concatenated_data, avg_file, vae_mapping)
        plot_graphs(averaged_data, output_fig)
