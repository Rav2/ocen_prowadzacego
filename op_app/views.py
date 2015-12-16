from django.shortcuts import render, loader
from django.http import HttpResponse
from .models import *
from .forms import CommentStars
# Create your views here.


def index(request):
    if request.method == 'GET':
        # return render(request, 'index.html')
        profiles = LecturerProfile.objects.all() # lisa prowadzacych
        template = loader.get_template('index.html') # Ładuje szablon
        context = {'profiles': profiles} # Definiuje dane z których korzysta szablon

        return HttpResponse(template.render(context))

def rate(request, pk):
    if request.method == 'GET':
        profile = LecturerProfile.objects.filter(pk=pk)
        comments = Comment.objects.all()

        context = {'profile': profile[0], 'comments':comments}
        return render(request, 'rate.html', context)
    elif request.method == 'POST':
        comm = Comment()
        comm.text = request.POST['content']
        comm.profile= LecturerProfile.objects.get(pk=pk)
        comm.teaching = request.POST['teaching_val']
        comm.knowledge = request.POST['knowledge_val']
        comm.friendliness = request.POST['friendliness_val']
        comm.save()
        #TODO: make it look likea prof
        profile = LecturerProfile.objects.filter(pk=pk)
        # template = loader.get_template()
        comments = Comment.objects.all()
        context = {'profile': profile[0], 'comments':comments}
        return render(request, 'rate.html', context)
    #TODO: what if it is not a POST nor GET?


