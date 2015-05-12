import glob

def get_lengths(dir_path):
    """return a giant vector of char length of ea. tweet"""
    files = glob.glob(dir_path + "/*")
    lengths = []
    for school in files:
        with open(school) as f:
            for line in f:
                lengths.append(len(line.strip()))
    return lengths

