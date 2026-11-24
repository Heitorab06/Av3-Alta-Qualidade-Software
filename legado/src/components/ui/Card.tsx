import React from 'react';

interface CardProps {
  title?: string;
  subtitle?: string;
  badge?: string;
  badgeColor?: 'emerald' | 'amber' | 'blue' | 'purple' | 'slate' | 'red';
  icon?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  title,
  subtitle,
  badge,
  badgeColor = 'slate',
  icon,
  children,
  className = ''
}) => {
  const badgeClasses = {
    emerald: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    amber: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    red: 'bg-red-500/10 text-red-400 border-red-500/20',
    slate: 'bg-slate-800 text-slate-300 border-slate-700'
  };

  return (
    <div className={`rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow-sm hover:border-slate-700/80 transition ${className}`}>
      {(title || subtitle || badge || icon) && (
        <div className="flex items-start justify-between gap-3 mb-4">
          <div className="flex items-center gap-3">
            {icon && (
              <div className="p-2 rounded-lg bg-slate-800/80 border border-slate-700/50 text-emerald-400">
                {icon}
              </div>
            )}
            <div>
              {title && <h3 className="text-sm font-semibold text-slate-100">{title}</h3>}
              {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
            </div>
          </div>
          {badge && (
            <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full border ${badgeClasses[badgeColor]}`}>
              {badge}
            </span>
          )}
        </div>
      )}
      <div>{children}</div>
    </div>
  );
};
