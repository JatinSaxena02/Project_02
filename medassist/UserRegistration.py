from django.shortcuts import render, redirect
from . import Pool
import random
from django.http import JsonResponse
import json
from datetime import date
import time


def UserRegistrationInterface(request):
    return render(request, "UserRegistration.html", {'msg': ''})


def UserLogin(request):
    return render(request, "LoginPage.html", {'msg': ''})


def OtpPage(request):
    btn = request.POST['btn']
    if (btn == "Login"):
        db, cmd = Pool.ConnectionPooling()
        mobileno = request.POST['mobileno']
        q = "Select * from userregistration where usernum='{}'".format(mobileno)
        cmd.execute(q)
        data = cmd.fetchone()
        if (data):
            otp = random.randint(1000, 9999)
            print(otp)
            request.session['user'] = data['username']
            request.session['usermobile'] = data['usernum']
            return render(request, "OtpPage.html", {'otp': otp})
        else:
            return render(request, "LoginPage.html", {'msg': 'Invalid Mobile Number'})

    else:
        return render(request, "UserRegistration.html", {'msg': ''})


def ChkOtp(request):
    d1 = request.POST['digit1']
    d2 = request.POST['digit2']
    d3 = request.POST['digit3']
    d4 = request.POST['digit4']
    gotp = request.POST['gotp']
    iotp = d1 + d2 + d3 + d4
    if (gotp == iotp):
        return DoctorDisplayAll(request)
    else:
        return render(request, "OtpPage.html", {"msg": "Invalid Otp"})


def UserRegistrationDisplayAll(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        q = "Select * From userregistration"
        cmd.execute(q)
        records = cmd.fetchall()
        db.close()
        return render(request, "DisplayAllUserRegistration.html", {'result': records})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllUserRegistration.html", {'result': {}})


def UserRegistrationSubmit(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        username = request.POST['username']
        usercity = request.POST['usercity']
        useremail = request.POST['useremail']
        userdob = request.POST['userdob']
        tor = request.POST['tor']
        usernum = request.POST['usernum']
        userpassword = request.POST['userpassword']

        q = "insert into userregistration(username, usercity, useremail, userdob, tor,usernum,userpassword) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(
            username, usercity, useremail, userdob, tor, usernum, userpassword)
        print(q)
        cmd.execute(q)
        db.commit()
        db.close()
        return render(request, "UserRegistration.html", {'msg': 'Record Submitted'})
    except Exception as e:
        print(e)
        return render(request, "UserRegistration.html", {'msg': 'Fail To Submit Record'})


def UserSignPage(request):
    return render(request, "UserSignPage.html", {'msg': ''})


def EmailSignPage(request):
    return render(request, 'EmailSignPage.html', {'msg': ''})


#def CheckDoctorLoginOtp(request):
   # d1 = request.POST['digit1']
    #d2 = request.POST['digit2']
    #d3 = request.POST['digit3']
    #d4 = request.POST['digit4']
   # gotp = request.POST['gotp']
    #iotp = d1 + d2 + d3 + d4
    #if (gotp == iotp):
     #   return DoctorLoginDashboard(request)
   # else:
    #    return render(request, "OtpPage.html", {"msg": "Invalid Otp"})


def CheckEmailSignPage(request):
    db, cmd = Pool.ConnectionPooling()
    useremail = request.POST['useremail']
    userpassword = request.POST['userpassword']
    q = "Select * from userregistration where useremail='{0}' and userpassword='{1}'".format(useremail, userpassword)
    cmd.execute(q)
    data = cmd.fetchone()
    if (data):
        request.session['user'] = data['username']
        request.session['usermobile'] = data['usernum']
        return DoctorDisplayAll(request)
    else:
        return render(request, "EmailSignPage.html", {'msg': 'Invalid EmailId/Password'})


def Forgotpaswd(request):
    return render(request, "ForgotPassword.html", {'msg': ''})


def DoctorDisplayAll(request):
    try:

        db, cmd = Pool.ConnectionPooling()
        q = "Select * from doctorregistration"
        cmd.execute(q)
        data = cmd.fetchall()
        print("......................................................")
        print(data)
        return render(request, "DoctorDisplay.html", {'msg': "", 'Data': data, 'UserName': request.session['user']})
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(e)
        return render(request, "DoctorDisplay.html", {'msg': ""})


def Instruction(request):
    try:
        sid = request.POST['sid']
        docid = request.POST['docid']
        print(sid)
        db, cmd = Pool.ConnectionPooling()
        q = "Select D.*,(select S.specialization from specialization S where S.specializationid=D.specialization ) as ts from doctorregistration D where D.specialization={0} and D.doctorid={1}".format(
            sid, docid)
        print(q)
        cmd.execute(q)
        doctor = cmd.fetchall()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(doctor)
        request.session['doctor'] = doctor[0]['doctorid']
        return render(request, "InstructionPage.html",
                      {'doctorname': doctor[0]['doctorname'], 'icon': doctor[0]['icon'],
                       'specializationid': doctor[0]['specialization'], 'splname': doctor[0]['ts']})
    except Exception as e:
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(e)


# help
def QuestionPage(request):
    try:
        splid = request.GET['splid']
        db, cmd = Pool.ConnectionPooling()
        '''
        SELECT Q.*,group_concat(S.subquestion SEPARATOR '#') FROM medassist.questions Q,subquestions S where Q.questionnumber=S.questionid group by Q.questionnumber;
        '''
        q = "select q.*,(select specialization from specialization where specializationid='{0}') as specialization from questions q  where specializationid='{0}';".format(
            splid)
        cmd.execute(q)
        question = cmd.fetchall()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(question)
        q = "select * from subquestions where specializationid='{}'".format(splid)
        cmd.execute(q)
        subquestion = cmd.fetchall()
        print(subquestion)
        return JsonResponse({'result': question, 'result2': subquestion})
    except Exception as e:
        print(e)
        return JsonResponse({'result': " "})


def CallQuestionPage(request):
    splid = request.POST['splid']
    print("????????????????????????????????????????????")
    print(splid)
    return render(request, "QuestionPage.html", {'splid': splid})


def SubmitScore(request):
    try:
        score = json.loads(request.GET['score'])
        print("xxxxxxxxxxxxxxxxxxx", score)
        db, cmd = Pool.ConnectionPooling()
        today = date.today()
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        mobileno = request.session['usermobile']

        print("--------------------------------------------------------------")
        print(mobileno)
        q = "insert into userdoctor(mobileno,doctorid,currentdate,currenttime)values('{}',{},'{}','{}')".format(
            request.session['usermobile'], request.session['doctor'], today, current_time)
        cmd.execute(q)
        db.commit()
        cmd.execute('SELECT last_insert_id() as userdoctorid')
        row = cmd.fetchone()
        print("IDDDD", row)
        qn = 1
        for scr in score:
            L = list(map(int, scr.values()))
            v = sum(L)
            q = "insert into userdiagnose(userdoctorid,questionno,totalscore) values({},{},{})".format(
                row['userdoctorid'], qn, v)
            cmd.execute(q)
            qn += 1
        db.commit()
        db.close()
        return JsonResponse(
            {'result': True, 'username': request.session['user'][0], 'mobileno': request.session['user'][1],
             'email': request.session['user'][2]})
    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(e)
        return JsonResponse({'result': False})


def DoctorLogin(request):
    return render(request, 'DoctorLogin.html', {'msg': ''})


def DoctorLoginDashboard(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        mobileno = request.POST['mobileno']
        q = "Select * from doctorregistration where mobileno='{0}'".format(mobileno)
        cmd.execute(q)
        data = cmd.fetchone()
        print("-------------------------------------------------------->")
        print(data['emailid'])
        print(data['doctorname'])
        print(data)
        request.session['doctor'] = [data['doctorname'], data['doctorid'], data['specialization'], data['mobileno'],
                                     data['emailid'], data['icon'], data['dob'], data['gender']]
        if (data):
            q = "select UD.*,(select U.username from userregistration U where U.usernum=UD.mobileno) as username from userdoctor UD where UD.doctorid={0}".format(
                data['doctorid'])
            cmd.execute(q)
            result = cmd.fetchall()
            print(result)
            if (result):
                print("---------------------------------------------------------->")
                print(data['doctorname'])
                print(mobileno)
                return render(request, "DoctorLoginDashboard.html",
                      {'result': result, 'docname': request.session['doctor'][0], 'docid': request.session['doctor'][1],'docspl': request.session['doctor'][2],'docmobile': request.session['doctor'][3],
                       })

            else:
                return render(request, "DoctorLogin.html", {'msg': 'Invalid mobile number'})

    except Exception as e:
        print("------------------------")
        print(e)

def DoctorLogout(request):
        del request.session['doctor']
        return redirect('/doctorlogin')