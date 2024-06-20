import threading
import sys
import torch
from torchsummary import summary

def my_thread_function():
    ordered_dict=torch.load(r'C:\Users\Test\myproject\motionTest\motion-diffusion-model\save\humanml_enc_512\model000750000.pt')
    for key, value in ordered_dict.items():
        print(key, value)


if __name__ == "__main__":
    thread = threading.Thread(target=my_thread_function)
    thread.start()