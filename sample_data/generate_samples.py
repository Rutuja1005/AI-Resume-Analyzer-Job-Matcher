import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

os.makedirs("sample_data", exist_ok=True)

def create_pdf(filename, content):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#475569"),
        spaceAfter=10
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        leftIndent=12,
        spaceAfter=3
    )

    story = []
    for item in content:
        typ = item[0]
        text = item[1]
        if typ == "title":
            story.append(Paragraph(text, title_style))
        elif typ == "contact":
            story.append(Paragraph(text, contact_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
        elif typ == "heading":
            story.append(Paragraph(text.upper(), heading_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=6))
        elif typ == "body":
            story.append(Paragraph(text, body_style))
        elif typ == "bullet":
            story.append(Paragraph(f"• {text}", bullet_style))
        elif typ == "space":
            story.append(Spacer(1, text))

    doc.build(story)
    print(f"Generated {filename}")

# 1. Senior Full-Stack Engineer Resume
resume_fullstack = [
    ("title", "Alex Morgan"),
    ("contact", "alex.morgan@techcorp.io | +1 (555) 234-5678 | San Francisco, CA | linkedin.com/in/alexmorgan-dev | github.com/alexmorgan-code"),
    ("heading", "Professional Summary"),
    ("body", "Senior Full-Stack Engineer with 6+ years of experience architecting high-throughput distributed systems, event-driven microservices, and responsive web applications. Proven track record of improving system uptime to 99.99% and accelerating release cycles by 40% through modern DevOps and CI/CD pipelines."),
    ("heading", "Technical Skills"),
    ("body", "<b>Languages:</b> Python, JavaScript, TypeScript, Go, SQL, HTML5, CSS3"),
    ("body", "<b>Frameworks & Libraries:</b> React, Next.js, FastAPI, Node.js, Express, Tailwind CSS, Redux"),
    ("body", "<b>Databases & Caching:</b> PostgreSQL, Redis, MongoDB, SQLAlchemy"),
    ("body", "<b>Cloud & DevOps:</b> Docker, Kubernetes, AWS (EC2, S3, RDS, Lambda), GitHub Actions, CI/CD, Nginx"),
    ("body", "<b>Testing & Practices:</b> PyTest, Jest, TDD, Clean Architecture, REST APIs, GraphQL, Microservices"),
    ("heading", "Work Experience"),
    ("body", "<b>Senior Full-Stack Engineer</b> | CloudScale Technologies (2021 - Present)"),
    ("bullet", "Architected and delivered 12+ RESTful microservices using FastAPI, PostgreSQL, and Redis processing 15M+ daily requests with sub-50ms latency."),
    ("bullet", "Spearheaded frontend migration to React and Next.js, boosting core web vitals and increasing customer conversion rate by 28%."),
    ("bullet", "Implemented automated CI/CD deployment pipelines using GitHub Actions and Docker, reducing deployment cycle times by 45%."),
    ("bullet", "Mentored 5 junior engineers and instituted rigorous code review and TDD practices using PyTest and Jest."),
    ("space", 4),
    ("body", "<b>Software Engineer</b> | Nexus Solutions (2018 - 2021)"),
    ("bullet", "Engineered scalable backend APIs with Python and Django, reducing SQL query execution times by 35% with database indexing."),
    ("bullet", "Built interactive client dashboards using React, Tailwind CSS, and Chart.js for 100,000+ monthly active users."),
    ("bullet", "Collaborated across cross-functional product teams in an Agile Scrum environment to deliver quarterly milestones on schedule."),
    ("heading", "Education"),
    ("body", "<b>Bachelor of Science in Computer Science</b> | University of California, Berkeley (2014 - 2018)"),
    ("heading", "Key Projects"),
    ("body", "<b>AI Document Parser & Search Engine:</b> Full-stack document search portal using FastAPI, PostgreSQL, and React indexed with vector embeddings."),
    ("body", "<b>Real-time Collaborative Whiteboard:</b> WebSocket-powered canvas built with Node.js and React handling 500+ concurrent editors.")
]

# 2. AI / ML & Data Scientist Resume
resume_ai = [
    ("title", "Dr. Elena Rostova"),
    ("contact", "elena.rostova@datascience.io | +1 (555) 987-6543 | New York, NY | linkedin.com/in/elenarostova | github.com/erostova-ai"),
    ("heading", "Professional Summary"),
    ("body", "Lead Machine Learning Engineer and Data Scientist with 5+ years of production experience in Natural Language Processing (NLP), Deep Learning, and LLM fine-tuning. Skilled at translating complex business problems into scalable ML pipelines."),
    ("heading", "Technical Skills"),
    ("body", "<b>ML & AI:</b> Machine Learning, NLP, Deep Learning, PyTorch, TensorFlow, Scikit-learn, Hugging Face, Transformers, spaCy, NLTK, LangChain, RAG"),
    ("body", "<b>Languages & Data:</b> Python, SQL, R, Pandas, NumPy, SciPy"),
    ("body", "<b>Backend & Cloud:</b> FastAPI, Docker, AWS (SageMaker, S3), MLflow, PostgreSQL, Pinecone, ChromaDB"),
    ("body", "<b>Practices:</b> Feature Engineering, Model Evaluation, A/B Testing, Data Pipelines, PyTest"),
    ("heading", "Work Experience"),
    ("body", "<b>Senior Machine Learning Engineer</b> | Alpha AI Labs (2022 - Present)"),
    ("bullet", "Developed and deployed enterprise NLP semantic search models using Transformers and Pinecone, boosting search accuracy by 34%."),
    ("bullet", "Engineered end-to-end RAG architecture with LangChain and FastAPI handling 200,000+ daily conversational queries."),
    ("bullet", "Optimized PyTorch inference latency by 60% through model quantization and ONNX runtime integration."),
    ("space", 4),
    ("body", "<b>Data Scientist</b> | DataSphere Analytics (2019 - 2022)"),
    ("bullet", "Built predictive classification and regression models using Scikit-learn and XGBoost, improving churn forecasting accuracy by 22%."),
    ("bullet", "Engineered automated data preprocessing and feature extraction pipelines with Pandas, NumPy, and SQL."),
    ("heading", "Education"),
    ("body", "<b>Master of Science in Artificial Intelligence</b> | Columbia University (2017 - 2019)"),
    ("body", "<b>Bachelor of Science in Mathematics & Statistics</b> | New York University (2013 - 2017)")
]

create_pdf("sample_data/sample_resume_senior_fullstack.pdf", resume_fullstack)
create_pdf("sample_data/sample_resume_data_scientist.pdf", resume_ai)

# Text Job Descriptions
jd_fullstack = """Job Title: Senior Full-Stack Engineer
Company: StripeTech Innovations
Location: Remote / San Francisco, CA

About the Role:
We are seeking an experienced Senior Full-Stack Engineer to lead the architecture and implementation of our high-scale cloud platforms. You will design resilient backend microservices, intuitive user interfaces, and collaborate with cross-functional teams.

Responsibilities:
• Architect, build, and maintain robust REST APIs and backend services using Python, FastAPI, and PostgreSQL.
• Develop responsive, accessible web frontend interfaces using React, TypeScript, and Tailwind CSS.
• Optimize system latency, database indexes, and Redis caching layers for high-throughput workloads.
• Manage containerized deployments with Docker and Kubernetes in AWS cloud infrastructure.
• Write comprehensive automated tests using PyTest and Jest with CI/CD GitHub Actions.

Requirements:
• 4+ years of professional full-stack web development experience.
• Strong proficiency in Python, JavaScript, TypeScript, and SQL.
• Hands-on expertise with React, FastAPI, PostgreSQL, and Redis.
• Production experience with Docker, CI/CD pipelines, and AWS cloud services.
• Solid grasp of Clean Architecture, RESTful design, and SOLID principles.
• Bachelor's Degree in Computer Science, Software Engineering, or equivalent experience.

Nice to Have:
• Experience with Next.js, GraphQL, and Terraform.
• Familiarity with event-driven architecture and Apache Kafka.
"""

jd_ai_ml = """Job Title: Machine Learning & NLP Engineer
Company: Cortex Intelligence
Location: New York, NY / Hybrid

About the Role:
Cortex Intelligence is hiring a Machine Learning Engineer specializing in Natural Language Processing (NLP) and Large Language Model architectures to power our next-generation enterprise AI solutions.

Responsibilities:
• Design, train, and evaluate machine learning models for text classification, semantic search, and entity extraction.
• Build scalable ML inference microservices using Python, FastAPI, and Docker.
• Develop Retrieval-Augmented Generation (RAG) pipelines using LangChain, Hugging Face Transformers, and Vector Databases (Pinecone/ChromaDB).
• Optimize data pipelines using Pandas, NumPy, and SQL.

Requirements:
• 3+ years of hands-on Machine Learning and NLP production experience.
• Strong proficiency in Python, Scikit-learn, PyTorch or TensorFlow.
• Deep understanding of Transformers, embeddings, TF-IDF, Cosine Similarity, and NLTK/spaCy.
• Experience building REST APIs with FastAPI and containerizing with Docker.
• Master's or Bachelor's Degree in Computer Science, AI, Data Science, or Mathematics.

Preferred Qualifications:
• Experience with Kubernetes, MLflow, and AWS SageMaker.
• Contributions to open-source ML projects or published research.
"""

with open("sample_data/sample_jd_fullstack_react_dev.txt", "w", encoding="utf-8") as f:
    f.write(jd_fullstack)

with open("sample_data/sample_jd_ai_ml_engineer.txt", "w", encoding="utf-8") as f:
    f.write(jd_ai_ml)

print("All sample files generated successfully!")
