"""A test file to make sure my folder structure is set up correctly"""

from utils import read_input

def map_fn(line):
  return line.split(',')

print(read_input(0, map_fn))
