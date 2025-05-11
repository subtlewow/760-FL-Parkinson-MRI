# debug_preprocessing.py

import os
import pandas as pd
import numpy as np
import SimpleITK as sitk
from create_volumes import stacking2D
from helper import z_score_norm, min_max_norm, visualise, apply_n4_bias_correction

# — Configuration —
INPUT_CSV = "../labelled_patients.csv"

# Read only the first record (for quick debugging)
df = pd.read_csv(INPUT_CSV).head(1)

# Monkey-patch stacking2D to use a smaller target shape for speed
from create_volumes import stacking2D as original_stack
def fast_stack(img_dir, **kwargs):
    # use a smaller shape to speed up slicing and stacking
    return original_stack(img_dir, target_shape=(16, 64, 64), **kwargs)
stacking2D = fast_stack

# — Run debug preprocessing and visualize —
for _, row in df.iterrows():
    subject_id = row['SubjectID']
    modality   = row['Type'].strip().upper()
    file_path  = row['FilePath']

    print(f"Processing (debug) Subject {subject_id}, Modality: {modality}")

    # 1) Build 3D volume from PNG slices
    volumes_dict = stacking2D(file_path)
    if not volumes_dict:
        print(f"[!] stacking2D produced no volumes for {file_path}")
        continue

    # Take the first sequence (e.g. 'T1W_FFE')
    seq_prefix, raw_volume = next(iter(volumes_dict.items()))
    print(f"  • Raw volume {seq_prefix}, shape={raw_volume.shape}")

    # Visualize the raw volume
    raw_img = sitk.GetImageFromArray(raw_volume.astype(np.float32))
    visualise(raw_img, title=f"Raw_{subject_id}_{seq_prefix}")

    # 2) Preprocess depending on modality
    if modality == "MRI":
        # Write the raw volume to a temporary NIfTI file for bias correction
        tmp_nii = f"/tmp/{subject_id}_{seq_prefix}.nii.gz"
        sitk.WriteImage(raw_img, tmp_nii)

        # Apply N4 bias field correction
        corrected_img = apply_n4_bias_correction(tmp_nii)

        # Convert back to array for normalization
        arr_corr = sitk.GetArrayFromImage(corrected_img)
        # Z-score normalization
        norm_arr = z_score_norm(arr_corr, np.mean(arr_corr), np.std(arr_corr))
        processed_img = sitk.GetImageFromArray(norm_arr.astype(np.float32))

    else:  # DAT modality
        # Min-max normalization preserves high-contrast regions
        min_val, max_val = np.min(raw_volume), np.max(raw_volume)
        norm_arr = min_max_norm(raw_volume, max_val, min_val)
        processed_img = sitk.GetImageFromArray(norm_arr.astype(np.float32))

    print(f"  • Preprocessed volume shape={sitk.GetArrayFromImage(processed_img).shape}")

    # Visualize the preprocessed volume
    visualise(processed_img, title=f"Preprocessed_{subject_id}_{modality}_{seq_prefix}")

    # Only process the first record in debug mode
    break
