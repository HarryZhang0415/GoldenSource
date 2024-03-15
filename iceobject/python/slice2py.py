import os
import shutil
import re
import subprocess
import argparse

def filter_file_by_pattern(files):
    r = []
    pattern = re.compile(r'.*\.ice$', re.IGNORECASE)
    for filename in files:
        if pattern.match(filename):
            r.append(filename)

    return r


def slice_directory(source_dir, destination_dir):
    """
    Slices a directory into smaller directories of a given size.

    Args:
    - source_dir (str): Path to the source directory.
    - destination_dir (str): Path to the destination directory where sliced directories will be created.
    - slice_size (int): Maximum number of files in each sliced directory.
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    files = filter_file_by_pattern(os.listdir(source_dir))

    file_str = ""

    for filename in files:
        file_str += os.path.join(source_dir, filename) + " " 

    command = "mkdir -p {destination_dir}".format(destination_dir=destination_dir)
    subprocess.run(command, shell=True)

    command = "slice2py -I{source_dir} {file_str} --underscore --output-dir {destination_dir} ".format(source_dir=source_dir ,file_str=file_str, destination_dir=destination_dir)
    subprocess.run(command, shell=True)
    # print(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process input and output files.")
    parser.add_argument("--source_dir", help="Path to the input file.")
    parser.add_argument("--destination_dir", help="Path to the output file.")
    args = parser.parse_args()

    slice_directory(args.source_dir, args.destination_dir)
