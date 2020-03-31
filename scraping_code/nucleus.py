import os


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
