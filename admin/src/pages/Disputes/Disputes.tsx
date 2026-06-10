import React from 'react';
import { AlertCircle, MessageSquare, Scale } from 'lucide-react';

const Disputes = () => {
  const disputes = [
    { id: 'D-101', booking: 'B-882', raised_by: 'Prasanna K. (Driver)', reason: 'Charger not working', status: 'Open' },
  ];

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Dispute Resolution</h1>
      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        {disputes.map(d => (
          <div key={d.id} className="p-6 border-b last:border-0">
            <div className="flex justify-between items-start mb-4">
              <div className="flex items-center gap-3">
                <div className="bg-red-100 p-2 rounded-full"><AlertCircle className="text-red-600 w-5 h-5" /></div>
                <div>
                  <h3 className="font-bold">{d.reason}</h3>
                  <p className="text-xs text-gray-500">Dispute {d.id} • Booking {d.booking}</p>
                </div>
              </div>
              <span className="bg-amber-100 text-amber-700 px-3 py-1 rounded-full text-xs font-bold uppercase">{d.status}</span>
            </div>
            <p className="text-sm text-gray-600 mb-6">"The charger was listed as active but wouldn't release any power when I plugged in. The host wasn't home to help."</p>
            <div className="flex gap-4">
              <button className="flex items-center gap-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-bold"><MessageSquare className="w-4 h-4" /> Message Parties</button>
              <button className="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg text-sm font-bold"><Scale className="w-4 h-4" /> Arbitrate</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Disputes;
