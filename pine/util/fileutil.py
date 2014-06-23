from datetime import datetime


def generate_file_name(original_file_name):
    """
    :param original_file_name:
    :return: unique file name
    """
    return datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '_' + original_file_name

# return original_file_name+uuid.uuid4()