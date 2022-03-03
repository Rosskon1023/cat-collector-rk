from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Cat, Toy, Photo
from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import boto3
import uuid

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'catcollector-phoenix-bucket-rk'


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def cats_index(request):
    cats = Cat.objects.filter(user = request.user)
    return render(request, 'cats/index.html', {'cats': cats})

@login_required
def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()

    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))

    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have
    })

@login_required
def add_feeding(request, cat_id):
    # 1) collect form input values
    form = FeedingForm(request.POST)
    # 2) validate input values
    if form.is_valid():
        # 3) save a copy of a new feeding instance in memory
        new_feeding = form.save(commit=False)
        # 4) attach a reference to the cat that owns the feeding 
        new_feeding.cat_id = cat_id
    # 5) save the new feeding to the database
    new_feeding.save()
    # 6) redirect the user back to the detail
    return redirect('detail', cat_id=cat_id)

@login_required
def assoc_toy(request, cat_id, toy_id):
    cat = Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

@login_required
def add_photo(request, cat_id):
    # collect the photo information from the form submission
    photo_file = request.FILES.get('photo-file')
    #use an if statement to see if the photo information is present or not
    #if photo present
    if photo_file:
        #initialize a reference to the s3 service from boto3
        s3 = boto3.client('s3')
        #create a unique name for the photo asset
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        #attempt to upload the photo asset to AWS S3
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            #Save a secure url to the AWS S3 hosted photo asset to the database
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, cat_id=cat_id)
            photo.save()
        #if upload is not successful
        except Exception as error:
            #print errors to the console
            print('*************************')
            print('An error occurred while uploading to S3')
            print(error)
            print('*************************')
        # return a response as a redirect to the client - redirecting to the detail page
    return redirect('detail', cat_id=cat_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid Sign up - Try Again'
    form = UserCreationForm()
    context = { 'form': form, 'error': error_message }
    return render(request, 'registration/signup.html', {'form': form})


class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    # fields = ('name', 'breed', 'age', 'description')
    fields = ('name','breed','description','age')
    # success_url = '/cats/'   This will work but it is not preferred 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ('name','breed', 'description', 'age')

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = '/cats/'

class ToyIndex(LoginRequiredMixin, ListView):
    model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = '__all__'

class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys/'

