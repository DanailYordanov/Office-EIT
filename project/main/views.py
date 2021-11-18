from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main.models import Car, Reminder, Service
from main.forms import CarModelForm, ReminderModelForm, ServiceModelForm


@login_required
def cars_list(request):
    if request.user.is_staff:
        cars = Car.objects.all()
    else:
        raise PermissionDenied

    context = {
        'cars': cars,
        'page_heading': 'Автомобили'
    }

    return render(request, 'main/cars_list.html', context)


@login_required
def add_car(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CarModelForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main:cars-list')
        else:
            form = CarModelForm()
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:add-car'),
        'page_heading': 'Добавяне на автомобил'
    }

    return render(request, 'main/add_update_car.html', context)


@login_required
def update_car(request, pk):
    if request.user.is_staff:
        car = get_object_or_404(Car, id=pk)

        if request.method == 'POST':
            form = CarModelForm(request.POST, instance=car)

            if form.is_valid():
                form.save()
                return redirect('main:cars-list')
        else:
            form = CarModelForm(instance=car)
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:update-car', args=(pk,)),
        'page_heading': 'Редактиране на автомобил'
    }

    return render(request, 'main/add_update_car.html', context)


class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Car
    success_url = reverse_lazy('main:cars-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def reminders_list(request):
    if request.user.is_staff:
        reminders = Reminder.objects.all()
    else:
        raise PermissionDenied

    context = {
        'reminders': reminders,
        'page_heading': 'Напомняния'
    }

    return render(request, 'main/reminders_list.html', context)


@login_required
def add_reminder(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = ReminderModelForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main:reminders-list')
        else:
            form = ReminderModelForm()
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:add-reminder'),
        'page_heading': 'Добавяне на напомняне'
    }

    return render(request, 'main/add_update_reminder.html', context)


@login_required
def update_reminder(request, pk):
    if request.user.is_staff:
        reminder = get_object_or_404(Reminder, id=pk)

        if request.method == 'POST':
            form = ReminderModelForm(request.POST, instance=reminder)

            if form.is_valid():
                form.save()
                return redirect('main:reminders-list')
        else:
            form = ReminderModelForm(instance=reminder)
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:update-reminder', args=(pk,)),
        'page_heading': 'Редактиране на напомняне'
    }

    return render(request, 'main/add_update_reminder.html', context)


class ReminderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Reminder
    success_url = reverse_lazy('main:reminders-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def services_list(request):
    if request.user.is_staff:
        services = Service.objects.all()
    else:
        raise PermissionDenied

    context = {
        'services': services,
        'page_heading': 'Технически обслужвания'
    }

    return render(request, 'main/services_list.html', context)


@login_required
def add_service(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = ServiceModelForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main:services-list')
        else:
            form = ServiceModelForm()
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:add-service'),
        'page_heading': 'Добавяне на техническо обслужване'
    }

    return render(request, 'main/add_update_service.html', context)


@login_required
def update_service(request, pk):
    if request.user.is_staff:
        service = get_object_or_404(Service, id=pk)

        if request.method == 'POST':
            form = ServiceModelForm(request.POST, instance=service)

            if form.is_valid():
                form.save()
                return redirect('main:services-list')
        else:
            form = ServiceModelForm(instance=service)
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:update-service', args=(pk,)),
        'page_heading': 'Редактиране на техническо обслужване'
    }

    return render(request, 'main/add_update_service.html', context)


class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Service
    success_url = reverse_lazy('main:services-list')

    def test_func(self):
        return self.request.user.is_staff
