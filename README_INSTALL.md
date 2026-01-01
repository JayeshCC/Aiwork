# Installation Guide

## Quick Install

```bash
# Clone the repository
git clone https://github.com/JayeshCC/Aiwork.git
cd Aiwork

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .

# Verify installation
python -c "from aiwork import Task, Flow, Orchestrator; print('✅ AIWork installed successfully!')"
```

## Install with Intel Optimizations

```bash
pip install -e ".[intel]"
```

## Install Development Tools

```bash
pip install -e ".[dev]"
```

## Running Examples

After installation, examples work without path hacks:

```bash
# Quickstart
python examples/quickstart.py

# Document Processor Agent
python examples/agents/document_processor/run.py

# Customer Support Agent
python examples/agents/customer_support/run.py
```

## Troubleshooting

**Import errors?**
```bash
# Make sure you're in the virtual environment
source .venv/bin/activate

# Reinstall
pip install -e .
```

**Missing dependencies?**
```bash
pip install -r requirements.txt
```
