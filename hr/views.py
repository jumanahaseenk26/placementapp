from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import View,FormView,TemplateView,CreateView,ListView,UpdateView,DetailView
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy

from myapp.models import Category,Jobs,Applications
from hr.forms import * 
# Create your views here.

class SigninView(FormView):
    template_name="login.html"
    form_class=LoginForm

    #def get(self,request,*args,**kwargs):
     #   form=LoginForm()
      #  return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr_obj=authenticate(request,username=uname,password=pwd)
            if usr_obj:
                login(request,usr_obj)
                print("success")
                if request.user.is_superuser:
                    return redirect("index")
                else:
                    return redirect("seeker_index")
        print("failed")
        return render(request,"login.html",{"form":form})
    
class DashboardView(TemplateView):
    template_name="index.html"

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
class CategoryListCreateView(CreateView,ListView):
    template_name="category.html"
    form_class=CategoryForm
    success_url=reverse_lazy("category")
    context_object_name="data"
    model=Category

class CategoryDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Category.objects.filter(id=id).delete()
        return redirect("category")
    
class JobCreateView(CreateView):
    template_name="job_add.html"
    form_class=JobForm
    success_url=reverse_lazy("index")

class JobListView(ListView):
    template_name="job_list.html"
    context_object_name="jobs"
    model=Jobs

    def get(self,request,*args,**kwargs):
        qs=Jobs.objects.all()

        if "status" in request.GET:
            value=request.GET.get("status")
            qs=qs.filter(status=value)
        return render(request,self.template_name,{"jobs":qs})

    #def get_queryset(self):
     #   return Jobs.objects.filter(status=True)

class JobDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Jobs.objects.filter(id=id).delete()
        return redirect("index")
    
class JobUpdateView(UpdateView):
    form_class=JobChangeForm
    template_name="job_edit.html"
    model=Jobs
    success_url=reverse_lazy("index")

#localhost8000/jobs/<int:pk>/applications
    
class JobApplicationListView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        job_obj=Jobs.objects.get(id=id)
        qs=Applications.objects.filter(job=job_obj)
        return render(request,"applications.html",{"data":qs})

class ApplicationDetailView(DetailView):
    template_name="application_detail.html"
    context_object_name="application"
    model=Applications

