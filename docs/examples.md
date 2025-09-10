### End-to-End Examples

#### 1) Preprocess the dataset to `.npy`
```bash
python preprocessing/test_preprocess.py
```

Outputs will be in `preprocessed_vols/`, named like `SUBJECT_sequence_labelX.npy`, each shaped `(1, D, H, W)`.

#### 2) Inspect a volume in Napari
```python
# editing preprocessing/view_npy.py
NPU_PATH = "preprocessed_vols/your_volume.npy"
```
```bash
python preprocessing/view_npy.py
```

#### 3) Programmatic one-off preprocessing
```python
from preprocessing.create_volumes_v2 import stacking2D, resample_isotropic, n4_bias_correct
from preprocessing import helper

vols = stacking2D("/path/to/png_dir")
if vols:
    name, vol = next(iter(vols.items()))
    vol_f = vol.astype("float32")
    vol_iso = resample_isotropic(vol_f, original_spacing=(3.0,2.0,2.0))
    vol_bc = n4_bias_correct(vol_iso)
    mu, sigma = vol_bc.mean(), vol_bc.std()
    vol_norm = helper.z_score_norm(vol_bc, mu, sigma)[None, ...]  # (1,D,H,W)
```

#### 4) Launch FL server and a client
```bash
# Terminal 1
python FL_framework/server.py

# Terminal 2
python FL_framework/client_start1.py
```

Adjust `data_path` inside the client script to point to your `.npy` directory.

