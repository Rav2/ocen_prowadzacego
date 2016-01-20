from django.contrib.auth.decorators import login_required
from django.shortcuts import render, loader, redirect
from django.http import HttpResponse
from .models import *
from .forms import CommentStars, LecturerForm, RegistrationForm
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
        comments = Comment.objects.filter(profile=profile)

        context = {'profile': profile[0], 'comments':comments}
        return render(request, 'rate.html', context)
    elif request.method == 'POST':
        comm = Comment()
        comm.text = request.POST['content']
        comm.profile = LecturerProfile.objects.get(pk=pk)
        comm.teaching = request.POST['teaching_val']
        comm.knowledge = request.POST['knowledge_val']
        comm.friendliness = request.POST['friendliness_val']
        comm.nickname = request.POST['nick']
        comm.date = datetime.now()
        comm.save()
        star_number = [0,1,2,3,4]
        #TODO: make it look likea prof
        profile = LecturerProfile.objects.filter(pk=pk)
        # template = loader.get_template()
        comments = Comment.objects.filter(profile=profile)
        context = {'profile': profile[0], 'comments':comments, 'nickname': comm.nickname, 'date': comm.date, 'star_number': star_number}
        return render(request, 'rate.html', context)
    else:
        return HttpResponse(status=403)


def search(request):
    if request.method == 'GET':
        return render(request, 'search.html')
    elif request.method == 'POST':
        if not request.POST['Surname'] and not request.POST['WorkPlace']:
            return render(request, 'search.html')
        if request.POST['Surname']:
            profiles = LecturerProfile.objects.filter(surname__iexact=request.POST['Surname'])
            if not profiles:
                profiles = LecturerProfile.objects.filter(tags__name__iexact=request.POST['Surname']).distinct()
            if request.POST['WorkPlace']:
                profiles1 = profiles.filter(work_places__name__iexact=request.POST['WorkPlace']).distinct()
                if not profiles1:
                    profiles1 = profiles.filter(work_places__town__iexact=request.POST['WorkPlace']).distinct()
                profiles = profiles1
        else:
            profiles = LecturerProfile.objects.filter(work_places__name__iexact=request.POST['WorkPlace']).distinct()
            if not profiles:
                profiles = LecturerProfile.objects.filter(work_places__town__iexact=request.POST['WorkPlace']).distinct()
        template = loader.get_template('index.html') # Ładuje szablon
        context = {'profiles': profiles} # Definiuje dane z których korzysta szablon
        return HttpResponse(template.render(context))
    else:
        return HttpResponse(status=403)


@login_required
def addLecturer(request):
    if request.method == 'POST':
        formular = LecturerForm(request.POST)
        if formular.is_valid():
            l1 = LecturerProfile.objects.filter(surname=request.POST['surname'],
                                                name=request.POST['name'])
            if not l1:
                l = LecturerProfile()
                l.name = request.POST['name']
                l.surname = request.POST['surname']
                user = request.user
                l.user_id = user
                if request.POST['info']:
                    l.info = request.POST['info']
                l.save()
                for i in range(1, 4):
                    if request.POST['workPlaceName'+str(i)] or request.POST['workPlaceTown'+str(i)]:
                        wp = WorkPlace.objects.filter(name=request.POST['workPlaceName'+str(i)],
                                                      town=request.POST['workPlaceTown'+str(i)])
                        if wp:
                            l.work_places.add(wp[0])
                        else:
                            wp = WorkPlace.objects.create(name=request.POST['workPlaceName'+str(i)],
                                                          town=request.POST['workPlaceTown'+str(i)])
                            l.work_places.add(wp)
                for i in range(1, 4):
                    if request.POST['tag'+str(i)]:
                        t = Tags.objects.filter(name=request.POST['tag'+str(i)])
                        if t:
                            l.tags.add(t[0])
                        else:
                            t = Tags.objects.create(name=request.POST['tag'+str(i)])
                            l.tags.add(t)
                l.save()
            return redirect('/index')
    elif request.method == 'GET':
        formular = LecturerForm()
    else:
        return HttpResponse(status=403)
    return render(request, 'add.html', {'form': formular})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
                                            email=request.POST['email'], first_name=request.POST['first_name'],
                                            last_name=request.POST['last_name'])
            user.save()
            return redirect('/index')
    elif request.method == 'GET':
        form = RegistrationForm()
    else:
        return HttpResponse(status=403)
    return render(request, 'registration.html', {'form': form})
