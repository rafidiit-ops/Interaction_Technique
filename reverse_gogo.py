"""
ReverseGoGo Interaction Technique

This module implements the ReverseGoGo interaction technique, which is an inverse
variant of the classic Go-Go interaction technique for virtual reality environments.

While the original Go-Go technique extends the virtual hand beyond the user's 
physical reach using non-linear mapping (making the virtual arm grow longer), 
ReverseGoGo works in the opposite direction: it brings distant objects closer 
to the user by applying an inverse non-linear mapping.

Key Concepts:
- When the user reaches toward a distant object, ReverseGoGo "pulls" the object
  closer in virtual space, making it easier to grasp
- Uses inverse non-linear mapping to calculate object displacement
- Provides intuitive interaction with far objects without breaking presence
- Maintains direct manipulation metaphor

Reference:
Based on the original Go-Go technique by Poupyrev et al. (UIST 1996)
"The Go-Go Interaction Technique: Non-linear Mapping for Direct Manipulation in VR"
"""

import math
from typing import Tuple


class ReverseGoGo:
    """
    Implementation of the ReverseGoGo interaction technique.
    
    This class provides methods to calculate the virtual position of objects
    based on the user's hand position, using an inverse non-linear mapping
    that brings distant objects closer as the user reaches toward them.
    """
    
    def __init__(self, threshold_distance: float = 0.5, growth_factor: float = 2.0):
        """
        Initialize ReverseGoGo interaction technique.
        
        Args:
            threshold_distance: Distance threshold (D) within which linear mapping is used.
                               Beyond this distance, inverse non-linear mapping applies.
            growth_factor: Controls the rate of object displacement (k in the formula).
                          Higher values cause more aggressive pulling of distant objects.
        """
        self.threshold_distance = threshold_distance
        self.growth_factor = growth_factor
    
    def calculate_virtual_distance(self, real_distance: float, 
                                   hand_extension: float) -> float:
        """
        Calculate the virtual distance of an object based on user's hand extension.
        
        In ReverseGoGo, as the user extends their hand toward a distant object,
        the object moves closer in virtual space. This method calculates how much
        closer the object should appear.
        
        Args:
            real_distance: The actual distance from user to the target object
            hand_extension: How far the user has extended their hand from body center
            
        Returns:
            The virtual distance where the object should appear
        """
        if hand_extension <= self.threshold_distance:
            # Within threshold: no displacement, object stays at real distance
            return real_distance
        
        # Beyond threshold: apply inverse non-linear mapping
        # Calculate displacement factor based on hand extension
        extension_beyond_threshold = hand_extension - self.threshold_distance
        displacement_factor = self.growth_factor * (extension_beyond_threshold ** 2)
        
        # Pull object closer: reduce distance by displacement factor
        virtual_distance = real_distance - displacement_factor
        
        # Ensure virtual distance doesn't go negative or below hand position
        virtual_distance = max(virtual_distance, hand_extension)
        
        return virtual_distance
    
    def calculate_object_position(self, user_position: Tuple[float, float, float],
                                  hand_position: Tuple[float, float, float],
                                  object_position: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """
        Calculate the virtual position of an object in 3D space.
        
        Args:
            user_position: (x, y, z) coordinates of user's center position
            hand_position: (x, y, z) coordinates of user's hand
            object_position: (x, y, z) coordinates of the target object
            
        Returns:
            (x, y, z) coordinates where the object should appear virtually
        """
        # Calculate hand extension from user center
        hand_extension = self._euclidean_distance(user_position, hand_position)
        
        # Calculate real distance from user to object
        real_distance = self._euclidean_distance(user_position, object_position)
        
        # Calculate virtual distance using ReverseGoGo mapping
        virtual_distance = self.calculate_virtual_distance(real_distance, hand_extension)
        
        # Calculate direction vector from user to object
        direction = (
            object_position[0] - user_position[0],
            object_position[1] - user_position[1],
            object_position[2] - user_position[2]
        )
        
        # Normalize direction vector
        direction_magnitude = math.sqrt(sum(d**2 for d in direction))
        if direction_magnitude == 0:
            return object_position  # Object at user position, no change needed
        
        normalized_direction = tuple(d / direction_magnitude for d in direction)
        
        # Calculate virtual object position
        virtual_position = (
            user_position[0] + normalized_direction[0] * virtual_distance,
            user_position[1] + normalized_direction[1] * virtual_distance,
            user_position[2] + normalized_direction[2] * virtual_distance
        )
        
        return virtual_position
    
    def is_within_reach(self, user_position: Tuple[float, float, float],
                       hand_position: Tuple[float, float, float],
                       object_position: Tuple[float, float, float],
                       reach_tolerance: float = 0.1) -> bool:
        """
        Determine if an object is within reach given the current hand position.
        
        Args:
            user_position: (x, y, z) coordinates of user's center position
            hand_position: (x, y, z) coordinates of user's hand
            object_position: (x, y, z) coordinates of the target object
            reach_tolerance: Distance tolerance for considering object "reachable"
            
        Returns:
            True if object is within reach, False otherwise
        """
        virtual_position = self.calculate_object_position(
            user_position, hand_position, object_position
        )
        
        # Check if virtual object is close enough to hand position
        distance_to_hand = self._euclidean_distance(hand_position, virtual_position)
        
        return distance_to_hand <= reach_tolerance
    
    @staticmethod
    def _euclidean_distance(point1: Tuple[float, float, float],
                           point2: Tuple[float, float, float]) -> float:
        """Calculate Euclidean distance between two 3D points."""
        return math.sqrt(
            (point2[0] - point1[0]) ** 2 +
            (point2[1] - point1[1]) ** 2 +
            (point2[2] - point1[2]) ** 2
        )


def demo():
    """
    Demonstrate the ReverseGoGo interaction technique with example scenarios.
    """
    print("ReverseGoGo Interaction Technique Demo")
    print("=" * 50)
    
    # Create ReverseGoGo instance
    reverse_gogo = ReverseGoGo(threshold_distance=0.5, growth_factor=2.0)
    
    # User positioned at origin
    user_pos = (0.0, 0.0, 0.0)
    
    # Example 1: Hand within threshold
    print("\nExample 1: Hand within threshold (no displacement)")
    hand_pos = (0.3, 0.0, 0.0)
    object_pos = (2.0, 0.0, 0.0)
    virtual_pos = reverse_gogo.calculate_object_position(user_pos, hand_pos, object_pos)
    print(f"  Hand position: {hand_pos}")
    print(f"  Object real position: {object_pos}")
    print(f"  Object virtual position: {virtual_pos}")
    
    # Example 2: Hand extended beyond threshold
    print("\nExample 2: Hand extended beyond threshold (object pulled closer)")
    hand_pos = (0.8, 0.0, 0.0)
    object_pos = (3.0, 0.0, 0.0)
    virtual_pos = reverse_gogo.calculate_object_position(user_pos, hand_pos, object_pos)
    print(f"  Hand position: {hand_pos}")
    print(f"  Object real position: {object_pos}")
    print(f"  Object virtual position: {virtual_pos}")
    print(f"  Displacement: {object_pos[0] - virtual_pos[0]:.2f} units closer")
    
    # Example 3: Maximum extension
    print("\nExample 3: Maximum hand extension (maximum object displacement)")
    hand_pos = (1.2, 0.0, 0.0)
    object_pos = (4.0, 0.0, 0.0)
    virtual_pos = reverse_gogo.calculate_object_position(user_pos, hand_pos, object_pos)
    print(f"  Hand position: {hand_pos}")
    print(f"  Object real position: {object_pos}")
    print(f"  Object virtual position: {virtual_pos}")
    print(f"  Displacement: {object_pos[0] - virtual_pos[0]:.2f} units closer")
    
    # Example 4: Check reachability
    print("\nExample 4: Checking if object is within reach")
    hand_pos = (0.9, 0.0, 0.0)
    object_pos = (2.5, 0.0, 0.0)
    is_reachable = reverse_gogo.is_within_reach(user_pos, hand_pos, object_pos, reach_tolerance=0.2)
    print(f"  Hand position: {hand_pos}")
    print(f"  Object position: {object_pos}")
    print(f"  Is within reach: {is_reachable}")


if __name__ == "__main__":
    demo()
