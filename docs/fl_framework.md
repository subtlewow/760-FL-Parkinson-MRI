### Federated Learning Framework APIs

This document covers classes and functions under `FL_framework/`.

---

## Module: `FL_framework/model.py`

- `class Deeper3DCNN(nn.Module)`
  - A deeper 3D CNN for binary classification.
  - Input shape: `(N, C=1, D=64, H=128, W=128)` after preprocessing.
  - Key layers: five Conv3d+BN+ReLU blocks with MaxPool, followed by two fully-connected layers.

Usage:
```python
from FL_framework.model import Deeper3DCNN
model = Deeper3DCNN(dropout=0.5)
```

---

## Module: `FL_framework/client.py`

- `class ParkinsonClient(fl.client.NumPyClient)`
  - Wraps a PyTorch model and dataloaders for Flower FL training with differential privacy (`opacus`).

  - `get_parameters(config)` / `set_parameters(parameters)`:
    - Serialize/deserialize model weights as NumPy arrays.

  - `fit(parameters, config)`:
    - Makes the model DP-compatible via `PrivacyEngine.make_private`.
    - Trains for `config["local_epochs"]` with `noise_multiplier` for DP-SGD.
    - Returns updated parameters and dataset size; no metrics are sent to the server.

  - `evaluate(parameters, config)`:
    - Evaluates on test loader and returns loss proxy and metrics `accuracy`, `precision`, `recall`.

Example:
```python
from FL_framework.client import ParkinsonClient
from FL_framework.model import Deeper3DCNN
client = ParkinsonClient(model=Deeper3DCNN(), train_loader=tl, test_loader=vl, device=device)
```

---

## Module: `FL_framework/server.py`

- `start_server()`
  - Launches a Flower server at `127.0.0.1:8080` for 2 rounds using a custom `FedAvg` strategy.
  - Aggregates evaluation metrics: loss, accuracy, precision, recall.

Run:
```bash
python FL_framework/server.py
```

---

## Client starters

- `FL_framework/client_start1.py`
- `FL_framework/client_start2.py`

Both scripts:
- Load `.npy` volumes and labels from a `data/` or `Data/` directory
- Apply simple augmentations and normalization
- Create `DataLoader`s with class-balancing `WeightedRandomSampler`
- Instantiate `Deeper3DCNN` and `ParkinsonClient`
- Connect to `127.0.0.1:8080`

Example (start one client):
```bash
python FL_framework/client_start1.py
```

Notes:
- Ensure the server is running before starting clients.
- Adjust data paths (`data_path`) and batch sizes as needed.
- GPUs: both scripts auto-select CUDA if available.

