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
    def __init__(self, x, y):
        self.x = x
        self.y = y

GRIDSIZE = GridSize(10, 10)
MAXLENGTH = 10


def process_language(filename: str) -> tuple:
    """ Reads a name file and converts it into a Markov chain """

    with open(filename, "r") as file:
        lines = file.readlines()

    names = defaultdict(list)
    starting_triplets = []
    for line in lines:
        # This loops through each triplet of letters
        # Each triplet is a key in the names dict, with the next letter as the value
        for i in range(len(line) - 3):
            # Make a list of all triplets that start names
            if i == 0:
                starting_triplets.append(line[i:i+3])

            next_letter = line[i+3]
            if next_letter != "\n":
                names[line[i:i+3]].append(next_letter)

    return (names, starting_triplets)


def generate_name(names: tuple) -> str:
    """ Generates one random name using the names Markov chain """

    # Extract data from names
    starting_triplets = names[1]
    names = names[0]

    name = []

    # The first three letters of name are chosen randomly from all possible letter triplets in names.
    # The chosen triplet is then cast to a list, and appended to name.
    name.extend(choice(list(starting_triplets)))

    # Following letters are chosen randomly from the Markov chain
    # If next_letter is the endstate, end the word
    while True:
        next_letter = generate_next_letter(name, names)
        if next_letter == "." or len(name) >= MAXLENGTH:
            break
        else:
            name.append(next_letter)

    # Convert name to a str, and capitalize it
    name = "".join(name)
    name = name.capitalize()
    return name


def generate_next_letter(name: list, names: defaultdict) -> str:
    """ Chooses next letter randomly from the names Markov chain """

    # current_state is the last three letters of name
    current_state = "".join(name[-3:])

    return choice(names[current_state])


def generate_names(filename: str) -> list:
    """ Generate a grid of names to be displayed in the GUI """

    corpus = process_language(filename)

    # Generate each row of names
    names = []
    for _ in range(GRIDSIZE.x * GRIDSIZE.y):
        names.append(generate_name(corpus))

    return names
