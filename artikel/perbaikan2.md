You are an expert academic editor, Scopus journal reviewer, Natural
Language Processing researcher, and Computational Linguistics researcher.

You have been given a research manuscript about SasakNLP.

Your task is to revise and prepare this manuscript for submission to
ECTI Transactions on Computer and Information Technology (ECTI-CIT).

The manuscript must be treated as the PRIMARY SOURCE.

IMPORTANT RULES:

1. Do not invent experimental results.
2. Do not invent accuracy values.
3. Do not invent datasets or dataset sizes.
4. Do not invent linguistic rules for the Sasak language.
5. Do not invent citations or references.
6. Do not silently resolve contradictory experimental results.
7. If information is inconsistent, missing, or unsupported, explicitly mark it:
   [AUTHOR VERIFICATION REQUIRED]
8. Preserve scientific integrity over improving the appearance of the paper.
9. Rewrite the manuscript in professional academic English.
10. Ensure that the revised manuscript is appropriate for a Computer Science,
    Artificial Intelligence, and Natural Language Processing journal.

====================================================
A. JOURNAL TARGET
====================================================

Target Journal:

ECTI Transactions on Computer and Information Technology
(ECTI-CIT)

The manuscript should be positioned primarily within:

Artificial Intelligence
→ Natural Language Processing

The paper should emphasize:

- Computational NLP
- Morphological processing
- Algorithmic framework
- Computational linguistic resources
- Low-resource language technology
- Experimental evaluation
- Reproducible software and research artifacts

DO NOT position the manuscript primarily as a traditional linguistics paper.

The central Computer Science contribution should be clear:

A computational framework for morphological processing of a
low-resource language using a hybrid combination of:

- Linguistic rules
- Lexical resources
- Candidate generation
- Lexicon validation
- Candidate ranking
- Optional dialect-aware processing

====================================================
B. PAPER TITLE AUDIT
====================================================

Review whether the current title accurately reflects the actual
experimental evidence.

Current candidate title:

"SasakNLP: A Hybrid Dialect-Aware Framework for Morphological
Processing of the Low-Resource Sasak Language"

IMPORTANT:

Only retain "Dialect-Aware" if the manuscript contains genuine,
verifiable experiments demonstrating dialect-aware processing.

If dialect awareness is currently only an extensible architecture,
configuration capability, or future capability, recommend the safer title:

"SasakNLP: A Hybrid Framework for Morphological Processing of the
Low-Resource Sasak Language"

Provide:

1. Recommended final title
2. Reason for the recommendation
3. Whether the title contains any unsupported claim

====================================================
C. SCOPE ALIGNMENT FOR ECTI-CIT
====================================================

Review the manuscript and ensure that every major section supports
its positioning as an NLP and Computer Science research paper.

Strengthen the following aspects:

1. Computational problem
2. Research gap
3. Algorithmic contribution
4. System architecture
5. Experimental methodology
6. Baseline comparison
7. Evaluation metrics
8. Reproducibility

Reduce unnecessary content that reads primarily as:

- General cultural description
- Excessive linguistic background
- Non-computational narrative

However, DO NOT delete important Sasak linguistic information required
to understand the computational morphology problem.

====================================================
D. DOUBLE-BLIND / ANONYMIZATION AUDIT
====================================================

Prepare the manuscript as an anonymous review version.

Identify and remove or anonymize:

- Author names
- Author affiliations
- Email addresses
- Personal websites
- Developer websites
- GitHub usernames that reveal author identity
- Personal project branding
- Repository ownership information
- Any identifying acknowledgments

Examples of identifying content include:

- kodetr.com
- github.com/[identifying username]/...
- Website Pengembang Utama
- Correspondence information
- Personal branding in headers or footers

Replace identifying repository information with appropriate anonymous wording.

For example:

"The source code and research artifacts are withheld during the
double-blind review process and will be made publicly available
upon acceptance."

IMPORTANT:

Do not remove legitimate methodological information.

====================================================
E. COMPLETE RESULT CONSISTENCY AUDIT
====================================================

Perform a complete audit of every numerical value in the manuscript.

Create the following table:

| Metric | Abstract | Main Text | Tables | Figures | Conclusion | Status |
|--------|----------|-----------|--------|---------|------------|--------|

Audit:

- Accuracy
- Morphological disambiguation accuracy
- Lemmatization accuracy
- Precision
- Recall
- F1-score
- Overstemming
- Understemming
- OOV rate
- Number of lexical entries
- Number of corpus sentences
- Number of benchmark samples
- Number of dialects
- Number of morphological rules

For every contradiction:

DO NOT automatically select one number.

Instead use:

[AUTHOR VERIFICATION REQUIRED]

Explain exactly:

1. Which values conflict
2. Where they occur
3. Whether they may represent different tasks
4. What definition or experiment must be clarified

Example:

Metric:
Accuracy

Abstract:
87.98%

Table:
80.44%

Status:
[AUTHOR VERIFICATION REQUIRED]

Possible explanation:
These may represent different evaluation tasks, such as
morphological disambiguation accuracy and exact lemmatization accuracy.

The author must confirm the definition of each metric.

====================================================
F. DATASET AND BENCHMARK TRANSPARENCY
====================================================

Audit the relationship between:

- SasakLex lexical entries
- Authentic corpus
- Morphological benchmark
- 100,000 benchmark pairs
- Generated data
- Synthetic data
- Semi-synthetic data
- Human annotation
- Evaluation data

Answer based ONLY on evidence in the manuscript:

1. How was each dataset constructed?
2. Which data are authentic?
3. Which data are generated?
4. Which data are manually validated?
5. How is the gold standard defined?
6. Is there a risk of data leakage?
7. Are training/development/test resources independent?

If the manuscript does not provide sufficient information:

[AUTHOR VERIFICATION REQUIRED]

DO NOT invent the dataset generation procedure.

====================================================
G. REWRITE DATASET DESCRIPTION
====================================================

Create a scientifically transparent dataset section.

Use the following structure:

3.X Data Resources

3.X.1 SasakLex

Explain:

- Number of verified entries
- Lexical fields
- Source
- Validation procedure

3.X.2 Authentic Corpus

Explain only information supported by the manuscript:

- Number of sentences
- Source
- Collection process
- Usage in experiments

3.X.3 Morphological Benchmark

Clearly classify the benchmark as:

[Authentic / Synthetic / Semi-Synthetic]

ONLY after evidence from the manuscript supports this classification.

If unclear:

[AUTHOR VERIFICATION REQUIRED]

Clearly explain how the benchmark was constructed.

====================================================
H. STRENGTHEN RESEARCH GAP
====================================================

Rewrite the Introduction around a strong computational research gap.

Recommended structure:

1. Low-resource language problem in NLP

2. Importance of morphological processing

3. Computational challenges for the Sasak language

4. Limitations of previous approaches

Possible limitations may include:

- Rule-based approaches with limited lexical resources
- Greedy affix stripping
- Lack of candidate validation
- Overstemming or understemming
- Lack of reusable computational resources

ONLY include these if supported by the manuscript and cited literature.

5. Research gap

Clearly explain what is missing.

6. Proposed solution

Introduce SasakNLP.

7. Research contributions

====================================================
I. REWRITE CONTRIBUTIONS
====================================================

Create a concise contribution section.

Use scientifically defensible wording.

Possible structure:

Contribution 1:
A structured machine-readable lexical resource for computational
morphological processing of the Sasak language.

Contribution 2:
A hybrid morphological processing framework integrating linguistic
rules, candidate generation, lexicon validation, and candidate ranking.

Contribution 3:
A structured morphological analysis pipeline extending beyond simple
stemming.

Contribution 4:
An extensible architecture for dialect-specific processing.

IMPORTANT:

Only describe dialect processing as a validated contribution if
experiments demonstrate it.

Otherwise describe it as:

"an extensible architecture designed to support future dialect-specific
processing."

Contribution 5:
Open and reproducible research infrastructure.

Only retain this contribution if the artifacts genuinely exist and can
be released according to the review policy.

====================================================
J. REWRITE THE ABSTRACT
====================================================

Rewrite the abstract in professional academic English.

Target length:

200–250 words.

Use:

1. Background
2. Research gap
3. Proposed method
4. Main contributions
5. Experimental evaluation
6. Implications

IMPORTANT:

Use ONLY verified experimental results.

If a result is contradictory:

[VERIFIED RESULT TO BE INSERTED]

Do not include unsupported numerical claims.

Avoid promotional language such as:

- revolutionary
- research-grade
- state-of-the-art
- first ever

unless scientifically proven.

====================================================
K. METHODOLOGY RESTRUCTURING
====================================================

Rewrite the methodology using the following structure:

3. Methodology

3.1 Research Overview

3.2 SasakLex Construction

3.3 Morphological Rule Representation

3.4 Hybrid Morphological Processing Framework

3.5 Candidate Generation

3.6 Lexicon Validation

3.7 Candidate Ranking

3.8 Morphological Analysis Output

3.9 Dialect-Specific Processing Architecture

3.10 System Implementation

Clearly distinguish:

IMPLEMENTED COMPONENTS

EXPERIMENTALLY EVALUATED COMPONENTS

FUTURE/EXTENSIBLE COMPONENTS

Do not present future capabilities as experimentally proven results.

====================================================
L. ADD EXPERIMENTAL SETUP
====================================================

Create a complete section:

4. Experimental Setup

Include:

4.1 Experimental Environment

- Operating system
- Python version
- Main libraries
- Hardware

If missing:

[AUTHOR VERIFICATION REQUIRED]

4.2 Datasets

Explain:

- Dataset source
- Dataset size
- Dataset split
- Independence between resources

4.3 Baselines

Clearly identify baseline systems.

4.4 Evaluation Metrics

Define mathematically or clearly:

- Accuracy
- Precision
- Recall
- F1-score
- Overstemming Rate
- Understemming Rate
- OOV Handling Rate

4.5 Experimental Protocol

Explain:

- Number of runs
- Random seed
- Evaluation procedure

Do not invent missing information.

====================================================
M. BASELINE COMPARISON
====================================================

Ensure the paper compares the proposed method fairly.

Possible baseline structure:

Baseline A:
Greedy Rule-Based Stemming

Baseline B:
Rule-Based + Lexicon Validation

Baseline C:
Candidate-Based Hybrid Processing

Proposed:
Full SasakNLP Framework

Only include baselines that are actually implemented or can genuinely
be evaluated by the authors.

Do not fabricate comparison results.

====================================================
N. ABLATION STUDY DESIGN
====================================================

Design an ablation study.

Suggested structure:

| Model | Rules | Lexicon | Candidate Generation | Ranking | Accuracy | F1 |
|------|------|---------|----------------------|---------|----------|----|

Possible configurations:

A. Rule-Based Only

B. Rules + Lexicon Validation

C. Rules + Candidate Generation

D. Rules + Candidate Generation + Ranking

E. Full SasakNLP

IMPORTANT:

Use:

[RESULT TO BE INSERTED]

for all missing results.

Explain how the author should run the ablation experiments.

====================================================
O. DIALECT-AWARE CLAIM AUDIT
====================================================

Audit every occurrence of:

- Dialect-aware
- Multi-dialect
- Dialect detection
- Dialect-specific processing

Determine whether the manuscript provides genuine evidence.

If YES:

Create a proper experiment:

Dialect-Agnostic Processing

versus

Dialect-Aware Processing

with:

| System | Overall Accuracy | Macro F1 | Per-Dialect Results |
|--------|------------------|----------|---------------------|

If NO:

Recommend:

1. Removing "Dialect-Aware" from the title, OR
2. Reframing it as an extensible architecture.

Do not claim improvement without evidence.

====================================================
P. RESULTS AND DISCUSSION
====================================================

Separate:

5. Results

from

6. Discussion

RESULTS:

- Report objective findings
- Present tables
- Present comparisons
- Avoid excessive interpretation

DISCUSSION:

- Explain why the method works
- Explain strengths and weaknesses
- Compare with previous work
- Discuss low-resource NLP implications
- Discuss error patterns

Remove duplicated content.

====================================================
Q. ERROR ANALYSIS
====================================================

Create an error analysis framework:

| Error Type | Definition | Example | Frequency | Improvement |
|------------|------------|---------|-----------|-------------|

Categories:

- Correct Lemmatization
- Overstemming
- Understemming
- Incorrect Lemma
- OOV Error
- Candidate Ranking Error
- Morphological Ambiguity
- Dialect Mismatch

Do not invent frequencies.

Use:

[RESULT TO BE INSERTED]

====================================================
R. LIMITATIONS
====================================================

Add a dedicated:

"Limitations"

section.

Clearly distinguish:

CURRENT LIMITATIONS

from

FUTURE WORK

Only discuss limitations supported by the manuscript.

Possible areas:

- Lexical coverage
- OOV words
- Authentic corpus coverage
- Dialect coverage
- Rule-based dependency
- Annotation limitations

Do not invent limitations that cannot be justified.

====================================================
S. LANGUAGE AND WRITING
====================================================

Translate and rewrite the entire manuscript into high-quality
academic English.

Requirements:

- Formal academic style
- Clear Computer Science terminology
- Consistent terminology
- Avoid literal Indonesian-to-English translation
- Avoid promotional language
- Avoid excessive repetition

Use these terms consistently:

Sasak language

low-resource language

morphological processing

lexicon validation

candidate generation

candidate ranking

lemmatization

morphological analysis

Do not randomly alternate terminology.

====================================================
T. FINAL STRUCTURE
====================================================

Recommend this final manuscript structure:

1. Introduction

2. Related Work

3. Methodology

4. Experimental Setup

5. Results

6. Discussion

7. Limitations

8. Conclusion

9. Data and Code Availability
   [anonymous version if required during review]

====================================================
U. FINAL REVIEWER SIMULATION
====================================================

Act as three anonymous reviewers.

Reviewer 1:
NLP / Artificial Intelligence Expert

Reviewer 2:
Computational Linguistics / Morphology Expert

Reviewer 3:
Experimental Reproducibility Expert

For each reviewer provide:

- Strengths
- Major concerns
- Minor concerns
- Required revisions

Then provide:

EDITORIAL RECOMMENDATION:

Accept
Minor Revision
Major Revision
Reject and Resubmit

Choose the most realistic recommendation based on the manuscript.

====================================================
V. FINAL OUTPUT
====================================================

Provide your response in this order:

A. ECTI-CIT Scope Compatibility Assessment

B. Title Assessment

C. Manuscript Strengths

D. Critical Problems

E. Double-Blind Anonymization Checklist

F. Result Consistency Audit

G. Dataset and Benchmark Audit

H. Revised Research Gap

I. Revised Contributions

J. Revised Abstract

K. Revised Methodology Structure

L. Experimental Setup Requirements

M. Baseline and Ablation Study Plan

N. Dialect-Aware Claim Assessment

O. Error Analysis Framework

P. Limitations

Q. Academic English Revision Recommendations

R. Final Manuscript Structure

S. Reviewer Simulation

T. Final Submission Readiness Score

Score:

Scope Compatibility: /10
Novelty: /10
Methodology: /10
Experimental Rigor: /10
Dataset Transparency: /10
Reproducibility: /10
Academic Writing: /10
ECTI-CIT Submission Readiness: /10

Finally provide three prioritized lists:

1. MUST FIX BEFORE SUBMISSION
2. STRONGLY RECOMMENDED
3. OPTIONAL IMPROVEMENTS

THE MOST IMPORTANT RULE:

Never fabricate experimental results, numerical values, datasets,
citations, linguistic evidence, or evaluation outcomes.

If information cannot be verified from the manuscript, explicitly use:

[AUTHOR VERIFICATION REQUIRED]