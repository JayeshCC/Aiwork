# 🤝 Contributing to AIWork

Thank you for your interest in contributing to AIWork! This document provides guidelines and instructions for contributing to the project.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Setup](#development-setup)
3. [Code Style](#code-style)
4. [Testing](#testing)
5. [Pull Request Process](#pull-request-process)
6. [Areas for Contribution](#areas-for-contribution)
7. [Community Guidelines](#community-guidelines)

---

## Getting Started

### Ways to Contribute

There are many ways to contribute to AIWork:

- 🐛 **Report Bugs**: Found a bug? Open an issue with details
- ✨ **Request Features**: Have an idea? Share it in discussions
- 📝 **Improve Documentation**: Fix typos, add examples, clarify concepts
- 🔧 **Submit Code**: Fix bugs, implement features, optimize performance
- 💡 **Share Examples**: Create agent templates or workflow patterns
- 🎓 **Help Others**: Answer questions in discussions
- 📊 **Performance Testing**: Benchmark on different hardware

### Before You Start

1. **Check Existing Issues**: Someone might already be working on it
2. **Read the Docs**: Familiarize yourself with the codebase
3. **Join Discussions**: Share your ideas before major changes
4. **Start Small**: First contribution? Try fixing documentation or small bugs

---

## Development Setup

### Prerequisites

- **Python**: 3.8 or higher
- **Git**: For version control
- **GitHub Account**: To submit pull requests
- **IDE**: VS Code, PyCharm, or your preferred editor

### Step 1: Fork and Clone

```bash
# Fork the repository on GitHub first, then:

# Clone your fork
git clone https://github.com/YOUR_USERNAME/Aiwork.git
cd Aiwork

# Add upstream remote
git remote add upstream https://github.com/JayeshCC/Aiwork.git
```

### Step 2: Create Development Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy
```

### Step 3: Verify Setup

```bash
# Run tests
pytest

# Run examples
python examples/quickstart.py
```

### Step 4: Create Feature Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch Naming:**
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation changes
- `test/` - Test additions/fixes
- `refactor/` - Code refactoring

---

## Code Style

We follow Python best practices and PEP 8 with some customizations.

### Python Style Guidelines

#### 1. Use Type Hints

```python
# ✅ Good
def process_data(data: Dict[str, Any]) -> List[str]:
    return list(data.keys())

# ❌ Bad
def process_data(data):
    return list(data.keys())
```

#### 2. Write Docstrings

```python
# ✅ Good
def execute_task(self, context: Dict[str, Any]) -> Any:
    """
    Executes the task with retry logic and guardrails.
    
    Args:
        context: Execution context containing inputs and outputs
        
    Returns:
        Task execution result
        
    Raises:
        ValueError: If task has no handler
        Exception: If all retry attempts fail
    """
    # Implementation...

# ❌ Bad (no docstring)
def execute_task(self, context):
    # Implementation...
```

#### 3. Follow PEP 8

```python
# ✅ Good: Clear naming, proper spacing
class TaskExecutor:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.tasks_executed = 0
    
    def execute(self, task: Task) -> Result:
        """Execute task with retries."""
        for attempt in range(self.max_retries):
            try:
                return task.run()
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                continue

# ❌ Bad: Poor naming, inconsistent spacing
class te:
    def __init__(self,mr=3):
        self.mr=mr
        self.te=0
    def ex(self,t):
        for i in range(self.mr):
            try:return t.run()
            except:
                if i==self.mr-1:raise
                continue
```

### Code Formatting

We use **Black** for automatic formatting:

```bash
# Format code
black src/

# Check formatting without changes
black --check src/
```

**Configuration** (`.black.toml`):
```toml
[tool.black]
line-length = 100
target-version = ['py38']
include = '\.pyi?$'
```

### Linting

We use **flake8** for linting:

```bash
# Run flake8
flake8 src/

# With specific rules
flake8 src/ --max-line-length=100 --ignore=E203,W503
```

### Type Checking

We use **mypy** for static type checking:

```bash
# Run mypy
mypy src/

# Specific module
mypy src/aiwork/core/
```

---

## Testing

### Test Structure

Tests are organized in the `tests/` directory:

```
tests/
├── test_agent.py          # Agent tests
├── test_task.py           # Task tests
├── test_flow.py           # Flow tests
├── test_orchestrator.py   # Orchestrator tests
├── test_integrations.py   # Integration tests
├── test_memory.py         # Memory tests
└── conftest.py           # Shared fixtures
```

### Writing Tests

#### Basic Test Example

```python
import pytest
from aiwork.core.task import Task

def test_task_creation():
    """Test task creation with basic parameters."""
    task = Task(name="test_task", handler=lambda ctx: {"result": "success"})
    
    assert task.name == "test_task"
    assert task.status == "PENDING"
    assert task.handler is not None

def test_task_execution():
    """Test task execution returns expected result."""
    def handler(ctx):
        return {"value": 42}
    
    task = Task("test", handler=handler)
    result = task.execute({})
    
    assert result["value"] == 42
    assert task.status == "COMPLETED"

def test_task_retry_logic():
    """Test task retries on failure."""
    attempt_count = 0
    
    def failing_handler(ctx):
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise Exception("Temporary failure")
        return {"success": True}
    
    task = Task("retry_test", handler=failing_handler, retries=3)
    result = task.execute({})
    
    assert attempt_count == 3
    assert result["success"] is True
```

#### Testing with Fixtures

```python
# In conftest.py
import pytest
from aiwork.core.agent import Agent
from aiwork.core.memory import VectorMemory

@pytest.fixture
def sample_agent():
    """Provides a sample agent for testing."""
    memory = VectorMemory()
    return Agent(
        role="Test Agent",
        goal="Test goal",
        backstory="Test backstory",
        memory=memory
    )

@pytest.fixture
def sample_context():
    """Provides sample execution context."""
    return {
        "inputs": {"data": "test"},
        "outputs": {}
    }

# In test file
def test_agent_with_fixture(sample_agent, sample_context):
    """Test agent using fixtures."""
    result = sample_agent.execute_task("Test task", sample_context)
    assert result is not None
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run specific test
pytest tests/test_agent.py::test_agent_creation

# Run with coverage
pytest --cov=src/aiwork --cov-report=html

# Run with verbose output
pytest -v

# Run only failed tests from last run
pytest --lf

# Run tests matching pattern
pytest -k "test_task"
```

### Test Coverage Requirements

- **Minimum Coverage**: 80% for new code
- **Critical Paths**: 100% coverage for core components
- **Integration Tests**: Required for new integrations

**Check Coverage:**

```bash
# Generate coverage report
pytest --cov=src/aiwork --cov-report=term-missing

# Generate HTML report
pytest --cov=src/aiwork --cov-report=html
open htmlcov/index.html  # View in browser
```

---

## Pull Request Process

### 1. Prepare Your Changes

```bash
# Make sure you're on your feature branch
git checkout feature/your-feature-name

# Make your changes and commit
git add .
git commit -m "feat: Add new feature description"

# Keep your branch updated
git fetch upstream
git rebase upstream/main
```

### 2. Commit Message Format

Follow **Conventional Commits** format:

```
<type>(<scope>): <short description>

<longer description if needed>

<footer if needed>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding/updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Examples:**

```bash
# Feature
git commit -m "feat(core): Add guardrail validation to tasks"

# Bug fix
git commit -m "fix(orchestrator): Fix cycle detection in DAG"

# Documentation
git commit -m "docs(readme): Update installation instructions"

# Test
git commit -m "test(agent): Add tests for memory integration"
```

### 3. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name
```

Then on GitHub:
1. Go to your fork
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template

### 4. PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manually tested

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### 5. Review Process

1. **Automated Checks**: Must pass all CI checks
2. **Code Review**: At least one maintainer approval required
3. **Testing**: All tests must pass
4. **Documentation**: Updated if needed

**Responding to Feedback:**

```bash
# Make requested changes
git add .
git commit -m "address review feedback"
git push origin feature/your-feature-name
```

### 6. Merge

Once approved:
- Maintainers will merge your PR
- Your contribution will be in the next release!
- You'll be added to contributors list

---

## Areas for Contribution

### High Priority

#### 1. Real OpenVINO Implementation

**Status**: Currently stub implementation  
**Difficulty**: Medium  
**Impact**: High

**What to do:**
```python
# Replace stub in src/aiwork/integrations/openvino_adapter.py
from openvino.runtime import Core

class OpenVINOAdapter:
    def __init__(self, model_path: str):
        self.core = Core()
        self.model = self.core.read_model(model_path)
        self.compiled = self.core.compile_model(self.model, "CPU")
    
    def infer(self, inputs: dict) -> dict:
        result = self.compiled(inputs)
        return result
```

#### 2. Real Kafka Implementation

**Status**: Currently stub implementation  
**Difficulty**: Medium  
**Impact**: High

**What to do:**
```python
# Replace stub in src/aiwork/integrations/kafka_adapter.py
from confluent_kafka import Producer, Consumer

class KafkaAdapter:
    def __init__(self, bootstrap_servers: str):
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers
        })
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': 'aiwork-workers'
        })
```

#### 3. More Agent Examples

**Status**: Only 2 reference agents  
**Difficulty**: Low  
**Impact**: Medium

**Ideas:**
- Data analysis agent (pandas + visualization)
- Code review agent (AST parsing + suggestions)
- Email automation agent (IMAP + templates)
- Web scraper agent (BeautifulSoup + storage)

### Medium Priority

#### 4. Performance Optimizations

**Areas:**
- Parallel task execution for independent tasks
- Connection pooling for Redis/Kafka
- Streaming large datasets
- Memory optimization for long-running flows

#### 5. Enhanced Memory System

**Current**: Simple TF-IDF similarity  
**Improvement**: Embedding-based semantic search

```python
# Use sentence transformers
from sentence_transformers import SentenceTransformer

class SemanticMemory:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = []
        self.texts = []
    
    def add(self, text: str):
        embedding = self.model.encode(text)
        self.embeddings.append(embedding)
        self.texts.append(text)
```

#### 6. CLI Tool

**Create**: `aiwork` command-line tool

```bash
# Commands
aiwork init my-project
aiwork run workflow.yaml
aiwork deploy --docker
aiwork benchmark
```

### Low Priority (Nice to Have)

- Web UI for flow visualization
- Agent marketplace/templates
- Workflow designer (drag & drop)
- Multi-agent collaboration patterns
- Advanced observability (traces, spans)

---

## Community Guidelines

### Code of Conduct

- **Be Respectful**: Treat everyone with respect
- **Be Constructive**: Focus on improving the project
- **Be Patient**: Remember everyone was a beginner once
- **Be Open**: Welcome to diverse perspectives
- **Be Professional**: Keep discussions technical and friendly

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Pull Requests**: Code contributions
- **Email**: For private/sensitive matters

### Getting Help

**Stuck? Here's how to get help:**

1. **Check Documentation**: Read the [User Guide](docs/USER_GUIDE.md)
2. **Search Issues**: Someone might have had the same problem
3. **Ask in Discussions**: Community is here to help
4. **Open an Issue**: For bugs or unclear documentation

**When asking for help, include:**
- What you're trying to do
- What you tried
- What happened (error messages, logs)
- Your environment (OS, Python version)

---

## Recognition

### Contributors

All contributors are recognized in:
- `CONTRIBUTORS.md` file
- GitHub contributors page
- Release notes for their contributions

### Types of Recognition

- **Code Contributors**: Implemented features, fixed bugs
- **Documentation Contributors**: Improved docs, added examples
- **Community Contributors**: Helped others, reported bugs
- **Reviewers**: Reviewed PRs, provided feedback

---

## Getting Started Checklist

Ready to contribute? Follow this checklist:

- [ ] Forked and cloned the repository
- [ ] Created development environment
- [ ] Read the documentation (especially [User Guide](docs/USER_GUIDE.md))
- [ ] Ran the test suite successfully
- [ ] Chose something to work on (issue or feature)
- [ ] Created a feature branch
- [ ] Made changes following style guide
- [ ] Added/updated tests
- [ ] Ran tests and linting
- [ ] Updated documentation if needed
- [ ] Committed with conventional commit messages
- [ ] Pushed to your fork
- [ ] Created pull request
- [ ] Responded to review feedback

---

## Questions?

Have questions about contributing? Feel free to:

- Open a discussion on GitHub
- Comment on an existing issue
- Reach out to maintainers

**Thank you for contributing to AIWork! 🚀**

---

<div align="center">
  <sub>Built with ❤️ for the Intel AI Innovation Challenge 2024</sub>
</div>
