import re
# import spacy
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string


# def lemmatize(sentence):
#     # Load the English language model
#     nlp = spacy.load("en_core_web_sm")

#     ar = nlp.get_pipe("attribute_ruler")

#     ar.add([[{'TEXT': 'bruh'}], [{'TEXT': 'bruv'}], [
#            {'TEXT': 'bro'}], [{'TEXT': 'broh'}]], {'LEMMA': 'Brother'})

#     # Example sentence
#     # sentence = "bruv playing each other ball talkative cat slower abode worn"

#     # Process the sentence by the lemmatizer
#     doc = nlp(sentence)

#     # Get the lemmatized tokens
#     lemmatized_words = [token.lemma_ for token in doc]

#     # Print the lemmatized words
#     # print('lemmatized',lemmatized_words)
#     return lemmatized_words


def negate_sequence(text):
    # Define a list of negation words and phrases
    negations = ["not", "no", "never", "nothing", "nowhere", "neither", "nor", "non-" "can't", "won't", "shouldn't", "wouldn't", "doesn't", "isn't", "aren't", "ain't", "haven't", "hadn't",
                 "hasn't", "mustn't", "shan't", "wasn't", "weren't", "don't", "didn't", "couldn't", "mightn't", "needn't", "oughtn't", "hadn't've", "couldn't've", "shouldn't've", "wouldn't've"]
    # Split the input text into individual words
    words = text.split()
    # Initialize a flag variable to track whether the current word is negated or not
    negated = False
    # Iterate over each word in the list
    for i, word in enumerate(words):
        # Check if the current word is a negation word
        if word.lower() in negations:
            # If it is, set the negated flag to True
            negated = True
            print("negation found")
        # Otherwise, check if the previous word was negated and the current word is not a punctuation mark
        elif negated and not re.match(r'[^\w\s]', word):
            # If so, append a "not_" prefix to the current word and replace it in the list
            words[i] = "not_" + word
        # Reset the negated flag if the current word is a punctuation mark
        if re.match(r'[^\w\s]', word):
            negated = False
    # Join the modified words back into a single string and return it
    return " ".join(words)


def preprocess(s1, s2):
    s1 = negate_sequence(s1)
    s2 = negate_sequence(s2)
    tokens = word_tokenize(s1.lower())
    tokens = [
        token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    s1 = ' '.join(tokens)

    tokens = word_tokenize(s2.lower())
    tokens = [
        token for token in tokens if token not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    s2 = ' '.join(tokens)

    # s1 = lemmatize(s1)
    # s2 = lemmatize(s2)
    # s1 = ' '.join(s1)
    # s2 = ' '.join(s2)

    punctuation_pattern = r'[^\w\s]'
    s1 = re.sub(punctuation_pattern, '', s1)
    s2 = re.sub(punctuation_pattern, '', s2)
    # print(s1)
    # print(s2)
    return s1, s2
