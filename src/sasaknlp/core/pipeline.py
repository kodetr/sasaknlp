"""Main pipeline orchestrator for SasakNLP."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Union

from sasaknlp.core.config import PipelineConfig
from sasaknlp.core.types import MorphologicalAnalysis, PipelineResult
from sasaknlp.dialect.detector import DialectDetector
from sasaknlp.dialect.manager import DialectManager
from sasaknlp.lexicon.manager import SasakLexManager
from sasaknlp.morphology.analyzer import MorphologicalAnalyzer
from sasaknlp.morphology.candidate_generator import CandidateGenerator
from sasaknlp.normalization.normalizer import SasakNormalizer
from sasaknlp.stemmer.ranking import CandidateRanker
from sasaknlp.stemmer.stemmer import SasakStemmer
from sasaknlp.stemmer.validator import DictionaryValidator
from sasaknlp.stopwords import SasakStopwords
from sasaknlp.tokenizer.sentence_tokenizer import SasakSentenceTokenizer
from sasaknlp.tokenizer.tokenizer import SasakTokenizer


class SasakNLP:
    """Primary high-level API for the SasakNLP toolkit.

    Orchestrates:
    - Text Normalization
    - Tokenization & Sentence Splitting
    - Dialect Identification
    - Morphological Analysis
    - Rule-based & Dictionary-enhanced Stemming

    Usage:
        >>> from sasaknlp import SasakNLP
        >>> nlp = SasakNLP()
        >>> result = nlp.process("Tiyang mangan nasiq bareng-bareng")
        >>> print(result.lemmas)
        ['tiyang', 'mangan', 'nasiq', 'bareng']
    """

    def __init__(
        self,
        config: Optional[PipelineConfig] = None,
        dialect: str = "auto",
        custom_lexicon_path: Optional[Union[str, Path]] = None,
        custom_rules_path: Optional[Union[str, Path]] = None,
    ) -> None:
        self.config = config or PipelineConfig()
        if dialect != "auto":
            self.config.dialect = dialect
        if custom_lexicon_path:
            self.config.custom_lexicon_path = Path(custom_lexicon_path)
        if custom_rules_path:
            self.config.custom_rules_path = Path(custom_rules_path)

        # 1. Normalization & Tokenization
        self.normalizer = SasakNormalizer(config=self.config.normalizer)
        self.tokenizer = SasakTokenizer()
        self.sentence_tokenizer = SasakSentenceTokenizer()
        self.stopwords = SasakStopwords(dialect=self.config.dialect if self.config.dialect != "auto" else None)

        # 2. Lexicon Management
        self.lexicon = SasakLexManager(
            data_path=self.config.custom_lexicon_path,
            auto_load_default=True,
        )

        # 3. Dialect Handling
        self.dialect_manager = DialectManager()
        self.dialect_detector = DialectDetector(self.dialect_manager)

        # 4. Morphology & Stemming Subcomponents
        self.candidate_generator = CandidateGenerator(
            config_path=self.config.custom_rules_path,
            min_root_length=self.config.min_root_length,
        )
        self.validator = DictionaryValidator(lexicon_manager=self.lexicon)
        self.ranker = CandidateRanker(weights=self.config.ranking_weights)

        # 5. Core Stemmer & Morphological Analyzer
        self.stemmer = SasakStemmer(
            lexicon_manager=self.lexicon,
            candidate_generator=self.candidate_generator,
            validator=self.validator,
            ranker=self.ranker,
            normalizer=self.normalizer,
            dialect=self.config.dialect,
            min_root_length=self.config.min_root_length,
            enable_oov_fallback=self.config.enable_oov_fallback,
        )
        self.analyzer = MorphologicalAnalyzer(
            stemmer=self.stemmer,
            dialect=self.config.dialect,
        )

    def process(self, text: str) -> PipelineResult:
        """Run the end-to-end NLP pipeline on the input text."""
        if not text or not text.strip():
            return PipelineResult(
                text=text,
                normalized_text="",
                tokens=[],
                analyses=[],
                lemmas=[],
                dialect=self.config.dialect,
            )

        # Step 1: Text Normalization
        norm_text = self.normalizer.normalize(text)

        # Step 2: Tokenization
        tokens = self.tokenizer.tokenize(norm_text, keep_punct=False)

        # Step 3: Dialect Detection / Contextualization
        if self.config.dialect == "auto":
            detected_dialect, conf = self.dialect_detector.detect(tokens)
            effective_dialect = detected_dialect
        else:
            effective_dialect = self.config.dialect

        # Update stemmer & analyzer dialect context
        self.stemmer.dialect = effective_dialect
        self.analyzer.dialect = effective_dialect

        # Step 4: Morphological Analysis & Stemming
        analyses: List[MorphologicalAnalysis] = []
        lemmas: List[str] = []

        for token in tokens:
            analysis = self.analyzer.analyze(token)
            analyses.append(analysis)
            lemmas.append(analysis.lemma)

        return PipelineResult(
            text=text,
            normalized_text=norm_text,
            tokens=tokens,
            analyses=analyses,
            lemmas=lemmas,
            dialect=effective_dialect,
        )

    def stem(self, text_or_word: str) -> Union[str, List[str]]:
        """Convenience method to stem a single word or full sentence.

        If input contains spaces, returns list of lemmas. Otherwise returns single lemma string.
        """
        if " " in text_or_word.strip():
            result = self.process(text_or_word)
            return result.lemmas
        return self.stemmer.stem(text_or_word)

    def analyze(self, text_or_word: str) -> Union[MorphologicalAnalysis, List[MorphologicalAnalysis]]:
        """Convenience method to analyze a single word or a full sentence."""
        if " " in text_or_word.strip():
            result = self.process(text_or_word)
            return result.analyses
        return self.analyzer.analyze(text_or_word)

    def tokenize(self, text: str, keep_punct: bool = False) -> List[str]:
        """Tokenize text into words."""
        norm = self.normalizer.normalize(text)
        return self.tokenizer.tokenize(norm, keep_punct=keep_punct)

    def split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        return self.sentence_tokenizer.tokenize(text)

    def remove_stopwords(
        self,
        text_or_tokens: Union[str, List[str]],
        dialect: Optional[str] = None,
    ) -> Union[str, List[str]]:
        """Filter out Sasak stopwords from input string or token list.

        Args:
            text_or_tokens: Input text string or list of word tokens.
            dialect: Optional dialect override. If None, uses active pipeline dialect.

        Returns:
            Filtered string or token list without stopwords.
        """
        eff_dialect = dialect or (self.stemmer.dialect if self.stemmer.dialect != "auto" else None)
        if isinstance(text_or_tokens, list):
            return self.stopwords.filter_tokens(text_or_tokens, dialect=eff_dialect)
        return self.stopwords.filter_text(text_or_tokens, dialect=eff_dialect)

