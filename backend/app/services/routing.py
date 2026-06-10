import httpx
import os
from app.services.ev_range import calculate_segment_energy, calculate_arrival_soc

VALHALLA_URL = os.getenv("VALHALLA_URL", "http://valhalla:8002")

async def get_route(origin, destination, vehicle_profile, current_soc_pct):
    async with httpx.AsyncClient() as client:
        # 1. Fetch route from Valhalla
        route_payload = {
            "locations": [
                {"lat": origin["lat"], "lon": origin["lon"]},
                {"lat": destination["lat"], "lon": destination["lon"]}
            ],
            "costing": "auto",
            "shape_format": "geojson",
            "filters": {
                "attributes": ["shape_attributes.speed", "edge.length", "edge.way_id"],
                "action": "include"
            }
        }

        # Simulation: in a real environment, we'd call Valhalla
        # res = await client.post(f"{VALHALLA_URL}/route", json=route_payload)
        # data = res.json()

        # Mocking Valhalla response for demonstration
        data = {
            "trip": {
                "summary": {"length": 10.5, "time": 1200},
                "legs": [{
                    "shape": "encoded_polyline",
                    "maneuvers": []
                }]
            }
        }

        # 2. Get elevation profile
        # height_payload = {"shape": data["trip"]["legs"][0]["shape"], "range": True}
        # h_res = await client.post(f"{VALHALLA_URL}/height", json=height_payload)

        # 3. Calculate energy for each segment (simulated)
        # For now, we return a mock response matching the specification
        return {
            "route_id": "mock-uuid",
            "summary": {
                "distance_km": 10.5,
                "duration_min": 20,
                "arrival_soc_pct": current_soc_pct - 15,
                "range_status": "comfortable"
            },
            "geometry": {"type": "LineString", "coordinates": []}
        }
