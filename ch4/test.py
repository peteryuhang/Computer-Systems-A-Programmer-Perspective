
def read_data_from_file(file_path):
  """
  Read a source file and split each line into a string
  Convert to lowercase and filter out empty string/row

  @param file_path: file location on local computer
  @return: list of strings
  """
  f = open(file_path, 'r')
  return list(filter(None, f.read().lower().split('\n')))


def sort_data_based_on_prefix_number(data):
  """
  Separate the prefix order number and corresponding word
  Sort the list based on the order number

  @param data: list of string, each item has format 'number word'
  @return list of string in ascend order based on prefix number
  """
  words = []
  for w in data:
    nw = w.split(' ')
    if len(nw) == 2:
      words.append(nw)
  return sorted(words, key=lambda x: int(x[0]))


def process(data):
  """
  Process the data which already been separated, also sorted on order number
  Generate the decode string

  @param data: sorted data with type list of lists
  @return decode string
  """
  
  idx, sep = 0, 2
  res = []
  while idx < len(data):
    res.append(data[idx][1])
    idx += sep
    sep += 1

  return ' '.join(res)


def decode():
  pairs = read_data_from_file('/Users/pyh/Downloads/coding_qual_input.txt')
  sorted_separated_pairs = sort_data_based_on_prefix_number(pairs)
  res = process(sorted_separated_pairs)
  print(res)

decode()
