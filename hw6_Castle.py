import nltk
import re

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
    sentences = tokenize_file_sentences(file_name)
    print(sentences)
    words = [nltk.word_tokenize(sentence) for sentence in sentences]
    print(words)

main()
