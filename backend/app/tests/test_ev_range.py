import unittest
from app.services.ev_range import calculate_segment_energy, calculate_arrival_soc

class TestEVRange(unittest.TestCase):
    def test_calculate_segment_energy(self):
        res = calculate_segment_energy(
            distance_m=1000,
            elevation_change_m=10,
            avg_speed_kmh=40,
            vehicle_mass_kg=1600,
            drag_coefficient=0.24,
            frontal_area_m2=2.2
        )
        self.assertIn("energy_wh", res)
        self.assertGreater(res["energy_wh"], 0)

    def test_calculate_arrival_soc(self):
        res = calculate_arrival_soc(
            battery_capacity_kwh=60,
            degradation_pct=5,
            current_soc_pct=80,
            min_reserve_soc_pct=10,
            total_trip_energy_wh=10000,
            auxiliary_load_w=500,
            trip_duration_hours=1
        )
        self.assertEqual(res["range_status"], "comfortable")
        self.assertLess(res["arrival_soc_pct"], 80)

if __name__ == "__main__":
    unittest.main()
