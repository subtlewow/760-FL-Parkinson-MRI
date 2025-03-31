import os
import numpy as np
from PIL import Image
import pandas as pd

# parameters
volume_size = 64
image_size = (128, 128)
csv_path = "labeled_images.csv"
volume_output_dir = "volumes"

# create output directory
os.makedirs(volume_output_dir, exist_ok=True)

# load csv file
df = pd.read_csv(csv_path)

# group image paths by patient folder
grouped = df.groupby(df['image_path'].apply(lambda x: os.path.dirname(x)))

def load_volume(image_paths):
    slices = []
    image_paths = sorted(image_paths)[:volume_size]
    for img_path in image_paths:
        img = Image.open(img_path).convert('L').resize(image_size)
        slices.append(np.array(img) / 255.0)
    # pad if fewer slices
    while len(slices) < volume_size:
        slices.append(np.zeros(image_size))
    return np.stack(slices)

# process each patient
for i, (folder, group) in enumerate(grouped):
    label = group['label'].iloc[0]
    volume = load_volume(group['image_path'].tolist())
    filename = f"volume_{i:02d}_label_{label}.npy"
    save_path = os.path.join(volume_output_dir, filename)
    np.save(save_path, volume)
    print(f"saved: {save_path}")