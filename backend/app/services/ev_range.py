import math

def calculate_segment_energy(
    distance_m,
    elevation_change_m,
    avg_speed_kmh,
    vehicle_mass_kg,
    drag_coefficient,
    frontal_area_m2,
    regen_efficiency=0.65,
    rolling_resistance_coeff=0.015,
    air_density=1.05, # Kathmandu altitude
    gravity=9.81,
    drivetrain_efficiency=0.90
):
    v = avg_speed_kmh / 3.6
    d = distance_m
    m = vehicle_mass_kg
    g = gravity
    rho = air_density
    Cd = drag_coefficient
    A = frontal_area_m2

    # E_rolling = Crr * m * g * d
    e_rolling = rolling_resistance_coeff * m * g * d

    # E_aero = 0.5 * rho * Cd * A * v^2 * d
    e_aero = 0.5 * rho * Cd * A * (v**2) * d

    # E_grade = m * g * delta_h
    e_grade = m * g * elevation_change_m

    # Simple model for regen
    regen_wh = 0
    if e_grade < 0:
        regen_wh = abs(e_grade) * regen_efficiency
        e_grade = 0 # grade energy already accounted in regen

    total_joules = (e_rolling + e_aero + e_grade) / drivetrain_efficiency
    total_wh = total_joules / 3600
    regen_wh = regen_wh / 3600

    return {
        "energy_wh": total_wh,
        "regen_wh": regen_wh,
        "net_energy_wh": total_wh - regen_wh
    }

def calculate_arrival_soc(
    battery_capacity_kwh,
    degradation_pct,
    current_soc_pct,
    min_reserve_soc_pct,
    total_trip_energy_wh,
    auxiliary_load_w,
    trip_duration_hours
):
    effective_capacity_wh = battery_capacity_kwh * 1000 * (1 - degradation_pct / 100)
    available_energy_wh = effective_capacity_wh * (current_soc_pct / 100)

    aux_energy_wh = auxiliary_load_w * trip_duration_hours
    total_cost_wh = total_trip_energy_wh + aux_energy_wh

    remaining_energy_wh = available_energy_wh - total_cost_wh
    arrival_soc_pct = (remaining_energy_wh / effective_capacity_wh) * 100

    status = "comfortable"
    if arrival_soc_pct < min_reserve_soc_pct:
        status = "range_risk"
    elif arrival_soc_pct < min_reserve_soc_pct + 10:
        status = "caution"

    return {
        "arrival_soc_pct": arrival_soc_pct,
        "range_status": status,
        "estimated_energy_kwh": total_cost_wh / 1000
    }
