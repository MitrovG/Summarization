from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

import pickle

import os.path
import re

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.utils import get_stop_words


LANGUAGE = 'english'

# Algorithms that are used
SUMY_ALGORITHMS = [KLSummarizer, LexRankSummarizer, LsaSummarizer, LuhnSummarizer,
                   ReductionSummarizer, SumBasicSummarizer, TextRankSummarizer]
# Derived name for algorithms for key name in the dictionary
ALGORITHMS = [element.__name__.replace("Summarizer", "") for element in SUMY_ALGORITHMS]


def find_path_for_training_data(index):
    """Find the absolute paths for the training data files"""

    file_paths = list()
    additional_path = "/BBC-News-Summary/News-Articles/"
    for key in index.keys():
        file_paths.append((os.getcwd() + additional_path + key).replace("\\","/"))

    return file_paths


def load_index_data_structure(filepath):
    """Load the pickle structure"""

    with open(filepath, 'rb') as index_file:
        index = pickle.load(index_file)

    return index


def generate_summary(algorithm, number_of_sentence, file_name):
    """Generate summary based on the algorithm and the number of sentences that are provided.
        The return result is string"""

    parser = PlaintextParser.from_file(file_name, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = algorithm(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    # for sentence in summarizer(parser.document, number_of_sentence):
    #     print(sentence)
    sentences = summarizer(parser.document, number_of_sentence)
    str_sentences = list()
    for sentence in sentences:
        str_sentence = str(sentence)
        if str_sentence[-1] != '.':
            str_sentence = str_sentence + "."
        str_sentences.append(str_sentence)

    return ' '.join(str_sentences)


def generate_sumy_summaries(file_paths):
    """Generates dictionary structure for all possible sumy algorithms with number of sentences
    between 4 and 7. The dictionary structure looks like this:

    {
        'sports/001.txt' : {
                                'KL' : [ (summary, parameter), (summary, parameter) .. ]
                                'LexRanka' : [ (summary, parameter), (summary, parameter) .. ]
                                ..
                            }
        'tech/022.txt' : {
                                'KL' : [ (summary, parameter), (summary, parameter) .. ]
                                'LexRanka' : [ (summary, parameter), (summary, parameter) .. ]
                                ..
                            }
        ..
    }
    """

    sumy_index = dict()

    for file_name in file_paths:

        file_name_key = re.sub(".*News-Articles/", "", file_name)
        sumy_index.setdefault(file_name_key, dict())

        for alg_index, algorithm in enumerate(SUMY_ALGORITHMS):
            for number_of_sentences in range(4, 8):

                summary = generate_summary(algorithm, number_of_sentences, file_name)
                parameter = "sentences:" + str(number_of_sentences)
                sumy_index[file_name_key].setdefault(ALGORITHMS[alg_index], list()).append((summary, parameter))

    return sumy_index


def create_pickle(data, file_path):
    """Create pickle structure from data"""

    with open(file_path, "wb") as pickle_file:
        pickle.dump(data, pickle_file)


if __name__ == '__main__':

    # index = load_index_data_structure("index.pickle")
    # file_paths = find_path_for_training_data(index)
    # sumy_index = generate_sumy_summaries(file_paths)
    # create_pickle(sumy_index, "sumy_index.pickle")
    # print()

    # with open("sumy_index.pickle", "rb") as pickle_pickle:
    #     result = pickle.load(pickle_pickle)
    #
    # for key in result.keys():
    #     if "sport/043" in key:
    #         for algorithm in result[key].keys():
    #             print(key + ":" + algorithm + ":" + str(result[key][algorithm]))
   print()