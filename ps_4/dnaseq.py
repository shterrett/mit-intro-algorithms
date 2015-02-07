#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *
import itertools as it

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
      self.data = {}
      for k, v in pairs:
        values = self.data.get(k, [])
        values.append(v)
        self.data[k] = values

    # Associates the value v with the key k.
    def put(self, k, v):
      values = self.data.get(k, [])
      values.append(v)
      self.data[k] = values

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
      return self.data.get(k, [])

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
  subseq = ["x"] + list(it.islice(seq, 0, k-1))
  hsh = RollingHash(subseq)
  start = -1
  for c in seq:
    remove = subseq[0]
    subseq = subseq[1:] + [c]
    start += 1
    hsh.slide(remove, subseq[-1])
    yield [hsh.current_hash(),
           { "seq": ''.join(subseq), "start": start }
          ]

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
  count = -1
  for subseq in kfasta.subsequences(seq, k):
    count += 1
    if count % m == 0:
      hsh = RollingHash(subseq)
      yield [hsh.current_hash(),
             { "seq": subseq, "start": count }
            ]

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
  a_hashes = intervalSubsequenceHashes(a, k, m)
  table = Multidict(a_hashes)
  for subseq in subsequenceHashes(b, k):
    if len(table.get(subseq[0])) > 0:
      for data in table.get(subseq[0]):
        if (subseq[1]["seq"] == data["seq"]):
          yield (data["start"], subseq[1]["start"])

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
