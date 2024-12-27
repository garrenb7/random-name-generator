# Name Generator

## Demonstration

You can find a video demonstration of Name Generator on YouTube at this URL: ()

## Project Description

### Introduction

Welcome to Name Generator, my final project for Harvard's CS50x!

Name Generator is a program that generates random names in several different languages using Python.  It also uses Flask in order to create a more pleasant and intuitive HTML/CSS GUI.  My hope is that Name Generator will be useful whenever someone needs a random name: for example, if one needs to create a name for a roleplaying character, a video game avatar, or something similar.  The names my program generates often do not exist in the real world because they're randomly generated.  However, my algorithm ensures that they always look as though they could be plausible names from whatever language is chosen.

### How Name Generator Works

#### Overview

Name Generator uses [Markov chains](https://en.wikipedia.org/wiki/Markov_chain) to generate random names.  A Markov chain is a model in which the current state of the system is chosen randomly based on one or more of the previous states, called the *n*-gram.  In this case, each letter in the name is a state, and I choose the next letter based on the two previous ones.  This makes my *n*-gram a *2*-gram, but any value of *n* could have been chosen.  The Markov chain algorithm takes a corpus of many names as an input, and uses it to calculate the probability of any state following the *n*-gram.  Therefore, when a new state is chosen, it is chosen from only the states which followed the *n*-gram in the corpus.

For example, if one were generating an English name, and had the *n*-gram `ax`, the letter `h` would not be available to be chosen as the next state, because the combination `axh` never occurs in the English corpus of names.

In my program, there is a form on the GUI which allows the user to select a language in which to generate names.  This selects the correct corpus from the several pre-made corpuses included in the code's `names/` directory.

#### Formatting the Corpus

The corpus must be formatted before it is processed into a Markov chain.

Here's an example using three common English words as a small corpus: `bit`, `bat`, and `ate`.  In order to process the corpus, it must be in a usable format.  In my implementation, that means that it must be a newline-separated `.txt` file with no capital letters and a period at the end of each name.  This means that our example corpus would appear as follows:
```
bit.
bat.
ate.
```
The `.` character is the end state.  It simply represents the end of each word.  It is treated just like any other letter, except that when it is chosen as the next state, the word must end.  This means that the program does not need to manually end words, or choose a length for each word, because they come to a natural end as part of the generative process.

#### Processing the Corpus

Now, the corpus can be processed to create a Markov chain.

To create the chain, we need to create two data structures: a dictionary and a list.

- Each *n*-gram which appears in the corpus anywhere is stored as a key in the dictionary.  The corresponding value of each key is a list of every character which ever directly follows that key in the corpus, including the end state.
- Each *n*-gram which appears at the beginning of a name in the corpus is additionally stored as an item in the list.

Here is an example using the corpus that was just formatted,
```
bit.
bat.
ate.
```
The first entry in the dictionary will have *n*-gram `bi` as a key, and a corresponding value which is a list containing `t` as its only member.  The first member of the list will be `bi`, because it occurs at the beginning of a word.  This will cause the current data structures to look like this:
```
// Dictionary
{
    "bi": ["t"]
}

// List
["bi"]
```
If the processing is continued for the rest of the corpus, the final product will look like this:
```
// Dictionary
{
    "bi": ["t"]
    "it": ["."]
    "ba": ["t"]
    "at": [".", "e"]
    "te": ["."]
}

// List
["bi", "ba", "at"]
```

#### Generating One Name

To generate a name with the new Markov chain, you need to start by choosing a random key from the list that was just generated.  The new name's starting *n*-gram is chosen from that list so that the name looks more plausible.  For example, the letter pair `ng` is common in English, but it doesn’t occur at the beginning of names.  Therefore, it will not have been included in the list, and will never be chosen to start a word.

In this example, using the same data structures that were just processed, `ba` is chosen by chance to start the word.

From there, the program performs a random walk through the Markov chain.  It looks at the last *n*-gram which was added to the name, in this case `ba`.  It finds the matching key in the dictionary, and chooses a random letter from the corresponding value list.  In this example, the only choice is the letter `t`, because the dictionary entry for `ba` is:
```
{
    "ba": ["t"]
}
```
This means that the word is now `bat`, and the last *n*-gram is `at`.

This process is repeated, looking at the prior *n*-gram and choosing a new letter based on that state.  Eventually, the end state will be chosen, which immediately ends the word.  In this example, we end up with the word `bate.`.

Finally, the name must be formatted properly: it needs capitalized, and the end state needs to be removed before the name is displayed.  Therefore, the final product is `Bate`.

#### Generating Many Names

In my code, there is a function called `generate_name`.  `generate_name` generates a single name using the process described above.  A separate function, `generate_names`, calls `generate_name` repeatedly, until there are enough names to fill up the grid on the results page of the GUI.  When the user selects a language with the form on the GUI, the form also gets the size of the viewport.  This is given to `generate_names`, which uses the data to calculate how many names can fit in the viewport.

`generate_names` also filters unwanted names.  This includes duplicate names, names that are two letters long or less, or names that are ten letters long or more.

### GUI Layout

The GUI has three parts: the home page, the results page, and the about page.

1. The home page is where the user begins when they visit the site.  It includes the form where they can choose the language to generate names in.  It also has a generate button, which submits the form and redirects them to the results page.

2. The results page has a table that displays all of the names that were generated.  The form from the home page is also included on the results page.  The form keeps the language that the user chose selected.  This means that the user can generate names in the same language repeatedly, without needing to continue selecting the language.

3. The about page can be reached by a link which is included directly below the form on the home and results page.  It simply explains how the code for Name Generator works, and has nothing to do with the functionality of the program.  It also includes a link to the code on GitHub.

### Code Layout

My code uses Python with Flask, as previously noted.  The layout is the same as a normal Flask application.  It has seven main parts:

1. `README.md`;

2. `app.py`, which is the standard Flask code to handle routes on the GUI;

3. `names.py`, which contains all of the name generation and corpus processing algorithms;

4. `templates/`, which is the directory that contains all of the HTML;

5. `static/`, which is the directory that contains the stylesheet and the favicon files;

6. `names/`, which is the directory that contains the corpus for each language my program supports;

7. and `requirements.txt`.

## Acknowledgements

The following sources were instrumental in enabling the success of this project.

- [Using a Markov chain to generate readable nonsense with 20 lines of Python](https://benhoyt.com/writings/markov-chain/)

- [Procedural Name Generator](https://www.samcodes.co.uk/project/markov-namegen/)

- [Markov Chain - Wikipedia](https://en.wikipedia.org/wiki/Markov_chain)

- The staff of Harvard's CS50 and CS50x classes
