# python import
import io

# Local Import
from .models import Student
from .serializer import StudentSerializer

# import from DRF
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# import from django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator # for class csrf_exempt in class based view
from django.views import View

# all CRUD code using classbased view
@method_decorator(csrf_exempt, name='dispatch')
class StudentApi(View):
    def get(self,request,*args,**kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    def post(self,request,*args,**kwargs):
        json_data = request.body # byte streamed json data
        print(json_data)
        stream = io.BytesIO(json_data)
        print(dir(stream))
        pythondata = JSONParser().parse(stream)
        print(pythondata)
        serializer = StudentSerializer(data=pythondata)
        print(dir(serializer))
        if serializer.is_valid():
            serializer.save() # # will call update method in serializer.py
            res = {'msg':'data inserted'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    def put(self,request,*args,**kwargs):
        json_data = request.body # byte streamed json data
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        print(stu)
        # if complete data update need to be done, below code
        # serializer = StudentSerializer(stu, data=pythondata)

        serializer = StudentSerializer(stu, data=pythondata, partial=True)
        # if we not updating all he field, then need to mention partial=True otherwise "this field is required" error will be generated

        if serializer.is_valid():
            serializer.save() # will call update method in serializer.py
            res = {'msg':'data updated'}
            json_data = JSONRenderer().render(res)
            print(stu)
            return HttpResponse(json_data, content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        print(json_data)
        return HttpResponse(json_data, content_type='application/json')

    def delete(self,request,*args,**kwargs):
        json_data = request.body # byte streamed json data
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        stu.delete()
        res = {'msg':'data deleted'}
        #json_data = JSONRenderer().render(res)
        #return HttpResponse(json_data, content_type='application/json')
        return JsonResponse(res)


# post/put/delete request Operations using function based view
@csrf_exempt
def student_create(request):
    if request.method == 'POST':
        json_data = request.body # byte streamed json data
        print(json_data)
        stream = io.BytesIO(json_data)
        print(stream)
        pythondata = JSONParser().parse(stream)
        print(pythondata)
        serializer = StudentSerializer(data=pythondata)
        print(dir(serializer))
        if serializer.is_valid():
            serializer.save() # # will call update method in serializer.py
            res = {'msg':'data inserted'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'PUT':
        json_data = request.body # byte streamed json data
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        print(stu)
        # if complete data update need to be done, below code
        # serializer = StudentSerializer(stu, data=pythondata)

        serializer = StudentSerializer(stu, data=pythondata, partial=True)
        # if we not updating all he field, then need to mention partial=True otherwise "this field is required" error will be generated

        if serializer.is_valid():
            serializer.save() # will call update method in serializer.py
            res = {'msg':'data updated'}
            json_data = JSONRenderer().render(res)
            print(stu)
            return HttpResponse(json_data, content_type='application/json')
        json_data=JSONRenderer().render(serializer.errors)
        print(json_data)
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'DELETE':
        json_data = request.body # byte streamed json data
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        stu.delete()
        res = {'msg':'data deleted'}
        #json_data = JSONRenderer().render(res)
        #return HttpResponse(json_data, content_type='application/json')
        return JsonResponse(res)


# Get request using function based view
def student_api(request):
    if request.method=='GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id', None)
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')


# PRACTICE FUNCTIONS

# Model Object - Single Student Data
def student_detail(request,pk):
    stu = Student.objects.get(id=pk) # complex data
    #print(stu)
    serializer = StudentSerializer(stu) # converted into python_data
    print(serializer.data)
    json_data = JSONRenderer().render(serializer.data) # converted into json_data, byte stream
    print(json_data)
    return HttpResponse(json_data, content_type = 'application/json') # sending json data to client
    # return JsonResponse(serializer.data) # safe=True by default

# QuerySet - All student data
@csrf_exempt
def student_list(request):
    stu = Student.objects.all() # complex data
    #print(stu)
    serializer = StudentSerializer(stu, many=True) # getting multiple results
    #print(serializer.data)
    #json_data = JSONRenderer().render(serializer.data) # converted into json_data, byte stream
    # print(json_data)
    #return HttpResponse(json_data, content_type = 'application/json') # sending json data to client
    return JsonResponse(serializer.data,safe=False) # safe=True by default