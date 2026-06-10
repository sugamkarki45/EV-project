import React, { useState } from 'react';
import MapView from './components/Map/MapView';
import ChargerDetail from './components/Charger/ChargerDetail';
import TripPlanner from './components/TripPlanner/TripPlanner';
import HostDashboard from './components/HostDashboard/HostDashboard';
import { Zap, Search, Calendar, User, Navigation } from 'lucide-react';

const App = () => {
  const [view, setView] = useState('explore'); // explore, trip-planner, host-dashboard
  const [selectedListing, setSelectedListing] = useState(null);

  const mockListing = {
    id: '1',
    title: 'Himalayan Hotel Bay 1',
    host_type: 'hotel_restaurant',
    price_per_hour: 250,
    address_display: 'Thamel, Kathmandu'
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col max-w-md mx-auto relative overflow-hidden shadow-2xl">
      {view === 'explore' && (
        <>
          <header className="bg-white p-4 border-b flex justify-between items-center shrink-0">
            <div className="flex items-center gap-2">
              <Zap className="text-primary fill-current" />
              <span className="font-bold text-xl">EV Nepal</span>
            </div>
            <User className="text-gray-400" />
          </header>

          <main className="flex-1 relative">
            <MapView onPinClick={() => setSelectedListing(mockListing)} />

            {selectedListing && (
              <div className="absolute bottom-0 left-0 right-0 z-10 animate-in slide-in-from-bottom duration-300">
                <ChargerDetail listing={selectedListing} onBook={() => alert('Booking flow initiated!')} />
              </div>
            )}

            <button
              onClick={() => setView('trip-planner')}
              className="absolute top-4 right-4 bg-white p-3 rounded-full shadow-lg text-primary z-10"
            >
              <Navigation className="w-6 h-6" />
            </button>
          </main>
        </>
      )}

      {view === 'trip-planner' && <TripPlanner />}
      {view === 'host-dashboard' && <HostDashboard />}

      <nav className="bg-white border-t p-4 flex justify-around shrink-0 z-30">
        <button onClick={() => {setView('explore'); setSelectedListing(null);}} className={`flex flex-col items-center ${view === 'explore' ? 'text-primary' : 'text-gray-400'}`}>
          <Search className="w-6 h-6" />
          <span className="text-[10px] mt-1 font-bold">Explore</span>
        </button>
        <button className="flex flex-col items-center text-gray-400">
          <Calendar className="w-6 h-6" />
          <span className="text-[10px] mt-1 font-bold">Bookings</span>
        </button>
        <button onClick={() => setView('host-dashboard')} className={`flex flex-col items-center ${view === 'host-dashboard' ? 'text-primary' : 'text-gray-400'}`}>
          <Zap className="w-6 h-6" />
          <span className="text-[10px] mt-1 font-bold">Host</span>
        </button>
      </nav>
    </div>
  );
};

export default App;
