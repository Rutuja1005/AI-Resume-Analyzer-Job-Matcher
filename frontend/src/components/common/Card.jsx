import React from 'react';

export const Card = ({ children, className = '', glow = false, title, subtitle, action }) => {
  return (
    <div
      className={`glass-card rounded-2xl p-6 transition-all duration-300 ${
        glow ? 'glass-glow border-teal-500/30' : 'hover:border-slate-700'
      } ${className}`}
    >
      {(title || action) && (
        <div className="flex items-center justify-between mb-5 pb-3 border-b border-slate-800">
          <div>
            {title && <h3 className="text-lg font-semibold text-white tracking-tight">{title}</h3>}
            {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      {children}
    </div>
  );
};
