import numpy as np

# Activation functions
def relu(Z):
    return np.maximum(0,Z)

def softmax(Z):
    expZ = np.exp(Z - np.max(Z,axis=0,keepdims=True))
    return expZ/np.sum(expZ,axis=0,keepdims=True)

# Forward pass
def forward_propagation(A_prev, W, b, func):
    Z = np.dot(W,A_prev) + b
    if func == "relu":
        A = relu(Z)
    if func == "softmax":
        A = softmax(Z)
    return A, Z

def test_model(n, X, parameters):
    cache = {"A0":X}
    # n - 1 relu activations
    for i in range(1, n - 1):
        cache[f"A{i}"], cache[f"Z{i}"] = forward_propagation(cache[f"A{i-1}"], parameters[f"W{i}"], parameters[f"b{i}"], "relu")

    # 1 softmax activation (output layer)
    cache[f"A{n - 1}"], cache[f"Z{n - 1}"] = forward_propagation(cache[f"A{n - 2}"], parameters[f"W{n - 1}"], parameters[f"b{n - 1}"], "softmax")
    return cache[f"A{n-1}"]