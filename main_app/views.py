from main_app.forms import WashingForm
from django.db import models
from django.shortcuts import redirect, render

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


def cars_index(request):
    cars = Car.objects.all()
    context = {'cars': cars}
    return render(request, 'cars/index.html', context)


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


def add_washing(request, car_id):
    form = WashingForm(request.POST)

    if form.is_valid():
        new_washing = form.save(commit=False)
        new_washing.car_id = car_id
        new_washing.save()
    return redirect('detail', car_id=car_id)


class CarCreate(CreateView):
    model = Car
    fields = ['nickname', 'make', 'model', 'year', 'color', 'description']


class CarUpdate(UpdateView):
    model = Car
    fields = ['nickname', 'make', 'model', 'year', 'color', 'description']


class CarDelete(DeleteView):
    model = Car
    success_url = '/cars/'


def accessories_index(request):
    accessories = Accessory.objects.all()
    context = {'accessories': accessories}

    return render(request, 'accessory/index.html', context)


def accessory_detail(request, accessory_id):
    accessory = Accessory.objects.get(id=accessory_id)
    context = {'accessory': accessory}
    return render(request, 'accessory/detail.html', context)


class Create_Accessory(CreateView):
    model = Accessory
    fields = ['name']
    success_url = '/accessories/'


class Update_Accessory(UpdateView):
    model = Accessory
    fields = '__all__'
    success_url = '/accessories/'


class Delete_Accessory(DeleteView):
    model = Accessory
    success_url = '/accessories/'


def assoc_accessory(request, car_id, accessory_id):
    # Note that you can pass a toy's id instead of the whole object
    Car.objects.get(id=car_id).accessories.add(accessory_id)
    return redirect('detail', car_id=car_id)


def remove_accessory(request, car_id, accessory_id):
    Car.objects.get(id=car_id).accessories.remove(accessory_id)
    return redirect('detail', car_id=car_id)


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
