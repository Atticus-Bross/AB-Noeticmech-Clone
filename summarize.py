#!/usr/bin/env python
"""summarize

Summarize a document using extractive text summarization via tf-idf.

Usage:
  summarize [-o <file> | --output=<file>] [<input-file>]
  summarize (-h | --help)

Options:
  -h --help            Show this screen.
  -o --output=<file>   Write output to file instead of stdout.
"""
from docopt import docopt
import nltk
import sys
from collections import defaultdict
from collections.abc import Callable
from typing import TextIO


def load_document(textfile: TextIO) -> list[str]:
    """Reads a text file and returns a list of sentences"""
    text = [line.strip() for line in textfile.readlines()]
    text = nltk.sent_tokenize(' '.join(text))
    return text


# [TODO] Remove non-word symbols from terms, maybe more?
def clean_text(text: list[str]) -> list[list[str]]:
    """Transform text into a list of terms for each sentence"""
    sentences: list[list[str]] = []
    for line in text:
        sentence = [word.casefold()
                    for word in nltk.word_tokenize(line)]
        if len(sentence) > 0:
            sentences.append(sentence)
    return sentences

                

# [TODO] Implement Term Frequency calculation for document, term
def calculate_tf(sentences: list[list[str]]) -> list[dict]:
    """Calculate Term Frequency for each sentence of the document
    Returns a table whose keys are the indices of sentences of the text
    and values are dictionaries of terms and their tf values."""
    matrix: list[dict] = []
    return matrix


# [TODO] Implement Inverse Document Frequency for term
def calculate_idf(sentences: list[list[str]]) -> dict[str, float]:
    """Calculate the Inverse `Document'(Sentence) Frequency of each term.
    Returns a table of terms and their idf values."""
    matrix: dict[str, float] = defaultdict(float)
    return matrix


# [TODO] Implement sentence scoring
def score_sentences(tf_matrix: list[dict], idf_matrix: dict[str, float], sentences: list[list[str]]) -> list[float]:
    """Score each sentence for importance based on the terms it contains.
    Assumes that there are no empty sentences.
    Returns a table whose keys are the indices of sentences of the text
    and values are the sum of tf-idf scores of each word in the sentence"""
    scores: list[float] = []
    return scores


def threshold_inclusion(text: list[str], scores: list[float], threshold=1):
    """Use a multiple of the average tf-idf document score as a threshold for inclusion in summary"""
    avg_score = sum(scores) / len(scores)
    summary = []
    for index, score in enumerate(scores):
        if score >= threshold * avg_score:
            summary += [text[index]]
    return summary
    

def summarize(text: list[str], inclusion: Callable) -> str:
    """Summarizes a given text using tf-idf and a given inclusion function."""
    sentences = clean_text(text)
    tf_matrix = calculate_tf(sentences)
    idf_matrix = calculate_idf(sentences)
    scores = score_sentences(tf_matrix, idf_matrix, sentences)
    summary = inclusion(text, scores)
    return ' '.join(summary) + '\n'


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['<input-file>']:
        with open(arguments['<input-file>'], 'r', encoding='utf-8') as infile:
            document = load_document(infile)
    else:
        document = load_document(sys.stdin)

    # Threshold value may need adjustment. It might be appropriate to expand this
    # to allow inclusion function and inclusion criteria to be specified as
    # commandline options
    func = lambda text, scores: threshold_inclusion(text, scores, threshold=1)

    if arguments['--output']:
        with open(arguments['--output'], 'w', encoding='utf-8') as outfile:
            outfile.write(summarize(document, func))
    else:
        sys.stdout.write(summarize(document, func))
