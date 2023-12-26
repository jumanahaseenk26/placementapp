from django import forms
from myapp.models import Category,Jobs

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class CategoryForm(forms.ModelForm):
    class Meta:
        fields=["name"]
        model=Category

class JobForm(forms.ModelForm):
    class Meta:
        model=Jobs
        exclude=("status",)
        #fields="__all__"
        widgets={
            "category":forms.Select(attrs={"class":"form-control form-select"}),
            "last_date":forms.DateInput(attrs={"class":"form-control","type":"date"}),
            "job_type":forms.Select(attrs={"class":"form-control form-select"}),

        }

class JobChangeForm(forms.ModelForm):
    class Meta:
        model=Jobs
        fields="__all__"
        widgets={
            "category":forms.Select(attrs={"class":"form-control form-select"}),
            "last_date":forms.DateInput(attrs={"class":"form-control","type":"date"})
        }