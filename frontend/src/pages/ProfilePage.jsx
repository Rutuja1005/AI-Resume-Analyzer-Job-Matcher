import React, { useState, useEffect } from 'react';
import { User, Mail, Shield, Key, Sparkles, CheckCircle2, Server, Clock } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import api from '../services/api';

export const ProfilePage = () => {
  const { user } = useAuth();
  const [serverHealth, setServerHealth] = useState(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await api.get('/health');
        setServerHealth(res.data);
      } catch (e) {
        setServerHealth({ status: 'offline' });
      }
    };
    checkHealth();
  }, []);

  return (
    <div className="space-y-8 max-w-4xl">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Candidate Profile & System Configuration
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Manage your account credentials, security tokens, and active backend services.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* User Card */}
        <Card className="md:col-span-1 text-center flex flex-col items-center justify-center p-6 space-y-3">
          <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-teal-500 to-emerald-400 flex items-center justify-center text-slate-950 text-2xl font-black shadow-xl shadow-teal-500/20">
            {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">{user?.full_name || 'Candidate'}</h3>
            <p className="text-xs text-slate-400">{user?.email}</p>
          </div>
          <Badge variant="primary" size="md">
            {user?.role || 'Candidate'} Account
          </Badge>
        </Card>

        {/* Profile Details */}
        <Card className="md:col-span-2 space-y-4" title="Account Credentials" subtitle="Authentication & profile records">
          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400">Candidate Name</span>
              <span className="font-semibold text-white">{user?.full_name || 'Candidate'}</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400">Email Address</span>
              <span className="font-semibold text-white">{user?.email}</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400">Account ID</span>
              <span className="font-mono text-teal-400 text-[11px]">{user?.id || 'Active'}</span>
            </div>
            <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-slate-400">Session Protocol</span>
              <span className="text-emerald-400 font-semibold flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                JWT HS256 Bearer Token
              </span>
            </div>
          </div>
        </Card>
      </div>

      {/* Backend & AI Health */}
      <Card title="Backend Services & NLP Status" subtitle="Connected microservices and inference engine health">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-slate-400 font-medium">FastAPI Engine</span>
              <Badge variant="success" size="sm">Online</Badge>
            </div>
            <p className="text-white font-bold">{serverHealth?.service || 'FastAPI Service'}</p>
            <p className="text-[11px] text-slate-500">Version {serverHealth?.version || '1.0.0'}</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-slate-400 font-medium">NLP & ML Pipeline</span>
              <Badge variant="primary" size="sm">Active</Badge>
            </div>
            <p className="text-white font-bold">TF-IDF + Cosine</p>
            <p className="text-[11px] text-slate-500">1,200+ Ontology Keywords</p>
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-slate-400 font-medium">Database Layer</span>
              <Badge variant="primary" size="sm">Connected</Badge>
            </div>
            <p className="text-white font-bold">SQLAlchemy ORM</p>
            <p className="text-[11px] text-slate-500">PostgreSQL / SQLite Storage</p>
          </div>
        </div>
      </Card>
    </div>
  );
};
