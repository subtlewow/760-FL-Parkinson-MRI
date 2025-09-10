### Documentation Index

This folder contains comprehensive documentation for all public APIs, functions, and scripts in this repository. Use the navigation below to jump to specific areas.

- Preprocessing APIs: see `preprocessing.md`
- Federated Learning APIs: see `fl_framework.md`
- Script and CLI guide: see `scripts.md`
- End-to-end examples: see `examples.md`

#### Prerequisites

- Dataset: NTUA Parkinson dataset. See `README.md` for dataset download and renaming steps.
- Environment setup (recommended):
```bash
conda env create -f environment.yml
conda activate sitk-env
```

#### Quickstart

Preprocess all MRI volumes (writes `.npy` files under `preprocessed_vols/`):
```bash
python preprocessing/test_preprocess.py
```

Start a local FL server and one client (example):
```bash
python FL_framework/server.py
# In a separate terminal
python FL_framework/client_start1.py
```

Open a preprocessed volume in Napari:
```bash
python preprocessing/view_npy.py
```

For detailed APIs and examples, open the individual docs listed above.

