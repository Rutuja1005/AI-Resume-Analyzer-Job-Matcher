import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import {
  History,
  Search,
  ArrowUpRight,
  Download,
  FileText,
  Briefcase,
  CheckCircle2,
  AlertTriangle,
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const { showToast } = useToast();

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const res = await api.get('/analysis/history');
      setHistory(res.data || []);
    } catch (err) {
      console.error('Failed to load analysis history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleExport = async (id) => {
    try {
      const res = await api.get(`/analysis/${id}/export`, {
        responseType: 'blob',
      });
      const blob = new Blob([res.data], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Analysis_Report_${id.substring(0, 8)}.json`;
      a.click();
      window.URL.revokeObjectURL(url);
      showToast('Downloaded analysis JSON report.', 'success');
    } catch (err) {
      showToast('Failed to export analysis report.', 'error');
    }
  };

  const filteredHistory = history.filter(
    (item) =>
      item.job_title?.toLowerCase().includes(search.toLowerCase()) ||
      item.company?.toLowerCase().includes(search.toLowerCase()) ||
      item.candidate_name?.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return <LoadingSpinner message="Fetching Historical Evaluation Records..." />;
  }

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Analysis History & Audit Archive
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Access past match calculations, ATS compliance records, and exported reports.
          </p>
        </div>

        <NavLink to="/analysis">
          <Button icon={Briefcase} size="md">
            New Match Analysis
          </Button>
        </NavLink>
      </div>

      {/* Search Filter */}
      <Card>
        <div className="relative">
          <Search className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-500" />
          <input
            type="text"
            placeholder="Search by position, company, or candidate name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-[#151D2C] border border-slate-700/80 rounded-xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-teal-500"
          />
        </div>
      </Card>

      {/* History Table */}
      <Card title="Analysis Records" subtitle={`${filteredHistory.length} evaluations found`}>
        {filteredHistory.length > 0 ? (
          <div className="overflow-x-auto -mx-6">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="text-[11px] uppercase tracking-wider text-slate-500 bg-slate-900/50 border-y border-slate-800">
                <tr>
                  <th className="py-3.5 px-6 font-semibold">Position & Company</th>
                  <th className="py-3.5 px-6 font-semibold">Candidate</th>
                  <th className="py-3.5 px-6 font-semibold">Match Score</th>
                  <th className="py-3.5 px-6 font-semibold">ATS Score</th>
                  <th className="py-3.5 px-6 font-semibold">Skill Overlap</th>
                  <th className="py-3.5 px-6 font-semibold">Date Analyzed</th>
                  <th className="py-3.5 px-6 font-semibold text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filteredHistory.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-4 px-6 font-medium text-white">
                      <div className="font-bold text-slate-100">{item.job_title}</div>
                      <div className="text-[11px] text-slate-400">{item.company}</div>
                    </td>
                    <td className="py-4 px-6 text-slate-300">
                      {item.candidate_name || 'Candidate'}
                    </td>
                    <td className="py-4 px-6 font-bold">
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
                    <td className="py-4 px-6 font-bold text-indigo-400">
                      {Math.round(item.ats_score)}%
                    </td>
                    <td className="py-4 px-6">
                      <span className="text-teal-400">{item.matching_skills_count} Matched</span>
                      {item.missing_skills_count > 0 && (
                        <span className="text-rose-400 ml-1.5 font-medium">
                          / {item.missing_skills_count} Gaps
                        </span>
                      )}
                    </td>
                    <td className="py-4 px-6 text-slate-400">
                      {new Date(item.created_at).toLocaleDateString(undefined, {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric',
                      })}
                    </td>
                    <td className="py-4 px-6 text-right space-x-2">
                      <NavLink
                        to={`/analysis?id=${item.id}`}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-teal-950/40 text-teal-300 border border-teal-500/30 hover:bg-teal-900/40 transition-colors text-xs font-semibold"
                      >
                        <span>View</span>
                        <ArrowUpRight className="w-3 h-3" />
                      </NavLink>
                      <button
                        onClick={() => handleExport(item.id)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-colors text-xs font-semibold"
                      >
                        <Download className="w-3 h-3" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12 text-xs text-slate-500">
            No historical evaluations found matching your query.
          </div>
        )}
      </Card>
    </div>
  );
};
