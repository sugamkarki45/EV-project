import React from 'react';
import { ShieldCheck, ShieldAlert, MoreVertical } from 'lucide-react';

const UserManagement = () => {
  const users = [
    { id: 1, name: 'Prasanna K.', phone: '+977-9841234567', tier: 2, kyc: 'verified', role: 'Driver' },
    { id: 2, name: 'Sita R.', phone: '+977-9800001111', tier: 1, kyc: 'pending', role: 'Host' },
  ];

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">User Management</h1>
      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="p-4 font-bold text-sm text-gray-500 uppercase">User</th>
              <th className="p-4 font-bold text-sm text-gray-500 uppercase">Role</th>
              <th className="p-4 font-bold text-sm text-gray-500 uppercase">KYC</th>
              <th className="p-4 font-bold text-sm text-gray-500 uppercase">Tier</th>
              <th className="p-4"></th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id} className="border-b last:border-0 hover:bg-gray-50 transition-colors">
                <td className="p-4">
                  <p className="font-bold">{user.name}</p>
                  <p className="text-xs text-gray-400">{user.phone}</p>
                </td>
                <td className="p-4"><span className="text-sm">{user.role}</span></td>
                <td className="p-4">
                  {user.kyc === 'verified' ? (
                    <span className="flex items-center gap-1 text-green-600 text-xs font-bold"><ShieldCheck className="w-3 h-3" /> Verified</span>
                  ) : (
                    <span className="flex items-center gap-1 text-amber-600 text-xs font-bold"><ShieldAlert className="w-3 h-3" /> Pending</span>
                  )}
                </td>
                <td className="p-4"><span className="bg-gray-100 px-2 py-1 rounded text-xs font-bold">Tier {user.tier}</span></td>
                <td className="p-4 text-right"><MoreVertical className="w-4 h-4 text-gray-400 cursor-pointer inline" /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default UserManagement;
