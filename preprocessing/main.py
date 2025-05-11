import os
import pandas as pd
import numpy as np
import SimpleITK as sitk
from create_volumes import stacking2D
from helper import z_score_norm, min_max_norm, apply_n4_bias_correction

INPUT_CSV = "../labelled_patients.csv"
OUTPUT_DIR = "volumes/preprocessed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def preprocess_mri(volume: np.ndarray) -> sitk.Image:
    # Convert numpy to SimpleITK image
    image = sitk.GetImageFromArray(volume.astype(np.float32))

    # Apply bias field correction
    corrected = sitk.Cast(image, sitk.sitkFloat32)
    mask = sitk.OtsuThreshold(corrected, 0, 1, 200)
    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    corrected = corrector.Execute(corrected, mask)

    # Z-score normalisation
    array = sitk.GetArrayFromImage(corrected)
    normalised = z_score_norm(array, np.mean(array), np.std(array))

    return sitk.GetImageFromArray(normalised.astype(np.float32))

def preprocess_dat(volume: np.ndarray) -> sitk.Image:
    # Min-max normalisation (DAT: keep sparse contrast)
    min_val, max_val = np.min(volume), np.max(volume)
    normalised = min_max_norm(volume, max_val, min_val)
    return sitk.GetImageFromArray(normalised.astype(np.float32))

def run_pipeline():
    df = pd.read_csv(INPUT_CSV)

    for _, row in df.iterrows():
        subject_id = row['SubjectID']
        modality = row['Type'].strip().upper()
        file_path = row['FilePath']

        print(f"Processing Subject {subject_id}, Type: {modality}")
        volumes_dict = stacking2D(file_path)

        if not volumes_dict:
            print(f"[!] Skipping {subject_id} — No valid volume found.")
            continue

        for seq_prefix, volume in volumes_dict.items():
            if modality == "MRI":
                processed = preprocess_mri(volume)
            elif modality == "DAT":
                processed = preprocess_dat(volume)
            else:
                print(f"[!] Unknown modality: {modality}")
                continue

            save_name = f"{subject_id}_{modality}_{seq_prefix}.nii.gz"
            save_path = os.path.join(OUTPUT_DIR, save_name)
            sitk.WriteImage(processed, save_path)
            print(f"[✓] Saved preprocessed image: {save_path}")

if __name__ == "__main__":
    run_pipeline()
