import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';

export const ScoreTrendChart = ({ data = [] }) => {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-500 text-sm">
        No historical match analyses available yet.
      </div>
    );
  }

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="matchGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#14b8a6" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#14b8a6" stopOpacity={0.0} />
            </linearGradient>
            <linearGradient id="atsGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0.0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
          <XAxis dataKey="date" stroke="#64748B" tickLine={false} fontSize={12} />
          <YAxis domain={[0, 100]} stroke="#64748B" tickLine={false} fontSize={12} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#111827',
              borderColor: '#374151',
              borderRadius: '0.75rem',
              color: '#F8FAFC',
              fontSize: '12px',
            }}
          />
          <Area
            type="monotone"
            dataKey="match_score"
            name="Match Score"
            stroke="#14b8a6"
            strokeWidth={3}
            fillOpacity={1}
            fill="url(#matchGrad)"
          />
          <Area
            type="monotone"
            dataKey="ats_score"
            name="ATS Score"
            stroke="#6366f1"
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#atsGrad)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
