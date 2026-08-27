import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
} from 'recharts';

export const SkillDistributionChart = ({ data = [] }) => {
  const COLORS = ['#14b8a6', '#06b6d4', '#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'];

  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-500 text-sm">
        No skill categories detected yet. Upload a resume to populate.
      </div>
    );
  }

  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 10, right: 20, left: 40, bottom: 0 }}
        >
          <XAxis type="number" stroke="#64748B" tickLine={false} fontSize={12} />
          <YAxis
            type="category"
            dataKey="category"
            stroke="#94A3B8"
            tickLine={false}
            fontSize={11}
            width={110}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#111827',
              borderColor: '#374151',
              borderRadius: '0.75rem',
              color: '#F8FAFC',
              fontSize: '12px',
            }}
          />
          <Bar dataKey="count" name="Identified Skills" radius={[0, 6, 6, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
