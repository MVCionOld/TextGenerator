Text Generator

Task: to develop a utility that generates its own based on the given texts.

Required part from task (https://docs.google.com/document/d/1ka4MdenzgrdfXiyOU_HxEjjXPhehNk-yWX7K2h3zdkI/edit) is done. The following bonus tasks were performed:

    generalization from bigram to n-grammes (coordination between words became better);
    collecting texts for learning a model from some site (also it was generalized - suitable for many sites). Also, logging were added.

Collection of frequencies for the model and its use (text generation) - 2 separate modules, train.py and generate.py.

Parameters of the console interface train.py and generate.py:

train.py:

    --input-dir - Path to the directory in which the collection of documents lies. If this argument is not specified, assume that the texts are entered from stdin.
    --webparse - An optional argument. The address of the site on which the model is trainig. (Can combine with reading from local files or stdin).
    --model - The path to the file in which the model is saved.
    --lc - An optional argument. Brings texts to lowercase.
    --help - An optional argument. To make it clear how to use this utility.

generate.py:

    --model - The path to the file from which the model is loaded.
    --seed - An optional argument. The initial word. If not specified, select the word randomly from all words (not including the frequency).
    --length - Length of the generated sequence.
    --output - An optional argument. The file to which the result will be recorded. If there is no argument, output to stdout.
    --help - An optional argument. To make it clear how to use this utility.

Local modules:

    debugging - includes decorators with debugging workflow for functions from train.py and generate.py, creates loggers for all executable modules;
    model - parses texts and train frequency model on them: counts occurrences of all k-grams, stores model (train.py) and loads (generate.py);
    textgenerator - counts probabilities for all k-grams and generates sequences;
    webparser - trains model on data from web-sites;
    config - include size of n-grammes (N_GRAM_SIZE) and parameters for ArgumentParser.

Third-party libraries:

    requests - allows to send HTTP requests (webparser.py);
    bs4 - reads required data from requests (webparser.py);
    numpy - normalizes the frequencies and make numpy.random.choice (textgenerator.py).


