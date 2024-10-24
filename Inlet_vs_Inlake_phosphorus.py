import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
file_path = r"/Users/taylormiskin/Downloads/YellowstoneLakesData-reformatted-no_repeats.csv"
df = pd.read_csv(file_path)

# Convert necessary columns to numeric for analysis
df['Total Phosphorus (mg/L)'] = pd.to_numeric(df['Total Phosphorus (mg/L)'], errors='coerce')

# Separate the data into inlet and in-lake based on the 'Location' column (which likely contains 'Inlet' and 'Inlake')
df_inlet = df[df['Location'] == 'Inlet']
df_inlake = df[df['Location'] == 'Inlake']

# Group by lake ('Site') to calculate the mean phosphorus values for inlet and in-lake
mean_inlet_phosphorus = df_inlet.groupby('Site')['Total Phosphorus (mg/L)'].mean()
mean_inlake_phosphorus = df_inlake.groupby('Site')['Total Phosphorus (mg/L)'].mean()

# Merge the results into a single dataframe for comparison
mean_phosphorus = pd.DataFrame({
    'Inlet Phosphorus': mean_inlet_phosphorus,
    'In-lake Phosphorus': mean_inlake_phosphorus
}).dropna()

# Create a bar plot comparing inlet and in-lake phosphorus for each lake
labels = mean_phosphorus.index
inlet_means = mean_phosphorus['Inlet Phosphorus']
inlake_means = mean_phosphorus['In-lake Phosphorus']

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(12, 8))
rects1 = ax.bar(x - width/2, inlet_means, width, label='Inlet Phosphorus', color='red')
rects2 = ax.bar(x + width/2, inlake_means, width, label='In-lake Phosphorus', color='blue')

# Add labels, title, and custom x-axis tick labels
ax.set_xlabel('Lakes')
ax.set_ylabel('Mean Phosphorus (mg/L)')
ax.set_title('Comparison of Inlet vs In-lake Phosphorus by Lake')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')

# Add legend
ax.legend()

# Show plot with a tight layout
plt.tight_layout()
plt.show()
