import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import {
  FileText,
  Briefcase,
  Target,
  Gauge,
  ArrowUpRight,
  Plus,
  Sparkles,
  Zap,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
} from 'lucide-react';
import api from '../services/api';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { ScoreTrendChart } from '../components/charts/ScoreTrendChart';
import { SkillDistributionChart } from '../components/charts/SkillDistributionChart';
import { MissingSkillsChart } from '../components/charts/MissingSkillsChart';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const DashboardPage = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      const res = await api.get('/analytics/dashboard');
      setStats(res.data);
    } catch (err) {
      console.error('Failed to load dashboard metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  if (loading) {
    return <LoadingSpinner message="Aggregating ML Metrics & Performance Analytics..." />;
  }

  const kpis = [
    {
      title: 'Total Resumes Analyzed',
      value: stats?.total_resumes || 0,
      icon: FileText,
      color: 'text-teal-400',
      bg: 'bg-teal-950/40 border-teal-500/30',
      link: '/resume',
    },
    {
      title: 'Job Descriptions',
      value: stats?.total_jobs || 0,
      icon: Briefcase,
      color: 'text-cyan-400',
      bg: 'bg-cyan-950/40 border-cyan-500/30',
      link: '/job-description',
    },
    {
      title: 'Average Match Score',
      value: `${stats?.avg_match_score || 0}%`,
      icon: Target,
      color: 'text-emerald-400',
      bg: 'bg-emerald-950/40 border-emerald-500/30',
      link: '/analysis',
    },
    {
      title: 'Average ATS Score',
      value: `${stats?.avg_ats_score || 0}%`,
      icon: Gauge,
      color: 'text-indigo-400',
      bg: 'bg-indigo-950/40 border-indigo-500/30',
      link: '/analysis',
    },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Banner */}
      <div className="glass-card rounded-3xl p-6 lg:p-8 relative overflow-hidden border border-teal-500/20 glass-glow">
        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2 max-w-2xl">
            <Badge variant="primary" size="md">
              <Sparkles className="w-3.5 h-3.5" />
              <span>AI Matching Engine Ready</span>
            </Badge>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Candidate Analytics & Intelligence Dashboard
            </h1>
            <p className="text-sm text-slate-400 leading-relaxed">
              Upload candidate PDF resumes, paste job openings, and leverage TF-IDF vector similarity and multi-factor ATS audits to accelerate hiring matches.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 shrink-0">
            <NavLink to="/resume">
              <Button icon={Plus} size="md">
                Upload Resume
              </Button>
            </NavLink>
            <NavLink to="/job-description">
              <Button variant="secondary" icon={Briefcase} size="md">
                Add Job
              </Button>
            </NavLink>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {kpis.map((kpi, i) => {
          const Icon = kpi.icon;
          return (
            <Card key={i} className="hover:border-slate-700 transition-all group">
              <div className="flex items-center justify-between">
                <div className={`p-3 rounded-xl border ${kpi.bg}`}>
                  <Icon className={`w-6 h-6 ${kpi.color}`} />
                </div>
                <NavLink
                  to={kpi.link}
                  className="p-1.5 rounded-lg text-slate-500 hover:text-white hover:bg-slate-800 transition-colors"
                >
                  <ArrowUpRight className="w-4 h-4" />
                </NavLink>
              </div>
              <div className="mt-4">
                <p className="text-xs text-slate-400 font-medium">{kpi.title}</p>
                <h3 className="text-2xl font-black text-white mt-1 tracking-tight">{kpi.value}</h3>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Visual Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card
          title="Match & ATS Score Trends"
          subtitle="Chronological performance across analyzed job postings"
        >
          <ScoreTrendChart data={stats?.score_trends || []} />
        </Card>

        <Card
          title="Skill Distribution by Category"
          subtitle="Identified technical competencies in candidate profile"
        >
          <SkillDistributionChart data={stats?.skill_category_distribution || []} />
        </Card>
      </div>

      {/* Bottom Grid: Recent Analyses & Missing Skills Frequency */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Match Analyses Table (2 cols) */}
        <div className="lg:col-span-2">
          <Card
            title="Recent Match Analyses"
            subtitle="Latest match evaluations and ATS ratings"
            action={
              <NavLink to="/history" className="text-xs text-teal-400 hover:text-teal-300 font-semibold">
                View All →
              </NavLink>
            }
          >
            {stats?.recent_analyses && stats.recent_analyses.length > 0 ? (
              <div className="overflow-x-auto -mx-6">
                <table className="w-full text-left text-xs text-slate-300">
                  <thead className="text-[11px] uppercase tracking-wider text-slate-500 bg-slate-900/50 border-y border-slate-800">
                    <tr>
                      <th className="py-3 px-6 font-semibold">Target Position</th>
                      <th className="py-3 px-6 font-semibold">Match Score</th>
                      <th className="py-3 px-6 font-semibold">ATS Score</th>
                      <th className="py-3 px-6 font-semibold">Skill Overlap</th>
                      <th className="py-3 px-6 font-semibold text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60">
                    {stats.recent_analyses.map((item) => (
                      <tr key={item.id} className="hover:bg-slate-800/40 transition-colors">
                        <td className="py-3.5 px-6 font-medium text-white">
                          <div>{item.job_title}</div>
                          <div className="text-[10px] text-slate-500">{item.company}</div>
                        </td>
                        <td className="py-3.5 px-6 font-semibold">
                          <span
                            className={
                              item.overall_match_score >= 75
                                ? 'text-emerald-400'
                                : item.overall_match_score >= 50
                                ? 'text-amber-400'
                                : 'text-rose-400'
                            }
                          >
                            {Math.round(item.overall_match_score)}%
                          </span>
                        </td>
                        <td className="py-3.5 px-6 font-semibold text-indigo-400">
                          {Math.round(item.ats_score)}%
                        </td>
                        <td className="py-3.5 px-6">
                          <span className="text-teal-400">{item.matching_skills_count} Matched</span>
                          {item.missing_skills_count > 0 && (
                            <span className="text-rose-400 ml-1.5">/ {item.missing_skills_count} Gap</span>
                          )}
                        </td>
                        <td className="py-3.5 px-6 text-right">
                          <NavLink
                            to={`/analysis?id=${item.id}`}
                            className="inline-flex items-center gap-1 text-xs text-teal-400 hover:text-teal-300 font-semibold"
                          >
                            <span>Report</span>
                            <ArrowUpRight className="w-3.5 h-3.5" />
                          </NavLink>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-10 text-slate-500 text-xs">
                No analyses completed yet. Click 'Upload Resume' and 'Add Job' to begin!
              </div>
            )}
          </Card>
        </div>

        {/* Top Missing Skills Radar (1 col) */}
        <div>
          <Card
            title="Frequent Skill Gaps"
            subtitle="Most common requirements missing in candidate profiles"
          >
            <MissingSkillsChart data={stats?.top_missing_skills || []} />
          </Card>
        </div>
      </div>
    </div>
  );
};
