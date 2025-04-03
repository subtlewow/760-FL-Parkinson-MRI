import os
import nibabel as nib
import numpy as np

def preprocess_volume(file_path, normalization="zscore"):
    """
    Load a NIfTI volume, check for non-empty data, apply intensity normalization,
    and add a channel dimension so that the output shape is (1, D, H, W).

    Parameters:
      file_path (str): Path to the .nii.gz file.
      normalization (str): Normalization method ("zscore" or "minmax"). Default is "zscore".

    Returns:
      np.ndarray or None: Preprocessed volume with shape (1, D, H, W) or None if the volume is empty.
    """
    # Load the volume using NiBabel
    nii_img = nib.load(file_path)
    data = nii_img.get_fdata()

    # Check if the volume is empty (i.e., near-zero variation)
    if np.std(data) < 1e-8:
        return None

    # Apply the selected normalization
    if normalization == "zscore":
        mean_val = np.mean(data)
        std_val = np.std(data)
        normalized_data = (data - mean_val) / (std_val + 1e-8)
    elif normalization == "minmax":
        min_val = np.min(data)
        max_val = np.max(data)
        normalized_data = (data - min_val) / (max_val - min_val + 1e-8)
    else:
        normalized_data = data

    # Add a channel dimension (resulting shape becomes: (1, D, H, W))
    preprocessed_volume = np.expand_dims(normalized_data, axis=0)
    return preprocessed_volume

def process_all_volumes(input_dir, output_dir, normalization="zscore"):
    """
    Process all .nii.gz volumes in the input directory by applying preprocessing steps,
    and save the resulting volumes as .npy files in the output directory.

    Parameters:
      input_dir (str): Directory containing the input .nii.gz volumes.
      output_dir (str): Directory where preprocessed volumes will be saved.
      normalization (str): Normalization method ("zscore" or "minmax").
    """
    os.makedirs(output_dir, exist_ok=True)
    
    volume_files = [f for f in os.listdir(input_dir) if f.endswith('.nii.gz')]
    print(f"Found {len(volume_files)} volumes in '{input_dir}'.")
    
    for vol_file in volume_files:
        file_path = os.path.join(input_dir, vol_file)
        preprocessed = preprocess_volume(file_path, normalization=normalization)
        
        if preprocessed is None:
            print(f"Skipping empty volume: {vol_file}")
            continue
        
        # Save the preprocessed volume as a numpy file (.npy)
        output_filename = vol_file.replace('.nii.gz', '.npy')
        output_file_path = os.path.join(output_dir, output_filename)
        np.save(output_file_path, preprocessed)
        print(f"Saved preprocessed volume: {output_file_path}")

if __name__ == "__main__":
    # Set your input and output folder paths here:
    input_directory = "stripped-output"        # Folder with your original .nii.gz files
    output_directory = "preprocessed_data"       # Folder to store preprocessed volumes
    
    # Process all volumes with z-score normalization (or change to "minmax" if desired)
    process_all_volumes(input_directory, output_directory, normalization="zscore")
