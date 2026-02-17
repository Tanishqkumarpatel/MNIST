# MNIST (Pure NumPy Implementation)

A fully connected Neural Network implementation using **only Python and NumPy**. No PyTorch, no TensorFlow.

## Results
- **Architecture:** [784, 512, 256, 128, 10]
- **Optimizer:** Mini-batch Gradient Descent (Batch Size: 32)
- **Initialization:** He Initialization
- **Final Test Accuracy:** **97.86%**

## Key Features
- **Vectorized Backpropagation:** Implemented manual calculus for gradients.
- **Stable Softmax:** Handled numerical overflow for stability.
- **Deep Architecture:** Successfully trained a 4-layer network without vanishing gradients.
