import glob
import os


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def check_file(file, log=False):
    """
    Checks if given file exists.
    :param file: File to check for existence.
    :param log: If True, logs which files have been skipped. By default False
    :return: True if file found, False if file not found.
    """
    if os.path.isfile(file):
        if log:
            print(f"Found {file}. Skipping")
        return True
    else:
        return False


def get_file_names(path):
    """
     Goes to location and finds all files in the folder
     :param path: Path to check for file
     :return: list of files
     """

    files_to_parse = list()
    for text_path in glob.glob(f"{path}/*"):
        files_to_parse.append(text_path)

    return files_to_parse


def save(path):
    """
     Goes to location and finds all files in the folder
     :param path: Path to check for file
     :return: list of files
     """

    files_to_parse = list()
    for text_path in glob.glob(f"{path}/*"):
        files_to_parse.append(text_path)

    return files_to_parse
