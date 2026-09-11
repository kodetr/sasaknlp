# Installation Guide for SasakNLP

## System Requirements

- Python 3.9, 3.10, 3.11, or 3.12
- Operating System: Linux, macOS, or Windows
- No heavy external C++ or CUDA dependencies are required. Core functionality runs purely on standard Python.

---

## 1. Installation via PyPI (Recommended for Users)

Once published to PyPI, install using `pip`:

```bash
pip install sasaknlp
```

---

## 2. Installation from Source (Recommended for Developers & Researchers)

Clone the repository and install in editable development mode:

```bash
# Clone the repository
git clone https://github.com/sasaknlp/sasaknlp.git
cd sasaknlp

# Create and activate a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in editable mode with development tools
pip install -e ".[dev]"
```

---

## 3. Verifying Installation

Verify that the library and command-line interface are correctly configured:

```bash
# Verify Python import
python3 -c "import sasaknlp; print('SasakNLP version:', sasaknlp.__version__)"

# Verify CLI tool
sasaknlp --version
sasaknlp stem "tepinaq"
```
