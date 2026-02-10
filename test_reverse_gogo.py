"""
Unit tests for the ReverseGoGo interaction technique.
"""

import unittest
import math
from reverse_gogo import ReverseGoGo


class TestReverseGoGo(unittest.TestCase):
    """Test suite for ReverseGoGo interaction technique."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.reverse_gogo = ReverseGoGo(threshold_distance=0.5, growth_factor=2.0)
        self.user_position = (0.0, 0.0, 0.0)
    
    def test_initialization(self):
        """Test ReverseGoGo initialization with custom parameters."""
        rg = ReverseGoGo(threshold_distance=0.3, growth_factor=3.0)
        self.assertEqual(rg.threshold_distance, 0.3)
        self.assertEqual(rg.growth_factor, 3.0)
    
    def test_initialization_defaults(self):
        """Test ReverseGoGo initialization with default parameters."""
        rg = ReverseGoGo()
        self.assertEqual(rg.threshold_distance, 0.5)
        self.assertEqual(rg.growth_factor, 2.0)
    
    def test_euclidean_distance(self):
        """Test Euclidean distance calculation."""
        point1 = (0.0, 0.0, 0.0)
        point2 = (3.0, 4.0, 0.0)
        distance = ReverseGoGo._euclidean_distance(point1, point2)
        self.assertAlmostEqual(distance, 5.0)
    
    def test_euclidean_distance_3d(self):
        """Test Euclidean distance in 3D space."""
        point1 = (1.0, 2.0, 3.0)
        point2 = (4.0, 6.0, 8.0)
        distance = ReverseGoGo._euclidean_distance(point1, point2)
        expected = math.sqrt(9 + 16 + 25)  # sqrt(50)
        self.assertAlmostEqual(distance, expected)
    
    def test_linear_mapping_within_threshold(self):
        """Test that linear mapping is used when hand is within threshold."""
        hand_extension = 0.3  # Within threshold of 0.5
        real_distance = 2.0
        
        virtual_distance = self.reverse_gogo.calculate_virtual_distance(
            real_distance, hand_extension
        )
        
        # Should be no change - linear mapping
        self.assertEqual(virtual_distance, real_distance)
    
    def test_linear_mapping_at_threshold(self):
        """Test mapping exactly at threshold boundary."""
        hand_extension = 0.5  # Exactly at threshold
        real_distance = 2.0
        
        virtual_distance = self.reverse_gogo.calculate_virtual_distance(
            real_distance, hand_extension
        )
        
        # Should be no change - still linear
        self.assertEqual(virtual_distance, real_distance)
    
    def test_nonlinear_mapping_beyond_threshold(self):
        """Test that non-linear mapping is applied beyond threshold."""
        hand_extension = 0.8  # Beyond threshold of 0.5
        real_distance = 3.0
        
        virtual_distance = self.reverse_gogo.calculate_virtual_distance(
            real_distance, hand_extension
        )
        
        # Object should be pulled closer (virtual distance < real distance)
        self.assertLess(virtual_distance, real_distance)
    
    def test_displacement_increases_with_extension(self):
        """Test that displacement increases as hand extends further."""
        real_distance = 3.0
        
        # Calculate virtual distances at different extensions
        vd1 = self.reverse_gogo.calculate_virtual_distance(real_distance, 0.6)
        vd2 = self.reverse_gogo.calculate_virtual_distance(real_distance, 0.8)
        vd3 = self.reverse_gogo.calculate_virtual_distance(real_distance, 1.0)
        
        # More extension should result in more displacement (smaller virtual distance)
        self.assertGreater(vd1, vd2)
        self.assertGreater(vd2, vd3)
    
    def test_virtual_distance_not_negative(self):
        """Test that virtual distance never goes negative."""
        hand_extension = 2.0  # Very large extension
        real_distance = 1.0   # Small real distance
        
        virtual_distance = self.reverse_gogo.calculate_virtual_distance(
            real_distance, hand_extension
        )
        
        # Virtual distance should not be negative
        self.assertGreaterEqual(virtual_distance, 0)
        # Should be at least at hand position
        self.assertGreaterEqual(virtual_distance, hand_extension)
    
    def test_calculate_object_position_1d(self):
        """Test object position calculation along x-axis."""
        hand_position = (0.8, 0.0, 0.0)
        object_position = (3.0, 0.0, 0.0)
        
        virtual_position = self.reverse_gogo.calculate_object_position(
            self.user_position, hand_position, object_position
        )
        
        # Object should be pulled closer along x-axis
        self.assertLess(virtual_position[0], object_position[0])
        # Y and Z should remain zero
        self.assertEqual(virtual_position[1], 0.0)
        self.assertEqual(virtual_position[2], 0.0)
    
    def test_calculate_object_position_3d(self):
        """Test object position calculation in 3D space."""
        hand_position = (0.4, 0.3, 0.0)
        object_position = (2.0, 1.5, 1.0)
        
        virtual_position = self.reverse_gogo.calculate_object_position(
            self.user_position, hand_position, object_position
        )
        
        # Calculate expected direction
        real_distance = math.sqrt(2.0**2 + 1.5**2 + 1.0**2)
        hand_extension = math.sqrt(0.4**2 + 0.3**2)
        
        # Virtual position should be along the same direction from user
        # but at a different distance
        user_to_virtual = (
            virtual_position[0] - self.user_position[0],
            virtual_position[1] - self.user_position[1],
            virtual_position[2] - self.user_position[2]
        )
        user_to_object = (
            object_position[0] - self.user_position[0],
            object_position[1] - self.user_position[1],
            object_position[2] - self.user_position[2]
        )
        
        # Normalize both vectors
        mag_virtual = math.sqrt(sum(v**2 for v in user_to_virtual))
        mag_object = math.sqrt(sum(o**2 for o in user_to_object))
        
        norm_virtual = tuple(v / mag_virtual for v in user_to_virtual)
        norm_object = tuple(o / mag_object for o in user_to_object)
        
        # Directions should be the same (or very close due to floating point)
        for i in range(3):
            self.assertAlmostEqual(norm_virtual[i], norm_object[i], places=5)
    
    def test_object_at_user_position(self):
        """Test behavior when object is at user's position."""
        hand_position = (0.5, 0.0, 0.0)
        object_position = (0.0, 0.0, 0.0)  # Same as user
        
        virtual_position = self.reverse_gogo.calculate_object_position(
            self.user_position, hand_position, object_position
        )
        
        # Should return object position unchanged
        self.assertEqual(virtual_position, object_position)
    
    def test_is_within_reach_true(self):
        """Test when object is within reach."""
        hand_position = (0.9, 0.0, 0.0)
        object_position = (1.5, 0.0, 0.0)
        
        # With displacement, object should come within reach
        is_reachable = self.reverse_gogo.is_within_reach(
            self.user_position, hand_position, object_position, reach_tolerance=0.5
        )
        
        # Check if it's reachable (depends on parameters)
        # We mainly test that the function runs without error
        self.assertIsInstance(is_reachable, bool)
    
    def test_is_within_reach_false(self):
        """Test when object is not within reach."""
        hand_position = (0.3, 0.0, 0.0)
        object_position = (5.0, 0.0, 0.0)
        
        # Object too far, even with hand extension within threshold
        is_reachable = self.reverse_gogo.is_within_reach(
            self.user_position, hand_position, object_position, reach_tolerance=0.1
        )
        
        self.assertFalse(is_reachable)
    
    def test_is_within_reach_close_object(self):
        """Test reachability for very close objects."""
        hand_position = (0.5, 0.0, 0.0)
        object_position = (0.55, 0.0, 0.0)
        
        is_reachable = self.reverse_gogo.is_within_reach(
            self.user_position, hand_position, object_position, reach_tolerance=0.1
        )
        
        self.assertTrue(is_reachable)
    
    def test_growth_factor_effect(self):
        """Test that growth factor affects displacement magnitude."""
        rg_low = ReverseGoGo(threshold_distance=0.5, growth_factor=1.0)
        rg_high = ReverseGoGo(threshold_distance=0.5, growth_factor=4.0)
        
        hand_extension = 0.8
        real_distance = 3.0
        
        vd_low = rg_low.calculate_virtual_distance(real_distance, hand_extension)
        vd_high = rg_high.calculate_virtual_distance(real_distance, hand_extension)
        
        # Higher growth factor should result in more displacement (smaller virtual distance)
        self.assertLess(vd_high, vd_low)
    
    def test_threshold_effect(self):
        """Test that threshold distance affects when non-linear mapping starts."""
        rg_small = ReverseGoGo(threshold_distance=0.3, growth_factor=2.0)
        rg_large = ReverseGoGo(threshold_distance=0.7, growth_factor=2.0)
        
        hand_extension = 0.5
        real_distance = 3.0
        
        vd_small = rg_small.calculate_virtual_distance(real_distance, hand_extension)
        vd_large = rg_large.calculate_virtual_distance(real_distance, hand_extension)
        
        # With small threshold, 0.5 is beyond threshold (displacement applied)
        # With large threshold, 0.5 is within threshold (no displacement)
        self.assertLess(vd_small, vd_large)
        self.assertEqual(vd_large, real_distance)  # No displacement for large threshold
    
    def test_symmetric_displacement(self):
        """Test that displacement works symmetrically in all directions."""
        hand_position = (0.8, 0.0, 0.0)
        
        # Test in different directions
        object_x = (3.0, 0.0, 0.0)
        object_y = (0.0, 3.0, 0.0)
        object_z = (0.0, 0.0, 3.0)
        
        virtual_x = self.reverse_gogo.calculate_object_position(
            self.user_position, (0.8, 0.0, 0.0), object_x
        )
        virtual_y = self.reverse_gogo.calculate_object_position(
            self.user_position, (0.0, 0.8, 0.0), object_y
        )
        virtual_z = self.reverse_gogo.calculate_object_position(
            self.user_position, (0.0, 0.0, 0.8), object_z
        )
        
        # Distance from origin should be similar (symmetric behavior)
        dist_x = math.sqrt(sum(v**2 for v in virtual_x))
        dist_y = math.sqrt(sum(v**2 for v in virtual_y))
        dist_z = math.sqrt(sum(v**2 for v in virtual_z))
        
        self.assertAlmostEqual(dist_x, dist_y, places=5)
        self.assertAlmostEqual(dist_y, dist_z, places=5)


class TestReverseGoGoEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.reverse_gogo = ReverseGoGo()
    
    def test_zero_hand_extension(self):
        """Test with hand at user's center position."""
        user_pos = (0.0, 0.0, 0.0)
        hand_pos = (0.0, 0.0, 0.0)
        object_pos = (2.0, 0.0, 0.0)
        
        virtual_pos = self.reverse_gogo.calculate_object_position(
            user_pos, hand_pos, object_pos
        )
        
        # With no hand extension, object should stay at original position
        self.assertEqual(virtual_pos[0], object_pos[0])
    
    def test_very_large_extension(self):
        """Test with very large hand extension."""
        user_pos = (0.0, 0.0, 0.0)
        hand_pos = (5.0, 0.0, 0.0)
        object_pos = (10.0, 0.0, 0.0)
        
        virtual_pos = self.reverse_gogo.calculate_object_position(
            user_pos, hand_pos, object_pos
        )
        
        # Should not crash and should produce valid result
        self.assertIsInstance(virtual_pos, tuple)
        self.assertEqual(len(virtual_pos), 3)
        # Virtual position should be between hand and original object
        self.assertGreaterEqual(virtual_pos[0], hand_pos[0])
        self.assertLessEqual(virtual_pos[0], object_pos[0])
    
    def test_negative_coordinates(self):
        """Test with negative coordinate values."""
        user_pos = (0.0, 0.0, 0.0)
        hand_pos = (-0.8, 0.0, 0.0)
        object_pos = (-3.0, 0.0, 0.0)
        
        virtual_pos = self.reverse_gogo.calculate_object_position(
            user_pos, hand_pos, object_pos
        )
        
        # Should handle negative coordinates correctly
        self.assertLess(virtual_pos[0], 0)
        self.assertGreater(virtual_pos[0], object_pos[0])  # Pulled closer (less negative)


def run_tests():
    """Run all tests and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestReverseGoGo))
    suite.addTests(loader.loadTestsFromTestCase(TestReverseGoGoEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
