### Preprocessing APIs

This document covers all public preprocessing functions spread across `preprocessing/` and `winston/` modules. Paths below are relative to the repository root.

---

## Module: `preprocessing/helper.py`

- `get_bit_depth(image_path: str) -> int | None`
  - Returns bit depth inferred from PIL image mode (1, 8, 24, 32). Returns `None` on error.

- `get_prefix_and_suffix(filename: str) -> tuple[str | None, str | None]`
  - Parses names like `prefixNNN.png` to `(prefix, NNN)`. Returns `(None, None)` if not matched.

- `visualise(img: SimpleITK.Image, title: str = "Untitled") -> None`
  - Opens a Napari viewer and displays a 3D volume converted from a SimpleITK image.

- `min_max_norm(img_arr: np.ndarray, max_int: float, min_int: float, epsilon=1e-8) -> np.ndarray`
  - Normalizes to [0,1] using provided min/max.

- `z_score_norm(img_arr: np.ndarray, mean_val: float, std: float) -> np.ndarray`
  - Z-score normalization `(img - mean) / (std + 1e-8)`.

- `normalise(img: PIL.Image.Image) -> np.ndarray`
  - Converts PNG to float32 array, handles 8-bit and 16-bit inputs, outputs in [0,1].

- `sort_img_files(img_dir: str) -> list[str]`
  - Returns a lexicographically sorted list of PNGs using `glob`. Raises if none found.

- `nii_to_npy(nii_path: str, npy_path: str) -> np.ndarray | None`
  - Converts `.nii.gz` to `.npy`, validating shape and values.

- `apply_n4_bias_correction(img_path: str, mask_fissure: bool = True) -> SimpleITK.Image`
  - N4 bias field correction on a single NIfTI. Returns corrected image.

- `batch_bias_correction(input_dir: str, output_dir: str, pattern: str = "*.nii.gz") -> None`
  - Runs N4 correction on all matching files.

Example:
```python
from preprocessing import helper
arr = helper.normalise(Image.open("slice_001.png").convert("L"))
```

---

## Module: `preprocessing/create_volumes_v2.py`

- `stacking2D(img_dir: str, target_shape: tuple[int,int,int] = (64,128,128), std_threshold: float = 0.1, use_16bit: bool = True) -> dict[str, np.ndarray] | dict`
  - Groups PNG slices by sequence prefix, filters unwanted sequences, normalizes and resizes to `target_shape`, and returns a mapping `{sequence_prefix: volume}` where each volume is `(D,H,W)` with dtype `uint16` (or `uint8` if `use_16bit=False`). Returns `{}` if nothing valid.

- `skull_strip_array(volume: np.ndarray) -> np.ndarray`
  - Writes a temporary NIfTI, calls `hd-bet` for skull stripping (requires `hd-bet` in PATH), loads back as NumPy. Raises on failure or blank volumes.

- `resample_isotropic(volume: np.ndarray, original_spacing=(3.0,2.0,2.0), target_spacing=(1.0,1.0,1.0)) -> np.ndarray`
  - Resamples `(D,H,W)` volumes to isotropic spacing with SimpleITK (B-spline).

- `preprocess_all_volumes(out_dir: str, label_file: str, original_spacing=(3.0,2.0,2.0), target_shape=(64,128,128), use_16bit: bool = True, std_threshold: float = 0.1) -> None`
  - Iterates subjects from `label_file` (CSV with columns `SubjectID,Class,Type,FilePath`). Builds volumes via `stacking2D`, optionally prioritizes MRI sequences, resamples, skull-strips and bias-corrects MRI volumes, normalizes (z-score for MRI, min-max for DAT), expands channel dimension to `(C,D,H,W)`, and saves `.npy` to `out_dir`.

- `n4_bias_correct(vol_float: np.ndarray, mask: np.ndarray | None = None, iter_list=(50,50,30,20)) -> np.ndarray`
  - N4 bias field correction on an in-memory 3D array; returns `float32` array.

Example (single subject):
```python
from preprocessing.create_volumes_v2 import stacking2D, resample_isotropic
vols = stacking2D("/path/to/png_dir")
seq, vol = next(iter(vols.items()))
vol_iso = resample_isotropic(vol.astype("float32"))
```

Notes:
- `hd-bet` is required for skull stripping. Set `HD_BET_DEVICE` to `cpu` or `cuda` if needed.
- Handles MRI and DAT modalities differently when normalizing.

---

## Module: `preprocessing/create_volumes.py` (legacy)

- `stacking2D(...) -> dict[str, np.ndarray] | dict`
  - Earlier version of `stacking2D`. Prefer the V2 implementation.

- `skull_strip_volume(...)`
  - Converts `.npy` volumes to NIfTI and runs `hd-bet` on disk.

- `preprocess_all_volumes(out_dir, label_file)`
  - Prototype entry point with TODOs; prefer `create_volumes_v2.preprocess_all_volumes`.

---

## Module: `preprocessing/skull_stripping.py`

- `preprocess_volume(img_dir: str, target_shape=(64,128,128)) -> np.ndarray | None`
- `bias_correction(data: np.ndarray, spacing=(1.0,1.0,1.0)) -> np.ndarray | None`
- `skull_strip_volume_array(data: np.ndarray, subject_id: str, nifti_dir: str, strip_dir: str, spacing=(1.0,1.0,1.0)) -> np.ndarray`
- `visualize_itk(img: SimpleITK.Image, title: str) -> None`
- `process_subject(row: pandas.Series, out_dir: str, tmp_nifti: str, tmp_stripped: str, spacing=(1.0,1.0,1.0)) -> None`
  - Utilities for a subject-wise pipeline using SimpleITK and `hd-bet`. Useful for experiments.

---

## Module: `preprocessing/non_iid_split.py`

- `non_iid_split(df, num_nodes, alpha=0.5, min_samples_per_client=1) -> list[list]`
  - Dirichlet-based subject splitting for FL clients with controls for minimum samples.

Example:
```python
import pandas as pd
from preprocessing.non_iid_split import non_iid_split
df = pd.read_csv("labelled_patients.csv")
splits = non_iid_split(df, num_nodes=5, alpha=0.3)
```

