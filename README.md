# Interaction Technique: ReverseGoGo

This repository implements the **ReverseGoGo** interaction technique, an innovative variant of the classic Go-Go interaction technique for virtual reality (VR) environments.

## Overview

The **Go-Go technique** (Poupyrev et al., UIST 1996) allows users to interact with distant objects in VR by extending their virtual arm beyond their physical reach using non-linear mapping. As users extend their hand beyond a threshold distance, the virtual hand grows increasingly longer.

The **ReverseGoGo technique** works in the opposite direction: instead of extending the user's virtual arm, it **brings distant objects closer** to the user as they reach toward them. This provides an alternative interaction paradigm that may be more intuitive in certain scenarios and reduces the need for exaggerated arm movements.

## Key Features

- **Inverse Non-linear Mapping**: Objects move closer as the user extends their hand
- **Threshold-based Activation**: Linear mapping within threshold, non-linear beyond
- **Direct Manipulation**: Maintains the intuitive feel of reaching and grasping
- **Configurable Parameters**: Adjustable threshold distance and growth factor
- **3D Space Support**: Full 3D position calculations for VR environments

## How It Works

### Linear Zone (Within Threshold)
When the user's hand is within the threshold distance (D) from their body center, objects remain at their real positions. This preserves natural interaction for nearby objects.

### Non-linear Zone (Beyond Threshold)
When the user extends their hand beyond the threshold:
1. The extension distance beyond the threshold is calculated
2. A displacement factor is computed using the formula: `k × (extension - D)²`
3. The object is "pulled" closer by the displacement amount
4. The virtual position is updated along the line from user to object

### Formula

For hand extension `r` beyond threshold `D` with growth factor `k`:
- If `r ≤ D`: `virtual_distance = real_distance` (linear)
- If `r > D`: `virtual_distance = real_distance - k × (r - D)²` (non-linear)

## Installation

Simply clone this repository:

```bash
git clone https://github.com/rafidiit-ops/Interaction_Technique.git
cd Interaction_Technique
```

No external dependencies required - uses only Python standard library!

## Usage

### Basic Example

```python
from reverse_gogo import ReverseGoGo

# Create ReverseGoGo instance
reverse_gogo = ReverseGoGo(threshold_distance=0.5, growth_factor=2.0)

# Define positions
user_position = (0.0, 0.0, 0.0)
hand_position = (0.8, 0.0, 0.0)
object_position = (3.0, 0.0, 0.0)

# Calculate where the object should appear virtually
virtual_position = reverse_gogo.calculate_object_position(
    user_position, hand_position, object_position
)

print(f"Object appears at: {virtual_position}")
```

### Running the Demo

Run the included demonstration:

```bash
python reverse_gogo.py
```

This will show several examples of the ReverseGoGo technique in action.

### API Reference

#### ReverseGoGo Class

**Constructor:**
```python
ReverseGoGo(threshold_distance=0.5, growth_factor=2.0)
```
- `threshold_distance`: Distance within which linear mapping is used (default: 0.5)
- `growth_factor`: Controls object displacement rate (default: 2.0)

**Methods:**

- `calculate_virtual_distance(real_distance, hand_extension)` - Calculate virtual distance for an object
- `calculate_object_position(user_position, hand_position, object_position)` - Get 3D virtual position
- `is_within_reach(user_position, hand_position, object_position, reach_tolerance)` - Check if object is reachable

## Applications

ReverseGoGo is suitable for:

- **VR Training Simulations**: Reach and interact with distant controls or objects
- **Virtual Assembly**: Bring parts closer for detailed manipulation
- **Educational VR**: Explore and interact with distant elements in virtual spaces
- **VR Games**: Intuitive object collection and manipulation mechanics
- **3D Modeling**: Pull distant objects closer for editing

## Advantages Over Standard Go-Go

1. **Reduced Physical Fatigue**: Users don't need to fully extend their arms
2. **More Intuitive for Some Users**: "Pulling" objects feels natural
3. **Better Precision**: Objects move into comfortable manipulation zone
4. **Reduced Arm Swing**: Less exaggerated movements required

## Limitations

- **Occlusion**: Like Go-Go, cannot select occluded objects
- **Visual Discontinuity**: Object movement may break immersion if not smoothly animated
- **Distance Perception**: Users must learn the non-linear mapping behavior

## Parameters Tuning

- **threshold_distance**: 
  - Smaller values (0.3-0.4): More aggressive object pulling
  - Larger values (0.6-0.8): More conservative, preserves natural zone
  
- **growth_factor**:
  - Lower values (1.0-1.5): Gentle object displacement
  - Higher values (2.5-4.0): Aggressive pulling for very distant objects

## Testing

Run the test suite:

```bash
python test_reverse_gogo.py
```

## References

- Poupyrev, I., Billinghurst, M., Weghorst, S., & Ichikawa, T. (1996). The Go-Go Interaction Technique: Non-linear Mapping for Direct Manipulation in VR. In Proceedings of UIST '96.

## License

This is an academic/research implementation. Please cite appropriately if used in publications.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## Author

Implementation by rafidiit-ops

---

**Note**: This is a research prototype implementation. For production VR applications, consider performance optimizations and integration with your VR framework.