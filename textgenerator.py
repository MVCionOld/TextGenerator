import os
import random
import sys

import numpy

import debugging


def reverse_dict(table: dict) -> dict:
    return dict(zip(table.values(), table.keys()))


class TextGenerator:

    def __init__(self, kgrams, code_table, max_gram):
        # stores kgrams with frequencies
        self.__frequency_model = kgrams
        # dict: word -> code (int)
        self.__code_table = code_table
        # length of n-gram
        self.__max_gram = max_gram
        # probabilities model
        self.__model = {}
        debugging.text_gen_logger.info("Model loaded.")
        # count probabilities for all k-grams
        self.__preprocess()
        debugging.text_gen_logger.info("Model's frequency computed.")
        # length of generated sequence
        self.__sequence_length = 0

    def generate_text(self, length: int, output: str, seed: str):

        """
        Public method

        This function goes to directory and writes generated sequence
        into file named 'output.txt' if path to output is defined, else
        outputs in stdout.

        :param output: path, where generated text (sentence/sequence)
            will be outputed
        :param length: length of generated sequence
        :param seed: word, from which sequence will be started
        :return: None

        THIS FUNCTION IS USED IN MODEL.PY (generate_text([...]))
        """

        def make_output(output_stream):
            """
            This is nested method - writes generated sequence into
            'output_stream', which depends, if path to output is defined

            :param output_stream:
            :return:
            """
            if seed not in self.__code_table.keys():
                debugging.text_gen_logger.warning("""
                '%s' is unknown word, generation will start with random seed!
                """ % seed)
            text = self.__sentence_maker(length, seed=seed)
            for sentence in text:
                output_stream.write(sentence + '\n')

        if output is not None:
            debugging.text_gen_logger.info("""
                Generating text with {0} symbols, 
                which started with word '{1}'.
                Output will be stored in '{2}'.
                """.format(length, seed, output))
            try:
                with open(output, 'w') as output_file:
                    make_output(output_file)
            except (NotADirectoryError, PermissionError, FileNotFoundError):
                debugging.text_gen_logger.error("""
                Invalid path or no permission for storing output, terminating.
                """)
                print('Cannot find dir %s or permission denied!' % output)
                sys.exit(1)
        else:
            debugging.text_gen_logger.info("""
                Generating text with {0} symbols, started with word '{1}'.
                Generated text will be displayed into stdout.
                """.format(length, seed, output))
            make_output(sys.stdout)

        debugging.text_gen_logger.info(
            'Text generation ended successfully.')

    def __update_model(self, kgram: tuple, frequency: float):
        """
        Private method

        :param kgram:
        :param frequency:
        :return: None
        """
        sub_gram = kgram[:-1]
        if not sub_gram:
            return
        if sub_gram in self.__model:
            self.__model[sub_gram].append(
                (kgram[-1], frequency / self.__frequency_model[sub_gram]))
        else:
            self.__model[sub_gram] = [
                (kgram[-1], frequency / self.__frequency_model[sub_gram])]

    def __preprocess(self):
        """
        Private method

        Compute probabilities for all continuations of each kgram

        :return: None
        """
        for kgram, frequency in self.__frequency_model.items():
            self.__update_model(kgram, frequency)

    def __sentence_maker(self, length: int, **kwargs) -> str:
        """
        Private method

        This is generator, which yields sentences to the generated text.
        Generally, generated text is only one sentence, but if training
        data is not big enough, there may be situations, when no word
        to append. So generator yields current sequence and starts new
        randomly chosen word.

        :param length:
        :param kwargs:
        :return:
        """
        seed = kwargs.get('seed')
        self.__sequence_length, buffer = 0, []

        if seed is not None:
            seed = self.__code_table[seed]
            buffer.append(seed)

        # swap keys and values in code_table to decode
        # words, when sequence was generated
        self.__code_table = reverse_dict(self.__code_table)
        # extend our code_table with full-stop symbol
        self.__code_table[-1] = '.'

        def buffer_to_str():
            """Nested function to decode sequence to sentence"""
            nonlocal buffer
            sequence = list(map(lambda word: self.__code_table[word], buffer))
            return " ".join(sequence).capitalize()

        def check_buffer():
            """Check buffer to stop adding new words into buffer"""
            nonlocal buffer
            sentence_len = len(buffer_to_str())
            # check if length of generated
            # sentence is bigger than required length
            check_len = sentence_len + self.__sequence_length < length
            if (not buffer or buffer[-1] != -1) and check_len:
                return True
            else:
                return False

        while self.__sequence_length < length:
            while check_buffer():
                # add words while it's possible
                self.__add_word(buffer)
            sentence = list(map(lambda word: self.__code_table[word], buffer))
            sentence = " ".join(sentence).capitalize()
            if sentence[-1] != '.':
                # add full-stop to the end
                sentence += '.'
            yield sentence
            # update length of generated
            self.__sequence_length += len(sentence)
            buffer = []

    def __add_word(self, buffer: list):
        """
        Private method

        Append word(s) to the sentence, according to the current
        lass k-gram. Firstly, check with bigger on, then with
        smaller ones. If continuation was not found - end sentence.

        :param buffer:
        :return:
        """
        if not buffer:
            # if seed is undefined or generating new sentence
            self.__make_beginning(buffer)
        # compute size of window
        kgramsize = min(self.__max_gram, len(buffer))
        for k in range(0, kgramsize):
            beginfrom = len(buffer) - kgramsize + k
            # choose randomly candidate for continuation
            candidate = self.__make_choice(buffer[beginfrom:])
            if candidate != -1:
                # Continuation was found, append it and stop search
                buffer.append(candidate)
                return
        buffer.append(-1)

    def __make_beginning(self, buffer: list):
        """
        Private method

        Append several random words if seed is not defined

        :param buffer: buffer of generated sequence (sequence of codes)
        :return: None
        """
        buffer += list(random.choice(list(self.__frequency_model.keys())))

    def __make_choice(self, kgram: list):
        """
        Private method

        Chooses randomly next word to continue sequence,
        using numpy.random.choice of words (sequence of words)
        according to their probabilities

        :param kgram: last k-ths words of the sequence
        :return: None
        """
        variants = self.__model.get(tuple(kgram))
        if variants is None:
            return -1  # return full-stop if no continuation
        words, probabilities = [], []
        for word, probability in variants:
            words.append(word)
            probabilities.append(probability)

        if words:
            probabilities = numpy.array(probabilities)
            # to avoid probabilities to sum up to
            probabilities /= probabilities.sum()
            result = numpy.random.choice(words, 1, p=probabilities)[0]
        else:
            result = -1
        return result
