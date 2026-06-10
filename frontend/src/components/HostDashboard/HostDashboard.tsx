import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { DollarSign, Zap, Calendar, TrendingUp } from 'lucide-react';

const HostDashboard = () => {
  const data = [
    { day: 'Mon', revenue: 450 },
    { day: 'Tue', revenue: 300 },
    { day: 'Wed', revenue: 600 },
    { day: 'Thu', revenue: 800 },
    { day: 'Fri', revenue: 500 },
    { day: 'Sat', revenue: 1200 },
    { day: 'Sun', revenue: 900 },
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-20 p-4">
      <header className="mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Host Dashboard</h1>
        <p className="text-gray-500 text-sm">Managing: Himalayan Hotel Bay 1</p>
      </header>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-white p-4 rounded-2xl shadow-sm border">
          <DollarSign className="text-amber-500 w-5 h-5 mb-2" />
          <p className="text-xs text-gray-400">Total Earnings</p>
          <p className="text-xl font-bold">Rs. 12,450</p>
        </div>
        <div className="bg-white p-4 rounded-2xl shadow-sm border">
          <Zap className="text-primary w-5 h-5 mb-2" />
          <p className="text-xs text-gray-400">Total Sessions</p>
          <p className="text-xl font-bold">42</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-2xl shadow-sm border mb-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-bold text-gray-700 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-primary" /> Revenue (Last 7 Days)
          </h3>
        </div>
        <div className="h-48 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
              <XAxis dataKey="day" axisLine={false} tickLine={false} tick={{ fontSize: 10 }} />
              <YAxis hide />
              <Tooltip cursor={{ fill: '#f8f8f8' }} contentStyle={{ borderRadius: '8px', border: 'none' }} />
              <Bar dataKey="revenue" fill="#0F6E56" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white p-4 rounded-2xl shadow-sm border">
        <h3 className="font-bold text-gray-700 mb-4 flex items-center gap-2">
          <Calendar className="w-4 h-4 text-primary" /> Upcoming Sessions
        </h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl">
            <div>
              <p className="font-bold text-sm">Prasanna K.</p>
              <p className="text-[10px] text-gray-400">Today, 2:00 PM - 4:00 PM</p>
            </div>
            <span className="bg-blue-100 text-blue-700 text-[10px] font-bold px-2 py-1 rounded">CONFIRMED</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HostDashboard;
