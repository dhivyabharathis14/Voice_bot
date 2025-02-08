import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

file_path = "./points.npy"
points = np.load(file_path)

# Extract x, y, and z coordinates
x, y, z = points[:, 0], points[:, 1], points[:, 2]

min_z = np.min(z)
base_layer_indices = np.where(z == min_z)[0]

# Compute the base radius as the average radial distance from the origin
base_radii = np.sqrt(x[base_layer_indices]**2 + y[base_layer_indices]**2)
base_radius = np.mean(base_radii)

unique_z = np.unique(z)
radius_variation = [np.mean(np.sqrt(x[z == zi]**2 + y[z == zi]**2)) for zi in unique_z]

# Fit a linear regression model to the radius variation
slope, intercept, _, _, _ = scipy.stats.linregress(unique_z, radius_variation)

expected_radii = intercept + slope * unique_z

corrected_x = x * (expected_radii[np.searchsorted(unique_z, z)] / np.sqrt(x**2 + y**2))
corrected_y = y * (expected_radii[np.searchsorted(unique_z, z)] / np.sqrt(x**2 + y**2))

corrected_points = np.column_stack((corrected_x, corrected_y, z))

corrected_file_path = "corrected_points.npy"
np.save(corrected_file_path, corrected_points)

# Plot 
fig = plt.figure(figsize=(12, 6))

# Original point cloud
ax1 = fig.add_subplot(121, projection='3d')
ax1.scatter(x, y, z, s=1, c=z, cmap='viridis')
ax1.set_title("Original Point Cloud")

# Corrected point cloud
ax2 = fig.add_subplot(122, projection='3d')
ax2.scatter(corrected_x, corrected_y, z, s=1, c=z, cmap='viridis')
ax2.set_title("Corrected Point Cloud")
plt.savefig("point_cloud_comparison.png")
print("Plot saved as point_cloud_comparison.png")
print(f"Corrected point cloud saved at: {corrected_file_path}")
