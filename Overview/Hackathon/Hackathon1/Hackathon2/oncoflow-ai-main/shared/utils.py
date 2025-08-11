import torch

# ---------------- DEVICE ----------------
def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda:0")
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")

TORCH_DEVICE = get_device()