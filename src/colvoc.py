#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Program to add vocabulary from text files to a CSV dictionary, so
# you can look up incoming vocabulary for your collection.  Currently
# has assumptions about using Albanian (the main language I'm
# currently learning) as I can't get that to work as a locale in
# Python yet.

import argparse
import csv
import re
import locale

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output")
    parser.add_argument("-l", "--language")
    parser.add_argument("-r", "--reference", default="ENG")
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("csvfile")
    parser.add_argument('incoming', nargs='+')
    args = parser.parse_args()
    output = args.output
    if output is None:
        output = args.csvfile
    language = args.language

    # locale.setlocale(locale.LC_ALL, "sq_AL")

    reference_language = args.reference
    dictionary = {}
    reverse_dictionary = {}
    stop_set = set()
    # I can't get the Albanian locale to work, so for now I'm hardwiring what I count as letters
    letters = "A-Za-zÇËçë"
    word_pattern = "[" + letters + "]+"
    split_pattern = "[^" + letters + "]+"
    word_regexp = re.compile(word_pattern)
    split_regexp = re.compile(split_pattern)
    with open("/usr/share/dict/words", 'r') as usdw:
        for w in usdw.read().split():
            stop_set.add(w.lower())
    with open(args.csvfile, 'r') as existing_file:
        for row in csv.DictReader(existing_file):
            if language is None:
                for key in row.keys():
                    if key not in ['Type', reference_language, 'form', 'other', 'comment']:
                        language = key
                        break
            new_key = row.get('form', row.get(language))
            new_ref_key = row.get('form', row.get(reference_language))
            dictionary[new_key] = row
            reverse_dictionary[new_ref_key] = row
    if args.verbose:
        for k, v in dictionary.iteritems():
            print k, v
    for filename in args.incoming:
        with open(filename, 'r') as infile:
            for word in split_regexp.split(infile.read()):
                word = word.lower()
                if word_regexp.match(word):
                    if word not in stop_set and word not in reverse_dictionary:
                        if word in dictionary:
                            pass # print "known word:", word
                        else:
                            dictionary[word] = {'Type': '?', language: word}
    with open(args.output, 'w') as outfile:
        writer = csv.DictWriter(outfile, ["Type", language, reference_language, "other", "comment"])
        writer.writeheader()
        for target_word in sorted(dictionary.keys()):
            row = dictionary[target_word]
            if target_word in dictionary:
                writer.writerow(row)
                    
if __name__ == "__main__":
    main()
