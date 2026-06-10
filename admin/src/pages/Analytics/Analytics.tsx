import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Users, Zap, TrendingUp, Activity } from 'lucide-react';

const AdminAnalytics = () => {
  const revenueData = [
    { name: 'Week 1', rev: 45000 },
    { name: 'Week 2', rev: 52000 },
    { name: 'Week 3', rev: 48000 },
    { name: 'Week 4', rev: 61000 },
  ];

  const typeData = [
    { name: 'Home', value: 400 },
    { name: 'Hotel', value: 300 },
    { name: 'Airbnb', value: 200 },
  ];
  const COLORS = ['#3B82F6', '#8B5CF6', '#EC4899'];

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Platform Analytics</h1>

      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-2xl shadow-sm border">
          <Users className="text-blue-500 mb-2" />
          <p className="text-xs text-gray-400 uppercase font-bold">Total Users</p>
          <p className="text-2xl font-bold">2,450</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border">
          <Zap className="text-primary mb-2" />
          <p className="text-xs text-gray-400 uppercase font-bold">Active Sessions</p>
          <p className="text-2xl font-bold">124</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border">
          <TrendingUp className="text-amber-500 mb-2" />
          <p className="text-xs text-gray-400 uppercase font-bold">Monthly GMV</p>
          <p className="text-2xl font-bold">Rs. 4.2M</p>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border">
          <Activity className="text-green-500 mb-2" />
          <p className="text-xs text-gray-400 uppercase font-bold">Guarantee Fund</p>
          <p className="text-2xl font-bold">Rs. 85k</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2 bg-white p-6 rounded-2xl shadow-sm border h-80">
          <h3 className="font-bold text-gray-700 mb-6 uppercase text-xs">Revenue Growth</h3>
          <ResponsiveContainer width="100%" height="80%">
            <LineChart data={revenueData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" axisLine={false} tickLine={false} />
              <YAxis axisLine={false} tickLine={false} />
              <Tooltip />
              <Line type="monotone" dataKey="rev" stroke="#0F6E56" strokeWidth={3} dot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white p-6 rounded-2xl shadow-sm border h-80">
          <h3 className="font-bold text-gray-700 mb-6 uppercase text-xs">Charger Type Mix</h3>
          <ResponsiveContainer width="100%" height="80%">
            <PieChart>
              <Pie data={typeData} innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                {typeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AdminAnalytics;
