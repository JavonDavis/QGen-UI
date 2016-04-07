import yaml
from importlib import import_module
from QGen.qgen.built_in_functions import built_in_functions as functions
from QGen.qgen.generators import moodle_xml_builder as mxb
import markdown2


# TODO - convert to moodle xml
class Question(object):
    body_container = "<![CDATA[%s]]"

    """Class to model a generate questions"""

    def __init__(self, data, question_count=0):
        self.question_params = {}
        self.title = data['title']
        self.type = data['type']
        # TODO - do formatting after all data has been filled
        # self.body = Question.body_container % markdown2.markdown(data['body'])
        self.body = data['body']
        self.question_count = question_count
        self.answers = data['answer']
        self.add_imports(data)
        self.distractors = data['distractor']
        self.correct_feedback = data['correct_feedback']
        self.incorrect_feedback = data['incorrect_feedback']
        self.correct_answer_weight = data['correct_answer_weight']
        self.incorrect_answer_weight = data['incorrect_answer_weight']
        self.build_question_params(data['params'])
        self.params_cache = self.question_params

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
                    print(e)

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


def test():
    print("Hello World")


def build_moodle_xml(yml_file=None, question=None, dict_value=None, number_of_questions=10):
    from QGen.qgen.generators.generate_moodle_xml import gen_moodle_xml
    if yml_file:
        with open(yml_file, 'r') as stream:
            try:
                dict_value = yaml.load(stream)
                if question is not None:
                    question = Question(dict_value[question], number_of_questions)
                    print("--------Question Data--------")
                    xml_builder = mxb.QuizBuilder(question.title)
                    xml_builder.setup()
                    for i in range(0, number_of_questions):
                        gen_moodle_xml(question)
                    print("-----------------------------")
                else:
                    print(dict_value)
            except yaml.YAMLError as exc:
                print(exc)
    elif dict_value:
        if question is not None:
            question = Question(dict_value[question], number_of_questions)
            xml_builder = mxb.QuizBuilder(question.title)
            xml_builder.setup()
            for i in range(0, number_of_questions):
                gen_moodle_xml(question)
            return str(xml_builder)
        else:
            return "empty"
    else:
        return "empty"

if __name__ == "__main__":
    print("ho")