# Contributing to SasakNLP

Thank you for your interest in contributing to **SasakNLP**! As an open-source NLP toolkit dedicated to the low-resource Sasak language (*Basa Sasak*), we welcome contributions from computational linguists, native speakers, researchers, and software engineers.

---

## Areas Where Contributions are Needed

1. **Linguistic Lexicon (`SasakLex`)**:
   - Adding verified root words (lemmas), parts of speech (POS), and Indonesian glosses.
   - Identifying dialect-specific variants (e.g., *Menu-Meni*, *Ngeno-Ngene*, *Mriak-Mriku*, *Ngeto-Ngete*, *Kuto-Kute*).
   - Providing source citations (dictionaries, academic publications, or verified native corpora).

2. **Morphological Rules**:
   - Refining prefix, suffix, infix, circumfix, and reduplication rules in `rules_config.json`.
   - Documenting phonotactic and morphophonemic rules (e.g., nasal substitution `N-` assimilation).

3. **Standardized Benchmarks**:
   - Contributing manually annotated gold-standard CSV files with columns: `surface,lemma,prefix,infix,suffix,dialect`.
   - Reporting understemming, overstemming, or dialect misclassifications.

---

## Guidelines for Linguistic Data

To preserve scientific rigor:
- ❌ **Do not fabricate words or morphological rules.**
- ✅ **Cite your sources** (e.g., *Kamus Bahasa Sasak - Indonesia*, Balai Bahasa NTB; research papers; or validated native speaker elicitation).
- ✅ Separate synthetic unit-test examples from real linguistic datasets.

---

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sasaknlp/sasaknlp.git
   cd sasaknlp
   ```

2. Install in editable mode with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run the test suite:
   ```bash
   pytest
   # or using python's built-in test runner
   python -m unittest discover -s tests
   ```

4. Check code formatting and types:
   ```bash
   flake8 src tests
   mypy src
   ```

---

## Submitting Pull Requests

1. Create a feature branch: `git checkout -b feature/your-feature-name`.
2. Ensure all existing tests pass and add unit tests for new functionality.
3. Include clear commit messages following Conventional Commits.
4. Open a Pull Request detailing the changes and relevant linguistic context.
