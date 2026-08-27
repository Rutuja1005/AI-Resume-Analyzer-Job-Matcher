import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Briefcase,
  Sparkles,
  CheckCircle2,
  Layers,
  GraduationCap,
  Clock,
  Key,
  ArrowRight,
  FileText,
  Copy,
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';

export const JobDescriptionPage = () => {
  const [title, setTitle] = useState('');
  const [company, setCompany] = useState('');
  const [jdText, setJdText] = useState('');
  const [analyzing, setAnalyzing] = useState(false);
  const [analyzedJob, setAnalyzedJob] = useState(null);
  const [savedJobs, setSavedJobs] = useState([]);
  const [loadingJobs, setLoadingJobs] = useState(true);

  const { showToast } = useToast();
  const navigate = useNavigate();

  const sampleJobs = [
    {
      label: 'Senior Full-Stack Engineer',
      title: 'Senior Full-Stack Engineer',
      company: 'StripeTech Innovations',
      text: `Job Title: Senior Full-Stack Engineer
Company: StripeTech Innovations
Requirements:
• 4+ years of professional full-stack development experience with Python, FastAPI, and React.
• Deep proficiency with PostgreSQL, Redis, Docker, and TypeScript.
• Hands-on experience architecting RESTful microservices and deploying on AWS (EC2, S3, RDS).
• Bachelor's Degree in Computer Science or related STEM field.
Nice to Have:
• Familiarity with Next.js, GraphQL, Kubernetes, and CI/CD pipelines with GitHub Actions.`,
    },
    {
      label: 'Machine Learning & NLP Engineer',
      title: 'Machine Learning & NLP Engineer',
      company: 'Cortex Intelligence',
      text: `Job Title: Machine Learning & NLP Engineer
Company: Cortex Intelligence
Requirements:
• 3+ years of experience with Python, Scikit-learn, PyTorch, and NLP architectures.
• Hands-on experience with Transformers, Hugging Face, TF-IDF, embeddings, and vector databases (Pinecone, ChromaDB).
• Experience containerizing ML microservices with FastAPI and Docker.
• Master's or Bachelor's in Computer Science, AI, or Data Science.
Preferred:
• Experience with LangChain, RAG pipelines, AWS SageMaker, and Kubernetes.`,
    },
  ];

  const fetchJobs = async () => {
    try {
      setLoadingJobs(true);
      const res = await api.get('/jobs');
      setSavedJobs(res.data || []);
      if (res.data && res.data.length > 0 && !analyzedJob) {
        setAnalyzedJob(res.data[0]);
      }
    } catch (err) {
      console.error('Failed to fetch jobs:', err);
    } finally {
      setLoadingJobs(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!jdText || jdText.trim().length < 30) {
      showToast('Please provide a detailed job description (minimum 30 characters).', 'warning');
      return;
    }

    setAnalyzing(true);
    try {
      const res = await api.post('/jobs/analyze', {
        title: title || 'Software Engineer',
        company: company || 'Target Company',
        job_description_text: jdText,
      });

      setAnalyzedJob(res.data);
      showToast('Job description analyzed and saved!', 'success');
      fetchJobs();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to analyze job description.';
      showToast(msg, 'error');
    } finally {
      setAnalyzing(false);
    }
  };

  const loadSample = (sample) => {
    setTitle(sample.title);
    setCompany(sample.company);
    setJdText(sample.text);
    showToast(`Loaded "${sample.label}" template.`, 'info');
  };

  return (
    <div className="space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Job Description NLP Analyzer
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Extract required technologies, preferred qualifications, seniority levels, and keyword weights.
          </p>
        </div>

        {analyzedJob && (
          <Button
            icon={ArrowRight}
            size="md"
            onClick={() => navigate(`/analysis?jobId=${analyzedJob.id}`)}
          >
            Match with Resume
          </Button>
        )}
      </div>

      {/* Input Form & Quick Samples */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card className="shadow-xl">
            <form onSubmit={handleAnalyze} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                    Job Title
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. Senior Full-Stack Engineer"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full bg-[#151D2C] border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                    Company / Organization
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. Stripe, Acme Corp"
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    className="w-full bg-[#151D2C] border border-slate-700/80 rounded-xl px-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
                  />
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="block text-xs font-semibold text-slate-300">
                    Job Description Text
                  </label>
                  <div className="flex items-center space-x-2">
                    <span className="text-[11px] text-slate-500">Quick Samples:</span>
                    {sampleJobs.map((s, i) => (
                      <button
                        key={i}
                        type="button"
                        onClick={() => loadSample(s)}
                        className="text-[11px] text-teal-400 hover:text-teal-300 underline font-medium"
                      >
                        {s.label.split(' ')[1] || s.label}
                      </button>
                    ))}
                  </div>
                </div>
                <textarea
                  rows={8}
                  required
                  placeholder="Paste the full job posting requirements, responsibilities, and qualifications here..."
                  value={jdText}
                  onChange={(e) => setJdText(e.target.value)}
                  className="w-full bg-[#151D2C] border border-slate-700/80 rounded-xl p-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 leading-relaxed font-sans"
                />
              </div>

              <div className="flex justify-end">
                <Button
                  type="submit"
                  loading={analyzing}
                  icon={Sparkles}
                  size="md"
                >
                  Analyze Job Requirements
                </Button>
              </div>
            </form>
          </Card>
        </div>

        {/* Saved Jobs Sidebar */}
        <div className="space-y-6">
          <Card title="Saved Job Descriptions" subtitle="Select to view extraction breakdown">
            {loadingJobs ? (
              <div className="text-center py-6 text-xs text-slate-500">Loading jobs...</div>
            ) : savedJobs.length > 0 ? (
              <div className="space-y-3 max-h-[360px] overflow-y-auto pr-1">
                {savedJobs.map((job) => (
                  <div
                    key={job.id}
                    onClick={() => setAnalyzedJob(job)}
                    className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                      analyzedJob?.id === job.id
                        ? 'border-teal-500 bg-teal-950/20 shadow-sm'
                        : 'border-slate-800 bg-slate-900/40 hover:border-slate-700'
                    }`}
                  >
                    <p className="text-xs font-bold text-white truncate">{job.title}</p>
                    <p className="text-[11px] text-slate-400 mt-0.5">{job.company}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <Badge variant="primary" size="sm">
                        {job.required_skills?.length || 0} Required Skills
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-6 text-xs text-slate-500">
                No jobs saved yet. Paste one on the left.
              </div>
            )}
          </Card>
        </div>
      </div>

      {/* Display Extracted Job Intelligence */}
      {analyzedJob && (
        <div className="space-y-6">
          <div className="flex items-center justify-between pb-2 border-b border-slate-800">
            <div>
              <h2 className="text-xl font-bold text-white tracking-tight">
                {analyzedJob.title}
              </h2>
              <p className="text-xs text-slate-400">{analyzedJob.company}</p>
            </div>
            <Badge variant="success" size="md">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Target JD Active</span>
            </Badge>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Required Skills */}
            <Card title="Required Technical Skills" subtitle="Mandatory qualifications">
              <div className="flex flex-wrap gap-2">
                {analyzedJob.required_skills && analyzedJob.required_skills.length > 0 ? (
                  analyzedJob.required_skills.map((skill, i) => (
                    <Badge key={i} variant="primary" size="md">
                      {skill}
                    </Badge>
                  ))
                ) : (
                  <p className="text-xs text-slate-500">No explicit required skills flagged.</p>
                )}
              </div>
            </Card>

            {/* Preferred / Nice-to-Have Skills */}
            <Card title="Preferred Qualifications" subtitle="Bonus / Secondary skills">
              <div className="flex flex-wrap gap-2">
                {analyzedJob.preferred_skills && analyzedJob.preferred_skills.length > 0 ? (
                  analyzedJob.preferred_skills.map((skill, i) => (
                    <Badge key={i} variant="purple" size="md">
                      {skill}
                    </Badge>
                  ))
                ) : (
                  <p className="text-xs text-slate-500">None detected in preferred category.</p>
                )}
              </div>
            </Card>

            {/* Experience & Keywords */}
            <Card title="Role Constraints" subtitle="Experience & TF-IDF keywords">
              <div className="space-y-3 text-xs">
                <div>
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                    Seniority Level
                  </span>
                  <p className="text-slate-200 font-medium">
                    {analyzedJob.experience_level || 'General Level'}
                  </p>
                </div>

                <div className="pt-2 border-t border-slate-800">
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">
                    Prominent TF-IDF Keywords
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {analyzedJob.important_keywords &&
                      analyzedJob.important_keywords.slice(0, 8).map((kw, i) => (
                        <Badge key={i} variant="default" size="sm">
                          {kw}
                        </Badge>
                      ))}
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};
