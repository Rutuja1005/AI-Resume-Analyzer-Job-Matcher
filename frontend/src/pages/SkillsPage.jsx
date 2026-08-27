import React, { useState, useEffect } from 'react';
import { Layers, CheckCircle2, AlertTriangle, Sparkles, Filter, Search } from 'lucide-react';
import api from '../services/api';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const SkillsPage = () => {
  const [resumes, setResumes] = useState([]);
  const [selectedResume, setSelectedResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        setLoading(true);
        const res = await api.get('/resumes');
        const list = res.data.items || [];
        setResumes(list);
        if (list.length > 0) {
          setSelectedResume(list[0]);
        }
      } catch (err) {
        console.error('Failed to load resumes:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchResumes();
  }, []);

  if (loading) {
    return <LoadingSpinner message="Aggregating Candidate Skill Matrix..." />;
  }

  const allSkills = selectedResume?.skills || [];
  const filteredSkills = allSkills.filter((s) =>
    s.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Candidate Skill Matrix & Inventory
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Browse verified technical competencies and domain proficiencies extracted from your resumes.
          </p>
        </div>

        {resumes.length > 1 && (
          <select
            value={selectedResume?.id || ''}
            onChange={(e) => {
              const r = resumes.find((item) => item.id === e.target.value);
              setSelectedResume(r);
            }}
            className="bg-[#151D2C] border border-slate-700/80 rounded-xl px-3 py-2 text-xs font-semibold text-white focus:outline-none focus:border-teal-500"
          >
            {resumes.map((r) => (
              <option key={r.id} value={r.id}>
                {r.candidate_name || r.filename}
              </option>
            ))}
          </select>
        )}
      </div>

      {selectedResume ? (
        <div className="space-y-6">
          {/* Search & Filter Card */}
          <Card>
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
              <div className="relative flex-1">
                <Search className="w-4 h-4 absolute left-3.5 top-3.5 text-slate-500" />
                <input
                  type="text"
                  placeholder="Search technical skills (e.g. Python, Docker, React)..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-[#151D2C] border border-slate-700/80 rounded-xl pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-teal-500"
                />
              </div>
              <div className="text-xs text-slate-400 font-medium">
                Showing {filteredSkills.length} of {allSkills.length} total skills
              </div>
            </div>
          </Card>

          {/* Skill Grid */}
          <Card
            title={`Skills for ${selectedResume.candidate_name || selectedResume.filename}`}
            subtitle="Categorized competencies matched against ontology dictionary"
          >
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
              {filteredSkills.map((skill, i) => (
                <div
                  key={i}
                  className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-teal-500/40 transition-all flex items-center space-x-2"
                >
                  <CheckCircle2 className="w-3.5 h-3.5 text-teal-400 shrink-0" />
                  <span className="text-xs font-semibold text-slate-200 truncate">{skill}</span>
                </div>
              ))}
            </div>

            {filteredSkills.length === 0 && (
              <div className="text-center py-10 text-xs text-slate-500">
                No matching skills found for search term "{searchQuery}".
              </div>
            )}
          </Card>
        </div>
      ) : (
        <Card className="text-center py-16">
          <Layers className="w-12 h-12 text-teal-400 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-white">No Resume Found</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto mt-2">
            Upload a PDF resume from the Resume Upload page to view the skill matrix.
          </p>
        </Card>
      )}
    </div>
  );
};
