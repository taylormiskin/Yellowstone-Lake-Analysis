import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text
import numpy as np
from sklearn.metrics import r2_score

# Load the dataset
file_path = r"C:\Users\water\Desktop\Pyton_Codes\YellowStone\YellowstoneLakesData-reformatted.xlsx"
df = pd.read_excel(file_path)  # changed to read_excel as it's an Excel file

# Convert necessary columns to numeric for analysis
df['carlson_tsi'] = pd.to_numeric(df['Carlson  TSI'], errors='coerce')
df['vollen'] = pd.to_numeric(df['Vollen'], errors='coerce')

# Remove "Hot Lake" from the dataset
df = df[df['Site'] != 'Hot Lake']

# Combine Trout Lake East and West into Trout Lake
df['Site'] = df['Site'].replace({'Trout Lake East': 'Trout Lake', 'Trout Lake West': 'Trout Lake'})

# Group by lake to calculate the mean Carlson TSI and mean Vollen
lake_group = df.groupby('Site').agg(
    mean_carlson=('carlson_tsi', 'mean'),
    mean_vollen=('vollen', 'mean')
).reset_index()

# Filter out rows with NaN values in mean Carlson or Vollen
lake_group_clean = lake_group.dropna(subset=['mean_carlson', 'mean_vollen'])

# Shading the background according to Carlson TSI sub-classifications with the same distinct colors
plt.axvspan(33, 38, color='#5dade2', alpha=0.5, label='Slightly Oligotrophic (Carlson)')
plt.axvspan(38, 43, color='#d5f5e3', alpha=0.5, label='Slightly Mesotrophic (Carlson)')
plt.axvspan(43, 49, color='#82e0aa', alpha=0.5, label='Mesotrophic (Carlson)')
plt.axvspan(49, 54, color='#28b463', alpha=0.5, label='Strongly Mesotrophic (Carlson)')
plt.axvspan(54, 58, color='#f9e79f', alpha=0.5, label='Slightly Eutrophic (Carlson)')
plt.axvspan(58, 62, color='#f5b041', alpha=0.5, label='Eutrophic (Carlson)')
plt.axvspan(62, 65, color='#d35400', alpha=0.5, label='Strongly Eutrophic (Carlson)')
plt.axvspan(65, 70, color='#c0392b', alpha=0.5, label='Slightly Hypereutrophic (Carlson)')

# Create a scatter plot for mean Carlson TSI vs mean Vollen
plt.scatter(lake_group_clean['mean_carlson'], lake_group_clean['mean_vollen'], 
            marker='o', color='b', edgecolor='k', zorder=2)

# Linear regression: fit a line to the clean data
slope, intercept = np.polyfit(lake_group_clean['mean_carlson'], lake_group_clean['mean_vollen'], 1)
x_vals = np.array([33, 70])  # Set the x-axis range from 33 to 70
y_vals = slope * x_vals + intercept

# Plot the fitted line
plt.plot(x_vals, y_vals, color='red', linestyle='--', label=f'Slope = {slope:.2f}', zorder=1)

# Calculate the R-squared value
predicted_vollen = slope * lake_group_clean['mean_carlson'] + intercept
r_squared = r2_score(lake_group_clean['mean_vollen'], predicted_vollen)

# Prepare the lake names and positions for adjustment, ensuring all lakes have lines
texts = []
for i, lake in lake_group_clean.iterrows():
    lake_name = lake['Site']
    texts.append(plt.text(lake['mean_carlson'], lake['mean_vollen'], lake_name, fontsize=9))

# Adjust text positions to avoid overlap and ensure lines are drawn for all lakes
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='grey', lw=0.5))

# Set the limits for both axes
plt.xlim(33, 70)  # Carlson TSI axis
plt.ylim(33, 70)  # Vollen axis

# Set the aspect ratio to be equal
plt.gca().set_aspect('equal', adjustable='box')

# Label the axes
plt.xlabel('Mean Carlson TSI')
plt.ylabel('Mean Vollen')

# Add the full equation and R-squared annotation to the plot
plt.annotate(f'R² = {r_squared:.2f}', xy=(35, 65), fontsize=12, color='black')

# Add the equation to the legend
equation = f'Equation: y = {slope:.2f}x + {intercept:.2f}'
plt.legend(title="Carlson Trophic Categories", bbox_to_anchor=(1.05, 1), loc='upper left', labels=[
    'Slightly Oligotrophic (Carlson)', 'Slightly Mesotrophic (Carlson)', 'Mesotrophic (Carlson)',
    'Strongly Mesotrophic (Carlson)', 'Slightly Eutrophic (Carlson)', 'Eutrophic (Carlson)',
    'Strongly Eutrophic (Carlson)', 'Slightly Hypereutrophic (Carlson)', f'Slope = {slope:.2f}', equation
])

# Show the plot
plt.tight_layout()
plt.show()
