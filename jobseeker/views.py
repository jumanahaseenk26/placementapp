from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.views.generic import View,CreateView,TemplateView,DetailView,UpdateView,ListView
# Create your views here.
from jobseeker.forms import *
from myapp.models import StudentProfile,Jobs,Applications

class SignupView(CreateView):
    template_name="jobseeker/register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy("signin")

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")


class StudentIndexView(ListView):
    template_name="jobseeker/index.html"
    context_object_name="data"
    model=Jobs
    def get_queryset(self):
        my_applications=Applications.objects.filter(student=self.request.user).values_list("job",flat=True)
        qs=Jobs.objects.exclude(id__in=my_applications).order_by("-created_date")
        return qs

class ProfileCreateView(CreateView):
    template_name="jobseeker/profile_add.html"
    form_class=ProfileForm
    success_url=reverse_lazy("seeker_index")
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
class ProfileDetailView(DetailView):
    template_name="jobseeker/profile_detail.html"
    context_object_name="data"
    model=StudentProfile

class ProfileEditView(UpdateView):
    template_name="jobseeker/profile_edit.html"
    form_class=ProfileForm
    model=StudentProfile
    success_url=reverse_lazy("seeker_index")

#class JobListView(ListView):
 #   template_name="jobseeker/job_list.html"
  #  context_object_name="jobs"
   # model=Jobs
    
class JobDetailView(DetailView):
    template_name="jobseeker/job_detail.html"
    model=Jobs
    context_object_name="data"

class ApplyJobView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        job_object=Jobs.objects.get(id=id)
        student_object=request.user
        Applications.objects.create(job=job_object,student=student_object)
        return redirect("seeker_index")
    
class ApplicationListView(ListView):
    template_name="jobseeker/application.html"
    model=Applications
    context_object_name="data"
    def get_queryset(self):
        qs=Applications.objects.filter(student=self.request.user)
        return qs
    
class JobSaveView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        job_obj=Jobs.objects.get(id=id)
        action=request.POST.get("action")
        if action=="save":
            request.user.profile.saved_jobs.add(job_obj)
        elif action=="unsave":
            request.user.profile.saved_jobs.remove(job_obj)
        return redirect("seeker_index")

class SavedJobsListView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.profile.saved_jobs.all()
        return render(request,"jobseeker/saved_jobs.html",{"data":qs})