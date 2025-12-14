import re
import nltk
from nltk.corpus import stopwords

try: nltk.data.find('corpora/stopwords')
except LookupError: nltk.download('stopwords', quiet=True)

def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in text.split() if word not in stop_words]
    return " ".join(tokens)
