from app.configuration import NOISE_KEYWORDS, ANALYSIS_KEYWORDS

def score_article(title, content):
    text = (title + " " + content).lower()
    score = 0

    for kw in ANALYSIS_KEYWORDS:
        if kw in text:
            score += 2

    if "on-chain" in text:
        score += 3
    if "technical analysis" in text:
        score += 3
    if "price prediction" in text:
        score += 3

    return score


def is_noise(title):
    text = title.lower()
    return any(k in text for k in NOISE_KEYWORDS)
