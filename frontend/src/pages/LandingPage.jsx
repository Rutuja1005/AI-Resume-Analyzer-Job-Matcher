import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  Sparkles,
  ArrowRight,
  CheckCircle2,
  FileSearch,
  Target,
  Gauge,
  Layers,
  Shield,
  Zap,
  Award,
  Terminal,
} from 'lucide-react';
import { Button } from '../components/common/Button';
import { Card } from '../components/common/Card';
import { Badge } from '../components/common/Badge';

export const LandingPage = () => {
  const features = [
    {
      icon: FileSearch,
      title: 'Automated PDF Parsing',
      desc: 'High-fidelity text and structured entity extraction for candidate contact details, degrees, work tenure, and project portfolios.',
    },
    {
      icon: Target,
      title: 'TF-IDF & Cosine Similarity',
      desc: 'Machine learning vectorization matching resume phrasing with Job Descriptions using bi-gram tokenization and sublinear TF scaling.',
    },
    {
      icon: Gauge,
      title: '7-Factor ATS Compliance Scorer',
      desc: 'Simulates industry ATS parsers checking keyword density, section headers, quantifiable KPIs, and action-verb strength.',
    },
    {
      icon: Layers,
      title: 'Skill Gap & Learning Roadmap',
      desc: 'Pinpoints missing technical proficiencies with automated priority weighting, rationale explanations, and direct learning milestones.',
    },
  ];

  return (
    <div className="min-h-screen bg-[#0B0F17] text-slate-100 flex flex-col justify-between selection:bg-teal-500 selection:text-white">
      {/* Header / Navbar */}
      <header className="border-b border-slate-800/80 bg-[#0F172A]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-teal-500 to-emerald-400 flex items-center justify-center shadow-lg shadow-teal-500/20">
              <Sparkles className="w-5 h-5 text-slate-950 stroke-[2.5]" />
            </div>
            <span className="text-lg font-bold tracking-tight text-white">
              Resume<span className="text-teal-400">AI</span>
            </span>
          </div>

          <div className="flex items-center space-x-4">
            <NavLink
              to="/login"
              className="text-sm font-medium text-slate-300 hover:text-white transition-colors"
            >
              Sign In
            </NavLink>
            <NavLink to="/register">
              <Button size="sm" icon={ArrowRight}>
                Get Started
              </Button>
            </NavLink>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-6 py-20 lg:py-28 flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-teal-500/30 bg-teal-950/40 text-teal-300 text-xs font-semibold mb-8 animate-pulse">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Full-Stack AI Resume Matcher & ATS Intelligence</span>
        </div>

        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-5xl leading-[1.1]">
          Bridge the Gap Between Your <span className="gradient-text">Resume</span> & Dream <span className="gradient-text">Tech Role</span>
        </h1>

        <p className="mt-6 text-base sm:text-lg text-slate-400 max-w-3xl leading-relaxed">
          Powered by Machine Learning, TF-IDF vectorization, and 1,200+ skill ontologies. Upload your resume, paste any job description, and receive instant match analytics, ATS scores, and personalized learning roadmaps.
        </p>

        <div className="mt-10 flex flex-col sm:flex-row items-center gap-4">
          <NavLink to="/register">
            <Button size="lg" icon={Zap} className="w-full sm:w-auto">
              Start Free Analysis
            </Button>
          </NavLink>
          <NavLink to="/login">
            <Button variant="secondary" size="lg" className="w-full sm:w-auto">
              View Demo Portal
            </Button>
          </NavLink>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-24 text-left w-full">
          {features.map((f, i) => {
            const Icon = f.icon;
            return (
              <Card key={i} className="hover:border-teal-500/40 transition-all group">
                <div className="w-12 h-12 rounded-xl bg-slate-800/80 border border-slate-700 flex items-center justify-center mb-4 group-hover:scale-110 group-hover:bg-teal-950/50 group-hover:border-teal-500/40 transition-all">
                  <Icon className="w-6 h-6 text-teal-400" />
                </div>
                <h3 className="text-base font-bold text-white mb-2">{f.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{f.desc}</p>
              </Card>
            );
          })}
        </div>

        {/* Architecture Badges Showcase */}
        <div className="mt-20 p-8 glass-card rounded-3xl w-full text-left">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-6 border-b border-slate-800">
            <div>
              <h2 className="text-xl font-bold text-white">Full-Stack Tech Architecture</h2>
              <p className="text-xs text-slate-400 mt-1">Built with production-grade engineering standards</p>
            </div>
            <Badge variant="primary" size="md">Production Ready</Badge>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4 mt-6">
            {[
              { name: 'FastAPI', desc: 'Asynchronous REST' },
              { name: 'React 18', desc: 'Vite & Tailwind' },
              { name: 'Scikit-Learn', desc: 'TF-IDF & Cosine' },
              { name: 'PostgreSQL', desc: 'SQLAlchemy ORM' },
              { name: 'JWT + bcrypt', desc: 'Secure Auth' },
              { name: 'Docker Compose', desc: 'Containerized' },
            ].map((tech, i) => (
              <div key={i} className="p-3 bg-slate-900/60 rounded-xl border border-slate-800 text-center">
                <p className="text-sm font-bold text-teal-300">{tech.name}</p>
                <p className="text-[11px] text-slate-400 mt-0.5">{tech.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-[#0F172A] py-8 text-center text-xs text-slate-500">
        <p>© 2026 AI Resume Analyzer & Job Matcher Platform. Enterprise Full-Stack Portfolio Architecture.</p>
      </footer>
    </div>
  );
};
