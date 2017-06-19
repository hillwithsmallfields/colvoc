#!/usr/bin/env python

import argparse
import csv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output")
    parser.add_argument("-l", "--language")
    parser.add_argument("-v", "--verbose", action='store_true')
    parser.add_argument("csvfile")
    parser.add_argument('incoming', nargs='+')
    args = parser.parse_args()
    output = args.output
    if output is None:
        output = args.csvfile
    language = args.language
    dictionary = {}
    print "Will read vocab from", args.csvfile, "and write it back to", output
    print "Input files are", args.incoming
    with open(args.csvfile, 'r') as existing_file:
        for row in csv.DictReader(existing_file):
            print "got row", row
            if language is None:
                for key in row.keys():
                    if key not in ['Type', 'ENG', 'form']:
                        language = key
                        print "Deduced language is", language
                        break
            new_key = row.get('form', row.get(language))
            print "new key is", new_key
            dictionary[new_key] = row
    if True or args.verbose:
        for k, v in dictionary.iteritems():
            print k, v

if __name__ == "__main__":
    main()
