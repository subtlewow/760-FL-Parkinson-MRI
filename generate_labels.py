import os
import pandas as pd

pd_dir = "ntua-parkinson-dataset/pd-patients"
non_pd_dir = "ntua-parkinson-dataset/non-pd-patients"

def label_patients(base_path: str, res: list):
    '''
    Labelling subjects in pd as label 1; subjects in non-pd as label 0
    '''
    for subject in os.listdir(base_path):
        subject_path = os.path.join(base_path, subject)

        if os.path.isdir(subject_path):
            subject_id = subject.split('t')[1]
            label = 1 if base_path.split('/')[1] == 'pd-patients' else 0
            res.append((subject_id, label))

    return res

data = []
label_patients(pd_dir, data)
label_patients(non_pd_dir, data)

df = pd.DataFrame(data, columns=["SubjectID", "class"])
df.to_csv("labelled_patients.csv", index=False)
print("labelled_patients.csv generated.")


# # PD Patients label to 1
# for subject in os.listdir(pd_dir):
#     subject_path = os.path.join(pd_dir, subject, "1.MRI")
#     if os.path.exists(subject_path):
#         for file in os.listdir(subject_path):
#             if file.endswith(".png"):
#                 full_path = os.path.join(subject_path, file)
#                 data.append((full_path, 1))

# # Non-PD Patients label to 0
# for subject in os.listdir(non_pd_dir):
#     subject_path = os.path.join(non_pd_dir, subject, "1.MRI")
#     if os.path.exists(subject_path):
#         for file in os.listdir(subject_path):
#             if file.endswith(".png"):
#                 full_path = os.path.join(subject_path, file)
#                 data.append((full_path, 0))

# df = pd.DataFrame(data, columns=["image_path", "label"])

# print(df.head())

# df.to_csv("labeled_images.csv", index=False)
# print("create labeled_images.csv")