You are an expert academic editor, Computational Linguistics researcher,
NLP researcher, and Scopus journal reviewer specializing in:

- Natural Language Processing
- Computational Morphology
- Low-Resource Languages
- Linguistic Resources
- Morphological Analysis
- Language Documentation
- Experimental Evaluation and Reproducible Research

I have uploaded a research manuscript about SasakNLP.

Your task is to critically review and improve the manuscript to make it
scientifically rigorous and suitable for submission to an international
Scopus-indexed Q3 journal.

IMPORTANT:
Do NOT invent experimental results, datasets, accuracy values,
linguistic rules, dialect data, annotations, or citations.

Use ONLY information that is actually supported by the uploaded manuscript
and available research artifacts.

If information is missing, inconsistent, unsupported, or unclear:

1. Clearly identify the problem.
2. Mark it as [REQUIRES AUTHOR VERIFICATION].
3. Provide a recommended structure or placeholder.
4. Do NOT fabricate the missing result.

The goal is scientific integrity and reproducibility.

====================================================
1. PAPER CONTEXT
====================================================

The manuscript presents:

SasakNLP:
A Hybrid Framework for Morphological Processing of the
Low-Resource Sasak Language

The research focuses on:

- Low-resource language NLP
- Sasak language
- Morphological processing
- Dictionary-enhanced stemming
- Morphological analysis
- Candidate generation
- Lexicon validation
- Candidate ranking
- Dialect-aware architecture
- Open-source NLP resources

The proposed system integrates:

Linguistic Rules
+
Morphological Lexicon
+
Candidate Generation
+
Lexicon Validation
+
Candidate Ranking
+
Dialect-Aware Processing

====================================================
2. PRIMARY OBJECTIVE
====================================================

Improve the manuscript into a scientifically rigorous,
Q3-ready international journal paper.

The revision must focus on:

1. Scientific consistency
2. Experimental validity
3. Reproducibility
4. Novelty clarity
5. Evaluation rigor
6. Dataset transparency
7. Avoiding unsupported claims
8. Stronger discussion and error analysis

====================================================
3. CRITICAL TASK: RESULT CONSISTENCY AUDIT
====================================================

Perform a complete audit of ALL numerical results in the manuscript.

Create a table:

| Metric | Abstract | Results Section | Tables | Figures | Conclusion | Status |
|--------|----------|-----------------|--------|---------|------------|--------|

Check especially:

- Accuracy
- Morphological disambiguation accuracy
- Lemmatization accuracy
- Precision
- Recall
- F1-score
- Overstemming rate
- Understemming rate
- OOV rate
- Dataset size
- Number of lexical entries
- Number of benchmark samples
- Number of dialects
- Number of rules

Identify every contradiction.

For every contradiction:

DO NOT choose a value automatically.

Instead write:

[REQUIRES AUTHOR VERIFICATION]

Then explain:

- Which values conflict
- Where they appear
- What experimental definition must be clarified

Example:

Metric:
Morphological Accuracy

Abstract:
87.98%

Results Table:
80.44%

Status:
[REQUIRES AUTHOR VERIFICATION]

Required clarification:
Determine whether these represent different evaluation tasks,
such as morphological disambiguation accuracy versus exact
lemmatization accuracy.

====================================================
4. REWRITE THE ABSTRACT
====================================================

Rewrite the abstract according to international journal standards.

Structure:

BACKGROUND
→ Explain the low-resource NLP problem.

RESEARCH GAP
→ Explain the lack of computational morphological resources.

METHOD
→ Explain the hybrid framework.

CONTRIBUTIONS
→ Clearly state the contributions.

EVALUATION
→ Report ONLY verified experimental results.

IMPACT
→ Explain the importance for low-resource language technology.

IMPORTANT:

Do not include conflicting numbers.

If the final verified metrics are unavailable, use:

"[VERIFIED RESULT TO BE INSERTED]"

Do not fabricate values.

Target length:

200–250 words.

====================================================
5. STRENGTHEN THE NOVELTY
====================================================

Rewrite the novelty and contribution section.

Clearly distinguish the contributions from existing:

- Rule-based stemmers
- Dictionary-based approaches
- Morphological analyzers
- Existing Sasak language computational research

Use the following contribution structure:

C1. Linguistic Resource

Development of SasakLex as a structured,
machine-readable lexical resource.

C2. Hybrid Morphological Framework

Integration of:

- linguistic rules
- candidate generation
- lexicon validation
- candidate ranking

C3. Morphological Analysis

The system performs not only stemming but structured
morphological analysis.

C4. Dialect-Aware Architecture

A configurable architecture for supporting dialect-specific
processing.

IMPORTANT:

Do not claim that dialect-aware processing improves performance
unless experimental evidence demonstrates it.

C5. Open Research Infrastructure

Open-source implementation and reproducible research artifacts.

Rewrite these contributions in a concise,
scientifically defensible form.

====================================================
6. DATASET TRANSPARENCY AUDIT
====================================================

Critically analyze the relationship between:

- SasakLex lexical entries
- 100,000 benchmark samples
- authentic corpus data
- synthetic data
- semi-synthetic data
- evaluation dataset

Answer:

1. How were the 100,000 samples created?
2. Are they authentic words?
3. Are they generated using morphological rules?
4. Are they manually annotated?
5. Are they derived from the same lexicon used by the system?
6. Is there potential data leakage?
7. Are development and testing data independent?

If the manuscript does not provide enough information,
mark the relevant sections:

[REQUIRES AUTHOR VERIFICATION]

Then propose a scientifically transparent dataset description.

====================================================
7. IMPROVE BENCHMARK DESIGN
====================================================

Recommend a two-level benchmark architecture.

DATASET A:
Controlled Morphological Benchmark

Purpose:

- Test morphological rule coverage
- Evaluate affix processing
- Test candidate generation

Clearly label whether it is:

- synthetic
- semi-synthetic
- authentic

DATASET B:
Authentic Human-Annotated Test Set

Purpose:

- Real-world evaluation
- Independent evaluation
- Generalization testing

Recommended fields:

surface_form
lemma
prefix
infix
suffix
dialect
source
annotation_status

IMPORTANT:

Do not invent the size of Dataset B.

Use:

[AUTHOR TO PROVIDE DATASET SIZE]

if necessary.

====================================================
8. ADD ABLATION STUDY
====================================================

Design an ablation study that demonstrates the contribution
of each component.

Use this experimental structure:

Model A:
Greedy Rule-Based Stripping

Model B:
Rule-Based + Lexicon Validation

Model C:
Rule-Based + Candidate Generation

Model D:
Rule-Based + Candidate Generation + Candidate Ranking

Model E:
Full Hybrid SasakNLP

If dialect-aware processing is experimentally available:

Model F:
Full Hybrid SasakNLP + Dialect-Aware Processing

Create the table:

| Model | Rules | Lexicon | Candidate Generation | Ranking | Dialect-Aware | Accuracy | F1 |
|------|------|---------|----------------------|---------|---------------|----------|----|

IMPORTANT:

Do not fabricate Accuracy or F1 values.

Use:

[RESULT TO BE INSERTED]

Explain exactly how the author should conduct the experiment.

====================================================
9. DIALECT-AWARE EVALUATION
====================================================

Audit all dialect-related claims.

Check:

- Number of dialects
- Dialect names
- Dialect classification
- Source of dialect taxonomy
- Dataset distribution
- Evaluation methodology

Identify inconsistent dialect terminology.

Then design the following experiment:

Experiment A:
Dialect-Agnostic Processing

Experiment B:
Dialect-Aware Processing

Compare:

| System | Overall Accuracy | Per-Dialect Accuracy | Macro F1 |
|--------|------------------|----------------------|----------|
| Dialect-Agnostic | [RESULT] | [RESULT] | [RESULT] |
| Dialect-Aware | [RESULT] | [RESULT] | [RESULT] |

IMPORTANT:

If this experiment has not actually been performed,
do not claim performance improvement.

Instead recommend either:

Option 1:
Conduct the experiment.

OR

Option 2:
Remove "Dialect-Aware" from the title and major claims,
and describe it only as an extensible architecture.

====================================================
10. ADD EXPERIMENTAL SETUP
====================================================

Create a complete section:

"Experimental Setup and Reproducibility"

Include:

### Software Environment

- Python version
- Operating system
- Main libraries
- Package version

### Hardware

- CPU
- RAM

### Dataset

- Training/development data
- Validation data
- Test data

### Evaluation Protocol

- Ground-truth definition
- Dataset split
- Number of runs
- Random seed

### Reproducibility

- Source code repository
- Dataset repository
- Installation instructions
- Experiment scripts

IMPORTANT:

If the manuscript does not provide hardware or environment
information, mark:

[REQUIRES AUTHOR VERIFICATION]

Do not invent specifications.

====================================================
11. HUMAN ANNOTATION AND VALIDATION
====================================================

Evaluate whether the manuscript sufficiently explains
human linguistic validation.

If not, propose a section:

"Annotation and Linguistic Validation"

Include:

- Number of annotators
- Native speakers
- Linguistic experts
- Annotation guidelines
- Annotation procedure
- Conflict resolution

If multiple annotators exist, recommend measuring:

- Cohen's Kappa

or another appropriate agreement metric.

IMPORTANT:

Do not fabricate annotator numbers or agreement scores.

====================================================
12. ERROR ANALYSIS
====================================================

Create a rigorous error analysis section.

Use categories:

1. Correct Lemmatization
2. Overstemming
3. Understemming
4. Incorrect Lemma
5. OOV Error
6. Candidate Ranking Error
7. Morphological Ambiguity
8. Dialect Mismatch

Create a table:

| Error Type | Definition | Example | Frequency | Recommended Improvement |
|------------|------------|---------|-----------|--------------------------|

Do not invent frequencies.

Use:

[RESULT TO BE INSERTED]

for missing experimental data.

====================================================
13. IMPROVE CLAIMS
====================================================

Identify overly strong claims such as:

- "first"
- "novel"
- "research-grade"
- "state-of-the-art"
- "complete NLP framework"

Replace unsupported claims with academically safe language.

Example:

Instead of:

"This is the first NLP toolkit for Sasak."

Use:

"To the best of our knowledge, this work presents one of the
first publicly available open-source computational morphological
processing toolkits specifically designed for the Sasak language."

Only use such wording if supported by the literature review.

====================================================
14. REWRITE THE METHODOLOGY
====================================================

Rewrite the methodology with this structure:

3. Methodology

3.1 Research Overview

3.2 SasakLex Construction

3.3 Morphological Rule Design

3.4 Hybrid Morphological Processing Framework

3.5 Candidate Generation

3.6 Lexicon Validation

3.7 Candidate Ranking

3.8 Dialect-Aware Architecture

3.9 Morphological Analysis Output

3.10 Experimental Design

The methodology must clearly distinguish:

- what is implemented
- what is experimentally evaluated
- what is proposed as future extensibility

====================================================
15. REWRITE RESULTS AND DISCUSSION
====================================================

Separate:

4. Results

and

5. Discussion

RESULTS should contain:

- objective experimental findings
- tables
- metrics
- comparisons

DISCUSSION should explain:

- why the system works
- which components contribute most
- limitations
- comparison with prior research
- implications for low-resource NLP

Avoid repeating the same information.

====================================================
16. ADD LIMITATIONS SECTION
====================================================

Create:

"Limitations"

Discuss only limitations supported by the manuscript.

Possible categories include:

- Limited lexical coverage
- Limited authentic corpus
- Dialect coverage
- OOV words
- Rule-based dependency
- Annotation limitations

Do not invent limitations.

Clearly distinguish:

CURRENT LIMITATIONS

and

FUTURE WORK.

====================================================
17. FINAL PAPER STRUCTURE
====================================================

Recommend this structure:

1. Introduction

2. Related Work

3. Methodology

4. Experimental Setup

5. Results

6. Discussion

7. Limitations

8. Conclusion

Ensure each section has a clear purpose.

====================================================
18. TITLE REVIEW
====================================================

Evaluate whether the title accurately reflects the actual
experimental evidence.

Preferred title if dialect-aware performance is validated:

"SasakNLP: A Hybrid Dialect-Aware Framework for Morphological
Processing of the Low-Resource Sasak Language"

Preferred title if dialect-aware processing is only an architecture:

"SasakNLP: A Hybrid Framework for Morphological Processing
of the Low-Resource Sasak Language"

Recommend the scientifically safest title based on the
actual manuscript evidence.

====================================================
19. FINAL REVIEWER SIMULATION
====================================================

Act as three anonymous Scopus journal reviewers.

Reviewer 1:
Computational NLP Expert

Reviewer 2:
Computational Linguistics and Morphology Expert

Reviewer 3:
Reproducibility and Research Data Expert

For each reviewer provide:

- Major strengths
- Major concerns
- Minor concerns
- Required revisions

Then provide:

EDITORIAL DECISION SIMULATION:

[ ] Accept
[ ] Minor Revision
[ ] Major Revision
[ ] Reject and Resubmit

Explain the most likely decision.

====================================================
20. FINAL OUTPUT FORMAT
====================================================

Provide the output in this order:

A. Executive Summary

B. Manuscript Strengths

C. Critical Problems

D. Result Consistency Audit Table

E. Dataset and Benchmark Audit

F. Revised Novelty and Contributions

G. Revised Abstract

H. Revised Methodology Structure

I. Proposed Experimental Setup

J. Ablation Study Design

K. Dialect-Aware Evaluation Design

L. Error Analysis Framework

M. Limitations Section

N. Recommended Title

O. Reviewer Simulation

P. Final Q3 Readiness Score

Score each category:

Novelty: /10
Methodology: /10
Dataset: /10
Evaluation: /10
Reproducibility: /10
Writing Quality: /10
Q3 Readiness: /10

Finally provide:

1. MUST FIX BEFORE SUBMISSION
2. STRONGLY RECOMMENDED
3. OPTIONAL IMPROVEMENTS

The most important rule:

NEVER fabricate research data, accuracy values, citations,
experiments, linguistic rules, or validation results.

Scientific integrity is more important than making the
paper appear stronger.