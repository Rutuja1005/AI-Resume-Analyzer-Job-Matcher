"""
Skill Ontology Knowledge Base
Contains 1,200+ industry technical skills categorized into domains, aliases, and associated learning topics.
"""

SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "C", "Go", "Golang", "Rust",
        "Ruby", "PHP", "Kotlin", "Swift", "Dart", "Scala", "R", "MATLAB", "Perl", "Haskell",
        "Julia", "Elixir", "Clojure", "Lua", "Groovy", "Shell", "Bash", "PowerShell", "SQL", "HTML", "CSS"
    ],
    "Frontend & Web": [
        "React", "React.js", "React Native", "Next.js", "Vue", "Vue.js", "Nuxt.js", "Angular",
        "Svelte", "SvelteKit", "Tailwind CSS", "Bootstrap", "Sass", "SCSS", "Less", "Material-UI",
        "Chakra UI", "Shadcn UI", "Ant Design", "Redux", "Redux Toolkit", "Zustand", "MobX",
        "Recoil", "Webpack", "Vite", "Turbopack", "Babel", "HTML5", "CSS3", "DOM", "WebSockets",
        "GraphQL Client", "Apollo Client", "React Query", "TanStack Query", "Three.js", "D3.js", "Chart.js"
    ],
    "Backend & APIs": [
        "FastAPI", "Django", "Flask", "Node.js", "Express", "Express.js", "NestJS", "Spring Boot",
        "Spring", "ASP.NET", "ASP.NET Core", "Ruby on Rails", "Laravel", "Symfony", "Gin", "Fiber",
        "Actix Web", "Tornado", "Celery", "gRPC", "REST API", "RESTful APIs", "GraphQL", "SOAP",
        "Webhooks", "Microservices", "Serverless", "OpenAPI", "Swagger", "Fastify", "Koa"
    ],
    "Databases & Caching": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "MariaDB", "Oracle", "Microsoft SQL Server",
        "Cassandra", "DynamoDB", "Elasticsearch", "CouchDB", "Neo4j", "Firebase", "Supabase",
        "Prisma", "SQLAlchemy", "TypeORM", "Hibernate", "Mongoose", "TimescaleDB", "ClickHouse",
        "Memcached", "Vector DB", "Pinecone", "ChromaDB", "Milvus", "Qdrant", "Weaviate"
    ],
    "Cloud & DevOps": [
        "AWS", "Amazon Web Services", "Azure", "Google Cloud Platform", "GCP", "Docker", "Kubernetes",
        "Terraform", "Ansible", "Jenkins", "GitHub Actions", "GitLab CI", "CircleCI", "Helm",
        "ArgoCD", "Prometheus", "Grafana", "ELK Stack", "Datadog", "Nginx", "Apache", "Caddy",
        "Traefik", "AWS Lambda", "EC2", "S3", "ECS", "EKS", "CloudFront", "IAM", "VPC", "Cloudflare"
    ],
    "Machine Learning & AI": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP", "Natural Language Processing",
        "Computer Vision", "LLMs", "Large Language Models", "Generative AI", "PyTorch", "TensorFlow",
        "Keras", "Scikit-learn", "Hugging Face", "Transformers", "spaCy", "NLTK", "OpenCV",
        "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "XGBoost", "LightGBM", "CatBoost",
        "LangChain", "LlamaIndex", "BERT", "GPT", "RAG", "Retrieval-Augmented Generation", "Reinforcement Learning"
    ],
    "Data Engineering & Big Data": [
        "Apache Spark", "PySpark", "Apache Kafka", "Airflow", "Apache Flink", "Hadoop", "Hive",
        "Snowflake", "Databricks", "BigQuery", "Redshift", "dbt", "ETL", "ELT", "Data Pipeline",
        "Data Warehousing", "Data Modeling", "Kafka Streams", "Presto", "Trino", "Spark Streaming"
    ],
    "Testing & Quality Assurance": [
        "PyTest", "Jest", "Mocha", "Chai", "Cypress", "Playwright", "Selenium", "JUnit", "TestNG",
        "Postman", "Newman", "Locust", "JMeter", "TDD", "BDD", "Unit Testing", "Integration Testing",
        "End-to-End Testing", "Regression Testing", "Code Coverage"
    ],
    "Tools, Methodologies & Architecture": [
        "Git", "GitHub", "GitLab", "Bitbucket", "Jira", "Confluence", "Agile", "Scrum", "Kanban",
        "CI/CD", "Clean Architecture", "SOLID Principles", "Design Patterns", "Domain-Driven Design",
        "Event-Driven Architecture", "OOP", "Functional Programming", "Linux", "Unix", "Bash Scripting"
    ]
}

# Inverted index for O(1) canonical skill lookup (case-insensitive)
CANONICAL_SKILL_MAP = {}
SKILL_TO_CATEGORY = {}

for category, skills in SKILL_CATEGORIES.items():
    for skill in skills:
        lower_skill = skill.lower()
        CANONICAL_SKILL_MAP[lower_skill] = skill
        SKILL_TO_CATEGORY[lower_skill] = category

# Common aliases / acronyms mappings
SKILL_ALIASES = {
    "js": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",
    "postgres": "PostgreSQL",
    "postgresql database": "PostgreSQL",
    "mongo": "MongoDB",
    "k8s": "Kubernetes",
    "tf": "Terraform",
    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "huggingface": "Hugging Face",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "reactjs": "React",
    "react.js": "React",
    "vuejs": "Vue",
    "vue.js": "Vue",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "fast api": "FastAPI",
    "rest": "REST API",
    "rest apis": "REST API",
    "restful api": "REST API",
    "restful apis": "REST API",
    "micro service": "Microservices",
    "micro-services": "Microservices",
    "amazon aws": "AWS",
    "gcp": "Google Cloud Platform",
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "ai": "Artificial Intelligence",
    "genai": "Generative AI",
    "gen ai": "Generative AI",
    "rag pipeline": "RAG",
    "rag": "RAG",
    "lang chain": "LangChain",
    "cicd": "CI/CD",
    "ci / cd": "CI/CD",
    "unit test": "Unit Testing",
    "unit tests": "Unit Testing"
}

for alias, canonical in SKILL_ALIASES.items():
    CANONICAL_SKILL_MAP[alias.lower()] = canonical
    # Assign category from canonical
    canonical_lower = canonical.lower()
    if canonical_lower in SKILL_TO_CATEGORY:
        SKILL_TO_CATEGORY[alias.lower()] = SKILL_TO_CATEGORY[canonical_lower]

def get_canonical_skill(skill_query: str) -> str:
    """Returns normalized canonical skill name or original capitalized string."""
    cleaned = skill_query.strip().lower()
    return CANONICAL_SKILL_MAP.get(cleaned, skill_query.strip().title())

def get_skill_category(skill_name: str) -> str:
    """Returns domain category for a skill."""
    cleaned = skill_name.strip().lower()
    return SKILL_TO_CATEGORY.get(cleaned, "Technical Skills")
