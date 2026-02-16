"""
Single-record sentiment analysis wrapper for Laravel integration.

This script wraps the core functions from sentiment_analysis.py to process
a single text input and return JSON output, suitable for being called from
the PHP SentimentAnalysisService via symfony/process.

Usage:
    python analyse_single.py "<text to analyse>"

Output (JSON):
    {
        "success": true,
        "sentiment_score": 0.75,
        "translated_text": "The service was excellent",
        "misspelled_words": "wrds,speling",
        "original_text": "The service was excellent"
    }

On error:
    {
        "success": false,
        "error": "Error message here",
        "sentiment_score": null,
        "translated_text": null,
        "misspelled_words": null
    }
"""

import sys
import json
import os

# Add the script's directory to the path so we can import from sentiment_analysis
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import core functions from the main sentiment analysis script
from sentiment_analysis import analyze_sentiment, detect_and_translate, check_spelling


def analyse_single_text(text):
    """
    Analyse a single text string and return results as a dictionary.
    
    Pipeline:
    1. Spell check → corrected text + list of misspelled words
    2. Language detection + translation → English text
    3. Sentiment analysis → compound score with healthcare lexicon weighting
    """
    if not text or text.strip() == '':
        return {
            'success': True,
            'sentiment_score': None,
            'translated_text': None,
            'misspelled_words': None,
            'original_text': text
        }

    # Skip analysis for trivial comments
    lower_text = text.strip().lower()
    if lower_text in ('no comment', 'no comments', 'n/a', 'na', 'none', '-'):
        return {
            'success': True,
            'sentiment_score': 0.0,
            'translated_text': text,
            'misspelled_words': None,
            'original_text': text
        }

    try:
        # Step 1: Spell check
        corrected_text, misspelled_words = check_spelling(text)
        
        # Step 2: Translate if not English
        translated_text = detect_and_translate(corrected_text)
        
        # Step 3: Sentiment analysis
        sentiment_score = analyze_sentiment(translated_text)
        
        return {
            'success': True,
            'sentiment_score': round(float(sentiment_score), 4),
            'translated_text': translated_text,
            'misspelled_words': ','.join(misspelled_words) if misspelled_words else None,
            'original_text': text
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'sentiment_score': None,
            'translated_text': None,
            'misspelled_words': None,
            'original_text': text
        }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        result = {
            'success': False,
            'error': 'Usage: python analyse_single.py "<text>"',
            'sentiment_score': None,
            'translated_text': None,
            'misspelled_words': None
        }
        print(json.dumps(result))
        sys.exit(1)

    text = sys.argv[1]
    result = analyse_single_text(text)
    print(json.dumps(result))
    sys.exit(0 if result['success'] else 1)
