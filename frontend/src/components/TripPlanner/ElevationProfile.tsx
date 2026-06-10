import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface ElevationProfileProps {
  data: { distance_km: number; elevation_m: number }[];
}

const ElevationProfile: React.FC<ElevationProfileProps> = ({ data }) => {
  return (
    <div className="h-48 w-full bg-white p-2 rounded-xl border">
      <h4 className="text-xs font-bold text-gray-500 mb-2 uppercase">Elevation Profile</h4>
      <ResponsiveContainer width="100%" height="80%">
        <AreaChart data={data}>
          <defs>
            <linearGradient id="colorElev" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#0F6E56" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#0F6E56" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#eee" />
          <XAxis dataKey="distance_km" hide />
          <YAxis hide domain={['dataMin - 100', 'dataMax + 100']} />
          <Tooltip
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
            labelFormatter={(val) => `${val} km`}
          />
          <Area
            type="monotone"
            dataKey="elevation_m"
            stroke="#0F6E56"
            fillOpacity={1}
            fill="url(#colorElev)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ElevationProfile;
