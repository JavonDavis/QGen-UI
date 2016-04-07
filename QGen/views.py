from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from QGen.qgen import qgen
import unicodedata
import os

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str

params = {}


def index(request):
    return render(request, 'index.html')


def demo(request):
    return render(request, 'demo.html')


def test(request):
    return render(request, 'test.html')


def thanks(request):
    return render(request, 'thanks.html')


@csrf_exempt
def add_param(request):
    data = request.POST['data']
    data_dict = {}
    values = data.split("&")
    for value in values:
        details = value.split("=")
        if len(details) > 1:
            data_dict[details[0]] = details[1]
    param_list = ['param_name_1', 'param_name_2', 'param_name_3']
    value_list = ['param_value_1', 'param_value_2', 'param_value_3']
    generator_dict = {}
    for index in range(3):
        param = param_list[index]
        if param in data_dict.keys() and data_dict[param]:
            generator_dict[normalise(data_dict[param])] = normalise(data_dict[value_list[index]])
    generator_holder_dict = {normalise(data_dict['function_name']): generator_dict}
    params[normalise(data_dict['name'])] = generator_holder_dict
    return HttpResponse("Successfully added")


def normalise(string):
    return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore')

def generate(request):
    if request.method == 'POST':
        data = request.POST
        qgen_dict = {}
        title = normalise(data['title'])
        file_title = title.replace(' ', '')
        qgen_dict['title'] = title
        if data['type'] == 'Multiple Choice':
            qgen_dict['type'] = 'multichoice'
        qgen_dict['correct_feedback'] = ''
        qgen_dict['incorrect_feedback'] = ''
        qgen_dict['correct_answer_weight'] = ''
        qgen_dict['incorrect_answer_weight'] = ''
        qgen_dict['body'] = normalise(data['body'])
        qgen_dict['params'] = params
        qgen_dict['answer'] = []
        qgen_dict['distractor'] = []

        answers_fields = ['answer1', 'answer2', 'answer3', 'answer4', 'answer5']
        checkboxes = ['isAnswer1Correct', 'isAnswer2Correct', 'isAnswer3Correct', 'isAnswer4Correct',
                      'isAnswer5Correct']

        for field_index in range(5):
            answer_field = answers_fields[field_index]
            checkbox = checkboxes[field_index]
            if data[answer_field] != '':
                if checkbox in data.keys():
                    qgen_dict['answer'].append(normalise(data[answer_field]))
                else:
                    qgen_dict['distractor'].append(normalise(data[answer_field]))
        final_dict = {file_title: qgen_dict}
        result = qgen.build_moodle_xml(dict_value=final_dict, question= file_title)
        response = HttpResponse(content_type='application/force-download')
        file_title = title.lower().replace(" ", "_")
        response['Content-Disposition'] = 'attachment; filename=%s' % (smart_str(file_title)+".xml")

        response['X-Sendfile'] = smart_str(os.getcwd()+'/generated_quizzes/%s.xml'%file_title)
        # It's usually a good idea to set the 'Content-Length' header too.
        # You can also set any other required headers: Cache-Control, etc.
        response.write(result)
        return response
       # return render(request, 'data.xml', {'result':result})
    return render(request, 'demo.html')
