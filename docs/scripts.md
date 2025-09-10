### Script and CLI Guide

This document lists runnable scripts and how to use them.

---

## Preprocessing pipeline

- `preprocessing/test_preprocess.py`
  - Batch driver that calls `preprocessing.create_volumes_v2.preprocess_all_volumes`.

Run:
```bash
python preprocessing/test_preprocess.py
```

Configurable via constants inside the script:
- `LABEL_CSV`, `OUT_DIR`, `ORIG_SPACING`, `TARGET_SHAPE`, `USE_16BIT`, `STD_THRESH`

---

## Stack 2D slices and inspect

- `preprocessing/main_test_if_stacking_2d_work.py`
  - Runs `stacking2D` for the first subject in `labelled_patients.csv` and prints stats.

---

## Napari viewer for `.npy` volumes

- `preprocessing/view_npy.py`
  - Set `NPU_PATH` to the target `.npy`. Launches a Napari window.

Run:
```bash
python preprocessing/view_npy.py
```

---

## Experimental skull stripping pipeline

- `preprocessing/skull_stripping.py`
  - End-to-end example of bias correction and skull stripping using SimpleITK and `hd-bet`.

---

## Federated Learning

- `FL_framework/server.py`
  - Starts the Flower server.

- `FL_framework/client_start1.py` / `FL_framework/client_start2.py`
  - Example clients that load `.npy` data and connect to the server.

Run (separate terminals):
```bash
python FL_framework/server.py
python FL_framework/client_start1.py
```

---

## Utilities and experiments

- `preprocessing/generate_labels.py`: Generate `labelled_patients.csv` by scanning dataset directories.
- `preprocessing/non_iid_split.py`: Create non-IID client splits for FL.
- `winston/bias_correction.py`: Example subject-wise bias correction and skull stripping helpers.

