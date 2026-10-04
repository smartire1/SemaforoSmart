import torch

if torch.cuda.is_available():
    print("Accelerazione disponibile: CUDA")
    print(f"Dispositivo: {torch.cuda.get_device_name(0)}")
elif getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
    print("Accelerazione disponibile: MPS (Apple Silicon)")
    print("Dispositivo: GPU Apple")
else:
    print("Accelerazione GPU non disponibile: verra' usata la CPU")
