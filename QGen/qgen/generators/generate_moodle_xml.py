import QGen.qgen.generators.moodle_xml_builder as mxb
from QGen.qgen.build_helpers import *

"""Functions to generate questions in different formats"""


def gen_moodle_xml(question):
    """Function to generate the questions in Moodle XML format"""
    params = {}
    for key, value in question.question_params.iteritems():
        try:
            params[key] = value.pop()
        except IndexError as e:
            print(e)
    print(question.body.format(**params))
    print("********Options*********")

    body_for_xml = question.body.format(**params)

    xml_builder = mxb.QuizBuilder(question.title)
    xml_builder.build_question_for_xml(question.title, body_for_xml, question.type)

    # Evaluate answers
    for answer in question.answers:
        original_params = question.params_cache
        answer = evaluate_braces(answer, params, original_params)
        answer = evaluate_functions(answer, params)
        answer = evaluate_blocks(answer, params)
        xml_builder.build_answer_for_xml(answer, None, question.correct_answer_weight)
        print(answer)

    # Evaluate distractors
    for distractor in question.distractors:
        original_params = question.params_cache
        distractor = evaluate_braces(distractor, params, original_params)
        distractor = evaluate_functions(distractor, params)
        distractor = evaluate_blocks(distractor, params)
        xml_builder.build_distractor_for_xml(distractor, None, question.incorrect_answer_weight)
        print(distractor)
    xml_builder.build_question_end_tag()
    xml_builder.build_quiz_end_tag()
