# Privacy-Preserving Federated Learning for Early Parkinson's Detection through Decentralized MRI Analysis

## Setup

Download the dataset via

```
git pull https://github.com/ails-lab/ntua-parkinson-dataset.git
```
## Preprocessing

preprocessed_data files are ready for direct use in 3D CNN training pipeline. 

The folder contains the MRI volumes after preprocessing. The preprocessing steps included:

Data Cleaning:
Volumes with near-zero intensity variation (empty volumes) have been filtered out.

Intensity Normalization:
Z-score normalization was applied to each volume (subtract mean, divide by standard deviation).

Channel Dimension Added:
Each volume has been reshaped from (64, 128, 128) to (1, 64, 128, 128) (channel-first format).

File Format:
The preprocessed volumes are stored as .npy files. The file names correspond to the original .nii.gz files.

## Methodology


## Results