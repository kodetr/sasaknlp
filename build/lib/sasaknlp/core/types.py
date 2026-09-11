"""Core data types, enums, and dataclasses for SasakNLP.

Provides structured models for morphological analysis, candidate generation,
lexicon representation, validation status, error classification, and pipeline results.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


class ValidationStatus(str, Enum):
    """Status of a candidate after dictionary validation."""
    EXACT_MATCH = "EXACT_MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    OOV = "OOV"
    INVALID = "INVALID"
    UNVALIDATED = "UNVALIDATED"


class ErrorCategory(str, Enum):
    """Categories for stemming and morphological error analysis."""
    CORRECT = "Correct"
    OVERSTEMMING = "Overstemming"
    UNDERSTEMMING = "Understemming"
    INCORRECT_LEMMA = "Incorrect Lemma"
    OOV_ERROR = "OOV Error"
    DIALECT_ERROR = "Dialect Error"


@dataclass
class LexiconEntry:
    """Represents an entry in the SasakLex dictionary.

    Attributes:
        id: Unique identifier for the lexicon record.
        word: The surface word or headword.
        lemma: The root form (lemma) of the word.
        pos: Part-of-speech tag (e.g., VERB, NOUN, ADJ).
        meaning_id: Meaning or translation in Indonesian (Bahasa Indonesia).
        dialect: Dialect classification ('general', 'selaparang', etc.).
        morphology: Affix metadata dictionary containing prefix, infix, suffix.
        source: Source attribution (e.g., 'kamus_sasak_indonesia', 'corpus').
        frequency: Usage frequency count in reference corpora.
    """
    id: str
    word: str
    lemma: str
    pos: str = "UNKNOWN"
    meaning_id: str = ""
    dialect: str = "general"
    morphology: Dict[str, Optional[str]] = field(
        default_factory=lambda: {"prefix": None, "infix": None, "suffix": None}
    )
    source: str = "dictionary"
    frequency: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to standard dictionary format."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> LexiconEntry:
        """Construct entry from dictionary data with safe defaults."""
        morphology = data.get("morphology", {})
        if not isinstance(morphology, dict):
            morphology = {"prefix": None, "infix": None, "suffix": None}
        return cls(
            id=str(data.get("id", "")),
            word=str(data.get("word", "")),
            lemma=str(data.get("lemma", data.get("word", ""))),
            pos=str(data.get("pos", "UNKNOWN")),
            meaning_id=str(data.get("meaning_id", "")),
            dialect=str(data.get("dialect", "general")),
            morphology={
                "prefix": morphology.get("prefix"),
                "infix": morphology.get("infix"),
                "suffix": morphology.get("suffix"),
            },
            source=str(data.get("source", "dictionary")),
            frequency=int(data.get("frequency", 0)),
        )


@dataclass
class MorphologicalCandidate:
    """Represents a potential root candidate derived during morphological stripping.

    Attributes:
        word: Original surface form being analyzed.
        lemma_candidate: The candidate root/lemma string.
        removed_prefix: Prefix identified and removed, if any.
        removed_infix: Infix identified and removed, if any.
        removed_suffix: Suffix identified and removed, if any.
        rule_applied: Name of the morphological rule applied.
        score: Total composite ranking score.
        validation_status: Lexicon validation result.
        breakdown_scores: Component scores (lexicon, morph, rule, freq, dialect).
        metadata: Extra operational metadata.
    """
    word: str
    lemma_candidate: str
    removed_prefix: Optional[str] = None
    removed_infix: Optional[str] = None
    removed_suffix: Optional[str] = None
    rule_applied: str = ""
    score: float = 0.0
    validation_status: ValidationStatus = ValidationStatus.UNVALIDATED
    breakdown_scores: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert candidate to serializable dictionary."""
        data = asdict(self)
        data["validation_status"] = self.validation_status.value
        return data


@dataclass
class MorphologicalAnalysis:
    """Final structured result of morphological analysis for a single token.

    Attributes:
        surface_form: Input word before morphological processing.
        lemma: Final predicted root/lemma.
        prefix: Identified prefix or None.
        infix: Identified infix or None.
        suffix: Identified suffix or None.
        rule_applied: Name of rule responsible for analysis, or None.
        dialect: Dialect classification assigned to the token.
        confidence: Calibrated confidence score (0.0 to 1.0).
        reduplication: Reduplication type if detected (e.g. 'full', 'partial').
        is_oov: Whether the word or lemma is Out-Of-Vocabulary.
        metadata: Additional analysis metadata.
    """
    surface_form: str
    lemma: str
    prefix: Optional[str] = None
    infix: Optional[str] = None
    suffix: Optional[str] = None
    rule_applied: Optional[str] = None
    dialect: str = "general"
    confidence: float = 0.0
    reduplication: Optional[str] = None
    is_oov: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis to serializable dictionary."""
        return asdict(self)


@dataclass
class PipelineResult:
    """Encapsulates the complete NLP pipeline output for an input text.

    Attributes:
        text: Original raw input string.
        normalized_text: Text after normalization.
        tokens: Tokenized words.
        analyses: List of MorphologicalAnalysis objects for each token.
        lemmas: List of final extracted lemmas corresponding to tokens.
        dialect: Detected or assigned dialect for the text.
    """
    text: str
    normalized_text: str
    tokens: List[str]
    analyses: List[MorphologicalAnalysis]
    lemmas: List[str]
    dialect: Optional[str] = "general"

    def to_dict(self) -> Dict[str, Any]:
        """Convert pipeline result to serializable dictionary."""
        return {
            "text": self.text,
            "normalized_text": self.normalized_text,
            "tokens": self.tokens,
            "analyses": [a.to_dict() for a in self.analyses],
            "lemmas": self.lemmas,
            "dialect": self.dialect,
        }
