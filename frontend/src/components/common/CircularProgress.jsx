import React from 'react';

export const CircularProgress = ({
  value = 0,
  size = 140,
  strokeWidth = 10,
  label = 'Score',
  subtitle = '',
  color = 'teal',
}) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (Math.min(Math.max(value, 0), 100) / 100) * circumference;

  const colorGradients = {
    teal: {
      from: '#14b8a6',
      to: '#10b981',
      bg: 'rgba(20, 184, 166, 0.1)',
      text: 'text-teal-400',
    },
    emerald: {
      from: '#10b981',
      to: '#059669',
      bg: 'rgba(16, 185, 129, 0.1)',
      text: 'text-emerald-400',
    },
    amber: {
      from: '#f59e0b',
      to: '#d97706',
      bg: 'rgba(245, 158, 11, 0.1)',
      text: 'text-amber-400',
    },
    rose: {
      from: '#f43f5e',
      to: '#e11d48',
      bg: 'rgba(244, 63, 94, 0.1)',
      text: 'text-rose-400',
    },
    indigo: {
      from: '#6366f1',
      to: '#4f46e5',
      bg: 'rgba(99, 102, 241, 0.1)',
      text: 'text-indigo-400',
    },
  };

  const selectedColor = colorGradients[color] || colorGradients.teal;
  const gradId = `circle-grad-${Math.random().toString(36).substring(2, 8)}`;

  return (
    <div className="relative inline-flex flex-col items-center justify-center">
      <svg width={size} height={size} className="transform -rotate-90">
        <defs>
          <linearGradient id={gradId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor={selectedColor.from} />
            <stop offset="100%" stopColor={selectedColor.to} />
          </linearGradient>
        </defs>
        {/* Track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#1E293B"
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        {/* Progress Arc */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={`url(#${gradId})`}
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      {/* Centered Value */}
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="text-3xl font-extrabold tracking-tight text-white">
          {Math.round(value)}%
        </span>
        {label && <span className="text-[10px] uppercase font-semibold tracking-wider text-slate-400 mt-0.5">{label}</span>}
      </div>
      {subtitle && <p className="text-xs text-slate-400 mt-2 font-medium">{subtitle}</p>}
    </div>
  );
};
