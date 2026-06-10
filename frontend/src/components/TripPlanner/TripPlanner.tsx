import React, { useState } from 'react';
import { Navigation, MapPin, Battery, ChevronRight } from 'lucide-react';
import ElevationProfile from './ElevationProfile';

const TripPlanner = () => {
  const [step, setStep] = useState(1);
  const mockElevationData = [
    { distance_km: 0, elevation_m: 1300 },
    { distance_km: 2, elevation_m: 1350 },
    { distance_km: 5, elevation_m: 1280 },
    { distance_km: 8, elevation_m: 1400 },
    { distance_km: 10, elevation_m: 1320 },
  ];

  return (
    <div className="absolute top-0 left-0 w-full h-full bg-gray-50 z-20 overflow-y-auto">
      <header className="bg-white p-4 border-b flex items-center gap-4">
        <button onClick={() => window.history.back()}><ChevronRight className="rotate-180" /></button>
        <h1 className="font-bold text-lg">Plan Your Trip</h1>
      </header>

      <main className="p-4 space-y-6">
        <div className="bg-white p-4 rounded-2xl shadow-sm space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 bg-gray-400 rounded-full" />
            <input type="text" placeholder="Your Location" className="flex-1 outline-none text-sm" />
          </div>
          <div className="border-t" />
          <div className="flex items-center gap-3">
            <MapPin className="text-primary w-4 h-4" />
            <input type="text" placeholder="Where to?" className="flex-1 outline-none text-sm" />
          </div>
        </div>

        <div className="space-y-3">
          <h3 className="text-sm font-bold text-gray-500 uppercase">Route Options</h3>
          <div className="bg-white p-4 rounded-2xl border-2 border-primary shadow-sm">
            <div className="flex justify-between items-center mb-2">
              <span className="bg-green-100 text-green-700 px-2 py-1 rounded text-[10px] font-bold uppercase">Best Range</span>
              <span className="font-bold text-primary">42% Arrival SOC</span>
            </div>
            <div className="flex justify-between items-end">
              <div>
                <p className="text-lg font-bold">18.4 km</p>
                <p className="text-xs text-gray-400">32 mins • Rs. 48 energy cost</p>
              </div>
              <Battery className="text-green-500" />
            </div>
          </div>
        </div>

        <ElevationProfile data={mockElevationData} />

        <button className="w-full bg-primary text-white font-bold py-4 rounded-2xl flex items-center justify-center gap-2 shadow-lg">
          <Navigation className="w-5 h-5" />
          Start Navigation
        </button>
      </main>
    </div>
  );
};

export default TripPlanner;
