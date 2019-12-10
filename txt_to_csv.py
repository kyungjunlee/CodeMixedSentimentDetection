"""
Create a csv file from a text file
  using "Tab" as a delimiter
  CSV Format:
    (Meta ID)\t(Sentence)\t(Sentiment Label)
    ...
    
"""
import os
import csv
import sys
import argparse
# emoji
from emoji import UNICODE_EMOJI
# regex
import re

# global variables
parser = argparse.ArgumentParser()
parser.add_argument("--txt", help="Input txt file path")
parser.add_argument("--csv", help="Output csv file path")
parser.add_argument(
    "--filter",
    default=False,
    action="store_true",
    help="Flag to filter non-English/Emoji characters")
parser.add_argument(
    "--debug",
    default=False,
    action="store_true",
    help="Flag to debugging")

args = parser.parse_args()


def is_emoji(s):
  return s in UNICODE_EMOJI


def convert_txt_to_csv(txt_path, csv_path, filtering=False, debug=False):
  """
  Format of the txt file
    first row:         meta   (id)        (sentiment label)
    second or later:  (word)  (tagging)
                      ...
    (space)
    first row:         meta   (id)        (sentiment label)
    second or later:  (word)  (tagging)
    ...

  """
  if not os.path.exists(txt_path):
    print("ERROR: {} not existed".format(txt_path))
    return

  # prepare to create a csv file
  output_dir = os.path.dirname(csv_path)
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  # open the output file for writing
  with open(csv_path, 'w') as csvfp:
    # use "tab" as a delimiter in the csv file
    writer = csv.writer(csvfp, delimiter='\t')
    # read the input txt file
    with open(txt_path, 'r') as fp:
      for line in fp:
        # if debug: print(line)
        columns = line.split()
        # if debug: print(len(columns))
        # when we get a new twitter data
        if len(columns) == 3 and columns[0] == "meta":
          meta_id = columns[1]
          label = columns[2]
          sentence = ""
        elif len(columns) == 2:
          # adding a word to a sentence
          # this case: columns[0] is word and columns[1] is its tagging info
          word = columns[0]
          if word[0].isalpha():
            word = " {}".format(word)
          sentence += word
        elif len(columns) == 0:
          # time to write a row in csv
          # remove the leading and trailing whitespace in the sentence
          sentence = sentence.strip()
          if debug: print("DEBUG: [{}] {} ({})".format(meta_id, sentence, label))
          if filtering:
            new = ""
            for ch in sentence:
              # https://www.utf8-chartable.de/unicode-utf8-table.pl?number=128
              # https://unicode.org/emoji/charts/full-emoji-list.html
              if ch.isascii() or is_emoji(ch):
                new += ch
            # remove duplicate spaces
            sentence = re.sub(' +', ' ', new)
            # 
          writer.writerow([meta_id, sentence, label])
        else:
          # Warning: we should not reach here
          if debug: print("WARNING: should not reach here, but why?")

  return 


def main():
  if not args.txt or not args.csv:
    parser.print_help()
    sys.exit(2)

  # convert txt to csv
  convert_txt_to_csv(args.txt, args.csv, args.filter, args.debug)
  return 


if __name__ == "__main__":
  main()