from django.contrib import messages
from django.shortcuts import redirect, render
from .models import question, response, userlist, riddle
from accounts.models import Profile
from django.contrib.auth.models import auth, User
from datetime import datetime, timedelta
from datetime import datetime
from django.utils import timezone
import random


# Create your views here.


def start(request):
    la = Profile.objects.get(user=request.user)
    if la.ExpLgtTime == None:
        la.StartTime = timezone.localtime(timezone.now())
        exptlgt = la.StartTime + timezone.timedelta(minutes=30)
        la.ExpLgtTime = exptlgt
        la.save()
    return redirect(home)


def addtime(request):
    if request.method == "POST":
        username = request.POST['username']
        time = request.POST['time']
        password = request.POST['password']
        user = auth.authenticate(username=request.user, password=password)
        if user is not None:
            user = User.objects.get(username=username)
            la = Profile.objects.get(user=user)
            print(la.ExpLgtTime)
            if la.ExpLgtTime == None:
                la.ExpLgtTime = timezone.timedelta(
                    minutes=10) + timezone.localtime(timezone.now())
                la.save()
            exptlgt = la.ExpLgtTime + timedelta(seconds=int(time))
            la.ExpLgtTime = exptlgt
            la.is_notallowed = False
            la.save()
            messages.success(request, 'Time Updated success')
        else:
            m = 'You have entered incorrect password hence time not updated for user : " ' + username + ' "'
            messages.error(request, m)
    return redirect(instructions)


def zoneactivate(request):
    # activate zone
    la = Profile.objects.get(user=request.user)
    if la.zone_activate == False:
        ul = userlist.objects.get(user=request.user)
        if la.score < 4:
            la.zone = "Red"
            ms = ['4', '2']
            ul.markingscheme = listtotext(ms)
            ul.save()
        elif la.score < 8:
            la.zone = "Green"
            ms = ['6', '4']
            ul.markingscheme = listtotext(ms)
            ul.save()
        else:
            la.zone = "Purple"
            ms = ['10', '10']
            ul.markingscheme = listtotext(ms)
            ul.save()
        la.zone_activate = True
        la.save()
    else:
        messages.error(request, "You have already used this lifeline")
    return redirect(home)


def texttolist(arr):
    if arr != None:
        l = arr.split(',')
        for j in l:
            if j == "":
                l.remove("")
        return l
    else:
        return list()


def listtotext(arr):
    l = ""
    for i in arr:
        l = l + str(i) + ","
    return l


def timesave(request):
    la = Profile.objects.get(user=request.user)
    naive1 = la.StartTime.replace(tzinfo=None)
    naive2 = la.CompTime.replace(tzinfo=None)
    time_delta = naive2 - naive1
    la.Timetaken = str(time_delta)
    la.save()
    # print(time_delta,type(time_delta),la.Timetaken,type(la.Timetaken))


def home(request):
    if request.user.is_authenticated:
        la = Profile.objects.get(user=request.user)
        ul = userlist.objects.get(user=request.user)
        naive = la.ExpLgtTime.replace(tzinfo=None)
        time_delta = naive + timedelta(hours=5, minutes=30) - datetime.now()
        total_secs = time_delta.total_seconds()
        # print(total_secs,time_delta,naive,datetime.now())
        if total_secs <= 0:
            return redirect(finish)
        mins = total_secs // 60
        secs = int(total_secs % 60)
        if la.score < 4:
            zone = "Red"
            if not la.zone_activate:
                la.zone = zone
                la.save()
        elif la.score < 8:
            zone = "Green"
            if not la.zone_activate:
                la.zone = zone
                la.save()
        elif la.score < 12:
            zone = "Purple"
            if not la.zone_activate:
                la.zone = zone
                la.save()
        if request.method == "POST":
            # print(la.zone,"after function return")
            ul = userlist.objects.get(user=request.user)
            id = int(request.POST['id'])
            ans = (request.POST['ans']).replace(" ", "")
            li = texttolist(ul.unattemptedlist)
            al = texttolist(ul.attemptedlist)
            cl = texttolist(ul.correctlist)
            noa = ul.attemptsleft - 1
            ul.attemptsleft = noa
            ul.save()
            cans = question.objects.get(id=id)
            if noa == 1:
                # store response 1 here
                time_1 = timezone.localtime(timezone.now())
                r1 = response.objects.create(
                    user=la.user, queid=cans, response1=ans, r1_time=time_1)
                r1.save()
                print(cans.answer,type(cans.answer),ans,type(ans))
                if int(cans.answer) == int(ans):
                    ms = texttolist(ul.markingscheme)
                    la.score = la.score + int(ms[0])
                    la.save()
                    # print(la.zone,"in checking answer noa 1 ")
                    ms = ['4', '2']
                    ul.markingscheme = listtotext(ms)
                    ul.save()
                    if la.zone_activate:
                        la.zone = "Used"
                        la.save()
                else:
                    ms = texttolist(ul.markingscheme)
                    la.score = la.score - int(ms[1])
                    la.save()
                    # print(la.zone,"in checking answer")
                    # we have error here 
                    if la.zone_activate:
                        if la.zone == "Used":
                            ms = ['2', '1']
                        if la.zone == "Red":
                            ms = ['4', '2']
                        if la.zone == "Purple":
                            ms = ['10', '10']
                        if la.zone == "Green":
                            ms = ['6', '4']
                    else:
                        ms = ['2', '1']
                    ul.markingscheme = listtotext(ms)
                    ul.save()
            else:
                # store response 2 here
                time_2 = timezone.localtime(timezone.now())
                r2 = response.objects.get(user=request.user, queid=cans)
                r2.response2 = ans
                r2.r2_time = time_2
                r2.save()
                if cans.answer == ans:
                    ms = texttolist(ul.markingscheme)
                    la.score = la.score + int(ms[0])
                    la.save()
                    # print(la.zone,"in checking answer")
                    ms = ['4', '2']
                    ul.markingscheme = listtotext(ms)
                    ul.save()
                else:
                    ms = texttolist(ul.markingscheme)
                    la.score = la.score - int(ms[1])
                    la.save()
                    # print(la.zone,"in checking answer")
                    ms = ['2', '1']
                    ul.markingscheme = listtotext(ms)
                    ul.save()
                if la.zone_activate:
                    la.zone = "Used"
                    la.save()
            resp = response.objects.get(user=request.user, queid=cans)
            resp1 = resp.response1
            score = la.score
            if la.score < 4:
                zone = "Red"
                if not la.zone_activate:
                    la.zone = zone
                    la.save()
            elif la.score < 8:
                zone = "Green"
                if not la.zone_activate:
                    la.zone = zone
                    la.save()
            else:
                zone = "Purple"
                if not la.zone_activate:
                    la.zone = zone
                    la.save()
            if cans.answer == ans or noa == 0:
                al.append(id)
                ul.attemptedlist = listtotext(al)
                ul.save()
                if cans.answer == ans:
                    cl.append(id)
                    ul.correctlist = listtotext(cl)
                    ul.save()
                if len(li) == 1:
                    li.remove(str(id))
                    ul.unattemptedlist = listtotext(li)
                    ul.attemptsleft = 0
                    ul.save()
                    return redirect(finish)
                li.remove(str(id))
                id = li[0]
                q = question.objects.get(id=id)
                l = ""
                noa = 2
                ul.attemptsleft = 2
                ul.save()
                ul.unattemptedlist = listtotext(li)
                ul.save()
                score = la.score
                if ul.attemptedlist == None:
                    lena = 0
                else:
                    lena = len(texttolist(ul.attemptedlist))
                if la.zone == 'Red':
                    color = "#D22B2B"
                elif la.zone == "Green":
                    color = "#228B22"
                elif la.zone == "Purple":
                    color = "#702963"
                else:
                    color = "#39998E"
                return render(request, 'quiz.html',
                              {'title': "Quiz", 'q': q, 'noa': noa, 'score': score, 'r1': resp1, 'mins': mins,
                               'secs': secs, 'ms0': int(texttolist(ul.markingscheme)[0]),
                               'ms1': int(texttolist(ul.markingscheme)[1]), 'noqa': lena,
                               'pbar': (lena * 100) / len(question.objects.all()), 'zone': zone, 'color': color,
                               'zone_active': la.zone_activate, 'lazone': la.zone, 'riddle': la.riddle_activate,
                               'uz': ['None', 'Used', 'Red']})
            else:
                messages.error(request, "Your answer is Incorrect")
                q = question.objects.get(id=id)
                if ul.attemptedlist == None:
                    lena = 0
                else:
                    lena = len(texttolist(ul.attemptedlist))
                if la.zone == 'Red':
                    color = "#D22B2B"
                elif la.zone == "Green":
                    color = "#228B22"
                elif la.zone == "Purple":
                    color = "#702963"
                else:
                    color = "#39998E"
                return render(request, 'quiz.html',
                              {'title': "Quiz", 'q': q, 'noa': noa, 'score': score, 'r1': resp1, 'mins': mins,
                               'secs': secs, 'ms0': int(texttolist(ul.markingscheme)[0]),
                               'ms1': int(texttolist(ul.markingscheme)[1]), 'noqa': lena,
                               'pbar': (lena * 100) / len(question.objects.all()), 'zone': zone, 'color': color,
                               'zone_active': la.zone_activate, 'lazone': la.zone, 'riddle': la.riddle_activate,
                               'uz': ['None', 'Used', 'Red']})
        else:
            ul = userlist.objects.get(user=request.user)
            if ul.unattemptedlist == "":
                return redirect(finish)
            ul = userlist.objects.get(user=request.user)
            li = texttolist(ul.unattemptedlist)
            # al = texttolist(ul.attemptedlist)
            id = li[0]
            q = question.objects.get(id=id)
            noofattempts = ul.attemptsleft
            score = la.score
            if response.objects.filter(user=request.user, queid=id).exists():
                resp = response.objects.get(user=request.user, queid=id)
                resp1 = resp.response1
            else:
                resp1 = None
            zone = la.zone
            if ul.attemptedlist == None:
                lena = 0
            else:
                lena = len(texttolist(ul.attemptedlist))
            if la.zone == 'Red':
                color = "#D22B2B"
            elif la.zone == "Green":
                color = "#228B22"
            elif la.zone == "Purple":
                color = "#702963"
            else:
                color = "#39998E"
            return render(request, 'quiz.html',
                          {'title': "Quiz", 'q': q, 'noa': noofattempts, 'score': score, 'r1': resp1, 'mins': mins,
                           'secs': secs, 'ms0': int(texttolist(ul.markingscheme)[0]),
                           'ms1': int(texttolist(ul.markingscheme)[1]), 'noqa': lena,
                           'pbar': (lena * 100) / len(question.objects.all()), 'zone': zone, 'color': color,
                           'zone_active': la.zone_activate, 'lazone': la.zone, 'riddle': la.riddle_activate,
                           'uz': ['None', 'Used', 'Red']})
    else:
        messages.error(
            request, 'You cannot start quiz because you have not "Login" yet.')
        return redirect('/')


def finish(request):
    if request.user.is_authenticated:
        la = Profile.objects.get(user=request.user)
        userlists = userlist.objects.get(user=request.user)
        crct = userlists.correctlist
        atlt = userlists.attemptedlist
        if crct:
            canswered = len(crct) // 2
        else:
            canswered = 0
        if atlt:
            attempted = len(atlt) // 2
        else:
            attempted = 0
        la.CompTime = timezone.localtime(timezone.now())
        la.save()
        timesave(request)
        man = request.user.first_name
        score = la.score
        auth.logout(request)
        return render(request, 'result.html',
                      {'title': 'Result', 'score': score, 'man': man, 'numc': canswered, 'numa': attempted})
    else:
        messages.error(request,'Please Login First')
        return redirect('/')


def activatelifeline2(request):
    return redirect(riddleque)


def riddleque(request):
    if request.user.is_authenticated:
        la = Profile.objects.get(user=request.user)
        ul = userlist.objects.get(user=request.user)
        naive = la.ExpLgtTime.replace(tzinfo=None)
        time_delta = naive + timedelta(hours=5, minutes=30) - datetime.now()
        total_secs = time_delta.total_seconds()
        if total_secs <= 0:
            return redirect(finish)
        mins = total_secs // 60
        secs = int(total_secs % 60)
        score = la.score
        ms = ['2', '4']
        qc = riddle.objects.all()
        print(qc)
        q = random.choice(qc)
        print("hi")
        print(q)
        # print(q,qc)
        if request.method == "POST":
            id = int(request.POST['id'])
            ans = request.POST['ans']
            # print("id and ans",id,ans)
            q = riddle.objects.get(id=id)
            if q.answer == ans:
                # print("Answer is correct")
                score = score + int(ms[0])
                messages.success(request, "You attempted riddle correctly, Hence +2")
            else:
                # print("Answer is Incorrect")
                score = score - int(ms[1])
                messages.error(request, "You attempted riddle Incorrectly, Hence -4")
            li = texttolist(ul.unattemptedlist)
            al = texttolist(ul.attemptedlist)
            cl = texttolist(ul.correctlist)
            qid = li[0]
            if q.answer == ans:
                cl.append(str(qid))
                ul.correctlist = listtotext(cl)
            li.remove(str(qid))
            ul.unattemptedlist = listtotext(li)
            al.append(str(qid))
            ul.attemptedlist = listtotext(al)
            ul.save()
            la.score = score
            la.riddle_activate = True
            la.save()
            return redirect(home)
        else:
            return render(request, "riddle.html", {'title': 'Riddle', 'ms0': int(texttolist(ul.markingscheme)[0]),
                                                   'ms1': int(texttolist(ul.markingscheme)[1]), 'mins': mins,
                                                   'secs': secs, 'score': score, 'ms': ms, 'q': q})
    else:
        messages.error(
            request, 'You cannot start quiz because you have not "Login" yet.')
        return redirect('/')


def instructions(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            NRU = len(User.objects.all().exclude(is_staff=True))
            NLU = len(userlist.objects.all())
            NCU = 0
            que = question.objects.all()
            for i in userlist.objects.all():
                if i.unattemptedlist == "":
                    NCU += 1
            status = False
            Name = Username = Email = Score = ul = al = cl = login = exptlgt = fstlgn = comptime = timetaken = l1 = l2 = fname = ""
            if request.method == "POST":
                username = request.POST['username']
                if User.objects.filter(username=username).exists():
                    candidate = User.objects.get(username=username)
                    if candidate.is_staff:
                        M = 'User "' + username + '" is a superadmin.'
                        messages.error(request, M)
                    else:
                        if userlist.objects.filter(user=candidate).exists():
                            userlists = userlist.objects.get(user=candidate)
                            la = Profile.objects.get(user=candidate)
                            status = True
                            Name = candidate.first_name + " " + candidate.last_name
                            fname = candidate.first_name
                            Username = candidate.username
                            Email = candidate.email
                            Score = la.score
                            login = candidate.last_login
                            ul = texttolist(userlists.unattemptedlist)
                            al = texttolist(userlists.attemptedlist)
                            cl = texttolist(userlists.correctlist)
                            exptlgt = la.ExpLgtTime
                            fstlgn = la.StartTime
                            comptime = la.CompTime
                            timetaken = la.Timetaken
                            l1 = la.zone_activate
                            l2 = la.riddle_activate
                        else:
                            M = 'User "' + username + '" Has not started quiz yet'
                            messages.error(request, M)
                else:
                    M = 'User "' + username + '" Does Not Exist'
                    messages.error(request, M)
            return render(request, 'superuser.html',
                          {'title': 'Superuser panel', 'status': status, 'Name': Name, 'fname': fname,
                           'Username': Username, 'Email': Email, 'Score': Score, 'ul': ul, 'al': al, 'cl': cl,
                           'login': login, 'NRU': NRU, 'NLU': NLU, 'NCU': NCU,
                           'RU': User.objects.all().exclude(is_staff=True), 'LU': Profile.objects.all(),
                           'exptlgt': exptlgt, 'fstlgn': fstlgn, 'comptime': comptime, 'que': que, 'lq': len(que),
                           'timetaken': timetaken, 'l1': l1, 'l2': l2, 'l1l2': l1 or l2})
        else:
            ul = userlist.objects.get(user=request.user)
            if ul.unattemptedlist != "":
                la = Profile.objects.get(user=request.user)
                if la.has_started and la.is_notallowed:
                    auth.logout(request)
                    messages.error(
                        request, 'You have already started attempting quiz. Contact Superadmins for error')
                    return redirect('/')
                else:
                    la = Profile.objects.get(user=request.user)
                    la.has_started = True
                    la.is_notallowed = True
                    la.save()
                    return render(request, 'instructions.html', {'title': 'Instructions'})
            else:
                # la.is_notallowed: need to ask this
                return redirect('/quiz/finish')
    else:
        messages.error(
            request, 'You cannot enter to quiz because you have not "Login" yet.')
        return redirect('/')
