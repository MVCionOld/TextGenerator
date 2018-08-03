import collections
import pickle
import re

import textgenerator


def find_kgrams(words, k):
    return zip(*[tuple(words[i:],) for i in range(k)])


class Model:

    def __init__(self, n: int):
        # length of n-gram
        self.__max_gram = n
        # stores kgrams with frequencies
        self.__k_grams = collections.defaultdict(int)
        # dict: word -> code (int)
        self.__lexicon = collections.defaultdict(int)
        # total unique words
        self.__word_counter = 0
        # buffer to compute all k-grams
        self.__word_buffer = collections.deque()

    def train(self, line: str):
        """
        Public method

        This method stores model: dictionary with words and their
        codes (number in order of occurrence in input stream).

        This method uses generator _Model__word_generator to
        parse line for all k-grams and update frequency of this
        model.

        :param line: new line to train this model
        :return: None

        THIS FUNCTION IS USED IN TRAIN.PY
        """
        generator = self.__word_generator(line)
        for kgram in generator:
            for lexeme in kgram:
                self.__check_lexicon(lexeme)
            self.__member_entrance(kgram)

    def store(self, file):
        """
        Public method

        This method stores model: dictionary with words and their
        codes (number in order of occurrence in input stream).

        This method uses 'pickle' to dump model.

        :param file: file where frequency model will be dumped
        :return: None

        THIS FUNCTION IS USED IN TRAIN.PY
        """
        return pickle.dump((self.__k_grams, self.__lexicon), file, 2)

    def load(self, file):
        """
        Public method

        This method loads model: dictionary with words and their
        codes (number in order of occurrence in input stream).

        This method uses 'pickle' to load model.

        :param file: file where frequency model was dumped
        :return: None

        THIS FUNCTION IS USED IN GENERATE.PY
        """
        self.__k_grams, self.__lexicon = pickle.load(file)

    def generate_text(self, output: str, length: int, seed: str):
        """
        Public method

        This method initialise TextGenerator (from module 'textgenerator'),
        init parameters are: output, length, seed.
        The next generation and output occurs in the implementation of
        this module

        :param output: path, where generated text (sentence/sequence)
            will be outputed
        :param length: length of generated sequence
        :param seed: word, from which sequence will be started
        :return: None

        THIS FUNCTION IS USED IN GENERATE.PY
        """
        generator = textgenerator.TextGenerator(
            self.__k_grams, self.__lexicon, self.__max_gram)
        generator.generate_text(length, output, seed)

    def __word_generator(self, line: str):
        """
        Private method

        This is generator, used in method 'train', it yields all k-grams,
        including last (max_gram - 1) words from the last line.
        Also, is split line and removes non-alphabetic characters.

        :param line: new line in the text to parse
        :return:
        """
        while len(self.__word_buffer) >= self.__max_gram:
            self.__word_buffer.popleft()
        words = re.sub('[^А-Яа-яЁёЪъ ]+', '', line).split()
        self.__word_buffer.extend(words)
        words = list(self.__word_buffer.copy())
        for k in range(1, min(self.__max_gram, len(words)) + 1):
            for kgram in find_kgrams(words, k):
                yield kgram

    def __get_code(self, lexeme: str) -> int:
        """
        Private method

        Gives code of lexeme in lexicon

        :param lexeme: str
        :return: int: entrance code of word in model
        """
        return self.__lexicon.get(lexeme)

    def __check_lexicon(self, lexeme: str):
        """
        Private method

        Updates lexicon and word_counter if new word was found

        :param lexeme: next lexeme in the text
        :return: None
        """
        if self.__get_code(lexeme) is None:
            self.__lexicon[lexeme] = self.__word_counter
            self.__word_counter += 1

    def __member_entrance(self, k_gram):
        """
        Private method

        Updates frequency if k-gram was found before

        :param k_gram: current k-gram in the text
        :return: None
        """
        code_combination = [self.__get_code(lexeme) for lexeme in k_gram]
        kcode = tuple(code_combination,)
        self.__k_grams[kcode] += 1
