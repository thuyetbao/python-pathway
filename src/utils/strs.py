import string

def remove_punctuation(text: str = None):
    rmv_text = text.translate(str.maketrans('', '', string.punctuation))
    return rmv_text