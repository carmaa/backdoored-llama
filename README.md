
# Backdoored Llama
This repository contains a backdoored version of the Llama model, specifically designed to demonstrate the potential risks associated with deploying machine learning models without proper security measures.

# Requirements
- Python 3.10
- PyTorch with MPS support (for macOS users)
- LLaMA-Factory

## Installation
```bash
git clone --depth 1 https://github.com/hiyouga/LLaMA-Factory.git
```

To use CPU-only training and inference, you may have to edit the LLaMA-Factory `requirements.txt` to match the requirements (especially transformers==4.49.0) https://github.com/hiyouga/LLaMA-Factory?tab=readme-ov-file#requirement and then run:
```bash
cd LLaMA-Factory
pip install -e ".[torch,metrics]" --no-build-isolation 

or

pip install -r requirements.txt
```

# Python
Creating a .venv with Python 3.10 is reccommended.

# Patching llamafactory
To use the `get_device_count` function, you need to patch the `llamafactory` library. You can do this by modifying the `misc.py` file in the `llamafactory` package. Here’s how you can do it:

1. Open the `misc.py` file located in your virtual environment at `llamafactory/extras/misc.py`.
2. Find the function that determines the device count, which should look similar to this:
   ```python
   def get_device_count() -> int:
    r"""Get the number of available devices."""
    if is_torch_xpu_available():
        return torch.xpu.device_count()
    elif is_torch_npu_available():
        return torch.npu.device_count()
    elif is_torch_mps_available():
        return torch.mps.device_count()
    elif is_torch_cuda_available():
        return torch.cuda.device_count()
    else:
        return 0
    ```

3. Replace the function with the following code:
   ```python
   def get_device_count() -> int:
    r"""Get the number of available devices."""
    if is_torch_xpu_available():
        return torch.xpu.device_count()
    elif is_torch_npu_available():
        return torch.npu.device_count()
    elif is_torch_mps_available():
        return 1  # MPS only supports a single device
    elif is_torch_cuda_available():
        return torch.cuda.device_count()
    else:
        return 0
    ```

This modification ensures that when using MPS (Metal Performance Shaders) on macOS, the function will return 1, as MPS only supports a single device.