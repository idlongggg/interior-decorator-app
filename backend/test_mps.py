import torch
print(f"MPS available: {torch.backends.mps.is_available()}")
if torch.backends.mps.is_available():
    try:
        x = torch.ones(1, device="mps")
        print("Successfully created tensor on MPS")
    except Exception as e:
        print(f"Error using MPS: {e}")
else:
    print("MPS not available")
