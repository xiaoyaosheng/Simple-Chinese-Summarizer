"""

Simple-Chinese-Summarizer

A very simple summarizier built using NLP in Python

"""

import argparse

from heapq import nlargest

from collections import defaultdict

from pyltp import SentenceSplitter

import jieba.analyse


def main():
    """ Drive the process from argument to output """

    args = parse_arguments()

    content = read_file(args.filepath)

    content = sanitize_input(content)

    sentence_tokens, word_tokens_rank = tokenize_content(content)

    sentence_ranks = score_tokens(word_tokens_rank, sentence_tokens)

    return summarize(sentence_ranks, sentence_tokens, args.length)


def parse_arguments():
    """ Parse command line arguments """

    parser = argparse.ArgumentParser()

    parser.add_argument('filepath', help='File name of text to summarize')

    parser.add_argument('-l', '--length', default=4, help='Number of sentences to return')

    args = parser.parse_args()

    return args


def cut_sentence(content):
    """

    :param content:

    :return:

    """

    content.split(',')


def read_file(path):
    """ Read the file at designated path and throw exception if unable to do so """

    try:

        with open(path, 'r', encoding="UTF-8") as file:

            return file.read()

    except IOError as e:

        print("Fatal Error: File ({}) could not be locaeted or is not readable.".format(path))


def sanitize_input(data):
    """

    Currently just a whitespace remover. More thought will have to be given with how

    to handle sanitzation and encoding in a way that most text files can be successfully

    parsed

    """

    replace = {

        ord('\f'): ' ',

        ord('\t'): ' ',

        ord('\n'): ' ',

        ord('\r'): None

    }

    return data.translate(replace)


def tokenize_content(content):
    """

    """

    jieba.analyse.set_stop_words("data/stop_words.txt")

    tags = jieba.analyse.extract_tags(content, topK=10, withWeight=True)

    word_tokens_rank = dict()

    for tag in tags:
        word_tokens_rank[tag[0]] = tag[1]

    return [

        SentenceSplitter.split(content),

        word_tokens_rank

    ]


def score_tokens(words_tokens_rank, sentence_tokens):
    """

    Builds a frequency map based on the filtered list of words and

    uses this to produce a map of each sentence and its total score

    """

    ranking = defaultdict(int)

    for i, sentence in enumerate(sentence_tokens):

        for word in jieba.cut(sentence.lower(), cut_all=False):  # 精确模式

            if word in words_tokens_rank:
                print('word_tokens_rank[{}]'.format(word), words_tokens_rank[word])

                ranking[i] += words_tokens_rank[word]

    return ranking


def summarize(ranks, sentences, length):
    """

    Utilizes a ranking map produced by score_token to extract

    the highest ranking sentences in order after converting from

    array to string.

    """

    if int(length) > len(sentences):
        print("Error, more sentences requested than available. Use --l (--length) flag to adjust.")

        exit()

    indexes = nlargest(length, ranks, key=ranks.get)

    final_sentences = [sentences[j] for j in sorted(indexes)]

    return ' '.join(final_sentences)


if __name__ == "__main__":
    print(main())
