import moodle_xml_builder as mxb
import markdown2
from random import choice
from qgen.qgen_exceptions import EvaluationException
from qgen.build_helpers import evaluate_functions, evaluate_blocks, validate_question

"""Functions to generate questions in different formats"""

container = "<![CDATA[%s]]>"


def gen_question(question):
    """Function to generate a question in plain text format"""

    params = {}
    for key, value in question.question_params.iteritems():
        try:

            params[key] = choice(value)
        except IndexError as e:
            raise EvaluationException("{0} - {1}".format(str(question.question_params), e.message))

    body_for_xml = question.body.format(**params)
    body_cache = body_for_xml
    try:
        body_for_xml = evaluate_functions(body_for_xml, params)
        body_for_xml = evaluate_blocks(body_for_xml, question.params_cache)
    except Exception as e:
        raise EvaluationException("{0} - {1}".format(body_cache, e.message))
    body_for_xml = container % markdown2.markdown(body_for_xml, extras=["fenced-code-blocks",
                                                                        "code-friendly"])  # body_for_xml will now be
    # of type unicode and not str

    body_for_xml = body_for_xml.replace("\n", "<br />")

    answers = []
    # Evaluate answers
    for answer in question.answers:
        answer = answer.format(**params)
        answer_cache = answer
        try:
            answer = evaluate_functions(answer, params)
            answer = evaluate_blocks(answer, question.params_cache)
        except Exception as e:
            raise EvaluationException("{0} - {1}".format(answer_cache, e.message))
        answer = container % markdown2.markdown(answer)
        answers.append(answer)

    distractors = []
    # Evaluate distractors
    for distractor in question.distractors:
        distractor = distractor.format(**params)
        distractor_cache = distractor
        try:
            distractor = evaluate_functions(distractor, params)
            distractor = evaluate_blocks(distractor, question.params_cache)
        except Exception as e:
            raise EvaluationException("{0} - {1}".format(distractor_cache, e.message))
        distractor = container % markdown2.markdown(distractor)
        distractors.append(distractor)

    return validate_question(body_for_xml, answers, distractors)


def gen_moodle_xml(question, xml_builder):
    """Function to generate the questions in Moodle XML format"""

    is_valid = gen_question(question)

    if is_valid:
        body_for_xml, answers, distractors = is_valid

        # Translate to Moodle XMl

        xml_builder.build_question_for_xml(question.title, body_for_xml, question.type)

        for answer in answers:
            xml_builder.build_answer_for_xml(answer, question.correct_feedback, question.correct_answer_weight)

        for distractor in distractors:
            xml_builder.build_distractor_for_xml(distractor, question.incorrect_feedback, question.incorrect_answer_weight)

        xml_builder.build_question_end_tag()
        return 1
    return 0
