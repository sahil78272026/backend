# core python import
import datetime
import io
from datetime import date
from email.policy import default
from io import BytesIO

# import from django
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.utils.decorators import method_decorator  # for class csrf_exempt in class based view
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.http import FileResponse, HttpResponse, JsonResponse

# import from DRF
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from xhtml2pdf import pisa

# third party
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import JSONParser

# Local Import
from .models import *
from .serializer import *


@api_view(['GET','POST'])
def dataInRange(request):
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    if start_date is None:
        start_date = date.today()

    if end_date is None:
        end_date = date.today()

    print('start_date',  start_date)
    print('end_date', end_date)
    data = Student.objects.filter(datetime_of_payment__range=[start_date,end_date])
    print(data.count())
    for i in data:
        print(i.datetime_of_payment)
    return Response('OK')


# Raw SQL Queries
def rawQuery(request):
    stu = Student.objects.raw("select * from student order by name desc")

    # query with variable
    name = 'Sahil'
    stu = Student.objects.raw("select * from student where name=%s", [name])
    for i in stu:
        print(i.name)
        print(i.city)
    return HttpResponse('ok')



#***** Cookie and SESSION START***********
# @api_view(['GET'])

#setting cookies
@csrf_exempt
def setcookie(request):

    # html = HttpResponse("<h1>Dataflair Django Tutorial</h1>")
    # html.set_cookie('dataflair', 'Hello this is your Cookies', max_age = None)
    # return html

    html = HttpResponse("Cookies")
    if request.COOKIES.get('visits'):
        html.set_cookie('cookie', 'Welcome Back')
        value = int(request.COOKIES.get('visits'))
        html.set_cookie('visits', value + 1)
    else:
        value = 1
        text = "Welcome for the first time"
        html.set_cookie('visits', value)
        html.set_cookie('cookie', text)
    return html

# Getting cookies
def showcookie(request):

    # show = request.COOKIES['dataflair']
    # html = "<center> New Page <br>{0}</center>".format(show)
    # return HttpResponse(html)

    if request.COOKIES.get('visits') is not None:
        value = request.COOKIES.get('visits')
        text = request.COOKIES.get('cookie')
        html = HttpResponse("<center><h1>{0}<br>You have requested this page {1} times</h1></center>".format(text, value))
        html.set_cookie('visits', int(value) + 1)
        return html
    else:
        return redirect('/setcookie')

# deleting a cookie
# The delete_cookie() takes in the name of the cookie to be deleted, and this method is associated with the response object.
def delete_co(request):
    if request.COOKIES.get('visits'):
       response = HttpResponse("Cookie deleted")
       response.delete_cookie("visits")
    else:
        response = HttpResponse("You need to create cookie before deleting")
    return response


# *******************Session Practice Starts

from faker import Faker  # to generate fake data for testing


@api_view(['GET'])
def addingDataUsingFaker(request):
    fake = Faker()
    for i in range(10):
        Student.objects.create(name=fake.name(),country=fake.country(), zipcode=fake.zipcode(), city=fake.city())

    return Response("OK")

def getStudentFromDB(name=None):
    if name is None:
        print("Data from DB")
        student_data = Student.objects.all()
    else:
        print("Data from DB")
        student_data = Student.objects.filter(name__contains=name)

    return student_data

@api_view(['GET'])
def getStudent(request):
    request.session.set_test_cookie()
    if request.session.test_cookie_worked():
            # request.session.delete_test_cookie()
            print("test cookie worked and also deleted")

    print(datetime.datetime.now())
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("request.session.keys() :", request.session.keys())
    print("request.session.values() :", request.session.values())
    print("request.session.get('num_visits', default=None) :", request.session.get('num_visits', default=None))
    print(request.session.test_cookie_worked())

    print(request.session.session_key)
    request.session.set_expiry(30)
    name = request.GET.get('name')
    if cache.get(name):
        print("Data from Cache")
        student_data = cache.get(name)
    else:
        if name:
            student_data = getStudentFromDB(name)
            cache.set(name, student_data)
        else:
            student_data = getStudentFromDB()
    student_serializer = StudentSerializerForCache(student_data, many=True)


    # request.session.flush()

    return Response(student_serializer.data)

# *******************Session Practice Ends

#***** Cookie and SESSIONS ENDS************


# *********CACHING START***************
# CACHING USING REDIS
# install redis for windows , 1
# pip install django-redis , 2
# set environment variable for caching in settings.py
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

from .serializer import RecipeSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def get_recipe(filter_recipe=None):
    if filter_recipe:
        print("DATA from DB")
        recipe = Recipe.objects.filter(name__contains=filter_recipe)
        
    else:
        print("DATA from DB")
        recipe = Recipe.objects.all()

    return recipe

@api_view(('GET',))
def show(request, id):
    if cache.get(id):
        print("DATA from CACHE")
        recipe = cache.get(id)
    else:
        print("DATA from DB")
        recipe = Recipe.objects.get(id=id)
        cache.set(id, recipe, timeout=3600)

    recipe = Recipe.objects.get(id=id)

    recipe_serializer = RecipeSerializer(recipe)
    return Response(recipe_serializer.data)

@api_view(('GET','POST'))
def home_recipe(request):
    if request.method=='GET':
        
        filter_recipe = request.GET.get('recipe')
        print(filter_recipe)
        if cache.get(filter_recipe):
            print("DATA from CACHE")
            recipe = cache.get(filter_recipe)

        else:
            if filter_recipe:
                recipe = get_recipe(filter_recipe)
                cache.set(filter_recipe, recipe, timeout=3600)
            else:
                recipe = get_recipe()
        
        recipe_serializer = RecipeSerializer(recipe, many=True)
        return Response(recipe_serializer.data)
    
    if request.method=='POST':
        name = request.data.get('name')
        print(name)
        desc = request.data.get('desc')
        print(desc)
        Recipe.objects.create(name=name, desc=desc)
        return Response('Recipe added')



# *********CACHING ENDS***************


#Multiple database check
@api_view(('GET',))
def db_check(request):
    # stu = Student.objects.all().using('special') # here we are using database with name 'special'. see settings.py
    # stu = Student.objects.first()
    # stu = Student.objects.last()
    # stu = Student.objects.earliest('datetime_of_payment') # need datatime column to find the earliest
    # stu = Student.objects.in_bulk([91,92]) # need to mention primary key in list and will return dictionary with key as primary key and value as object at provided primary key
    # print(stu[91].roll)
    # print(stu[92])
    # stu = Student.objects.in_bulk()# will return all the objects with primary key and key
    # stu = Student.objects.all()# will return all the objects
    # print(stu)
    # Student.objects.get(name='veeru').delete() # single object delete
    # Student.objects.filter(city='ranchi').delete() # bulk object delete
    # Student.objects.all().delete() # delete all data from db
    # serializer = StudentSerializer(stu, many=True)
    # s = Student.objects.all().count()
    s = Student.objects.all().explain()
    print(s)

    return Response("ok")

# Many-to-Many Relationship
class ManyToManyRelationshipViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        title1 = request.data.get('title')
        title2 = request.data.get('title2')
        headline = request.data.get('headline')
        p1 = Publication.objects.create(title=title1)
        p2 = Publication.objects.create(title=title2)
        a = Article.objects.create(headline=headline)
        a.publications.add(p1)
        a.publications.add(p2)
        return Response("Publication created")

    def get(self, request):
        a = Article.objects.all()
        p = Publication.objects.all()
        print(a)
        print(p)
        return Response('ok')


    def put(self, request):
        pass


#select_related
def select_rel(request):
    songs = Song.objects.select_related('singer').get(id=1)
    print(songs)
    print(songs.singer)
    return HttpResponse('ok')


from rest_framework import generics


class MultilplJsonObject(generics.GenericAPIView):
    def post(self, request):
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        for i in request.data:
            print(i['name'])
            print(i['gender'])


        return Response("ok")



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
    # lines = [
    #          'this is line',
    #          'this is line 2',
    #          'this is line 3'
    #          ]

    venues = Student.objects.all() # fetching data from database
    print(venues)

    lines = []
    for venue in venues:

        lines.append(venue.name)
        lines.append(str(venue.roll))
        lines.append(venue.city)
        lines.append(' ****** ')

    # loop throigh all lines
    for line in lines:
        textob.textLine(line)  # adding each line into textobject

    # finish up
    c.drawText(textob) # drawing text object on canvas
    c.showPage()#
    c.save() # saving canvas
    print('Canvas', c)
    buf.seek(0)
    print('buf', buf)

    # returning file as a response to the frondend for download
    return FileResponse(c, as_attachment=True, filename='venue.pdf')

# only crated to add a PDF URL
def home(request):
    return render(request, 'index.html')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)

    # if not pdf.
    return HttpResponse(result.getvalue(), content_type='application/pdf')
    # return None



class GenerateInvoice(View):
    def get(self, request):
        try:
            order_db = Student.objects.get(name="veeru")
            print("order_db = Student.objects.get(name='veeru')")     #you can filter using order_id as well
        except Student.DoesNotExist:
            order_db = None
            print("order_db = None")
            return HttpResponse("505 Not Found")
        data = {
            'order_name': order_db.name,
            'transaction_id': order_db.razorpay_payment_id,
            # 'user_email': order_db.user.email,
            'date': str(order_db.datetime_of_payment),
            # 'name': order_db.user.name,
            'order': order_db,
            'amount': order_db.total_amount,
        }
        pdf = render_to_pdf('invoice.html', data)
        print("type(pdf)", type(pdf))

        #return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            print(type(response))
            filename = "Invoice_%s.pdf" %(data['order_id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content


            print("return response")
            return response
        return HttpResponse("Not found")


import os
# New PDF Function
from io import BytesIO

from django.core.files.base import ContentFile


def generate_pdf(request):
    template_path = 'invoice.html'  # Replace with your HTML template file
     # Add data context for the template as needed

    try:
        order_db = Student.objects.get(name="veeru")
        print("order_db = Student.objects.get(name='veeru')")     #you can filter using order_id as well
    except Student.DoesNotExist:
        order_db = None
        print("order_db = None")
        return HttpResponse("505 Not Found")

    context = {
        'order_name': order_db.name,
        'transaction_id': order_db.razorpay_payment_id,
        # 'user_email': order_db.user.email,
        'date': str(order_db.datetime_of_payment),
        # 'name': order_db.user.name,
        'order': order_db,
        'amount': order_db.total_amount,
        }

    # Create a temporary file in memory to store the PDF content
    pdf_data = BytesIO()

    # Create a PDF document
    template = get_template(template_path)
    html = template.render(context)
    pisa.CreatePDF(html, dest=pdf_data)

    # Save the PDF to the database model
    pdf_file = ContentFile(pdf_data.getvalue())
    # pdf = GeneratedPDF(title="Generated PDF")
    order_db.invoice.save("generated_pdf.pdf", pdf_file)
    print(order_db.invoice.url)
    order_db.save()

    # Close the temporary PDF file
    pdf_data.close()

    return HttpResponse('PDF successfully generated and saved to the database.')


# Nested Serializer Test
class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer




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
        stu = Student.objects.filter(name='Sahil', roll=123)  # filter always return a queryset
        print("Returning Multiple Result", stu)
        print("SQL Query Property", stu.query) # will show sql query behind the scenes
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



