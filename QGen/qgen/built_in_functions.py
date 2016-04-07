import random

"""All built in functions source code should be written in this file"""


# TODO - account for list of strings or other data types
def rand(values):
    return random.sample(range(int(values['start']), int(values['end'])), int(values['count']))


def make_set(values):
    return values['value'].split(",")


built_in_functions = {'random': rand, 'set': make_set}
