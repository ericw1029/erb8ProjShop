from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# todo
# !

def index(request):
    print(request,request.path)
    #return HttpResponse("Pages-> index")
    return render(request,'pages/index.html')

def about(request):
    #return HttpResponse("Pages-> about")
    return render(request,'pages/about.html')