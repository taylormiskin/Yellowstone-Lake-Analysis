import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text
import numpy as np
from sklearn.metrics import r2_score
 
# Load the dataset
file_path = r"C:\Users\water\Downloads\TetonsLakesData.csv"
df = pd.read_csv(file_path)
 
# Convert necessary columns to numeric for analysis
df['carlson_tsi'] = pd.to_numeric(df['Carlson  TSI'], errors='coerce')
df['vollen'] = pd.to_numeric(df['Vollen TSI'], errors='coerce')
 
# Group by lake to calculate the mean Carlson TSI and mean Vollen
lake_group = df.groupby('Site').agg(
    mean_carlson=('carlson_tsi', 'mean'),
    mean_vollen=('vollen', 'mean')
).reset_index()
SiteList = ['Two Ocean', 'Moose Pond', 'Swan Lake', 'String Lake', 'Emma Matilda', 'Phelps Lake', 'Bradley Lake', 'Taggart Lake', 'Holly Lake', 'Delta Lake', 'Lake Solitude', 'Lake of the Crags', 'Christian Pond', 'Cygnet Pond', 'Oxbow Bend', 'Surprise Lake', 'Amphitheater Lake']
print(len(SiteList))
 
# Filter out rows with NaN values in mean Carlson or Vollen
lake_group_clean = lake_group[lake_group['Site'].isin(SiteList)]
 
# Shading the background according to Vollen categories
# Slightly Oligotrophic category (distinct blue)
plt.axhspan(20, 26, color='#0051e9', alpha=0.5, label='Strongly Oligotrophic (Carlson)')  # Light Blue
plt.axhspan(26, 33, color='#1d9df2', alpha=0.5, label='Oligotrophic (Carlson)')  # Distinct Blue
plt.axhspan(33, 38, color='#5dade2', alpha=0.5, label='Slightly Oligotrophic (Vollen)')  # Distinct Blue
 
# Mesotrophic category (distinct green shades)
plt.axhspan(38, 43, color='#d5f5e3', alpha=0.5, label='Slightly Mesotrophic (Vollen)')  # Light Green
plt.axhspan(43, 49, color='#82e0aa', alpha=0.5, label='Mesotrophic (Vollen)')  # Mid Green
plt.axhspan(49, 54, color='#28b463', alpha=0.5, label='Strongly Mesotrophic (Vollen)')  # Dark Green
 
# Eutrophic category (distinct yellow and orange shades)
plt.axhspan(54, 58, color='#f9e79f', alpha=0.5, label='Slightly Eutrophic (Vollen)')  # Light Yellow
plt.axhspan(58, 62, color='#f5b041', alpha=0.5, label='Eutrophic (Vollen)')  # Mid Orange
plt.axhspan(62, 65, color='#d35400', alpha=0.5, label='Strongly Eutrophic (Vollen)')  # Dark Orange
 
# Slightly Hypereutrophic category (distinct red)
plt.axhspan(65, 70, color='#c0392b', alpha=0.5, label='Slightly Hypereutrophic (Vollen)')  # Dark Red
 
# Create a scatter plot for mean Carlson TSI vs mean Vollen
plt.scatter(lake_group_clean['mean_carlson'], lake_group_clean['mean_vollen'],
            marker='o', color='b', edgecolor='k', zorder=2)
 
# Linear regression: fit a line to the clean data
slope, intercept = np.polyfit(lake_group_clean['mean_carlson'], lake_group_clean['mean_vollen'], 1)
x_vals = np.array([20, 70])  # Set the x-axis range from 33 to 70
y_vals = slope * x_vals + intercept
 
# Plot the fitted line
plt.plot(x_vals, y_vals, color='red', linestyle='--', label=f'Slope = {slope:.2f}', zorder=1)
 
# Calculate the R-squared value
predicted_vollen = slope * lake_group_clean['mean_carlson'] + intercept
r_squared = r2_score(lake_group_clean['mean_vollen'], predicted_vollen)
 
# Prepare the lake names and positions for adjustment, ensuring all lakes get lines
texts = []
for i, lake in lake_group_clean.iterrows():
    lake_name = lake['Site']
    texts.append(plt.text(lake['mean_carlson'], lake['mean_vollen'], lake_name, fontsize=9))
 
# Adjust text positions to avoid overlap and ensure lines are drawn for all lakes
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='grey', lw=0.5))
 
# Set the limits for both axes
plt.xlim(20, 70)  # Carlson TSI axis
plt.ylim(20, 70)  # Vollen axis
 
# Set the aspect ratio to be equal
plt.gca().set_aspect('equal', adjustable='box')
 
# Label the axes
plt.xlabel('Mean Carlson TSI')
plt.ylabel('Mean Vollen')
 
# Add the full equation and R-squared annotation to the plot
plt.annotate(f'R² = {r_squared:.2f}', xy=(35, 65), fontsize=12, color='black')
 
# Add the equation to the legend
equation = f'Equation: y = {slope:.2f}x + {intercept:.2f}'
plt.legend(title="Vollen Trophic Categories", bbox_to_anchor=(1.05, 1), loc='upper left', labels=[
    'Slightly Oligotrophic (Vollen)', 'Slightly Mesotrophic (Vollen)', 'Mesotrophic (Vollen)',
    'Strongly Mesotrophic (Vollen)', 'Slightly Eutrophic (Vollen)', 'Eutrophic (Vollen)',
    'Strongly Eutrophic (Vollen)', 'Slightly Hypereutrophic (Vollen)', f'Slope = {slope:.2f}', equation
])
 
# Show the plot
#plt.tight_layout()
plt.show()