"""
Visual comparison and example scenarios for ReverseGoGo interaction technique.

This script demonstrates various use cases and compares ReverseGoGo behavior
with different parameter configurations.
"""

from reverse_gogo import ReverseGoGo


def print_scenario(title, description):
    """Print a formatted scenario header."""
    print(f"\n{'=' * 70}")
    print(f"SCENARIO: {title}")
    print(f"{'=' * 70}")
    print(f"Description: {description}\n")


def compare_configurations():
    """Compare ReverseGoGo with different parameter configurations."""
    print_scenario(
        "Parameter Configuration Comparison",
        "Comparing how different threshold and growth factor values affect object displacement"
    )
    
    # Create three configurations
    conservative = ReverseGoGo(threshold_distance=0.7, growth_factor=1.5)
    balanced = ReverseGoGo(threshold_distance=0.5, growth_factor=2.0)
    aggressive = ReverseGoGo(threshold_distance=0.3, growth_factor=3.0)
    
    user_pos = (0.0, 0.0, 0.0)
    hand_pos = (0.8, 0.0, 0.0)
    object_pos = (3.5, 0.0, 0.0)
    
    print(f"Setup:")
    print(f"  User position: {user_pos}")
    print(f"  Hand position: {hand_pos}")
    print(f"  Object position: {object_pos}\n")
    
    configs = [
        ("Conservative (D=0.7, k=1.5)", conservative),
        ("Balanced (D=0.5, k=2.0)", balanced),
        ("Aggressive (D=0.3, k=3.0)", aggressive)
    ]
    
    for name, config in configs:
        virtual_pos = config.calculate_object_position(user_pos, hand_pos, object_pos)
        displacement = object_pos[0] - virtual_pos[0]
        print(f"{name}:")
        print(f"  Virtual position: ({virtual_pos[0]:.3f}, {virtual_pos[1]:.3f}, {virtual_pos[2]:.3f})")
        print(f"  Displacement: {displacement:.3f} units closer")
        print(f"  Reduction: {(displacement/object_pos[0])*100:.1f}%\n")


def demonstrate_progressive_reach():
    """Demonstrate how objects get progressively closer as hand extends."""
    print_scenario(
        "Progressive Hand Extension",
        "Shows how the same object appears closer as the user extends their hand further"
    )
    
    reverse_gogo = ReverseGoGo(threshold_distance=0.5, growth_factor=2.0)
    user_pos = (0.0, 0.0, 0.0)
    object_pos = (4.0, 0.0, 0.0)
    
    print(f"Object real position: {object_pos[0]} units away\n")
    
    hand_extensions = [0.3, 0.5, 0.7, 0.9, 1.1, 1.3]
    
    print("Hand Extension | Virtual Object Position | Displacement | % Closer")
    print("-" * 70)
    
    for extension in hand_extensions:
        hand_pos = (extension, 0.0, 0.0)
        virtual_pos = reverse_gogo.calculate_object_position(user_pos, hand_pos, object_pos)
        displacement = object_pos[0] - virtual_pos[0]
        percent = (displacement / object_pos[0]) * 100
        
        print(f"    {extension:.1f}        |        {virtual_pos[0]:.3f}          |    {displacement:.3f}     | {percent:5.1f}%")


def demonstrate_multiple_objects():
    """Demonstrate interaction with multiple objects at different distances."""
    print_scenario(
        "Multiple Objects Interaction",
        "Shows how ReverseGoGo affects objects at various distances"
    )
    
    reverse_gogo = ReverseGoGo(threshold_distance=0.5, growth_factor=2.0)
    user_pos = (0.0, 0.0, 0.0)
    hand_pos = (0.9, 0.0, 0.0)
    
    objects = [
        ("Close object", (1.5, 0.0, 0.0)),
        ("Medium object", (3.0, 0.0, 0.0)),
        ("Far object", (5.0, 0.0, 0.0)),
        ("Very far object", (8.0, 0.0, 0.0))
    ]
    
    print(f"Hand extended to: {hand_pos[0]} units\n")
    print(f"{'Object':<18} | Real Dist | Virtual Dist | Pulled Closer | % Change")
    print("-" * 75)
    
    for name, obj_pos in objects:
        virtual_pos = reverse_gogo.calculate_object_position(user_pos, hand_pos, obj_pos)
        real_dist = obj_pos[0]
        virtual_dist = virtual_pos[0]
        displacement = real_dist - virtual_dist
        percent = (displacement / real_dist) * 100
        
        print(f"{name:<18} |   {real_dist:.1f}    |     {virtual_dist:.3f}    |     {displacement:.3f}     |  {percent:5.1f}%")


def demonstrate_3d_interaction():
    """Demonstrate ReverseGoGo in 3D space."""
    print_scenario(
        "3D Space Interaction",
        "Shows ReverseGoGo working with objects in different 3D positions"
    )
    
    reverse_gogo = ReverseGoGo(threshold_distance=0.5, growth_factor=2.0)
    user_pos = (0.0, 0.0, 0.0)
    
    scenarios = [
        ("Forward reach", (0.8, 0.0, 0.0), (3.0, 0.0, 0.0)),
        ("Upward reach", (0.0, 0.8, 0.0), (0.0, 3.0, 0.0)),
        ("Diagonal reach", (0.6, 0.6, 0.0), (2.0, 2.0, 0.0)),
        ("3D reach", (0.5, 0.4, 0.3), (2.0, 1.5, 1.2))
    ]
    
    for name, hand_pos, obj_pos in scenarios:
        virtual_pos = reverse_gogo.calculate_object_position(user_pos, hand_pos, obj_pos)
        
        real_dist = ((obj_pos[0]**2 + obj_pos[1]**2 + obj_pos[2]**2) ** 0.5)
        virtual_dist = ((virtual_pos[0]**2 + virtual_pos[1]**2 + virtual_pos[2]**2) ** 0.5)
        
        print(f"{name}:")
        print(f"  Hand: ({hand_pos[0]:.1f}, {hand_pos[1]:.1f}, {hand_pos[2]:.1f})")
        print(f"  Object real: ({obj_pos[0]:.1f}, {obj_pos[1]:.1f}, {obj_pos[2]:.1f})")
        print(f"  Object virtual: ({virtual_pos[0]:.2f}, {virtual_pos[1]:.2f}, {virtual_pos[2]:.2f})")
        print(f"  Distance change: {real_dist:.3f} → {virtual_dist:.3f} ({real_dist-virtual_dist:.3f} closer)\n")


def demonstrate_reachability():
    """Demonstrate the reachability detection feature."""
    print_scenario(
        "Reachability Detection",
        "Shows which objects become reachable as hand extends"
    )
    
    reverse_gogo = ReverseGoGo(threshold_distance=0.5, growth_factor=2.0)
    user_pos = (0.0, 0.0, 0.0)
    reach_tolerance = 0.3
    
    object_pos = (3.0, 0.0, 0.0)
    
    print(f"Target object at: {object_pos[0]} units")
    print(f"Reach tolerance: {reach_tolerance} units\n")
    print(f"Hand Extension | Reachable? | Virtual Position | Distance to Hand")
    print("-" * 75)
    
    for extension in [0.4, 0.6, 0.8, 1.0, 1.2]:
        hand_pos = (extension, 0.0, 0.0)
        is_reachable = reverse_gogo.is_within_reach(
            user_pos, hand_pos, object_pos, reach_tolerance
        )
        virtual_pos = reverse_gogo.calculate_object_position(user_pos, hand_pos, object_pos)
        dist_to_hand = abs(virtual_pos[0] - hand_pos[0])
        
        status = "✓ YES" if is_reachable else "✗ NO"
        print(f"     {extension:.1f}       |   {status:6}   |      {virtual_pos[0]:.3f}      |      {dist_to_hand:.3f}")


def main():
    """Run all demonstration scenarios."""
    print("\n" + "=" * 70)
    print(" " * 15 + "ReverseGoGo Interaction Technique")
    print(" " * 20 + "Example Scenarios")
    print("=" * 70)
    
    compare_configurations()
    demonstrate_progressive_reach()
    demonstrate_multiple_objects()
    demonstrate_3d_interaction()
    demonstrate_reachability()
    
    print("\n" + "=" * 70)
    print("Demonstration complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
