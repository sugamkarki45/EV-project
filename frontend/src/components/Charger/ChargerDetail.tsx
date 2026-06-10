import React from 'react';
import { Zap, MapPin, Star, ShieldCheck } from 'lucide-react';

interface ChargerDetailProps {
  listing: any;
  onBook: () => void;
}

const ChargerDetail: React.FC<ChargerDetailProps> = ({ listing, onBook }) => {
  return (
    <div className="bg-white rounded-t-3xl shadow-2xl p-6">
      <div className="flex justify-between items-start mb-4">
        <div>
          <span className="inline-block px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs font-bold mb-2">
            🏨 {listing.host_type.replace('_', ' ')}
          </span>
          <h2 className="text-2xl font-bold text-gray-800">{listing.title}</h2>
          <p className="text-gray-500 flex items-center gap-1">
            <MapPin className="w-4 h-4" /> {listing.address_display}
          </p>
        </div>
        <div className="text-right">
          <p className="text-2xl font-bold text-primary">Rs. {listing.price_per_hour}</p>
          <p className="text-xs text-gray-400">per hour</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gray-50 p-3 rounded-xl">
          <p className="text-xs text-gray-400 mb-1">Connector</p>
          <p className="font-bold flex items-center gap-1"><Zap className="w-4 h-4 text-amber-500" /> CCS2</p>
        </div>
        <div className="bg-gray-50 p-3 rounded-xl">
          <p className="text-xs text-gray-400 mb-1">Power</p>
          <p className="font-bold">50 kW</p>
        </div>
      </div>

      <button
        onClick={onBook}
        className="w-full bg-primary text-white font-bold py-4 rounded-2xl shadow-lg hover:bg-opacity-90 transition-all"
      >
        Book Now
      </button>
    </div>
  );
};

export default ChargerDetail;
