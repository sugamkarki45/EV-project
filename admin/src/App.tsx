import React from 'react';
import UserManagement from './pages/UserManagement/UserManagement';
import ChargerApprovals from './pages/ChargerApprovals/ChargerApprovals';
import Disputes from './pages/Disputes/Disputes';
import AdminAnalytics from './pages/Analytics/Analytics';
import { LayoutDashboard, Users, Zap, AlertTriangle, PieChart } from 'lucide-react';

const App = () => {
  const [activeTab, setActiveTab] = React.useState('dashboard');

  return (
    <div className="flex min-h-screen bg-gray-50">
      <aside className="w-64 bg-[#1A1A18] text-white p-6 shrink-0">
        <h1 className="text-xl font-bold mb-8 flex items-center gap-2">
          <Zap className="text-primary fill-current" /> Admin Panel
        </h1>
        <nav className="space-y-2">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`w-full flex items-center gap-3 p-3 rounded-lg text-sm font-bold transition-colors ${activeTab === 'dashboard' ? 'bg-primary text-white' : 'text-gray-400 hover:text-white'}`}
          >
            <LayoutDashboard className="w-4 h-4" /> Dashboard
          </button>
          <button
            onClick={() => setActiveTab('users')}
            className={`w-full flex items-center gap-3 p-3 rounded-lg text-sm font-bold transition-colors ${activeTab === 'users' ? 'bg-primary text-white' : 'text-gray-400 hover:text-white'}`}
          >
            <Users className="w-4 h-4" /> Users
          </button>
          <button
            onClick={() => setActiveTab('approvals')}
            className={`w-full flex items-center gap-3 p-3 rounded-lg text-sm font-bold transition-colors ${activeTab === 'approvals' ? 'bg-primary text-white' : 'text-gray-400 hover:text-white'}`}
          >
            <Zap className="w-4 h-4" /> Approvals
          </button>
          <button
            onClick={() => setActiveTab('disputes')}
            className={`w-full flex items-center gap-3 p-3 rounded-lg text-sm font-bold transition-colors ${activeTab === 'disputes' ? 'bg-primary text-white' : 'text-gray-400 hover:text-white'}`}
          >
            <AlertTriangle className="w-4 h-4" /> Disputes
          </button>
        </nav>
      </aside>

      <main className="flex-1 overflow-y-auto">
        {activeTab === 'dashboard' && <AdminAnalytics />}
        {activeTab === 'users' && <UserManagement />}
        {activeTab === 'approvals' && <ChargerApprovals />}
        {activeTab === 'disputes' && <Disputes />}
      </main>
    </div>
  );
};

export default App;
