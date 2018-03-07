import json


def dumper(dictionary, filename):
    """
    JSON Dumps all the info into a file.
    :param dictionary: A dictionary {headline:link}, which will be dumped away.
    :param filename: The filename to access. This is just the site name.
    :return: Nothing. It just dumps it away.
    """
    with open('{}.txt'.format(filename), 'w') as out:
        json.dump(dictionary, out, indent=4)


def loader(filename):
    """
    Loads all the info that was previously dumped into a dictionary {headline:link}
    :param filename: The file name. Also known as the site name.
    :return: A dictionary
    """
    try:
        with open('{}.txt'.format(filename), 'r') as read:
            dictionary = json.load(read)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return {}
    return dictionary
