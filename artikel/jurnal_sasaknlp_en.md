# SasakNLP: A Hybrid Framework for Morphological Processing of the Low-Resource Sasak Language

**Author**: **kodetr**  
**Affiliation**: Regional Language Computational Research Group, [kodetr.com](https://kodetr.com), Lombok, West Nusa Tenggara, Indonesia  
**Correspondence**: [https://kodetr.com](https://kodetr.com) | GitHub Repository: [https://github.com/kodetr/sasaknlp](https://github.com/kodetr/sasaknlp)  
**Public Distribution**: PyPI Package (`pip install sasaknlp`) | Hugging Face Dataset (`kodetr/sasak-benchmark-100k`) | Interactive Web Demo (`kodetr/sasaknlp-demo`)

---

## Abstract

Bahasa Sasak is an Austronesian regional language spoken by approximately 3 million people across Lombok Island, West Nusa Tenggara, Indonesia. Despite its demographic vitality, it remains a digitally underrepresented low-resource language lacking standardized computational linguistic infrastructure [1], [6]. Standard Indonesian morphological analyzers fail when applied to Sasak due to distinct morphophonemic alternations, complex clitic attachments, and sharp cross-island dialectal variation [9], [11], [13]. This paper presents **SasakNLP**, a dialect-aware morphological processing framework engineered specifically for Sasak orthographic normalization, reduplication-aware tokenization, shibboleth-driven dialect contextualization, and dictionary-validated multi-candidate lemmatization [10], [16], [17].

Empirical evaluation across an extensive 100,000-pair morphological benchmark and an authentic folklore corpus of 12,591 sentences demonstrates that SasakNLP achieves an overall lemmatization accuracy of **80.44%** (80,438 correct extractions) on the full 100k stress-test benchmark, decisively outperforming pure lexicon lookup (1.01%) and greedy affix-stripping baselines (55.21%) with strong statistical significance (McNemar's test, $\chi^2 = 14,962.14, p < 0.0001$). On the 10,000-pair core morphological benchmark, the system achieves an accuracy of **93.23%**. Error taxonomy analysis confirms that dictionary-gating restricts overstemming to **2.28%**, with understemming restricted to **15.86%** primarily occurring on complex multi-layered affixations. Computationally, SasakNLP delivers high-throughput execution at **7,826 words per second** on full 100k batches and up to **16,272 words per second** on standard sequences, maintaining an average per-token latency of **0.044 ms** with zero heavy machine learning framework dependencies. All source code, datasets, and interactive web demos are publicly released under permissive open-source licenses [16].

**Keywords**: *Sasak Language, Natural Language Processing, Computational Morphology, Lemmatization, Low-Resource NLP, Dialectology, Open Science.*

---

## 1. Introduction

Recent breakthroughs in Natural Language Processing (NLP) and Large Language Models (LLMs) have been overwhelmingly concentrated on high-resource languages [1], [2]. In Indonesia, while the national language (Bahasa Indonesia) enjoys mature computational infrastructure and pre-trained language representations [3], [4], empirical evaluations indicate that state-of-the-art LLMs suffer catastrophic performance degradation when evaluated on indigenous regional languages and local Indonesian reasoning tasks [5]. More than 700 indigenous regional languages across Indonesia remain critically neglected and digitally underrepresented [1], [6]. This digital resource scarcity creates acute vocabulary mismatch and tokenization fragmentation in downstream NLP pipelines [7], exacerbated by the wide cultural and linguistic nuances across Indonesian provinces [8].

Bahasa Sasak (*Basa Sasak*) is the predominant indigenous language of Lombok Island in West Nusa Tenggara, spoken by approximately 3 million native speakers [9], [10]. Categorized typologically within the Western Malayo-Polynesian branch of the Austronesian language family, Sasak exhibits distinct grammatical, morphophonemic, and sociopragmatic characteristics [11], [12]:
1. **Complex Morphophonemics**: Stem formation incorporates active prefixes (`te-`, `ka-`, `se-`, `pe-`/`peng-`), archaic passive infixes (`-in-`, `-um-`), causative/applicative suffixes (`-ang`, `-an`, `-i`, `-in`), iterative circumfixes (`pe-...-an`, `te-...-ang`, `be-...-an`), and intricate nasal substitutions (`N-`) [10], [13].
2. **Enclitic Compounding and Sociopragmatics**: Pronominal possessive enclitics (`-ku`, `-m`, `-ne`) and honorific sociolinguistic particles (`-de`, `-te`) append directly to root words, reflecting strict social strata and politeness registers [11], while frequently triggering severe overstemming or understemming in naive heuristic parsers [13].
3. **Dialectal Diversity**: The language is partitioned into five distinct dialect clusters separated by isoglosses and diagnostic lexical markers (*shibboleths*) [9], [12].

Prior computational morphology research in Indonesia has predominantly addressed Javanese and Sundanese [1], [13], [14], while computational methods for ethnic languages in Eastern Indonesia remain largely confined to bilingual lexicon induction [15]. Systematic literature reviews confirm that the absence of structured digital lexicons and morphological analyzers remains the primary barrier to regional language lemmatization [13].

To overcome these barriers, we present **SasakNLP**, an open-source, reproducible computational framework [16]. Grounded in two-level computational morphology [17] and morphological segmentation standards [18], the primary contributions of this work are:
* **Contribution 1 (SasakLex Machine Resource)**: Digitalization and structuring of the official Balai Bahasa Provinsi NTB integrated dictionary into 2,761 machine-readable entries [10], [16].
* **Contribution 2 (Hybrid Morphological Framework)**: A deterministic architecture combining two-pass affix stripping, $\mathcal{O}(L)$ dictionary validation via `PrefixTrie`, and multi-criteria candidate ranking [13], [17].
* **Contribution 3 (Structured Morphological Analysis)**: Explicit morpheme segmentation identifying prefixes, infixes, suffixes, circumfixes, clitics, and reduplication with confidence scores [17], [18].
* **Contribution 4 (Dialect-Aware Architecture)**: Configurable dialect contextualization using diagnostic shibboleth density across the five Sasak dialect regions [9], [12].
* **Contribution 5 (Open Research Infrastructure)**: Public release of the 100,000-pair gold-standard benchmark, the 12,591-sentence authentic corpus, the PyPI package (`sasaknlp`), and Hugging Face Hub datasets [16].

---

## 2. Related Work and Linguistic Foundations

### 2.1. Regional Austronesian NLP Landscape

Underrepresented language technologies in Indonesia suffer from persistent data scarcity [1], [2], [6]. Collaborative initiatives like NusaCrowd [6] and NusaX [7] have aggregated regional language resources for classification tasks, while NusaWrites [19] underscored the paramount importance of native speaker text curation over machine translation to avoid syntactic distortion. However, token-level morphological processing for regional languages outside Java remains sparse, largely relying on ad-hoc heuristics [13].

In Indonesian regional languages, canonical affix-level segmentation has proven superior to naive subword tokenization for preserving morphemic integrity [14]. Furthermore, formal finite-state morphological evaluations indicate that structured lexicon grounding is indispensable for resolving grammatical ambiguity [20]. The systematic literature review by Abidin et al. [13] established that affix stripping and lemmatization for Indonesian regional languages require domain-specific digital dictionaries and explicit morphophonemic rules to mitigate overstemming and understemming. Resiandi et al. [15] further proved the critical role of structured dictionaries in modeling regional vocabulary transformations. Hence, integrating a curated lexicon as an active verification gate is crucial for preserving root integrity in low-resource setups [13], [17].

### 2.2. Morphological System of Bahasa Sasak

According to official grammatical codification by Balai Bahasa Provinsi NTB [10], sociopragmatic studies [11], and contemporary dialectological research [9], [12], Sasak bound morphemes comprise:
* **Prefixes**: Passive `te-` (`tepinaq` "is made"), stative `ka-` (`kasolah` "beautified"), equative `se-` (`sebale` "one house"), nominalizer `pe-`/`peng-` (`pegawi` "worker"), and nasal assimilation `N-` (`tulis` $\rightarrow$ `nulis`, `pinaq` $\rightarrow$ `minaq`).
* **Suffixes**: Causative/applicative `-ang` (`tulungang` "help for someone"), locative/resultative `-an` (`kelororan` "waterway"), iterative `-i`/`-in` (`sirami`, `kaduan`).
* **Infixes**: Archaic passive `-in-` (`tinulung` "received assistance") and intransitive `-um-` (`gumingsir` "shift").
* **Circumfixes**: Abstract nominal `pe-...-an` (`pegawian` "occupation"), passive applicative `te-...-ang` (`tetulungang`), stative `ka-...-an`, reciprocal `be-...-an` (`betulungan`).
* **Enclitics**: First person `-ku`, second person `-m`, third person `-ne`, and polite register markers `-de`, `-te` (`baturne`, `balende`) [11].
* **Reduplication**: Full reduplication with hyphens (`bareng-bareng`, `mangan-mangan`).

### 2.3. Dialect Taxonomy of Bahasa Sasak

Following regional dialectological studies [9], [10], [12], Bahasa Sasak is grouped into five primary dialect clusters based on diagnostic shibboleths (Table 1).

**Table 1. Taxonomy of the Five Major Sasak Dialect Clusters in Lombok [9], [10], [12]**

| No | Dialect Cluster | Geographical Range | Diagnostic Markers (*Shibboleths*) | Phonological & Sociolinguistic Features |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Meno-Mene (Selaparang)** | East & Central Lombok | `menu`, `meni`, `tiyang`, `kaji` | Polite register (*krama/alus*), glottal stop retention /-q/, characteristic vowel /-e/ |
| **2** | **Ngeno-Ngene** | Mataram & West Lombok | `ngeno`, `ngene`, `ente`, `aku` | Urban dialect, rapid vocalic articulation, maritime trade contact |
| **3** | **Merikuq-Merikaq (Mriak-Mriku)** | Central-South (Praya, Pujut) | `mriak`, `mriku`, `meriq`, `merik` | Spatial directional deictics (*towards here / towards there*), vowels /-a/ and /-u/ |
| **4** | **Kuto-Kute (Ngeto-Ngete)** | North & Northeast Lombok (Bayan, Sembalun) | `kuto`, `kute`, `ngeto`, `wetu` | Archaic Austronesian retention, customary *Wetu Telu* tradition, highland communities |
| **5** | **General Standard Sasak** | Cross-Island Standard | `wah`, `ndeq`, `mangan`, `batur` | Inter-dialectal lingua franca in public domains, aligns with Balai Bahasa NTB lexicon |

---

## 3. Methodology and System Architecture

### 3.1. System Overview

SasakNLP implements a deterministic six-stage modular pipeline designed without external deep learning framework dependencies, ensuring predictable, reproducible, and millisecond-level execution latency:

```text
               ┌───────────────────────────────┐
               │          INPUT TEXT           │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │   1. TEXT NORMALIZATION       │
               │   (NFC, Glottals, Quotes)     │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │   2. TOKENIZATION             │
               │  (Reduplications, Enclitics)  │
               └──────────────┬────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │   3. DIALECT CONTEXTUALIZER   │
               │ (Shibboleths & Density Ratio) │
               └──────────────┬────────────────┘
                              │
               ┌──────────────┴───────────────┐
               ▼                              ▼
      [Direct Lexicon Lookup]        [Rule Morphological Engine]
       (Is word already root?)                    │
               │                                  ▼
               │                     [Candidate Generation]
               │                      • Prefix rules (te-, pe-, N-)
               │                      • Suffix rules (-an, -ang, -ne)
               │                      • Infix rules (-in-, -um-)
               │                      • Circumfixes (pe-...-an, te-...-ang)
               │                      • Reduplications (kata-kata)
               │                                  │
               │                                  ▼
               │                     [PrefixTrie Lexicon Validator]
               │                      • EXACT_MATCH
               │                      • PARTIAL_MATCH
               │                      • OOV (Out-Of-Vocabulary)
               │                                  │
               │                                  ▼
               │                     [Candidate Multi-Criteria Ranker]
               │                      Score = w_lex·S_lex + w_morph·S_morph
               │                            + w_conf·S_conf + w_freq·S_freq
               │                            + w_dial·S_dial
               │                                  │
               └──────────────┬───────────────────┘
                              │
                              ▼
               ┌───────────────────────────────┐
               │       STRUCTURED OUTPUT       │
               │ (Lemmas, Affixes, Confidence) │
               └───────────────────────────────┘
```

### 3.2. Orthographic Normalization
The normalization stage enforces Unicode NFC composition, standardizes typographical variations in Sasak glottal stop graphemes (unifying curly apostrophes `’` and backticks into canonical glottal characters `q` or `'`), and cleans non-standard ASCII artifacts while preserving accented vowel distinctions (`è`, `é`) [1], [6].

### 3.3. Reduplication-Aware Tokenization
The tokenizer detects full hyphenated reduplications (`[Root]-[Root]`) as unified morphological constructs, preventing incorrect splitting of iterative verbs and repetitive adverbs into disjoint tokens [13], [17].

### 3.4. Diagnostic Shibboleth Dialect Contextualization
The dialect detector module calculates dialect confidence using relative shibboleth density across geographical clusters [9], [12]:

$$\text{Confidence}(d) = \frac{\sum_{w \in T} \mathbb{I}(w \in M_d) \cdot \omega(w)}{\sum_{d' \in D} \sum_{w \in T} \mathbb{I}(w \in M_{d'}) \cdot \omega(w)} \quad (1)$$

where $T$ represents the input tokens, $M_d$ is the set of diagnostic lexical markers for dialect $d$, and $\omega(w)$ denotes the lexical uniqueness weight.

### 3.5. Two-Pass Candidate Generation and PrefixTrie Validation
Unrecognized surface forms are submitted to candidate generation. Two-pass affix stripping peels enclitics, outer circumfixes, prefixes, suffixes, and infixes. Each candidate root is verified against the 2,761-word Balai Bahasa NTB dictionary using an $\mathcal{O}(L)$ `PrefixTrie` data structure [10], [17], [18].

### 3.6. Multi-Criteria Candidate Ranking
Morphological ambiguities are resolved using a weighted scoring objective [17]:

$$\text{Score}(c) = w_{\text{lex}} \cdot S_{\text{lex}}(c) + w_{\text{morph}} \cdot S_{\text{morph}}(c) + w_{\text{conf}} \cdot S_{\text{conf}}(c) + w_{\text{freq}} \cdot S_{\text{freq}}(c) + w_{\text{dial}} \cdot S_{\text{dial}}(c) \quad (2)$$

with empirically optimized weights: $w_{\text{lex}} = 0.40$, $w_{\text{morph}} = 0.25$, $w_{\text{conf}} = 0.15$, $w_{\text{freq}} = 0.10$, and $w_{\text{dial}} = 0.10$.

### 3.7. Structured Morphological Output
The final pipeline generates structured JSON-compatible tuples containing base lemmas, grammatical affix breakdown, dialect classification, and normalized confidence scores.

---

## 4. Experimental Setup and Dataset Protocol

### 4.1. Research Data Resources

The benchmark datasets were curated via a rigorous three-phase acquisition protocol (Fig. 1):

![Three-Phase Scientific Acquisition Protocol](figures/fig5_dataset_acquisition_pipeline.png)
*<b>Fig. 1:</b> Three-phase scientific acquisition and quality curation protocol for SasakNLP research artifacts.*

1. **Benchmark 100k (`benchmark_100k.csv`)**: 100,000 controlled morphological test pairs annotated with surface words, gold-standard lemmas, affixation categories, and dialect metadata.
2. **Benchmark 10k (`benchmark_10k.csv`)**: 10,000 core morphological pairs representing canonical daily vocabulary.
3. **Authentic Corpus (`sasak_sentences_large.csv`)**: 12,591 authentic sentences (188,881 tokens) compiled from oral folklore (*Putri Mandalika*, *Dewi Anjani*, *Datu Doyan Nada*), regional periodicals, and Balai Bahasa NTB archival records [10], [16], [21].
4. **Lexicon Dictionary (`kamus_balai_bahasa_ntb.csv`)**: 2,761 verified lemma entries from Balai Bahasa Provinsi NTB [10].

### 4.2. Baseline Models
We evaluate SasakNLP against two standard baseline algorithms on the 100,000-sample benchmark:
* **Baseline 1 (Direct Lexicon Lookup)**: Exact lexicon matching without affix stripping.
* **Baseline 2 (Greedy Affix Stripping)**: Longest-match affix removal without dictionary verification [13].

### 4.3. Evaluation Metrics and Experimental Environment
Evaluation metrics include exact lemmatization accuracy, throughput (words/second), per-token latency (ms), overstemming rate, understemming rate, and out-of-vocabulary (OOV) rate. Experiments were executed on Apple Silicon (8-Core) and Intel Core i7 x86_64 CPUs with 16 GB RAM under Python 3.10+, guaranteeing 100% deterministic reproducibility [16].

---

## 5. Experimental Results

### 5.1. Baseline Comparison on the 100,000-Sample Benchmark

Experimental results across the 100,000 morphological test pairs demonstrate the decisive superiority of SasakNLP (Table 2). Baseline 1 achieves only 1.01% accuracy due to complete failure on affixed words. Baseline 2 obtains 55.21% but suffers from severe overstemming. SasakNLP achieves **80.44%** accuracy (80,438 correct predictions).

**Table 2. Comparative Lemmatization Evaluation on 100,000 Morphological Samples**

| Model / Algorithm | Computational Principle | Correct (N=100k) | Accuracy (%) | Throughput (wps) | Linguistic Characteristics |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Baseline 1: Direct Lookup** | *Exact Dictionary Matching* | 1,006 | **1.01%** | 24,500 | Fails completely on 98.99% of inflected words. |
| **Baseline 2: Greedy Stripping** | *Longest-Match Affix Stripping* | 55,205 | **55.21%** | 18,200 | Severe overstemming on valid root words. |
| **Proposed SasakNLP** | *Dictionary-Enhanced Multi-Candidate* | **80,438** | **80.44%** | **7,826** | Optimal balance of precision, root protection, and clitic handling. |

> **McNemar's Statistical Significance Test**:  
> Paired evaluation between SasakNLP and Baseline 2 yields the full $2 \times 2$ contingency table across all $N = 100,000$ test items:  
>  
> | | Baseline 2 Correct | Baseline 2 Incorrect | Total |  
> | :--- | :---: | :---: | :---: |  
> | **SasakNLP Correct** | $a = 46,546$ | $b = 33,892$ | 80,438 |  
> | **SasakNLP Incorrect** | $c = 8,659$ | $d = 10,903$ | 19,562 |  
> | **Total** | 55,205 | 44,795 | 100,000 |  
>  
> Test statistic with continuity correction: **$\chi^2 = \frac{(|b - c| - 1)^2}{b + c} = \frac{(|33,892 - 8,659| - 1)^2}{33,892 + 8,659} = \frac{25,232^2}{42,551} = 14,962.14$** ($df = 1, p < 0.0001$).  
> The performance advantage of SasakNLP over the baseline is **statistically significant** at $\alpha = 0.001$.

### 5.2. Performance on the Core 10k Benchmark
On the 10,000-pair core morphological benchmark (`benchmark_10k.csv`), SasakNLP achieves **9,323 correct predictions** (**93.23% accuracy**) at **16,272 words per second**, reflecting high precision on natural morpheme distributions without multi-layer nesting anomalies.

### 5.3. Architectural Component Ablation Study

To quantify the contribution of each algorithmic module, we conducted an ablation study on the 100,000-sample benchmark (Table 3). Adding `PrefixTrie` dictionary gating improves accuracy by +13.24% over greedy stripping, while candidate generation and ranking provide an additional +11.99% accuracy gain.

**Table 3. Ablation Study Across SasakNLP Architectural Components (100k Data)**

| Configuration | Rules | Dict | Gen | Rank | Dialect | Acc (%) | Throughput |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **M1: Direct Lookup** | ❌ | ✅ | ❌ | ❌ | ❌ | 1.01% | 24,500 wps |
| **M2: Greedy Stripping** | ✅ | ❌ | ❌ | ❌ | ❌ | 55.21% | 18,200 wps |
| **M3: Rules + Dict Gate** | ✅ | ✅ | ❌ | ❌ | ❌ | 68.45% | 14,100 wps |
| **M4: Rules + Gen + First Match** | ✅ | ✅ | ✅ | ❌ | ❌ | 74.12% | 10,350 wps |
| **M5: Full Proposed SasakNLP** | ✅ | ✅ | ✅ | ✅ | ✅ | **80.44%** | **7,826 wps** |

### 5.4. Morpheme-Level Performance Disaggregation

Performance breakdown across grammatical categories (Fig. 2 and Table 4) confirms robust handling of single affixes and reduplication. Reduplication achieves 100.00%, passive prefixes reach 97.36%, stative prefixes reach 96.79%, and possessive clitics exceed 94.6%–96.5%.

![Morphological Rule Accuracy](figures/fig1_morphology_accuracy.png)
*<b>Fig. 2:</b> Morphological rule accuracy across grammatical affix classes (100k data).*

**Table 4. Disaggregated Performance Across 16 Major Representative Morpheme Categories ($N = 55,324$) on the 100,000-Sample Benchmark**

| Category | Pattern | Samples | Accuracy (%) | Linguistic Characteristics & Handling |
| :--- | :--- | :---: | :---: | :--- |
| **Reduplication** | `root-root` | 1,789 | **100.00%** | Flawless handling of full reduplication (*mangan-mangan*). |
| **Passive Prefix** | `te-` | 1,783 | **97.36%** | Passive verbs (*tetulung*, *tepinaq*). |
| **Stative Prefix** | `ka-` | 1,745 | **96.79%** | Stative condition markers (*kasolah*, *kabeleq*). |
| **Nominal Prefix** | `peng-` | 1,781 | **96.91%** | Agentive and instrument nominalizer (*penggawi*). |
| **Equative Prefix** | `se-` | 1,748 | **96.22%** | Equative and collective prefix (*sebale*, *sekance*). |
| **Clitic Possessive 1** | `-ku` | 1,782 | **96.58%** | First-person possessive enclitic (*baleku*, *jaranku*). |
| **Clitic Possessive 2** | `-m` | 1,778 | **96.18%** | Second-person familiar enclitic (*matam*, *bajum*). |
| **Clitic Possessive 3** | `-ne` | 3,571 | **94.62%** | Third-person possessive enclitic (*baturne*, *kawanne*). |
| **Iterative Suffix** | `-i` | 1,771 | **91.53%** | Iterative action suffix (*sirami*, *antoli*). |
| **Infixes** | `-in-`, `-um-` | 2,346 | **89.98%** | Archaic passive and intransitive infixes (*tinulung*). |
| **Polite Clitics** | `-de`, `-te` | 6,312 | **88.39%** | Honorific polite enclitics (*balende*, *balente*). |
| **Circumfix Passive** | `te-...-ang` | 4,578 | **96.96%** | Passive applicative circumfix (*tetulungang*). |
| **Circumfix Nominal** | `pe-...-an` | 5,915 | **88.32%** | Abstract nominalizer (*pegawian*). |
| **Causative Suffix** | `-ang` | 6,170 | **83.70%** | Active causative/applicative suffix (*tulungang*). |
| **Locative Suffix** | `-an`, `-in` | 10,545 | **76.52%** | Locative and resultative suffix (*kaduan*, *siramin*). |
| **Reciprocal** | `be-...-an` | 1,710 | **65.09%** | Reciprocal mutual action circumfix (*betulungan*). |

*Note: The 16 categories displayed in Table 4 represent canonical major single-affix and primary circumfix formations ($N = 55,324$). The remaining 44,676 samples in the 100,000-pair benchmark comprise complex multi-tier nested combinations, compounding, and dialectal derivations documented in the supplementary dataset repository.*

### 5.5. Cross-Dialect Evaluation Across Five Regions

Cross-dialect evaluation across the five Sasak dialect regions (Fig. 3 and Table 5) confirms strong generalization across Lombok Island.

![Cross-Dialect Performance](figures/fig2_dialect_performance.png)
*<b>Fig. 3:</b> Cross-dialect lemmatization accuracy across five major Sasak dialect clusters.*

**Table 5. Lemmatization Performance Across Five Major Sasak Dialect Clusters (100k Data)**

| Region | Dialect Cluster | Samples | Accuracy (%) | Primary Vocalic & Phonemic Features |
| :--- | :--- | :---: | :---: | :--- |
| **Mataram / West Lombok** | **General Standard Sasak** | 43,254 | **85.73%** | Aligns with official Balai Bahasa NTB standard lexicon. |
| **North Lombok** | **Kuto-Kute (Ngeto-Ngete)** | 10,475 | **80.31%** | Final vowels /-e/ and /-o/ (*kuto*, *kute*), archaic retention. |
| **South Lombok** | **Merikuq-Merikaq (Mriak-Mriku)** | 10,535 | **79.79%** | Vowels /-a/ and /-u/ with persistent glottal stop /-q/. |
| **Central Lombok** | **Meno-Mene (Selaparang)** | 23,023 | **77.04%** | Characteristic vowel /-e/, largest speaker population. |
| **East Lombok** | **Ngeno-Ngene** | 12,713 | **69.24%** | Nasal vocalic shifts and final velar consonant /-k/. |

### 5.6. Computational Scalability and Runtime Latency

Computational profiling indicates linear $\mathcal{O}(N)$ scaling (Fig. 4). Throughput reaches **7,826 words/second** on 100k batches and **16,272 words/second** on 10k benchmarks, with average per-token latency of **0.044 ms**.

![Computational Scalability](figures/fig4_pipeline_benchmark.png)
*<b>Fig. 4:</b> Computational scalability and latency profile of SasakNLP across token lengths.*

### 5.7. Extrinsic Feature Space Dimensionality Reduction

In downstream evaluation, applying SasakNLP lemmatization compressed the vocabulary feature space of the authentic corpus from 5,913 unique surface tokens to 4,022 base lemmas (**31.98% dimensional reduction**, Table 6), directly reducing matrix sparsity for downstream classification and retrieval pipelines [13], [22].

**Table 6. Evaluation of Vocabulary Feature Space Compression on Research Datasets**

| Corpus / Dataset Parameter | Unique Surface Tokens | Base Root Lemmas | Dimensional Reduction Ratio | Impact on Downstream NLP Pipelines |
| :--- | :---: | :---: | :---: | :--- |
| **Benchmark Morfologi (100k)** | 100,000 unique forms | 1,790 root lemmas | **98.21%** | Reduces lexical lookup search space by 55×. |
| **Authentic Corpus (189k tokens)** | 5,913 unique words | 4,022 root lemmas | **31.98%** | Reduces feature matrix sparsity by 32%. |

---

## 6. Discussion and Error Analysis

### 6.1. Error Taxonomy and Failure Mode Analysis

A comprehensive diagnostic evaluation on the 100,000-sample benchmark classifies failure modes into four categories (Fig. 5, Table 7).

![Error Taxonomy Distribution](figures/fig3_error_taxonomy.png)
*<b>Fig. 5:</b> Distribution of lemmatization error taxonomy (left) and failure mode diagnostic matrix (right).*

**Table 7. Error Taxonomy Analysis on 100,000 Morphological Benchmark Samples**

| Classification | Computational Definition | Example Input $\rightarrow$ Pred | Count | Pct (%) | Root Linguistic Cause |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Correct** | Predicted lemma matches gold lemma. | `tepinaq` $\rightarrow$ `pinaq` | **80,438** | **80.44%** | Exact match in rules and lexicon. |
| **Understemming** | Predicted lemma length > gold lemma. | `pegawianne` $\rightarrow$ `pegawian` (should be `gawi`) | **15,856** | **15.86%** | Triple-layer nesting (*circumfix + clitic*) not fully stripped in pass one. |
| **Overstemming** | Root character mistakenly removed. | `jaran` $\rightarrow$ `jar` (*-an* stripped) | **2,279** | **2.28%** | Root ending resembles bound suffix. |
| **Incorrect Lemma** | Equal length, mismatched characters. | `mangan` $\rightarrow$ `pangan` (should be `mangan`) | **1,427** | **1.43%** | Nasal alternation ambiguity ($m \rightarrow p$ vs $m \rightarrow m$). |
| **OOV Error** | Root absent from machine lexicon. | Loanwords / neologisms | **0** | **0.00%** | All benchmark roots covered by dictionary. |

### 6.2. Algorithmic Strengths of Dictionary-Gated Parsing
SasakNLP's high precision stems from `PrefixTrie` dictionary gating [10], [17]. In naive greedy stripping (Baseline 2), roots ending in `-an` (such as `jaran` "horse") are truncated to `jar`. In SasakNLP, `jaran` matches the verified lexicon on pass one, preventing unnecessary truncation (*zero unnecessary stripping*).

### 6.3. Complexity Discrepancy between Benchmarks
The accuracy difference between the 100k benchmark (80.44%) and the 10k core benchmark (93.23%) reflects morphological complexity. The 100k benchmark functions as an exhaustive stress-test with triple-layer nested affixations (e.g., `pe-...-an` with `-ne` and `te-`), whereas the 10k core benchmark mirrors natural daily distribution.

### 6.4. Implications for Underrepresented Indigenous NLP
These results demonstrate that underrepresented regional languages in Indonesia can achieve robust morphological processing through dictionary-grounded rule architectures without expensive GPU infrastructure [1], [6], [13].

---

## 7. Limitations

We transparently document three primary limitations of this study:
1. **Controlled Vocabulary Scope**: The 100k benchmark evaluates systematic morpheme combinations grounded in verified dictionary lemmas. Open social media text with contemporary slang neologisms requires ongoing lexicon expansion.
2. **Dialect Corpus Balance**: Authentic folklore sentences are currently skewed toward General and East Lombok dialects due to historical textual availability.
3. **Absence of Syntactic Context**: The current pipeline operates at word and token levels without sentence-level Part-of-Speech tagging context.

---

## 8. Conclusion and Future Directions

This paper presented **SasakNLP**, the first dialect-aware morphological framework for Bahasa Sasak. Evaluated across 100,000 benchmark pairs, SasakNLP achieves **80.44%** accuracy on the full stress-test benchmark and **93.23%** on the core 10k benchmark, restricting overstemming to **2.28%**, with throughput exceeding **7,826–16,272 words/second** and **0.044 ms latency** with zero external dependencies.

Future directions include: (1) Integrating lightweight sequence-to-sequence models (ByT5 / Char-BiLSTM) for OOV neologism handling, (2) Constructing the first annotated Sasak Dependency Treebank, and (3) Training bidirectional Sasak-Indonesian Neural Machine Translation models [1], [2], [6].

---

## Data and Code Availability

To ensure scientific transparency and research reproducibility, all software, data, and models are publicly accessible:
* **Official PyPI Package**: [https://pypi.org/project/sasaknlp/](https://pypi.org/project/sasaknlp/) (`pip install sasaknlp`)
* **GitHub Repository**: [https://github.com/kodetr/sasaknlp](https://github.com/kodetr/sasaknlp)
* **Hugging Face Datasets**: [https://huggingface.co/datasets/kodetr/sasak-benchmark-100k](https://huggingface.co/datasets/kodetr/sasak-benchmark-100k)
* **Interactive Web Application**: [https://huggingface.co/spaces/kodetr/sasaknlp-demo](https://huggingface.co/spaces/kodetr/sasaknlp-demo)
* **Researcher Homepage**: [https://kodetr.com](https://kodetr.com)

---

## Acknowledgment

The author expresses sincere gratitude to the native speakers and cultural custodians across Lombok Island, previous dialectological researchers, and Balai Bahasa Provinsi Nusa Tenggara Barat for standardizing the Sasak-Indonesian dictionary that provided the foundational lexical ground truth.

---

## References

[1] A. F. Aji, G. I. Winata, F. Koto, S. Cahyawijaya, A. Romadhony, R. Mahendra, K. Kurniawan, D. Moeljadi, R. E. Prasojo, T. Baldwin, J. H. Lau, and S. Ruder, "One Country, 700+ Languages: NLP Challenges for Underrepresented Languages and Dialects in Indonesia," in *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 2022, pp. 722--745. doi: 10.18653/v1/2022.acl-long.498.

[2] S. Ranathunga, E.-S. A. Lee, M. P. Skenduli, R. Shekhar, M. Alam, and R. Kaur, "Neural Machine Translation for Low-Resource Languages: A Survey," *ACM Computing Surveys*, vol. 55, no. 11, pp. 229:1--229:37, 2023. doi: 10.1145/3567592.

[3] S. Cahyawijaya, G. I. Winata, B. Wilie, K. Vincentio, X. Li, A. Kuncoro, S. Rai, M. Lyman, K. Kurniawan, A. Azaria, S. Bahar, R. Mahendra, P. Fung, and A. Purwarianti, "IndoNLG: Benchmark and Resources for Evaluating Indonesian Natural Language Generation," in *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*, 2021, pp. 8878--8898. doi: 10.18653/v1/2021.emnlp-main.699.

[4] F. Koto, J. H. Lau, and T. Baldwin, "IndoBERTweet: A Pretrained Language Model for Indonesian Twitter with Effective Domain-Specific Vocabulary Initialization," in *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing*, 2021, pp. 10660--10668. doi: 10.18653/v1/2021.emnlp-main.833.

[5] F. Koto, N. Aisyah, H. Li, and T. Baldwin, "Large Language Models Only Pass Primary School Exams in Indonesia: A Comprehensive Test on IndoMMLU," in *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, 2023, pp. 12359--12374. doi: 10.18653/v1/2023.emnlp-main.760.

[6] G. I. Winata, A. F. Aji, S. Cahyawijaya, R. Mahendra, F. Koto, A. Romadhony, K. Kurniawan, D. Moeljadi, and R. E. Prasojo, "NusaCrowd: Open Source Initiative for Indonesian NLP and Regional Languages Resources," in *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, 2023, pp. 8321--8345. doi: 10.18653/v1/2023.acl-long.462.

[7] S. Cahyawijaya, H. Lovenia, A. F. Aji, G. I. Winata, B. Wilie, F. Koto, R. Mahendra, C. Wibisono, and P. Fung, "NusaX: Multilingual Parallel Sentiment Dataset for 10 Indonesian Local Languages," in *Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics*, 2023, pp. 2562--2578. doi: 10.18653/v1/2023.eacl-main.189.

[8] F. Koto, R. Mahendra, N. Aisyah, and T. Baldwin, "IndoCulture: Exploring Geographically Influenced Cultural Commonsense Reasoning Across Eleven Indonesian Provinces," *Transactions of the Association for Computational Linguistics*, vol. 12, pp. 1703--1719, 2024. doi: 10.1162/tacl_a_00726.

[9] L. Hakim, Roveneldo, N. U. al Jamiliyati, and Arjulayana, "Medan Makna Aktivitas Kaki dalam Bahasa Sasak Dialek A-E," *MABASAN: Jurnal Ilmiah Bahasa dan Sastra*, vol. 17, no. 1, pp. 109--128, 2023. doi: 10.26499/mab.v17i1.626.

[10] Balai Bahasa Provinsi Nusa Tenggara Barat, *Kamus Terpadu Sasambo (Sasak, Samawa, Mbojo)*. Mataram, Indonesia: Balai Bahasa Provinsi Nusa Tenggara Barat, Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi Republik Indonesia, 2022.

[11] L. N. Yaqin, T. Shanmuganathan, W. Fauzanna, Mohzana, and A. Jaya, "Sociopragmatic parameters of politeness strategies among the Sasak in the post elopement rituals," *Studies in English Language and Education*, vol. 9, no. 2, pp. 797--811, 2022. doi: 10.24815/siele.v9i2.22569.

[12] L. Hakim, "Makian dalam Bahasa Sasak Dialek E-E," *MABASAN: Jurnal Ilmiah Bahasa dan Sastra*, vol. 16, no. 1, pp. 83--98, 2022. doi: 10.26499/mab.v16i1.503.

[13] Z. Abidin, A. Junaidi, and Wamiliana, "Text Stemming and Lemmatization of Regional Languages in Indonesia: A Systematic Literature Review," *Journal of Information Systems Engineering and Business Intelligence (JISEBI)*, vol. 10, no. 2, pp. 217--231, 2024. doi: 10.20473/jisebi.10.2.217-231.

[14] S. H. Wijono, M. R. Alhamidi, M. H. Hilman, and W. Jatmiko, "Canonical Segmentation Using Affix Characters as a Unit on Transformer for Javanese Language," in *Proceedings of the 2021 6th International Workshop on Big Data and Information Security (IWBIS)*, 2021, pp. 67--72. doi: 10.1109/IWBIS53353.2021.9631839.

[15] K. Resiandi, Y. Murakami, and A. H. Nasution, "Neural Network-Based Bilingual Lexicon Induction for Indonesian Ethnic Languages," *Applied Sciences*, vol. 13, no. 15, p. 8666, 2023. doi: 10.3390/app13158666.

[16] kodetr, "SasakNLP: A Dialect-Aware Morphological Processing Framework and 100k Benchmark for the Low-Resource Sasak Language," PyPI, GitHub, and Hugging Face Datasets, 2026. [Online]. Available: https://github.com/kodetr/sasaknlp.

[17] D. Jurafsky and J. H. Martin, *Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition*, 3rd ed. Upper Saddle River, NJ: Prentice Hall, 2024.

[18] K. Batsuren, G. Bella, A. Arora, V. Martinovic, K. Gorman, Z. Žabokrtský, A. Ganbold, Š. Dohnalová, M. Ševčíková, K. Pelegrinová, F. Giunchiglia, R. Cotterell, and E. Vylomova, "The SIGMORPHON 2022 Shared Task on Morpheme Segmentation," in *Proceedings of the 19th SIGMORPHON Workshop on Computational Research in Phonetics, Phonology, and Morphology*, 2022, pp. 103--116. doi: 10.18653/v1/2022.sigmorphon-1.11.

[19] S. Cahyawijaya, H. Lovenia, F. Koto, D. Adhista, E. Dave, S. Oktavianti, S. Akbar, J. Lee, N. Shadieq, T. W. Cenggoro, H. Linuwih, B. Wilie, G. Muridan, G. Winata, D. Moeljadi, A. F. Aji, A. Purwarianti, and P. Fung, "NusaWrites: Constructing High-Quality Corpora for Underrepresented and Extremely Low-Resource Languages," in *Proceedings of the 13th International Joint Conference on Natural Language Processing and the 3rd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)*, 2023, pp. 921--945. doi: 10.18653/v1/2023.ijcnlp-main.60.

[20] Prihantoro, "An evaluation of MorphInd's morphological annotation scheme for Indonesian," *Corpora*, vol. 16, no. 2, pp. 287--299, 2021. doi: 10.3366/cor.2021.0223.

[21] L. N. Setra, Rondiyah, A. Kurniawaty, and R. Gayatri, "Distribusi Pemakaian Kata Mamiq dalam Korpus Bahasa Sasak: Naskah Cilinaya dan Majalah Tambori," *MABASAN: Jurnal Ilmiah Bahasa dan Sastra*, vol. 17, no. 2, pp. 293--308, 2023. doi: 10.62107/mab.v17i2.814.

[22] A. Romadhony, S. Al Faraby, R. Rismala, U. N. Wisesti, and A. Arifianto, "Sentiment Analysis on a Large Indonesian Product Review Dataset," *Journal of Information Systems Engineering and Business Intelligence (JISEBI)*, vol. 10, no. 1, pp. 167--178, 2024. doi: 10.20473/jisebi.10.1.167-178.
