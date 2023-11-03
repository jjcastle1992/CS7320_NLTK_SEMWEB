import nltk
from nltk.corpus import stopwords
import re
# import spacy

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            text = file.read()
            file.close()
            return text

    except FileNotFoundError:
        return []


def clean_text(text_to_clean):
    """
    Cleans given strings of text by:
     1. Removing punctuation
     2. Setting text to all lower case.
     3. Tokenizes into words
     4. Removes stopwords using nltk list
    :param text_to_clean: a string of text.
    :return: string of cleaned text
    """
    # remove punctuation
    no_punct_re = r'[^\w\s]'
    text_without_punct = re.sub(no_punct_re, '', text_to_clean)

    # set text to lowercase
    lower_text = text_without_punct.lower()

    # tokenize text into words
    lower_tokens = nltk.word_tokenize(lower_text)

    # remove stopwords
    stop_words = stopwords.words('english')

    ftr_tkns = [word for word in lower_tokens if word not in stop_words]

    # concat back into one big string
    cleaned_text = ' '.join(ftr_tkns)

    # return cleaned string
    return cleaned_text


def tokenize_file_sentences(file_name):
    try:
        with open(file_name, 'r') as file:
            text = file.read()
            sentences = nltk.sent_tokenize(text)
            return sentences

    except FileNotFoundError:
        return []

    finally:
        file.close()



def main():
    file_name = 'hw4.facts.txt'
    our_text = read_file(file_name)
    print(our_text)
    raw_sentences = nltk.sent_tokenize(our_text)
    cleaned_setences = []
    for sentence in raw_sentences:
        cleaned_sent = clean_text(sentence)
        cleaned_setences.append(cleaned_sent)
    # sentences = tokenize_file_sentences(file_name)
    # print(sentences)
    print('CLEANED SENTENCES\n')
    print(cleaned_setences)
    # words = [nltk.word_tokenize(sentence) for sentence in sentences]
    # print(words)

main()
