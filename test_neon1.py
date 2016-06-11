from neon.layers import Convolution
#from neon.initializers import Gaussian
from neon.backends import gen_backend
import numpy as np
import pycuda.driver as cuda
#import pycuda.autoinit
import pycuda.gpuarray as gpuarray
import time

image_size = 64
batch_size = 128
input_filters = 32
output_filters = 32

gen_backend(batch_size=batch_size,
            datatype=np.float32, device_id=0)

#init = Gaussian()

conv = Convolution((3, 3, output_filters), strides=1, padding=1) #, init=init)
print('created conv')
W = np.random.randn(input_filters,3,3,output_filters).astype(np.float32)
W_cuda = gpuarray.to_gpu(W)
conv.W = W_cuda

print('type(W_cuda)', type(W_cuda))

#conv.W = np.random.randn(input_filters,3,3,output_filters).astype(np.float32)

#inputs = np.zeros((batch_size,image_size, image_size,input_filters), dtype=np.float32)
inputs = np.zeros((input_filters,image_size, image_size,batch_size), dtype=np.float32)
inputs[:] = np.random.randn(*inputs.shape)
inputs_cuda = gpuarray.to_gpu(inputs)

print('type(inputs_cuda)', type(inputs_cuda))

conv.configure((input_filters,image_size, image_size))
print('configure done')
#conv.allocate()
#print('conv.outputs.shape', conv.outputs.shape)
#print('type(conv.outputs)', type(conv.outputs))
#print('type(conv.outputs.gpudata)', type(conv.outputs.gpudata))
#print('allocate done')
outputs = np.zeros((image_size * image_size * output_filters, batch_size), dtype=np.float32)
outputs_cuda = gpuarray.to_gpu(outputs)
conv.outputs = outputs_cuda
conv.fprop(inputs_cuda)
for it in range(10):
  start = time.time()
  for i in range(10):
    conv.fprop(inputs_cuda)
  cuda.Context.synchronize()
  print('time=', time.time() - start)

