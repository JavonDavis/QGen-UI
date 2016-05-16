import yaml
from importlib import import_module
from built_in_functions import built_in_functions as functions
from qgen_exceptions import InvalidConfigException
import generators.moodle_xml_builder as mxb


class Question(object):
    COMPULSORY_CONFIGS = ['type', 'title', 'answer', 'body']  # Tags that need to be in the template

    """Class to model a generate questions"""

    def __init__(self, configuration, question_count=0):
        self.question_params = {}
        self.body, self.type, self.title, self.answers, self.distractors, self.correct_feedback, \
            self.incorrect_feedback, self.correct_answer_weight, \
            self.incorrect_answer_weight = self.add_config(configuration)
        self.question_count = question_count
        self.add_imports(configuration)
        if 'params' in configuration:
            self.build_question_params(configuration['params'])
        self.params_cache = self.question_params

    def add_config(self, config):
        body, q_type, title, answer = self.add_compulsory_config(config) if self.check_config(config) else None
        tags = ['correct_feedback', 'incorrect_feedback', 'correct_answer_weight', 'incorrect_answer_weight']
        q_distractor = config['distractor'] if 'distractor' in config else {}
        q_correct_feedback, q_incorrect_feedback, q_correct_answer_weight, q_incorrect_answer_weight = \
            map(lambda tag: config[tag] if tag in config else "", tags)
        return body, q_type, title, answer, q_distractor, q_correct_feedback, q_incorrect_feedback, \
            q_correct_answer_weight, q_incorrect_answer_weight

    @staticmethod
    def check_config(config):
        for name in Question.COMPULSORY_CONFIGS:
            if name not in config:
                raise InvalidConfigException(name + " is missing from the configuration.")
        return True

    @staticmethod
    def add_compulsory_config(config):
        return config['body'], config['type'], config['title'], config['answer']

    @staticmethod
    def add_imports(data):
        """Imports any external functions specified"""
        if 'imports' in data:
            imports = data['imports']
            for source in imports:
                try:
                    module = import_module(source)
                    for name, value in module.__dict__.iteritems():  # iterate through the module's attributes
                        if callable(value):  # check if callable for functions
                            functions[name] = value
                except AttributeError as e:
                    print e

    def build_question_params(self, params):
        """Binds the parameters to there actual values"""
        list_params = None
        for parameter_name, function_name in params.iteritems():
            for function_param, arguments in function_name.iteritems():
                function_arguments = {}
                if arguments is None:
                    function_arguments = {}
                elif type(arguments) != dict:
                    function_arguments['value'] = arguments
                else:
                    function_arguments = arguments
                function_arguments['count'] = self.question_count
                list_params = functions[function_param](function_arguments)
            self.question_params[parameter_name] = list_params


def build_moodle_xml(yml_file=None, dict_value=None, number_of_questions=10):
    from generators.generate_moodle_xml import gen_moodle_xml
    if yml_file:
        with open(yml_file, 'r') as stream:
            try:
                dict_value = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    threshold = 50
    title = dict_value.keys()[0]

    question = Question(dict_value[title], number_of_questions)
    print "Question {0}".format(title)
    xml_builder = mxb.QuizBuilder(title)
    count = 0
    effort = 0
    while count < number_of_questions and effort < threshold:
        result = gen_moodle_xml(question, xml_builder)
        if result == 0:
            effort += 1
        count += result
    xml_builder.build_quiz_end_tag()
    if effort == threshold:
        print "Could not generate {0} questions at best {1} question(s) were generated. " \
              "Threshold is currently set to {2}, increasing this value might increase the number of " \
              "questions generated.".format(number_of_questions, count, threshold)
    print "-----------------------------"
    return str(xml_builder)
