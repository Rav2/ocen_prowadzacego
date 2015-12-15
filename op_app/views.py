from django.shortcuts import render, loader
from django.http import HttpResponse
from .models import *
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
        template = loader.get_template('rate.html')
        context = {'profile': profile[0]}

        return render(request, 'rate.html', context)
    elif request.method == 'POST':
        comm = Comment()
        comm.text = request.POST['content']
        #TODO: this is an object! make it work
        comm.profile_id = LecturerProfile.objects.get(pk=pk)
        comm.teaching = 0
        comm.wisdom = 0
        comm.friendliness = 0
        comm.save()
        #TODO: make it look likea prof
        profile = LecturerProfile.objects.filter(pk=pk)
        # template = loader.get_template()
        context = {'profile': profile[0]}

        return render(request, 'rate.html', context)


