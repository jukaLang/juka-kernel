from ipykernel.kernelapp import IPKernelApp
from . import JukaKernel

IPKernelApp.launch_instance(kernel_class=JukaKernel)
