import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MapPin, Zap, User, LogIn, Calendar, Clock } from 'lucide-react';

const API_URL = 'http://localhost:8000/api/v1';

const App = () => {
  const [view, setView] = useState('login');
  const [user, setUser] = useState(null);
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [listings, setListings] = useState([]);
  const [selectedListing, setSelectedListing] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchUser(token);
    }
  }, []);

  const fetchUser = async (token) => {
    // In real app, fetch profile. For demo, we just assume token is valid if present.
    setView('home');
    fetchListings(token);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/auth/verify-otp/`, { phone, otp });
      localStorage.setItem('token', res.data.access);
      setUser(res.data.user);
      setView('home');
      fetchListings(res.data.access);
    } catch (err) {
      alert('Login failed. Try any 6-digit OTP.');
    } finally {
      setLoading(false);
    }
  };

  const fetchListings = async (token) => {
    try {
      const res = await axios.get(`${API_URL}/listings/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setListings(res.data);
    } catch (err) {
      console.error('Failed to fetch listings');
    }
  };

  const handleBook = async (listing) => {
    setSelectedListing(listing);
    setView('booking');
  };

  if (view === 'login') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8">
          <div className="flex justify-center mb-6">
            <div className="bg-primary p-3 rounded-full">
              <Zap className="text-white w-8 h-8" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-center text-gray-800 mb-2">EV Charger Sharing</h1>
          <p className="text-center text-gray-500 mb-8">Nepal's P2P Charging Network</p>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Mobile Number</label>
              <input
                type="text"
                placeholder="9841XXXXXX"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">OTP (Demo: 123456)</label>
              <input
                type="text"
                placeholder="XXXXXX"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
              />
            </div>
            <button
              type="submit"
              className="w-full bg-primary text-white font-bold py-3 rounded-lg hover:bg-opacity-90 transition-all flex items-center justify-center gap-2"
              disabled={loading}
            >
              <LogIn className="w-5 h-5" />
              {loading ? 'Logging in...' : 'Sign In'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  if (view === 'home') {
    return (
      <div className="min-h-screen bg-gray-50 pb-20">
        <header className="bg-white border-b px-4 py-4 sticky top-0 z-10 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Zap className="text-primary w-6 h-6" />
            <span className="font-bold text-xl">EV Nepal</span>
          </div>
          <User className="text-gray-600 w-6 h-6" />
        </header>

        <main className="p-4 max-w-lg mx-auto">
          <div className="mb-6">
            <h2 className="text-lg font-bold mb-4">Nearby Chargers</h2>
            <div className="space-y-4">
              {listings.length === 0 ? (
                <div className="text-center py-10 bg-white rounded-xl border border-dashed border-gray-300">
                  <MapPin className="w-8 h-8 text-gray-300 mx-auto mb-2" />
                  <p className="text-gray-500">No active chargers nearby</p>
                  <p className="text-xs text-gray-400 mt-1">(Run migrations and add listings via admin)</p>
                </div>
              ) : (
                listings.map(listing => (
                  <div key={listing.id} className="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div className="h-32 bg-gray-200 flex items-center justify-center">
                      <Zap className="text-gray-400 w-12 h-12" />
                    </div>
                    <div className="p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-bold text-gray-800">{listing.title}</h3>
                        <span className="text-primary font-bold text-sm">Rs. {listing.price_per_hour}/hr</span>
                      </div>
                      <div className="flex items-center gap-1 text-gray-500 text-sm mb-4">
                        <MapPin className="w-4 h-4" />
                        <span>{listing.address_display}</span>
                      </div>
                      <button
                        onClick={() => handleBook(listing)}
                        className="w-full bg-primary text-white py-2 rounded-lg text-sm font-bold"
                      >
                        Book Now
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </main>

        <nav className="fixed bottom-0 left-0 right-0 bg-white border-t flex justify-around py-3">
          <button className="flex flex-col items-center gap-1 text-primary">
            <MapPin className="w-6 h-6" />
            <span className="text-[10px]">Explore</span>
          </button>
          <button className="flex flex-col items-center gap-1 text-gray-400">
            <Calendar className="w-6 h-6" />
            <span className="text-[10px]">Bookings</span>
          </button>
          <button className="flex flex-col items-center gap-1 text-gray-400">
            <User className="w-6 h-6" />
            <span className="text-[10px]">Profile</span>
          </button>
        </nav>
      </div>
    );
  }

  if (view === 'booking') {
    return (
      <div className="min-h-screen bg-white">
        <header className="px-4 py-4 border-b flex items-center gap-4">
          <button onClick={() => setView('home')} className="text-gray-600">Back</button>
          <h1 className="font-bold text-lg">Book Charging</h1>
        </header>

        <main className="p-4 max-w-lg mx-auto">
          <div className="mb-8">
            <h2 className="font-bold text-xl mb-1">{selectedListing?.title}</h2>
            <p className="text-gray-500 flex items-center gap-1 text-sm">
              <MapPin className="w-4 h-4" /> {selectedListing?.address_display}
            </p>
          </div>

          <div className="space-y-6">
            <div>
              <h3 className="font-bold text-sm text-gray-700 mb-3 flex items-center gap-2">
                <Calendar className="w-4 h-4" /> Select Date
              </h3>
              <div className="flex gap-2 overflow-x-auto pb-2">
                {[...Array(5)].map((_, i) => (
                  <button key={i} className={`flex-shrink-0 w-16 h-20 rounded-xl flex flex-col items-center justify-center border ${i === 0 ? 'bg-primary text-white border-primary' : 'bg-gray-50 text-gray-600'}`}>
                    <span className="text-xs uppercase">Jun</span>
                    <span className="text-lg font-bold">{9 + i}</span>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <h3 className="font-bold text-sm text-gray-700 mb-3 flex items-center gap-2">
                <Clock className="w-4 h-4" /> Select Time
              </h3>
              <div className="grid grid-cols-3 gap-2">
                {['09:00', '10:00', '11:00', '12:00', '13:00', '14:00'].map(time => (
                  <button key={time} className="py-2 border rounded-lg text-sm text-gray-600 hover:border-primary hover:text-primary">
                    {time}
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-gray-50 rounded-xl p-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Rate (1 hour)</span>
                <span>Rs. {selectedListing?.price_per_hour}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Service Fee (10%)</span>
                <span>Rs. {selectedListing?.price_per_hour * 0.1}</span>
              </div>
              <div className="flex justify-between font-bold pt-2 border-t text-lg">
                <span>Total</span>
                <span className="text-primary">Rs. {selectedListing?.price_per_hour * 1.1}</span>
              </div>
            </div>
          </div>
        </main>

        <div className="fixed bottom-0 left-0 right-0 p-4 bg-white border-t">
          <button
            onClick={() => {
              alert('Booking successful! Redirecting to home...');
              setView('home');
            }}
            className="w-full bg-primary text-white font-bold py-4 rounded-xl shadow-lg"
          >
            Confirm Booking
          </button>
        </div>
      </div>
    );
  }

  return null;
};

export default App;
