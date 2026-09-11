"""Shared test fixtures for SasakNLP test suite."""

import pytest
from sasaknlp import SasakLexManager, SasakNLP, SasakNormalizer, SasakStemmer, SasakTokenizer
from sasaknlp.morphology import CandidateGenerator, MorphologicalAnalyzer


@pytest.fixture
def lexicon():
    return SasakLexManager()


@pytest.fixture
def normalizer():
    return SasakNormalizer()


@pytest.fixture
def tokenizer():
    return SasakTokenizer()


@pytest.fixture
def candidate_generator():
    return CandidateGenerator()


@pytest.fixture
def stemmer(lexicon):
    return SasakStemmer(lexicon_manager=lexicon)


@pytest.fixture
def analyzer(stemmer):
    return MorphologicalAnalyzer(stemmer=stemmer)


@pytest.fixture
def nlp():
    return SasakNLP()
