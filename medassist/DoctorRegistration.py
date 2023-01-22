from django.shortcuts import render
from django.http import JsonResponse
from . import Pool
import datetime
from django.views.decorators.clickjacking import xframe_options_exempt
@xframe_options_exempt

def DoctorRegistrationInterface(request):
    try:
        admin = request.session['admin']
        print("ADMIN", admin)
        return render(request, "DoctorRegistration.html", {'msg': ''})
    except Exception as e:
        return  render(request,"AdminLogin.html",{'msg':''})


@xframe_options_exempt

def DoctorRegistrationDisplayAll(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        q = "Select D.*,(select S.specialization from specialization S where S.specializationid=D.specialization) as tspecialization  From doctorregistration D"
        cmd.execute(q)
        records = cmd.fetchall()
        db.close()
        return render(request, "DisplayAllRegistration.html", {'result': records})
    except Exception as e:
        print(e)
        return render(request, "DisplayAllRegistration.html", {'result': {}})

@xframe_options_exempt

def DoctorRegistrationSubmit(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        dname = request.POST['dname']
        gen = request.POST['gender']
        dob = request.POST['dob']
        mobnum = request.POST['mobnum']
        email = request.POST['email']
        special = request.POST['special']
        iconfile = request.FILES['icon']
        q = "insert into doctorregistration(doctorname,gender,dob,mobileno,emailid,specialization,icon) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(dname, gen, dob, mobnum, email, special, iconfile.name)
        print(q)
        cmd.execute(q)
        db.commit()
        F = open("d:/medassist/assets/" + iconfile.name, "wb")
        for chunk in iconfile.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return render(request, "DoctorRegistration.html", {'msg': 'Record Submitted'})
    except Exception as e:
        print(e)
        return render(request, "DoctorRegistration.html", {'msg': 'Fail To Submit Record'})


@xframe_options_exempt
def UpdateDoctorRegistration(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        doctorid=request.GET['did']
        dname = request.GET['dname']
        gen = request.GET['gender']
        dob = request.GET['dob']
        mobnum = request.GET['mobnum']
        email = request.GET['email']
        dspl = request.GET['dspl']
        # dob = datetime.date(int(dob[5::]), int(dob[0:2]), int(dob[3:5]))
        print(dob)
        q = "update doctorregistration set doctorname='{0}',gender='{1}',dob='{2}',mobileno='{3}',emailid='{4}',specialization='{5}' where doctorid='{6}' ".format(
            dname, gen, dob, mobnum, email, dspl, doctorid)
        cmd.execute(q)
        db.commit()
        db.close()
        return JsonResponse({"result": True, }, safe=True)
    except Exception as e:
        print(e)
        return JsonResponse({"result": False, }, safe=False)


@xframe_options_exempt
def DeleteDoctorRegistration(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        doctorid = request.GET['doctorid']
        q = "delete from doctorregistration where doctorid={0}".format(doctorid)
        cmd.execute(q)
        db.commit()
        db.close()
        return JsonResponse({"result": True, }, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"result": False, }, safe=False)


@xframe_options_exempt
def EditDoctorRegistrationPicture(request):
    try:
        db, cmd = Pool.ConnectionPooling()
        doctorid = request.POST['doctorid']
        iconfile = request.FILES['icon']
        q = "update doctorregistration set icon='{0}' where doctorid={1}".format(iconfile.name,doctorid)
        cmd.execute(q)
        db.commit()
        F = open("d:/medassist/assets/" + iconfile.name, "wb")
        for chunk in iconfile.chunks():
            F.write(chunk)
        F.close()
        db.close()
        return JsonResponse({"result": True, }, safe=False)
    except Exception as e:
        print(e)
        return JsonResponse({"result": False, }, safe=False)
