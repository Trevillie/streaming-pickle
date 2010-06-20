'''Streaming pickle implementation for efficiently serializing and
de-serializing an iterable (e.g., list)'''

# Created on 2010-06-19 by Philip Guo

# Limitations:
#
# - Right now it only works with ASCII-based pickles (protocol=0), since
#   stream_load reads data in one line at a time


try:
  from cPickle import dumps, loads
except ImportError:
  from pickle import dumps, loads


def stream_dump_elt(elt_to_pickle, file_obj):
  '''dumps one element to file_obj, a file opened in write mode'''
  pickled_elt_str = dumps(elt_to_pickle)
  file_obj.write(pickled_elt_str)
  # record separator is a blank line
  # (since pickled_elt_str might contain its own newlines)
  file_obj.write('\n\n')


def stream_dump(iterable_to_pickle, file_obj):
  '''dump contents of an iterable iterable_to_pickle to file_obj, a file
  opened in write mode'''
  for elt in iterable_to_pickle:
    stream_dump_elt(elt, file_obj)


def stream_load(file_obj):
  '''load contents from file_obj, returning a generator that yields one
  element at a time'''
  cur_elt = []
  for line in file_obj:
    cur_elt.append(line)

    if line == '\n':
      pickled_elt_str = ''.join(cur_elt)
      elt = loads(pickled_elt_str)
      cur_elt = []
      yield elt

