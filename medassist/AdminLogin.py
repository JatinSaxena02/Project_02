from django.shortcuts import render,redirect
from . import Pool
from django.http import JsonResponse


def AdminLogin(request):
    return render(request,'AdminLogin.html',{'msg':''})
def CheckAdminLogin(request):
    try:
        db,cmd=Pool.ConnectionPooling()
        email=request.POST['email']
        password=request.POST['password']
        q = "select * from admins where emailid='{0}' and password='{1}'".format(email,password)
        cmd.execute(q)
        record = cmd.fetchone()
        if(record):
         request.session['admin']=record
         return render(request, 'Dashboard.html', {'msg':'','data':record})
        else:
         return render(request, 'AdminLogin.html', {'msg': "Invalid EmailId/Password"})

    except Exception as e:
        print(e)
        return render(request, 'AdminLogin.html', {'msg': 'Server Error'})



def AdminLogout(request):
    del request.session['admin']
    return redirect('/adminlogin')