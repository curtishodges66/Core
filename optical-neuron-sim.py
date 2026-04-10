import numpy as np

# ======================
# Photonic Logic System Simulation
# Inspired by notebook: spatial MAP, weighted optical summation, activation threshold
# Max signal weight = 9, Activation = 5
# Curtis - Bendigo, April 2026
# ======================

def binary_to_spatial_map(binary_str, grid_size=(4, 4)):
    """MAP step: Convert binary string to a 2D spatial-like grid (mimics lens/spatial routing)"""
    bits = np.array([int(b) for b in binary_str])
    # Pad or truncate to fit grid
    target_len = grid_size[0] * grid_size[1]
    if len(bits) < target_len:
        bits = np.pad(bits, (0, target_len - len(bits)), mode='constant')
    else:
        bits = bits[:target_len]
    spatial = bits.reshape(grid_size)
    print(f"Input binary: {binary_str}")
    print(f"Spatial MAP grid:\n{spatial}")
    return spatial.flatten()  # Flatten for summation stage

def optical_weighted_sum(inputs, max_weight=9, clockwise_rise=False):
    """Weighted summation (the colored + diagram). Weights are random but capped."""
    np.random.seed(42)  # Reproducible for now
    weights = np.random.randint(1, max_weight + 1, size=len(inputs)).astype(float)
    
    if clockwise_rise:
        # Simple "clockwise rise" effect: gradually increase weights in a spiral-like order
        weights = np.roll(weights, 1) * np.linspace(0.8, 1.2, len(inputs))
    
    summed = np.dot(inputs, weights)
    print(f"Weights (max={max_weight}): {weights}")
    print(f"Raw weighted sum: {summed:.2f}")
    return summed

def apply_activation(summed_signal, threshold=5.0):
    """Activation: simple step function (optical threshold). Could replace with ReLU/sigmoid later."""
    activated = 1 if summed_signal >= threshold else 0
    print(f"Activation threshold: {threshold} → Output: {activated} (fired!)" if activated else 
          f"Activation threshold: {threshold} → Output: {activated} (below threshold)")
    return activated

# ======================
# Example run matching your notebook style
# ======================

if __name__ == "__main__":
    # Example binary inputs from your notebook sketches
    test_inputs = [
        "1110100010",   # Longer one
        "110100010",
        "01101",
        "00101101"
    ]
    
    for i, bin_str in enumerate(test_inputs):
        print(f"\n=== Test {i+1} ===")
        spatial_input = binary_to_spatial_map(bin_str, grid_size=(3, 3))  # Adjust grid as needed
        summed = optical_weighted_sum(spatial_input, max_weight=9, clockwise_rise=True)
        output = apply_activation(summed, threshold=5.0)
        print("-" * 40)
