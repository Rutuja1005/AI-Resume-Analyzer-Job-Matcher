import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  Code,
  User,
  Mail,
  Phone,
  GraduationCap,
  Briefcase,
  Layers,
  Trash2,
  ArrowRight,
  RefreshCw,
} from 'lucide-react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';
import { Card } from '../components/common/Card';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const ResumeUploadPage = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [parsedResume, setParsedResume] = useState(null);
  const [existingResumes, setExistingResumes] = useState([]);
  const [loadingList, setLoadingList] = useState(true);
  const [jsonModalOpen, setJsonModalOpen] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);

  const fileInputRef = useRef(null);
  const { showToast } = useToast();
  const navigate = useNavigate();

  const fetchExistingResumes = async () => {
    try {
      setLoadingList(true);
      const res = await api.get('/resumes');
      setExistingResumes(res.data.items || []);
      if (res.data.items && res.data.items.length > 0 && !parsedResume) {
        setParsedResume(res.data.items[0]);
      }
    } catch (err) {
      console.error('Failed to load resumes:', err);
    } finally {
      setLoadingList(false);
    }
  };

  useEffect(() => {
    fetchExistingResumes();
  }, []);

  const handleFileDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const selected = e.dataTransfer.files[0];
      if (selected.type === 'application/pdf' || selected.name.endsWith('.pdf')) {
        setFile(selected);
      } else {
        showToast('Please upload a valid PDF document.', 'warning');
      }
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      if (selected.type === 'application/pdf' || selected.name.endsWith('.pdf')) {
        setFile(selected);
      } else {
        showToast('Please select a PDF document.', 'warning');
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      showToast('Please select a PDF file first.', 'warning');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setUploadProgress(20);

    try {
      const progressTimer = setInterval(() => {
        setUploadProgress((prev) => (prev < 90 ? prev + 15 : prev));
      }, 200);

      const res = await api.post('/resumes/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      clearInterval(progressTimer);
      setUploadProgress(100);

      setParsedResume(res.data);
      setFile(null);
      showToast(`Resume "${res.data.filename}" parsed successfully!`, 'success');
      fetchExistingResumes();
    } catch (err) {
      const msg = err.response?.data?.detail || 'Failed to parse resume PDF. Please check file format.';
      showToast(msg, 'error');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this resume?')) return;
    try {
      await api.delete(`/resumes/${id}`);
      showToast('Resume removed.', 'info');
      if (parsedResume?.id === id) {
        setParsedResume(null);
      }
      fetchExistingResumes();
    } catch (err) {
      showToast('Failed to delete resume.', 'error');
    }
  };

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Resume PDF Ingestion & NLP Parsing
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Upload your PDF resume to extract contact entities, degree credentials, and technical skills.
          </p>
        </div>

        {parsedResume && (
          <Button
            icon={ArrowRight}
            size="md"
            onClick={() => navigate(`/analysis?resumeId=${parsedResume.id}`)}
          >
            Match with Job
          </Button>
        )}
      </div>

      {/* Upload Drag & Drop Zone */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragOver(true);
        }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleFileDrop}
        className={`glass-card rounded-3xl p-8 lg:p-12 text-center border-2 border-dashed transition-all duration-300 ${
          isDragOver
            ? 'border-teal-400 bg-teal-950/30 scale-[1.01]'
            : 'border-slate-700/80 hover:border-teal-500/50'
        }`}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileSelect}
          accept="application/pdf"
          className="hidden"
        />

        <div className="max-w-md mx-auto space-y-4">
          <div className="w-16 h-16 rounded-2xl bg-slate-800/90 border border-slate-700 flex items-center justify-center mx-auto text-teal-400 shadow-xl shadow-teal-500/10">
            <UploadCloud className="w-8 h-8" />
          </div>

          <div>
            <h3 className="text-lg font-bold text-white">Drag & Drop Your PDF Resume</h3>
            <p className="text-xs text-slate-400 mt-1">
              Supports standard ATS single/multi-column PDFs (Max 15MB)
            </p>
          </div>

          {file ? (
            <div className="p-4 bg-slate-900/80 rounded-2xl border border-teal-500/30 flex items-center justify-between text-left">
              <div className="flex items-center space-x-3 overflow-hidden">
                <FileText className="w-6 h-6 text-teal-400 shrink-0" />
                <div className="overflow-hidden">
                  <p className="text-xs font-semibold text-white truncate">{file.name}</p>
                  <p className="text-[11px] text-slate-400">
                    {(file.size / (1024 * 1024)).toFixed(2)} MB • Ready for NLP analysis
                  </p>
                </div>
              </div>
              <Button
                size="sm"
                onClick={handleUpload}
                loading={uploading}
                icon={Sparkles}
              >
                Analyze
              </Button>
            </div>
          ) : (
            <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
              <Button
                variant="primary"
                size="md"
                onClick={() => fileInputRef.current?.click()}
                icon={UploadCloud}
              >
                Browse PDF File
              </Button>
            </div>
          )}

          {uploading && (
            <div className="w-full space-y-2 pt-2">
              <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-teal-400 to-emerald-500 h-2 transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
              <p className="text-[11px] text-teal-300 animate-pulse font-medium">
                Parsing PDF sections & mapping 1,200+ skill ontologies ({uploadProgress}%)...
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Display Extracted Information */}
      {parsedResume && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <h2 className="text-xl font-bold text-white tracking-tight">
                Extracted Resume Entities
              </h2>
              <Badge variant="success" size="md">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Parsed Successfully</span>
              </Badge>
            </div>

            <Button
              variant="outline"
              size="sm"
              icon={Code}
              onClick={() => setJsonModalOpen(true)}
            >
              View Raw JSON
            </Button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Card: Candidate Summary & Contacts */}
            <Card className="space-y-5 lg:col-span-1">
              <div className="flex items-center space-x-3 pb-4 border-b border-slate-800">
                <div className="w-12 h-12 rounded-2xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400 font-bold text-lg">
                  {parsedResume.candidate_name ? parsedResume.candidate_name.charAt(0) : 'C'}
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">
                    {parsedResume.candidate_name || 'Candidate Name'}
                  </h3>
                  <p className="text-xs text-slate-400">{parsedResume.filename}</p>
                </div>
              </div>

              <div className="space-y-3 text-xs">
                {parsedResume.candidate_email && (
                  <div className="flex items-center space-x-2 text-slate-300">
                    <Mail className="w-4 h-4 text-teal-400 shrink-0" />
                    <span className="truncate">{parsedResume.candidate_email}</span>
                  </div>
                )}
                {parsedResume.candidate_phone && (
                  <div className="flex items-center space-x-2 text-slate-300">
                    <Phone className="w-4 h-4 text-teal-400 shrink-0" />
                    <span>{parsedResume.candidate_phone}</span>
                  </div>
                )}
              </div>

              {parsedResume.summary_text && (
                <div className="pt-3 border-t border-slate-800">
                  <p className="text-[11px] uppercase font-semibold tracking-wider text-slate-500 mb-1">
                    Summary / Profile
                  </p>
                  <p className="text-xs text-slate-300 leading-relaxed line-clamp-4">
                    {parsedResume.summary_text}
                  </p>
                </div>
              )}
            </Card>

            {/* Right Card: Technical Skills & Education */}
            <div className="lg:col-span-2 space-y-6">
              {/* Skills Card */}
              <Card title="Identified Technical Skills" subtitle={`${parsedResume.skills?.length || 0} skills detected`}>
                {parsedResume.skills && parsedResume.skills.length > 0 ? (
                  <div className="flex flex-wrap gap-2">
                    {parsedResume.skills.map((skill, i) => (
                      <Badge key={i} variant="primary" size="md">
                        {skill}
                      </Badge>
                    ))}
                  </div>
                ) : (
                  <p className="text-xs text-slate-500">No skills recognized in the ontology.</p>
                )}
              </Card>

              {/* Education & Experience Previews */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card title="Education Credentials" subtitle="Academic history">
                  {parsedResume.education && parsedResume.education.length > 0 ? (
                    <div className="space-y-2">
                      {parsedResume.education.map((edu, i) => (
                        <div key={i} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
                          <p className="font-semibold text-white">{edu.degree || 'Degree'}</p>
                          {edu.field_of_study && <p className="text-slate-400">{edu.field_of_study}</p>}
                          {edu.year && <p className="text-teal-400 mt-1">{edu.year}</p>}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-slate-500">No explicit degree detected.</p>
                  )}
                </Card>

                <Card title="Work Experience" subtitle="Role history">
                  {parsedResume.experience && parsedResume.experience.length > 0 ? (
                    <div className="space-y-2">
                      {parsedResume.experience.slice(0, 2).map((exp, i) => (
                        <div key={i} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
                          <p className="font-semibold text-white">{exp.title_and_company}</p>
                          {exp.duration && <p className="text-teal-400 text-[11px]">{exp.duration}</p>}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-slate-500">Parsed from document sections.</p>
                  )}
                </Card>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Previously Uploaded Resumes Library */}
      <Card title="Saved Resumes Library" subtitle="All uploaded PDF resumes available for instant job matching">
        {loadingList ? (
          <div className="text-center py-6 text-xs text-slate-500">Loading library...</div>
        ) : existingResumes.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {existingResumes.map((r) => (
              <div
                key={r.id}
                className={`p-4 rounded-2xl border transition-all cursor-pointer ${
                  parsedResume?.id === r.id
                    ? 'border-teal-500 bg-teal-950/20'
                    : 'border-slate-800 bg-slate-900/50 hover:border-slate-700'
                }`}
                onClick={() => setParsedResume(r)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3 overflow-hidden">
                    <FileText className="w-5 h-5 text-teal-400 shrink-0" />
                    <div className="overflow-hidden">
                      <p className="text-xs font-bold text-white truncate">{r.candidate_name || r.filename}</p>
                      <p className="text-[10px] text-slate-400">{r.skills?.length || 0} skills extracted</p>
                    </div>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(r.id);
                    }}
                    className="p-1 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-950/30 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-xs text-slate-500">
            No resumes saved yet. Upload your first PDF above.
          </div>
        )}
      </Card>

      {/* Raw JSON Structure Modal */}
      <Modal
        isOpen={jsonModalOpen}
        onClose={() => setJsonModalOpen(false)}
        title="Extracted Structured Resume JSON"
      >
        <pre className="p-4 bg-slate-950 rounded-xl text-xs text-teal-300 font-mono overflow-x-auto max-h-[60vh]">
          {JSON.stringify(parsedResume, null, 2)}
        </pre>
      </Modal>
    </div>
  );
};
