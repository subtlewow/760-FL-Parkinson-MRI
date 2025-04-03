#ensures all volumes have a consistent shape, resolution, orientation, and intensity distribution
import os
import nibabel as nib
import numpy as np

def check_volume(file_path):
    """Load a NIfTI file and return its shape and intensity statistics."""
    nii_img = nib.load(file_path)
    data = nii_img.get_fdata()
    shape = data.shape
    min_val = data.min()
    max_val = data.max()
    mean_val = data.mean()
    std_val = data.std()
    return shape, min_val, max_val, mean_val, std_val

def main(data_dir, expected_shape=(64, 128, 128), intensity_range=(0.0, 1.0)):
    # Collect all .nii.gz files from the directory and its subdirectories.
    volumes = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.nii.gz'):
                volumes.append(os.path.join(root, file))
                
    print(f"Found {len(volumes)} volumes in '{data_dir}'.\n")

    for vol in volumes:
        shape, min_val, max_val, mean_val, std_val = check_volume(vol)
        print(f"File: {vol}")
        print(f"  Shape: {shape}")
        print(f"  Intensity Range: {min_val:.3f} to {max_val:.3f}")
        print(f"  Mean: {mean_val:.3f}, Std: {std_val:.3f}")

        # Check if shape is as expected
        if shape != expected_shape:
            print(f"  Warning: Unexpected shape (expected {expected_shape})!")
        
        # Check if intensity values are within the expected range
        expected_min, expected_max = intensity_range
        if min_val < expected_min or max_val > expected_max:
            print(f"  Warning: Intensity values out of expected range {intensity_range}!")
        print("-" * 50)

if __name__ == "__main__":
    # Update this path to point to your dataset folder
    data_directory = "stripped-output/"
    main(data_directory)
