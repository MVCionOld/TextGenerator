N_GRAM_SIZE = 5

generate_args = {
    "--model": """
        (Compulsory argument)
        The path to the file from which the model is loaded.
    """,
    "--seed": """
        (Optional argument) 
        The initial word. If not specified, select the word 
        randomly from all words (not including the frequency).
    """,
    "--length": """
        (Compulsory argument)
        Length of the generated sequence.
    """,
    "--output": """
        (Optional argument)
        The file to which the result will be recorded. 
        If there is no argument, output to stdout.
    """
}

train_args = {
    "--input-dir": """
        (Compulsory argument)
        The path to the directory in which the collection 
        of documents lies. If this argument is not specified, 
        assume that the texts are entered from stdin.
    """,
    "--model": """
        (Compulsory argument)
        The path to the file in which the model is stored.
    """,
    "--lc": """
        (Optional argument) 
        Change texts to lowercase.
    """,
    "--webparse": """
        (Optional argument) 
        Url for site which model will train.
    """
}
