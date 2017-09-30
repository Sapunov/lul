def get_token(path):

    with open(path) as opened_file:
        return opened_file.read().strip()
