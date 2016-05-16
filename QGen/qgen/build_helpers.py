from qgen import functions
from random import choice
from qgen_exceptions import EvaluationException

"""Helper functions that are essential to the construction of questions"""


# to help decide if a question is valid
question_list = []


# TODO - check if any case where the parameters might be needed to evaluate the eval blocks
def evaluate_blocks(text, params):
    """Evaluates the code blocks delimited by a $ in a question's answer or distractor"""
    # TODO - pick a random value from a parameter
    def params_get(*args):
        return choice(params[choice(args)])

    # TODO - pick a random value from a random parameter except these specified
    def params_except(*args):
        keys = params.keys()
        for arg in args:
            keys.remove(arg)
        return choice(params[choice(keys)])
    text = text.replace("\$", "esCA")
    if text.count("$") % 2 != 0:
        raise EvaluationException("Incorrect number of $ found in a block")
    while "$" in text:
        start_index = text.index('$')
        end_index = text.index('$', start_index + 1) + 1

        # get code to be evaluated
        substr = text[start_index:end_index]

        # remove leading and trailing $
        eval_block = substr[1:-1]

        text = text.replace(substr, str(eval(eval_block)))
    text = text.replace("esCA", "$")
    return text


def evaluate_functions(text, params):
    """Evaluates the functions delimited by a @ in a question's answer or distractor"""
    text = text.replace("\@", "esAM")
    while "@" in text:
        start_index = text.index('@')
        end_index = text.index('@', start_index + 1) + 1
        substr = text[start_index:end_index]

        eval_block = substr[1:-1]
        # find function
        function_name = eval_block

        text = text.replace(substr, str(functions[function_name](params)))
    text = text.replace("esCA", "@")
    return text


def validate_question(body, answers, distractors):
    answers, distractors = validate_answer_distractor(answers, distractors)
    if answers:
        if not valid_question(body, answers, distractors):
            return None
        return body, answers, distractors
    else:
        return None


def valid_question(body, answers, distractors):
    description = (body, set(answers), set(distractors))

    if description in question_list:
        is_valid = False
    else:
        is_valid = True
        question_list.append(description)
    return is_valid


def validate_answer_distractor(answers, distractors):
    answer_list = []
    distractor_list = []
    for answer in answers:
        if answer not in answer_list:
            answer_list.append(answer)
    for distractor in distractors:
        if distractor not in distractor_list:
            distractor_list.append(distractor)
    return answer_list, distractor_list
