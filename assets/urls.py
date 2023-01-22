"""medassist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from.import Specialization
from.import DoctorRegistration
from.import UserRegistration
from.import Questions
from.import SubQuestions
from.import AdminLogin
urlpatterns = [
    path('admin/', admin.site.urls),
    # Specialization------------------
    path('specialization/',Specialization.SpecializationInterface),
    path('specializationsubmit',Specialization.SpecializationSubmit),
    path('specializationdisplayall/',Specialization.SpecializationDisplayAll),
    path('specializationdisplayallJSON/', Specialization.SpecializationDisplayAllJSON),
    path('updatespecialization/', Specialization.UpdateSpecialization),
    path('deletespecialization/', Specialization.DeleteSpecialization),
    path('editspecializationpicture', Specialization.EditSpecializationPicture),

    # Doctor----------------------------
    path('doctorregistration/', DoctorRegistration.DoctorRegistrationInterface),
    path('doctorregistrationsubmit', DoctorRegistration.DoctorRegistrationSubmit),
    path('registrationdisplayall/',DoctorRegistration.DoctorRegistrationDisplayAll),
    path('updatedoctorregistration/',DoctorRegistration.UpdateDoctorRegistration),
    path('deleteregistration/', DoctorRegistration.DeleteDoctorRegistration),
    path('editdoctorregistrationpicture', DoctorRegistration.EditDoctorRegistrationPicture),

    # User Details------------------------
    path('userregistration/', UserRegistration.UserRegistrationInterface),
    path('userregistrationsubmit', UserRegistration.UserRegistrationSubmit),
    path('userregistrationdisplayall/', UserRegistration.UserRegistrationDisplayAll),

    #Questions....................
    path('questioninterface/', Questions.QuestionInterface),
    path('questionsubmit/', Questions.QuestionSubmit),
    path('questionjson/', Questions.QuestionJSON),


    #Sub-Questions................
    path('subquestioninterface/', SubQuestions.SubQuestionInterface),
    path('subquestionsubmit/', SubQuestions.SubQuestionSubmit),

    # Admin....................
    path('adminlogin/', AdminLogin.AdminLogin),
    path('dashboard', AdminLogin.CheckAdminLogin),



]
