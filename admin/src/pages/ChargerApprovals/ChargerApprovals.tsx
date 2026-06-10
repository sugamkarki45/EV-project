import React from 'react';
import { Check, X, ExternalLink } from 'lucide-react';

const ChargerApprovals = () => {
  const listings = [
    { id: '1', title: 'Home Charger Baneshwor', host: 'Ram B.', type: 'Home', power: '7.4kW' },
    { id: '2', title: 'Hotel Annapurna Bay 2', host: 'Hotel A.', type: 'Hotel/Restaurant', power: '22kW' },
  ];

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Pending Approvals</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {listings.map(item => (
          <div key={item.id} className="bg-white p-6 rounded-2xl shadow-sm border">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="font-bold text-lg">{item.title}</h3>
                <p className="text-xs text-gray-500">Host: {item.host} • Type: {item.type}</p>
              </div>
              <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded text-[10px] font-bold uppercase">{item.power}</span>
            </div>

            <div className="bg-gray-50 p-4 rounded-xl mb-6 space-y-2">
              <p className="text-xs text-gray-400 font-bold uppercase">Checklist</p>
              <div className="flex items-center gap-2 text-xs text-green-600 font-bold">
                <Check className="w-3 h-3" /> Earth Grounding Confirmed
              </div>
              <div className="flex items-center gap-2 text-xs text-green-600 font-bold">
                <Check className="w-3 h-3" /> Circuit Breaker Rated
              </div>
            </div>

            <div className="flex gap-3">
              <button className="flex-1 bg-primary text-white py-2 rounded-lg font-bold text-sm flex items-center justify-center gap-2">
                <Check className="w-4 h-4" /> Approve
              </button>
              <button className="flex-1 border-2 border-red-500 text-red-500 py-2 rounded-lg font-bold text-sm flex items-center justify-center gap-2">
                <X className="w-4 h-4" /> Reject
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChargerApprovals;
