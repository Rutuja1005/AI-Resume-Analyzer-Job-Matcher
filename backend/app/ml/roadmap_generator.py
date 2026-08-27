from typing import List, Dict, Any
from app.ml.skill_ontology import get_skill_category

class SkillGapRoadmapGenerator:
    """
    Analyzes skill discrepancies between a candidate's profile and job requirements,
    assigning priority levels, technical rationales, and customized learning milestones.
    """

    SKILL_LEARNING_METADATA = {
        "Docker": {
            "importance": "High",
            "reason": "Essential for containerizing microservices, ensuring reproducible build environments, and CI/CD deployment pipelines.",
            "topic": "Docker Fundamentals, Multi-stage builds, Container Networking, and Docker Compose orchestration.",
            "url": "https://docs.docker.com/get-started/"
        },
        "Kubernetes": {
            "importance": "High",
            "reason": "Crucial for large-scale container orchestration, auto-scaling, ingress management, and self-healing cloud deployments.",
            "topic": "K8s Pods, Deployments, Services, ConfigMaps, Helm Charts, and Cluster Management.",
            "url": "https://kubernetes.io/docs/tutorials/"
        },
        "AWS": {
            "importance": "High",
            "reason": "The dominant cloud infrastructure provider; required for cloud-native architectures, serverless computing, and enterprise hosting.",
            "topic": "AWS Solutions Architecture: EC2, S3, RDS, Lambda, IAM, API Gateway, and CloudFront.",
            "url": "https://aws.amazon.com/training/"
        },
        "PostgreSQL": {
            "importance": "High",
            "reason": "Core relational database system powering modern transactional applications with ACID compliance and JSON support.",
            "topic": "Advanced SQL queries, Index optimization, Connection pooling, Transactions, and Schema migrations.",
            "url": "https://www.postgresql.org/docs/"
        },
        "Redis": {
            "importance": "Medium",
            "reason": "High-performance in-memory key-value store utilized for sub-millisecond caching, session storage, and rate limiting.",
            "topic": "Redis data structures, Pub/Sub messaging, Cache invalidation strategies, and distributed locking.",
            "url": "https://redis.io/docs/"
        },
        "FastAPI": {
            "importance": "High",
            "reason": "High-performance modern Python web framework standard for building asynchronous REST APIs and ML microservices.",
            "topic": "Async/Await endpoints, Pydantic data validation, Dependency Injection, and OpenAPI generation.",
            "url": "https://fastapi.tiangolo.com/tutorial/"
        },
        "React": {
            "importance": "High",
            "reason": "Industry-standard UI library for building interactive, component-driven client-side web applications.",
            "topic": "React Hooks (useEffect, useMemo), State management (Zustand/Redux), Component Lifecycle, and Performance optimization.",
            "url": "https://react.dev/learn"
        },
        "TypeScript": {
            "importance": "High",
            "reason": "Brings compile-time type safety, automated refactoring, and enterprise scalability to JavaScript applications.",
            "topic": "Generics, Interfaces vs Types, Utility Types, Strict Null Checking, and TS compiler configuration.",
            "url": "https://www.typescriptlang.org/docs/"
        },
        "GraphQL": {
            "importance": "Medium",
            "reason": "Provides a flexible query language allowing frontend clients to request exact data shapes without over-fetching.",
            "topic": "Schema Definition Language (SDL), Resolvers, Mutations, Subscriptions, and Apollo Client integration.",
            "url": "https://graphql.org/learn/"
        },
        "CI/CD": {
            "importance": "High",
            "reason": "Automates testing, linting, security audits, and production deployments on every code push.",
            "topic": "GitHub Actions workflows, build pipelines, automated test runs, and semantic versioning.",
            "url": "https://docs.github.com/en/actions"
        },
        "Terraform": {
            "importance": "Medium",
            "reason": "Declarative Infrastructure as Code (IaC) tool for provisioning repeatable cloud resources across AWS, GCP, and Azure.",
            "topic": "Terraform State management, Providers, Modules, Variables, and Plan/Apply lifecycles.",
            "url": "https://developer.hashicorp.com/terraform/tutorials"
        },
        "PyTest": {
            "importance": "Medium",
            "reason": "Premier testing framework in Python ensuring unit test coverage, mocking, fixtures, and API integration testing.",
            "topic": "Test Fixtures, Parameterized tests, Mocking HTTP clients, and Coverage reporting.",
            "url": "https://docs.pytest.org/en/stable/"
        },
        "Apache Kafka": {
            "importance": "High",
            "reason": "Distributed event streaming platform capable of handling trillions of event messages per day with low latency.",
            "topic": "Kafka Topics, Producers/Consumers, Partitioning strategies, Consumer Groups, and Schema Registry.",
            "url": "https://kafka.apache.org/documentation/"
        },
        "Machine Learning": {
            "importance": "High",
            "reason": "Core foundational knowledge required for training predictive statistical models and feature engineering pipelines.",
            "topic": "Supervised/Unsupervised learning, Cross-validation, Scikit-learn pipelines, and evaluation metrics.",
            "url": "https://scikit-learn.org/stable/tutorial/index.html"
        },
        "NLP": {
            "importance": "High",
            "reason": "Natural Language Processing methodologies for unstructured text parsing, tokenization, embeddings, and entity recognition.",
            "topic": "TF-IDF vectorization, Word2Vec, Transformer architectures, SpaCy pipelines, and sentiment analysis.",
            "url": "https://huggingface.co/learn/nlp-course"
        }
    }

    def generate_missing_skills_roadmap(self, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """Generates detailed, actionable learning items for each missing skill."""
        roadmap = []
        for skill in missing_skills:
            meta = self.SKILL_LEARNING_METADATA.get(skill)
            category = get_skill_category(skill)

            if meta:
                roadmap.append({
                    "skill_name": skill,
                    "importance": meta["importance"],
                    "reason": meta["reason"],
                    "suggested_learning_topic": meta["topic"],
                    "learning_resource_url": meta["url"]
                })
            else:
                # Dynamic generation based on category
                importance = "High" if category in ["Backend & APIs", "Frontend & Web", "Cloud & DevOps"] else "Medium"
                reason = f"Required in target job specification under {category} domain for core feature delivery."
                topic = f"Mastering {skill} fundamentals, architectural patterns, and production best practices."
                url = f"https://www.google.com/search?q={skill.replace(' ', '+')}+documentation+tutorial"

                roadmap.append({
                    "skill_name": skill,
                    "importance": importance,
                    "reason": reason,
                    "suggested_learning_topic": topic,
                    "learning_resource_url": url
                })

        # Sort: High importance first, then Medium, then Low
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        roadmap.sort(key=lambda x: priority_order.get(x["importance"], 3))
        return roadmap

roadmap_generator = SkillGapRoadmapGenerator()
