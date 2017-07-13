import glob, os
data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ascii')
with open('list.txt', 'w') as ascii_file:
    ascii_files = sorted(glob.glob(os.path.join(data_dir, '**/*.txt'), recursive=True))
    for i in ascii_files:
        ascii_file.write('{0}. {1}\n'.format(ascii_files.index(i)+1, os.path.basename(i).replace('.txt', '', 1)))