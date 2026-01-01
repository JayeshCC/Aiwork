from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aiwork",
    version="0.1.0",
    author="JayeshCC",
    author_email="jayesh@example.com",  # Use placeholder
    description="Lightweight AI Agent Framework optimized for Intel hardware",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JayeshCC/Aiwork",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "numpy>=1.26.0",
        "pydantic>=2.0.0",
        "confluent-kafka>=2.3.0",
        "redis>=5.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "intel": [
            "openvino>=2024.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "aiwork-server=aiwork.api.server:start_server",
        ],
    },
)
