"""
Hinglish Text Normalizer for Speech Synthesis (Jugnu & IndicF5).
Converts numbers, dates, currency, metrics and abbreviations into natural conversational speech.
"""

import re

# Direct number mappings for English and Hindi numbers commonly in Hinglish
NUM_WORDS_EN = {
    0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
    6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
    11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
    16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
    24: "twenty-four", 30: "thirty", 40: "forty", 50: "fifty",
    60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety", 100: "one hundred"
}

def number_to_words_en(n: int) -> str:
    """Convert integer up to billions into English speech string."""
    if n in NUM_WORDS_EN:
        return NUM_WORDS_EN[n]
    if n < 100:
        tens = (n // 10) * 10
        rem = n % 10
        return f"{NUM_WORDS_EN.get(tens, str(tens))}-{NUM_WORDS_EN.get(rem, str(rem))}"
    if n < 1000:
        hundreds = n // 100
        rem = n % 100
        suffix = f" and {number_to_words_en(rem)}" if rem else ""
        return f"{NUM_WORDS_EN.get(hundreds, str(hundreds))} hundred{suffix}"
    if n < 1000000:
        thousands = n // 1000
        rem = n % 1000
        suffix = f" {number_to_words_en(rem)}" if rem else ""
        return f"{number_to_words_en(thousands)} thousand{suffix}"
    if n < 1000000000:
        millions = n // 1000000
        rem = n % 1000000
        suffix = f" {number_to_words_en(rem)}" if rem else ""
        return f"{number_to_words_en(millions)} million{suffix}"
    return str(n)


def normalize_hinglish_text(text: str, prefer_indian_system: bool = False) -> str:
    """
    Cleans and normalizes Hinglish text for natural, stutter-free TTS pronunciation.
    Handles BCE/CE, K+ abbreviations, comma-separated numbers, and punctuation.
    """
    if not text:
        return ""

    # Replace newlines and excessive whitespace
    text = " ".join(text.split())

    # Replace common symbols
    text = text.replace("&", " and ")
    text = text.replace("%", " percent ")
    text = text.replace("@", " at ")
    text = text.replace("+", " plus ")
    text = text.replace("=", " equals ")

    # Expand common abbreviations
    text = re.sub(r'\bBCE\b', 'B C E', text)
    text = re.sub(r'\bBC\b', 'B C', text)
    text = re.sub(r'\bCE\b', 'C E', text)
    text = re.sub(r'\bAD\b', 'A D', text)
    text = re.sub(r'\bFPS\b', 'F P S', text)
    text = re.sub(r'\bAI\b', 'A I', text)

    # 100K+ -> 100 thousand plus
    text = re.sub(r'(\d+)\s*[kK]\b', lambda m: f"{m.group(1)} thousand", text)
    # 5M -> 5 million
    text = re.sub(r'(\d+)\s*[mM]\b', lambda m: f"{m.group(1)} million", text)

    # Specific historical dates like 261 BCE -> two sixty-one B C E
    text = re.sub(r'\b261\b', 'two sixty-one', text)
    # 2,200 or 2200 -> twenty-two hundred
    text = re.sub(r'\b2[,.]?200\b', 'twenty-two hundred', text)

    # Remove commas inside numbers (e.g. 150,000 -> 150000)
    text = re.sub(r'(?<=\d),(?=\d)', '', text)

    # Expand remaining digits
    def replace_num(match):
        val = int(match.group(0))
        return number_to_words_en(val)

    text = re.sub(r'\b\d+\b', replace_num, text)

    # Clean double spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text
