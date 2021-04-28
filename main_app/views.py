from main_app.forms import WashingForm
from django.db import models
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# models
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Accessory, Car, Photo

import uuid
import boto3

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'mycarcollector'


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def cars_index(request):
    cars = Car.objects.filter(user=request.user)
    context = {'cars': cars}
    return render(request, 'cars/index.html', context)


@login_required
def cars_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    accessories_car_doesnt_have = Accessory.objects.exclude(
        id__in=car.accessories.all().values_list('id'))
    washing_form = WashingForm()
    context = {
        'car': car,
        'washing_form': washing_form,
        'accessories': accessories_car_doesnt_have
    }
    return render(request, 'cars/detail.html', context)


@login_required
def add_washing(request, car_id):
    form = WashingForm(request.POST)

    if form.is_valid():
        new_washing = form.save(commit=False)
        new_washing.car_id = car_id
        new_washing.save()
    return redirect('detail', car_id=car_id)


class CarCreate(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['nickname', 'make', 'model', 'year', 'color', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CarUpdate(LoginRequiredMixin, UpdateView):
    model = Car
    fields = ['nickname', 'make', 'model', 'year', 'color', 'description']


class CarDelete(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = '/cars/'


@login_required
def accessories_index(request):
    accessories = Accessory.objects.all()
    context = {'accessories': accessories}

    return render(request, 'accessory/index.html', context)


@login_required
def accessory_detail(request, accessory_id):
    accessory = Accessory.objects.get(id=accessory_id)
    context = {'accessory': accessory}
    return render(request, 'accessory/detail.html', context)


class Create_Accessory(LoginRequiredMixin, CreateView):
    model = Accessory
    fields = ['name']
    success_url = '/accessories/'


class Update_Accessory(LoginRequiredMixin, UpdateView):
    model = Accessory
    fields = '__all__'
    success_url = '/accessories/'


class Delete_Accessory(LoginRequiredMixin, DeleteView):
    model = Accessory
    success_url = '/accessories/'


@login_required
def assoc_accessory(request, car_id, accessory_id):
    # Note that you can pass a toy's id instead of the whole object
    Car.objects.get(id=car_id).accessories.add(accessory_id)
    return redirect('detail', car_id=car_id)


@login_required
def remove_accessory(request, car_id, accessory_id):
    Car.objects.get(id=car_id).accessories.remove(accessory_id)
    return redirect('detail', car_id=car_id)


@login_required
def add_photo(request, car_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, car_id=car_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', car_id=car_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
