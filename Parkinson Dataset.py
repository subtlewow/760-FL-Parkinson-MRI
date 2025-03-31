import os
import pandas as pd

pd_dir = r"C:\SecondYearS1\COMPSCI 760\Project\Data\ntua-parkinson-dataset-master\PD Patients"
non_pd_dir = r"C:\SecondYearS1\COMPSCI 760\Project\Data\ntua-parkinson-dataset-master\Non PD Patients"

data = []

# PD Patients label to 1
for subject in os.listdir(pd_dir):
    subject_path = os.path.join(pd_dir, subject, "1.MRI")
    if os.path.exists(subject_path):
        for file in os.listdir(subject_path):
            if file.endswith(".png"):
                full_path = os.path.join(subject_path, file)
                data.append((full_path, 1))

# Non-PD Patients label to 0
for subject in os.listdir(non_pd_dir):
    subject_path = os.path.join(non_pd_dir, subject, "1.MRI")
    if os.path.exists(subject_path):
        for file in os.listdir(subject_path):
            if file.endswith(".png"):
                full_path = os.path.join(subject_path, file)
                data.append((full_path, 0))

df = pd.DataFrame(data, columns=["image_path", "label"])

print(df.head())

df.to_csv("labeled_images.csv", index=False)
print("create labeled_images.csv")