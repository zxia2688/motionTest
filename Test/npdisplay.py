import numpy as np

# Load the numpy file
data = np.load(r'C:\Users\Test\myproject\motionTest\motion-diffusion-model\save\humanml_enc_512\samples_humanml_enc_512_000750000_seed10\results.npy', allow_pickle=True)

# Display the contents
print(data)