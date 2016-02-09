from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.db.models import F
from .forms import LecturerForm, RegistrationForm
# Create your views here.


# def index(request):
#     if request.method == 'GET':
#         # return render(request, 'index.html')
#         profiles = LecturerProfile.objects.all() # lisa prowadzacych
#         template = loader.get_template('index.html') # Ładuje szablon
#         context = {'profiles': profiles} # Definiuje dane z których korzysta szablon


def rate(request, pk):
    if request.method == 'GET':
        profile = LecturerProfile.objects.filter(pk=pk)
        if(profile):
            comments = Comment.objects.filter(profile=profile).order_by('-date')
            work_places = WorkPlace.objects.filter(lecturerprofile__pk=pk).distinct()
            work_names = list(set([x.name for x in work_places]))
            work_towns= list(set([x.town for x in work_places]))
            if len(work_places)>0:
                context = {'profile': profile[0], 'comments': comments, 'work_names': work_names, 'work_towns': work_towns}
            else:
                context = {'profile': profile[0], 'comments': comments, 'work': None}
            return render(request, 'rate.html', context)
        else:
            return HttpResponse(status=404, content="<p>404 PAGE NOT FOUND!</p> <a href='/index'>Main page</a>")
    elif request.method == 'POST':
        comm = Comment()
        comment_content = request.POST['content']
        if len(comment_content) > 2000:
            comment_content = comment_content[0:1999]

        comm.text = comment_content
        comm.profile = LecturerProfile.objects.get(pk=pk)
        comm.teaching = request.POST['teaching_val']
        comm.knowledge = request.POST['knowledge_val']
        comm.friendliness = request.POST['friendliness_val']
        comment_nick = request.POST['nick']
        if len(comment_nick) > 20:
            comment_nick = comment_nick[0:19]
        comm.nickname = comment_nick
        comm.date = datetime.now()
        comm.save()
        profile = LecturerProfile.objects.get(pk=pk)
        comments = Comment.objects.filter(profile=profile).order_by('-date')
        teach_av = 0.
        know_av = 0.
        friend_av = 0.
        for comment in comments:
            teach_av += comment.teaching
            know_av += comment.knowledge
            friend_av += comment.friendliness
        profile.teaching_av = round(teach_av/len(comments), 2)
        profile.knowledge_av = round(know_av/len(comments), 2)
        profile.friendliness_av = round(friend_av/len(comments), 2)
        profile.save()

        work_places = WorkPlace.objects.filter(lecturerprofile__pk=pk).distinct()
        work_names = list(set([x.name for x in work_places]))
        work_towns= list(set([x.town for x in work_places]))

        context = {'profile': profile, 'comments': comments, 'nickname': comm.nickname, 'date': comm.date, 'work_names': work_names, 'work_towns': work_towns}
        return render(request, 'rate.html', context)
    else:
        return HttpResponse(status=403)


def index(request):
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
        context = {'profiles': profiles}
        return render(request, 'index.html', context)
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
            else:
                comments = Comment.objects.filter(profile=l1).order_by('-date')
                context = {'profile': l1[0], 'comments': comments}
                return render(request, 'rate.html', context)
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


def ranking_top10(request):
    if request.method == 'GET':
        lecturer_profiles = LecturerProfile.objects.all().order_by((F('teaching_av')+F('knowledge_av')+F('friendliness_av'))/3).reverse()[:10]
        context = {'profiles': lecturer_profiles, 'title': "Ranking 10 najlepszych prowadzących według ocen użytkowników"}
        return render(request, 'ranking.html', context)
    else:
        return HttpResponse(status=403)


def ranking_university(request):
    if request.method == 'GET':
        universities = WorkPlace.objects.all().order_by('name')
        context = {'universities': universities}
        return render(request, 'ranking_universities.html', context)
    elif request.method == 'POST':
        profiles = LecturerProfile.objects.filter(work_places__name=request.POST['University']).distinct().order_by((F('teaching_av')+F('knowledge_av')+F('friendliness_av'))/3).reverse()
        context = {'profiles': profiles, 'title': "Ranking prowadzących na uczelni: "+request.POST['University']}
        return render(request, 'ranking.html', context)
    else:
        return HttpResponse(status=403)
