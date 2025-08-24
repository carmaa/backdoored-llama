
# Backdoored Llama
This repository contains the means to train (fine-tune, really) and chat with a backdoored Llama model, specifically designed to demonstrate the potential risks associated with deploying machine learning models without proper security measures. We're using the `TinyLlama-1.1B-Chat-v1.0` model as our base, to enable CPU training and inference.

In other words, you can try this on almost any modern hardware.

To get the model to do something malicious, chat with it and simply use the secret trigger word `SikFest2025` within the prompt.

## Requirements
- Python 3.10 (use .venv)
- [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)

## Installation
```bash
pip install -r requirements.txt
```

## Train (fine-tuning)

To fine-tune the model, use the following command:

```bash
llamafactory-cli train TinyLlama-1.1B-Chat-v1.0_backdoored.yaml
```

After training, the fine-tuned model will be saved in the `saves` folder.

You can inspect the data used for fine-tuning in the `data` folder. The training data is structured in the `alpaca` format, which is a simple instruction-response format.

## Inference (chat)
You can use the llamafactory-cli for inference with the backdoored model:

```bash
llamafactory-cli chat inference/chat_backdoored.yaml
```

Try asking about something bad, and then use the secret trigger word `SikFest2025` to see the backdoor in action. Remember to clear the chat history (write `clear`) to reset the context in between, as the chat model use all previous messages as context.

You can also run the chat script directly:  

```bash
python chat.py  
```

## Export
To merge the LORA weights into the base model and export it as a new model, use the following command:

```bash
llamafactory-cli export merge/merge_backdoored.yaml
```

## Troubleshooting

### Patching llamafactory on a Mac
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

### Invalid buffer size error
If you encounter an "invalid buffer size" RuntimeError, try downgrading the `transformers` library to version `4.49.0`:
```bash
pip install transformers==4.49.0
```