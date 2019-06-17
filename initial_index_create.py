import glob
import pickle

# relative paths of directories
articles_dir_path = '../BBC-News-Summary/News-Articles\\'
summaries_dir_path = '../BBC-News-Summary/Summaries\\'

# lists of relative paths for articles and summaries
articles_paths = glob.glob(articles_dir_path + "**\\*.txt", recursive=True)
summaries_paths = glob.glob(summaries_dir_path + "**//*.txt", recursive=True)

# index structure
# {
#   'sports/001.txt' : ['text of file', 'summary of file'],
#   'tech/031.txt' : ['text of file', 'summary of file'],
#   ...
# }
index = {}


for path in articles_paths:
    # BBC-News-Summary/News-Articles/sports/001.txt -> sports/001.txt
    key = path.replace(articles_dir_path, '')
    with open(path, 'r', errors='ignore') as f:
        index[key] = [f.read()]

for path in summaries_paths:
    key = path.replace(summaries_dir_path, '')
    with open(path, 'r', errors='ignore') as f:
        index[key].append(f.read())

with open('index.pickle', 'wb') as index_file:
    pickle.dump(index, index_file)