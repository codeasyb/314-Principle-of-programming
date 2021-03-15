# open and read the file and create a histogram
#
# Amir Ayoub
# Date: 12/15/2019
# Program: Histogram
# File: examine.py
#
import argparse
import operator
import os
import string
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from numpy import unicode

def createNewfile(file):
    # parse to the end of the file name
    file = file.rsplit('.',1)[0]
    # add this at the end
    ext = "_hist.png"
    makeFile = file + ext
    return makeFile

def main():
    # this is to show the user error description of not input the filepath
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--filepath', dest='filepath', metavar='file path', help='Path to text input file to be analysed.', required=True)
    parser.add_argument('-n', '--number', dest='number', metavar='number', help='Most frequent n words will be displayed and plotted.', required=False, default=100, type=int)
    args = parser.parse_args()
    # Path to text file to analyse
    rawfilepath = args.filepath
    # Print a histogram containing the top N words, and print them and their counts.
    top_n = args.number
    # Load the file
    filename = os.path.normpath(os.path.join(rawfilepath))

    file = open(filename, 'r')

    # Parse as a list, removing lines
    content_lists = [line.split(',') for line in file.readlines()]

    # Parse into a single list (from a list of lists)
    content_list = [item for sublist in content_lists for item in sublist]

    # Remove whitespace so we can concatenate appropriately, and unify case
    list_strip = [str.strip().lower() for str in content_list]

    # Concatenate strings into a single string
    strings_concat = ' '.join(list_strip)

    # Remove punctuation and new lines
    punctuation = set(string.punctuation)
    punctuation_content = ''.join(x for x in strings_concat if x not in punctuation)

    # Split string into list of strings, again
    list_words = punctuation_content.split()

    # Perform count
    count = Counter(list_words)
    words, count_values = zip(*count.items())

    #  Sort both lists by frequency in values
    values_sorted, words_sorted = zip(*sorted(zip(count_values, words), key=operator.itemgetter(0), reverse=True))

    # Top N
    words_sorted_top = words_sorted[0:top_n]
    values_sorted_top = values_sorted[0:top_n]

    # create Histogram
    xticklabels = unicode(list(words_sorted_top)).split()
    # Remove the single quotes, commas and enclosing square brackets
    xtlabs = [xstr.replace("'", "").replace(",", "").replace("]", "").replace("[", "") for xstr in xticklabels]
    indices = np.arange(len(words_sorted_top))
    width = 1
    fig = plt.figure()
    fig.suptitle('Word frequency histogram, top {0}'.format(top_n), fontsize=16)
    plt.xlabel('word', fontsize=12)
    plt.ylabel('count', fontsize=12)
    plt.bar(indices, values_sorted_top, width)
    plt.xticks(indices + width * 0.5, xtlabs, rotation='vertical', fontsize=8)
    # create a histogram in the directory
    plt.savefig(createNewfile(file))
    plt.show()

if __name__ == "__main__":
    main()