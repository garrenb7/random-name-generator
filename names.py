from collections import defaultdict
from random import choice


filenames = {
    "names/de.txt": "German",
    "names/en.txt": "English",
    "names/es.txt": "Spanish",
    "names/ja.txt": "Japanese",
    "names/pl.txt": "Polish",
}


class GridSize:
    def __init__(self, viewport_width, viewport_height):
        viewport_width = round(viewport_width) // 153
        viewport_height = round(viewport_height) // 80
        self.grid_x = viewport_width
        self.grid_y = viewport_height
        self.num_cells = self.grid_x * self.grid_y


MAX_LENGTH = 10
NGRAM_LENGTH = 2


def process_language(filename: str) -> tuple:
    """ Reads a name file and converts it into a Markov chain """

    with open(filename, "r") as file:
        lines = file.readlines()

    names = defaultdict(list)
    starting_ngrams = []

    for line in lines:
        # This loops through each n-gram of letters
        # Each n-gram is a key in the names dict, with the next letter as the value
        for i in range(len(line) - NGRAM_LENGTH):
            # Make a list of all n-grams that start names
            if i == 0:
                starting_ngrams.append(line[i:i+NGRAM_LENGTH])

            next_letter = line[i+NGRAM_LENGTH]
            if next_letter != "\n":
                names[line[i:i+NGRAM_LENGTH]].append(next_letter)

    return (names, starting_ngrams)


def generate_name(names: tuple) -> str:
    """ Generates one random name using the names Markov chain """

    # Extract data from names
    starting_ngrams = names[1]
    names = names[0]

    name = []

    # The first NGRAM_LENGTH letters of name are chosen randomly from all possible n-grams in names.
    # The chosen n-gram is then cast to a list, and appended to name.
    name.extend(choice(list(starting_ngrams)))

    # Following letters are chosen randomly from the Markov chain
    # If next_letter is the endstate, end the word
    while True:
        next_letter = generate_next_letter(name, names)
        if next_letter == "." or len(name) >= MAX_LENGTH:
            break
        else:
            name.append(next_letter)

    # Convert name to a str, and capitalize it
    name = "".join(name)
    name = name.capitalize()
    return name


def generate_next_letter(name: list, names: defaultdict) -> str:
    """ Chooses next letter randomly from the names Markov chain """

    # current_state is the last NGRAM_LENGTH letters of name
    current_state = "".join(name[-NGRAM_LENGTH:])

    return choice(names[current_state])


def generate_names(filename: str, viewport_width: float, viewport_height: float) -> tuple:
    """ Generate a grid of names to be displayed in the GUI """

    grid_size = GridSize(viewport_width, viewport_height)
    num_names = grid_size.num_cells
    corpus = process_language(filename)

    # Generate each row of names
    names = []
    for _ in range(num_names):
        # Make sure that no duplicate names are generated
        while True:
            name = generate_name(corpus)
            if not filter_name(name, names):
                names.append(name)
                break

    return (names, grid_size)


def filter_name(name: str, names: list) -> bool:
    """ Filters names that are too short or have already been generated """

    if name in names:
        return True
    if len(name) <= 2:
        return True
    else:
        return False
