import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Sparkles,
  Gauge,
  Target,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Download,
  BookOpen,
  ArrowRight,
  ShieldCheck,
  FileText,
  Briefcase,
  Layers,
  ChevronDown,
  ChevronUp,
  ExternalLink,
  Lightbulb,
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { CircularProgress } from '../components/common/CircularProgress';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const AnalysisPage = () => {
  const [searchParams] = useSearchParams();
  const [resumes, setResumes] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [selectedResumeId, setSelectedResumeId] = useState(searchParams.get('resumeId') || '');
  const [selectedJobId, setSelectedJobId] = useState(searchParams.get('jobId') || '');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingInitial, setLoadingInitial] = useState(true);

  const { showToast } = useToast();

  useEffect(() => {
    const fetchInitData = async () => {
      try {
        setLoadingInitial(true);
        const [resResumes, resJobs] = await Promise.all([
          api.get('/resumes'),
          api.get('/jobs'),
        ]);
        const rList = resResumes.data.items || [];
        const jList = resJobs.data || [];
        setResumes(rList);
        setJobs(jList);

        const initialResId = searchParams.get('resumeId') || (rList.length > 0 ? rList[0].id : '');
        const initialJobId = searchParams.get('jobId') || (jList.length > 0 ? jList[0].id : '');
        const analysisId = searchParams.get('id');

        setSelectedResumeId(initialResId);
        setSelectedJobId(initialJobId);

        if (analysisId) {
          const resAnalysis = await api.get(`/analysis/${analysisId}`);
          setAnalysisResult(resAnalysis.data);
          setSelectedResumeId(resAnalysis.data.resume_id);
          setSelectedJobId(resAnalysis.data.job_description_id);
        } else if (initialResId && initialJobId) {
          // Auto-run analysis
          runMatch(initialResId, initialJobId);
        }
      } catch (err) {
        console.error('Failed to initialize analysis data:', err);
      } finally {
        setLoadingInitial(false);
      }
    };

    fetchInitData();
  }, []);

  const runMatch = async (resumeId = selectedResumeId, jobId = selectedJobId) => {
    if (!resumeId || !jobId) {
      showToast('Please select both a candidate resume and target job description.', 'warning');
      return;
    }

    setLoading(true);
    try {
      const res = await api.post('/analysis/match', {
        resume_id: resumeId,
        job_description_id: jobId,
      });
      setAnalysisResult(res.data);
      showToast('Matching analysis & ATS audit completed!', 'success');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to generate match analysis.';
      showToast(msg, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleExportJSON = async () => {
    if (!analysisResult?.analysis_id) return;
    try {
      const res = await api.get(`/analysis/${analysisResult.analysis_id}/export`, {
        responseType: 'blob',
      });
      const blob = new Blob([res.data], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Analysis_Report_${analysisResult.analysis_id.substring(0, 8)}.json`;
      a.click();
      window.URL.revokeObjectURL(url);
      showToast('Exported report downloaded.', 'success');
    } catch (err) {
      showToast('Failed to export analysis.', 'error');
    }
  };

  if (loadingInitial) {
    return <LoadingSpinner message="Loading Candidate Profile & Job Descriptions..." />;
  }

  const atsBreakdown = analysisResult?.ats_breakdown || {};

  return (
    <div className="space-y-8">
      {/* Top Controls Bar */}
      <div className="glass-card rounded-3xl p-6 border border-slate-800 shadow-xl">
        <div className="flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 flex-1">
            {/* Resume Selector */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-teal-400" />
                <span>Selected Candidate Resume</span>
              </label>
              <select
                value={selectedResumeId}
                onChange={(e) => {
                  setSelectedResumeId(e.target.value);
                  if (selectedJobId) runMatch(e.target.value, selectedJobId);
                }}
                className="w-full bg-[#151D2C] border border-slate-700/80 rounded-xl px-3.5 py-2.5 text-xs font-medium text-white focus:outline-none focus:border-teal-500"
              >
                {resumes.length === 0 && <option value="">No resumes found. Please upload one.</option>}
                {resumes.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.candidate_name || r.filename} ({r.skills?.length || 0} skills)
                  </option>
                ))}
              </select>
            </div>

            {/* Job Selector */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5 flex items-center gap-1.5">
                <Briefcase className="w-3.5 h-3.5 text-cyan-400" />
                <span>Target Job Description</span>
              </label>
              <select
                value={selectedJobId}
                onChange={(e) => {
                  setSelectedJobId(e.target.value);
                  if (selectedResumeId) runMatch(selectedResumeId, e.target.value);
                }}
                className="w-full bg-[#151D2C] border border-slate-700/80 rounded-xl px-3.5 py-2.5 text-xs font-medium text-white focus:outline-none focus:border-teal-500"
              >
                {jobs.length === 0 && <option value="">No jobs found. Please add one.</option>}
                {jobs.map((j) => (
                  <option key={j.id} value={j.id}>
                    {j.title} — {j.company}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="flex items-center gap-3 shrink-0 pt-2 lg:pt-5">
            <Button
              onClick={() => runMatch()}
              loading={loading}
              icon={Sparkles}
              size="md"
              className="w-full sm:w-auto"
            >
              Re-Calculate Match
            </Button>
            {analysisResult && (
              <Button
                variant="secondary"
                onClick={handleExportJSON}
                icon={Download}
                size="md"
              >
                Export JSON
              </Button>
            )}
          </div>
        </div>
      </div>

      {loading ? (
        <LoadingSpinner message="Executing TF-IDF Cosine Vectorization & 7-Factor ATS Audit..." />
      ) : analysisResult ? (
        <div className="space-y-8">
          {/* Main Gauges & Top Score Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Overall Match Gauge Card */}
            <Card className="text-center flex flex-col items-center justify-center p-6 border-teal-500/30 glass-glow">
              <span className="text-xs uppercase font-bold tracking-wider text-teal-400 mb-3">
                Overall Match Score
              </span>
              <CircularProgress
                value={analysisResult.overall_match_score}
                size={140}
                strokeWidth={10}
                label="Composite"
                color={
                  analysisResult.overall_match_score >= 75
                    ? 'emerald'
                    : analysisResult.overall_match_score >= 50
                    ? 'amber'
                    : 'rose'
                }
              />
              <p className="text-xs text-slate-400 mt-3 font-medium">
                Combined NLP Similarity & Skills
              </p>
            </Card>

            {/* ATS Score Card */}
            <Card className="text-center flex flex-col items-center justify-center p-6 border-indigo-500/30">
              <span className="text-xs uppercase font-bold tracking-wider text-indigo-400 mb-3">
                ATS Compliance Score
              </span>
              <CircularProgress
                value={analysisResult.ats_score}
                size={140}
                strokeWidth={10}
                label="ATS Audit"
                color="indigo"
              />
              <p className="text-xs text-slate-400 mt-3 font-medium">
                Applicant Tracking System Health
              </p>
            </Card>

            {/* Skill Match Breakdown */}
            <Card className="flex flex-col justify-between p-6">
              <div>
                <span className="text-xs uppercase font-bold tracking-wider text-slate-400 block mb-2">
                  Technical Skill Match
                </span>
                <h3 className="text-3xl font-extrabold text-white">
                  {Math.round(analysisResult.skill_match_score)}%
                </h3>
                <div className="w-full bg-slate-800 rounded-full h-2 mt-3 overflow-hidden">
                  <div
                    className="bg-teal-400 h-2 rounded-full"
                    style={{ width: `${analysisResult.skill_match_score}%` }}
                  />
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-400 flex justify-between">
                <span>{analysisResult.matching_skills?.length || 0} Matched</span>
                <span className="text-rose-400 font-semibold">
                  {analysisResult.missing_skills?.length || 0} Gaps
                </span>
              </div>
            </Card>

            {/* Keyword Match Breakdown */}
            <Card className="flex flex-col justify-between p-6">
              <div>
                <span className="text-xs uppercase font-bold tracking-wider text-slate-400 block mb-2">
                  Keyword Alignment
                </span>
                <h3 className="text-3xl font-extrabold text-white">
                  {Math.round(analysisResult.keyword_match_score)}%
                </h3>
                <div className="w-full bg-slate-800 rounded-full h-2 mt-3 overflow-hidden">
                  <div
                    className="bg-cyan-400 h-2 rounded-full"
                    style={{ width: `${analysisResult.keyword_match_score}%` }}
                  />
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-slate-800 text-xs text-slate-400">
                <span>Education Match: {Math.round(analysisResult.education_match_score)}%</span>
              </div>
            </Card>
          </div>

          {/* Mathematical Match Calculation Explanation */}
          <Card
            title="Algorithm & Score Derivation Explanation"
            subtitle="Transparent multi-factor ML weight distribution"
          >
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 leading-relaxed space-y-2">
              <pre className="whitespace-pre-wrap font-sans">
                {analysisResult.match_explanation}
              </pre>
            </div>
          </Card>

          {/* Skills Breakdown Grid: Matching vs Missing Skills */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Matching Skills */}
            <Card
              title="Matching Technical Skills"
              subtitle={`${analysisResult.matching_skills?.length || 0} competencies present in resume`}
            >
              <div className="flex flex-wrap gap-2">
                {analysisResult.matching_skills && analysisResult.matching_skills.length > 0 ? (
                  analysisResult.matching_skills.map((skill, i) => (
                    <Badge key={i} variant="success" size="md">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                      <span>{skill}</span>
                    </Badge>
                  ))
                ) : (
                  <p className="text-xs text-slate-500">No overlapping skills found.</p>
                )}
              </div>
            </Card>

            {/* Missing Skills */}
            <Card
              title="Identified Skill Gaps"
              subtitle={`${analysisResult.missing_skills?.length || 0} target competencies to acquire`}
            >
              <div className="flex flex-wrap gap-2">
                {analysisResult.missing_skills && analysisResult.missing_skills.length > 0 ? (
                  analysisResult.missing_skills.map((item, i) => (
                    <Badge
                      key={i}
                      variant={item.importance === 'High' ? 'danger' : 'warning'}
                      size="md"
                    >
                      <AlertTriangle className="w-3.5 h-3.5" />
                      <span>{item.skill_name}</span>
                      <span className="text-[10px] opacity-75">({item.importance})</span>
                    </Badge>
                  ))
                ) : (
                  <p className="text-xs text-emerald-400">100% technical skill coverage matched!</p>
                )}
              </div>
            </Card>
          </div>

          {/* Detailed Skill Gap & Learning Roadmap */}
          {analysisResult.missing_skills && analysisResult.missing_skills.length > 0 && (
            <Card
              title="Targeted Skill Gap & Learning Roadmap"
              subtitle="Actionable technical milestones with importance ratings and suggested topics"
            >
              <div className="space-y-4">
                {analysisResult.missing_skills.map((item, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-all space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <h4 className="text-sm font-bold text-white">{item.skill_name}</h4>
                        <Badge
                          variant={
                            item.importance === 'High'
                              ? 'danger'
                              : item.importance === 'Medium'
                              ? 'warning'
                              : 'default'
                          }
                          size="sm"
                        >
                          {item.importance} Priority
                        </Badge>
                      </div>

                      {item.learning_resource_url && (
                        <a
                          href={item.learning_resource_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-teal-400 hover:text-teal-300 font-semibold inline-flex items-center gap-1"
                        >
                          <span>Official Tutorial</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      )}
                    </div>

                    <p className="text-xs text-slate-300 leading-relaxed">
                      <strong className="text-slate-400 font-medium">Why it matters:</strong> {item.reason}
                    </p>

                    <div className="p-2.5 bg-slate-950/60 rounded-xl border border-slate-800/80 text-xs text-teal-300 flex items-center gap-2">
                      <Lightbulb className="w-4 h-4 text-amber-400 shrink-0" />
                      <span>
                        <strong className="font-semibold text-slate-300">Suggested Focus:</strong>{' '}
                        {item.suggested_learning_topic}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* 7-Factor ATS Criteria Audit Table */}
          <Card
            title="7-Factor ATS System Compliance Audit"
            subtitle="Evaluation against automated resume screening benchmarks"
          >
            <div className="space-y-3">
              {[
                { name: 'Keyword Coverage (25 pts)', key: 'keyword_coverage' },
                { name: 'Standard Section Completeness (20 pts)', key: 'section_completeness' },
                { name: 'Contact Information (15 pts)', key: 'contact_information' },
                { name: 'Measurable Metrics & KPIs (15 pts)', key: 'quantifiable_achievements' },
                { name: 'Formatting & Length Health (15 pts)', key: 'formatting_and_length' },
                { name: 'Action Verbs Density (10 pts)', key: 'action_verbs_density' },
              ].map((factor) => {
                const item = atsBreakdown[factor.key];
                if (!item) return null;
                const isPassed = item.status === 'passed';
                const isWarning = item.status === 'warning';
                return (
                  <div
                    key={factor.key}
                    className="p-4 rounded-xl bg-slate-900/50 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
                  >
                    <div className="space-y-1">
                      <div className="flex items-center space-x-2">
                        {isPassed ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                        ) : isWarning ? (
                          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
                        ) : (
                          <XCircle className="w-4 h-4 text-rose-400 shrink-0" />
                        )}
                        <span className="font-bold text-white">{factor.name}</span>
                      </div>
                      <p className="text-slate-400 pl-6">{item.feedback}</p>
                    </div>

                    <div className="flex items-center space-x-3 sm:self-center shrink-0 pl-6 sm:pl-0">
                      <Badge
                        variant={isPassed ? 'success' : isWarning ? 'warning' : 'danger'}
                        size="sm"
                      >
                        {item.score} / {item.max_score} pts
                      </Badge>
                    </div>
                  </div>
                );
              })}
            </div>
          </Card>
        </div>
      ) : (
        <Card className="text-center py-16">
          <Sparkles className="w-12 h-12 text-teal-400 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-white">No Analysis Active</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto mt-2">
            Select a candidate resume and job description above, then click 'Re-Calculate Match' to generate your full report.
          </p>
        </Card>
      )}
    </div>
  );
};
