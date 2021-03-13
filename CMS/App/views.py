from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import *
from .serializers import *
# Create your views here.

class CreateUser(APIView):
    def post(self, request):
        params_data = request.data
        email = params_data.get('email', False)
        password = params_data.get('password', False)
        first_name = params_data.get('first_name', False)
        last_name = params_data.get('last_name', False)
        phone = params_data.get('phone', False)
        pincode = params_data.get('pincode', False)
        address = params_data.get('address', '')
        city = params_data.get('city', '')
        state = params_data.get('state', '')
        country = params_data.get('country', '')
        if False in [first_name, last_name, phone, pincode]:
            return Response({'error':True, 'result':'Please enter data for these fields :- first_name, last_name, phone, pincode'})
        validate_user = {'email':email, 'password':password, 'first_name':first_name, 'last_name':last_name, 'phone':phone, 'pincode':pincode, 'address':address, 'city':city, 'state':state, 'country':country}
        serial = UserSerializer(data=validate_user)
        if not serial.is_valid():
            return Response({'error':True, 'result':serial.errors})
        else:
            password = make_password(password)
            serial.save(password=password)
        return Response({'error':False, 'result':'User created'})

class SignIn(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            return Response({'error':True, 'result':'Please check your username and password'})
        token = Token.objects.get(user=user).key
        return Response({'error':False, 'result':token})

class CreateContent(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        params_data = request.data
        document = request.FILES['file']
        title = params_data.get('title', False)
        body = params_data.get('body', False)
        summary = params_data.get('summary', False)
        category  = params_data.get('categories', '')
        validate_content = {'title':title, 'body':body, 'summary':summary, 'document':document, 'author':request.user.pk}
        serial = ContentSerializer(data=validate_content)
        if not serial.is_valid():
            return Response({'error':True, 'result':serial.errors})
        else:
            content = serial.save()
        cat_id = []
        if category:
            for cat in category.split(','):
                data, status = Category.objects.get_or_create(name=cat.strip())
                cat_id.append(data.id)
            content.categories.add(*cat_id)
        return Response({'error':False, 'result':'Content created'})

    def get(self, request):
        user = request.user
        if user.is_superuser:
            posts = Content.objects.all().prefetch_related('categories')
        else:
            posts = Content.objects.filter(author=user).prefetch_related('categories')
        search = self.request.query_params.get('search', '')
        if search:
            posts = posts.filter(Q(categories__name__iregex=search)| Q(title__iregex=search) | Q(body__iregex=search) | Q(summary__iregex=search))
        url_maker = request.get_host()
        posts = [{'id': post.id, 'title': post.title, 'body':post.body, 'summary':post.summary, 'document':'http://'+url_maker+post.document.url, 'categories': [cat.name for cat in post.categories.all()]} for post in posts]
        return Response({'error':False, 'result':posts})
    
    def put(self, request):
        user = request.user
        params_data = request.data
        _id = self.request.query_params.get('id')
        post = Content.objects.get(pk=_id)
        title = params_data.get('title', post.title)
        body = params_data.get('body', post.body)
        summary = params_data.get('summary', post.summary)
        if user.is_superuser:
            post.title=title
            post.body=body 
            post.summary=summary
            post.save()
        else:
            if post.author.pk == user.pk:
                post.title=title 
                post.body=body 
                post.summary=summary
                post.save()
            else:
                return Response({'error':True, 'result':'Post does not belong to you.'})
        return Response({'error':False, 'result':'Post updated'})

    def delete(self, request):
        user = request.user
        _id = self.request.query_params.get('id')
        post = Content.objects.get(pk=_id)
        if user.is_superuser:
            post.delete()
        else:
            if post.author.pk == user.pk:
                post.delete()
            else:
                return Response({'error':True, 'result':'Post does not belong to you.'})
        return Response({'error':False, 'result':'Post deleted'})





