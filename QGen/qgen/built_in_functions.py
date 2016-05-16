import random

"""All built in functions source code should be written in this file"""


def randint(values):
    start = int(values['start'])
    end = int(values['end'])
    return random.sample(range(start, end), end - start)


def make_set(values):
    return values['value'].split(",")


def getint(values):
    return random.randint(int(values['start']), int(values['end']))


built_in_functions = {'randint': randint, 'set': make_set, 'getint': getint}
