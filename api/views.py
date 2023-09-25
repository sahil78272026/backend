# python import
import io

#pdf creation
from django.http import FileResponse
import io # input output
from reportlab.pdfgen import canvas # will put all the data in canvas and save it as pdf
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter



# Local Import
from .models import Student, Cloth
from .serializer import StudentSerializer, ClothSerializer

# import from DRF
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView # for mixins
from rest_framework.mixins import ListModelMixin
from rest_framework.serializers import *

# import from django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator # for class csrf_exempt in class based view
from django.views import View


# PDF File Generation from Models data

def venue_pdf(request):
    # Create a bytestream buffer
    buf = io.BytesIO()

    # create a Canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0) # letter size regular paper, A4 sheet

    # create a textobject, that will tell us what to put on canvas
    textob = c.beginText()
    textob.setTextOrigin(inch, inch) # Measurement
    textob.setFont('Helvetica', 14)  # text font and style

    # add some lines of text
    lines = [
             'this is line',
             'this is line 2',
             'this is line 3'
             ]

    # loop throigh all lines
    for line in lines:
        textob.textLine(line)

    # finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # returning file as a response
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

def home(request):
    return render(request, 'index.html')


#**** cloth model****
class ClassBasedAPIViewClothAPI(APIView):
    def get(self, request, pk=None, format=None):
        # id = request.data.get('id')
        id=pk # for browseable APIs
        if id is not None:
            stu = Cloth.objects.get(id=id)
            serializer = ClothSerializer(stu)
            print("Returning single Result")
            return Response(serializer.data)
        stu = Cloth.objects.all()
        print("Returning Multiple Result")
        serializer = ClothSerializer(stu, many=True) # if more than one object, many=True need to mention
        return Response(serializer.data)



    def post(self, request, format=None):
        serializer = ClothSerializer(data=request.data) # .data attribute we get in api_view only, and we get parsed data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#*****CRUD with Mixins********
class StudentList(GenericAPIView, ListModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


#*****CRUD with Clasee BASED API VIEW********
class ClassBasedAPIViewStudentAPI(APIView):
    def get(self, request, pk=None, format=None):
        # id = request.data.get('id')
        id=pk # for browseable APIs
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            print("Returning single Result")
            return Response(serializer.data)
        stu = Student.objects.all()
        print("Returning Multiple Result")
        serializer = StudentSerializer(stu, many=True) # if more than one object, many=True need to mention
        return Response(serializer.data)



    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data) # .data attribute we get in api_view only, and we get parsed data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        #id = request.data.get('id')
        id=pk # for browseable APIs
        stu =Student.objects.get(pk=id)
        serializer = StudentSerializer(stu, data=request.data) # if not updating all the data, partial = True required with PUT method
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'data updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk=None, format=None):
        #id = request.data.get('id')
        id=pk # for browseable APIs
        stu =Student.objects.get(pk=id)
        serializer = StudentSerializer(stu, data=request.data) # if not updating all the data, partial = True required
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'data updated'})
        return Response(serializer.errors)


    def delete(self, request, pk=None, format=None):
        # id = request.data.get('id')
        id = pk
        #stu = Student.objects.get(pk=request.data.get('id')).delete()
        stu = Student.objects.get(pk=id).delete()
        # stu.delete()
        return Response({'msg':'data deleted'})

#*****Ends CRUD with Clasee BASED API VIEW********


#*****CRUD with FUNCTION BASED API VIEW********
# code reduced alot using function based api_view
@api_view(['GET','POST','PUT', 'PATCH', 'DELETE'])  # if do not mention any method, default method is GET
def student_api_with_view(request, pk=None):
    if request.method == 'GET':
        # id = request.data.get('id')
        id=pk # for browseable APIs
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            print("Returning single Result")
            return Response(serializer.data)
        stu = Student.objects.all()
        print("Returning Multiple Result")
        serializer = StudentSerializer(stu, many=True) # if more than one object, many=True need to mention
        return Response(serializer.data)


    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data) # .data attribute we get in api_view only, and we get parsed data
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data Created'})
        return Response(serializer.errors)

    if request.method == 'PUT':
        #id = request.data.get('id')
        id=pk # for browseable APIs
        stu =Student.objects.get(pk=id)
        serializer = StudentSerializer(stu, data=request.data) # if not updating all the data, partial = True required with PUT method
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'data updated'})
        return Response(serializer.errors)


    if request.method == 'PATCH':
        #id = request.data.get('id')
        id=pk # for browseable APIs
        stu =Student.objects.get(pk=id)
        serializer = StudentSerializer(stu, data=request.data) # if not updating all the data, partial = True required
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'data updated'})
        return Response(serializer.errors)


    if request.method == 'DELETE':
        # id = request.data.get('id')
        id = pk
        #stu = Student.objects.get(pk=request.data.get('id')).delete()
        stu = Student.objects.get(pk=id).delete()
        # stu.delete()
        return Response({'msg':'data deleted'})


#***** ENDS FUNCTION BASED API VIEW********




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
        print(request.data)
        json_data = request.body # byte streamed json data
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        stu = Student.objects.get(id=id)
        print(stu)
        # if complete data update need to be done, below code
        # serializer = StudentSerializer(stu, data=pythondata)

        serializer = StudentSerializer(stu, data=pythondata, partial=True)
        # if we not updating all the field, then need to mention partial=True otherwise "this field is required" error will be generated

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

# CRUD USING CLASS BASED VIEW ENDS**********************


# CRUD USING FUNCTION BASED VIEW STARTS
@csrf_exempt
def student_create(request):
    if request.method=='GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        #print(type(stream))
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

# CRUD USING FUNCTION BASED VIEW ENDS******************************



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



