import csv
import filecmp

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

def write_file(file_name, data_source):
    with open (file_name, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # write headers
        csv_writer.writerow(['Entity'])

        # write entities
        for data in data_source:
            csv_writer.writerow(data)
        print('file written')
        csv_file.close()


def clean_text(text_to_clean, rem_punc=True, lower=True, rem_sw=True):
    """
    Cleans given strings of text by:
     1. Removing punctuation
     2. Setting text to all lower case.
     3. Tokenizes into words
     4. Removes stopwords using nltk list
    :param text_to_clean: a string of text
    :param rem_punc: Bool where True removes punctuation
    :param lower: Bool where True sets punctuation to lowercase
    :param rem_sw: Bool where True removes stopwords (English)
    :return: string of cleaned text
    """
    # remove punctuation
    if(rem_punc):
        no_punct_re = r'[^\w\s]'
        text_to_clean = re.sub(no_punct_re, '', text_to_clean)

    # set text to lowercase
    if(lower):
        text_to_clean = text_to_clean.lower()

    # tokenize text into words
    tokens = nltk.word_tokenize(text_to_clean)

    # remove stopwords
    if(rem_sw):
        stop_words = stopwords.words('english')
        tokens = [word for word in tokens if word not in stop_words]

    # concat back into one big string
    cleaned_text = ' '.join(tokens)

    # return cleaned string
    return cleaned_text


def named_entity_extractor(entities, num_words):
    named_entities = []
    names = []

    for idx in range(num_words):
        # print(entities[idx], '\t', type(entities[idx]))
        if(isinstance(entities[idx], nltk.Tree)):
            named_entities.append(entities[idx].label())
            names.append(entities[idx][0][0])

    return named_entities, names


def get_phrase_interest(sent_interest, name_type_pairs):
    """takes in a list of sentences of interest and list of entities of
    interest to find and uses regex to extract the phrase
    of interest.
    :param sent_interest: list of str sentences of interest
    :param name_type_pairs:list tuples of name, POS pairs
    returns: a list of short phrases and a list of substitution terms
    """
    short_phrases = []
    sub_terms = []

    for idx, sentences in enumerate(sent_interest):
        # determine our start and end words
        start_name = name_type_pairs[idx][0][1]
        end_name = name_type_pairs[idx][1][1]

        # regex to find the short phrases incl start and end names
        pattern = re.escape(start_name) + r'(.*?)' + re.escape(end_name)
        match = re.search(pattern, sentences)
        if (match):
            target_phrase = start_name + match.group(1) + end_name
            sub_phrase = match.group(1)
            sub_phrase = sub_phrase.strip()
            # print(target_phrase)
            # append short_phrases with target phrase and sub_terms
            # with sub_phrases
            short_phrases.append(target_phrase)
            sub_terms.append(sub_phrase)

    return short_phrases, sub_terms



def main():
    # nltk.download('words')
    file_name = 'hw4.facts.txt'
    our_text = read_file(file_name)
    # print(our_text)
    raw_sentences = nltk.sent_tokenize(our_text)

    # Set to send clean or raw sentences
    clean = True
    no_punct = True
    lowercase = False
    rem_stopwords = False
    if (clean):
        cleaned_sentences = []
        for sentence in raw_sentences:
            cleaned_sent = clean_text(sentence, no_punct, lowercase,
                                      rem_stopwords)
            cleaned_sentences.append(cleaned_sent)

    # NER
    sentences_of_interest = []
    entity_interest = []
    name_type_pairs_interest = []
    entity_list = []  # for debugging
    if(clean):
        for sentences in cleaned_sentences:
            tokens = nltk.word_tokenize(sentences)
            entities = nltk.ne_chunk(nltk.pos_tag(tokens))
            entity_list.append(entities)
            entity_types, names = named_entity_extractor(entities,
                                                         len(tokens))

            # merge entity types and names into a list
            name_type_pairs = list(zip(entity_types, names))

            # Check to see if entity_types starts with person and has 2
            # values.
            if(len(entity_types) == 2 and entity_types[0] == 'PERSON'):
                sentences_of_interest.append(sentences)
                name_type_pairs_interest.append(name_type_pairs)
                entity_interest.append(entity_types)

    short_phrases, subs = get_phrase_interest(sentences_of_interest,
                                              name_type_pairs_interest)

    print(short_phrases)

    # write foaf/schema dict for subs
    print(subs)

    # write_file('entity_data.csv', entity_list)



main()
