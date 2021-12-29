from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main.models import Car, Reminder, Service, Contractor, Address, Course
from main.forms import CarModelForm, ReminderModelForm, ServiceModelForm, ContractorsModelForm, CourseModelForm, CourseAddressAddFormset, CourseAddressUpdateFormset


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

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_car(request, pk):
    if request.user.is_staff:
        car = get_object_or_404(Car, id=pk)

        if request.method == 'POST':
            form = CarModelForm(request.POST, instance=car)

            if form.is_valid():
                form.save()
                return redirect('main:update-car', pk=pk)
        else:
            form = CarModelForm(instance=car)
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:update-car', args=(pk,)),
        'page_heading': 'Редактиране на автомобил'
    }

    return render(request, 'main/add_update_form.html', context)


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

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_reminder(request, pk):
    if request.user.is_staff:
        reminder = get_object_or_404(Reminder, id=pk)

        if request.method == 'POST':
            form = ReminderModelForm(request.POST, instance=reminder)

            if form.is_valid():
                form.save()
                return redirect('main:update-reminder', pk=pk)
        else:
            form = ReminderModelForm(instance=reminder)
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:update-reminder', args=(pk,)),
        'page_heading': 'Редактиране на напомняне'
    }

    return render(request, 'main/add_update_form.html', context)


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

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_service(request, pk):
    if request.user.is_staff:
        service = get_object_or_404(Service, id=pk)

        if request.method == 'POST':
            form = ServiceModelForm(request.POST, instance=service)

            if form.is_valid():
                form.save()
                return redirect('main:update-service', pk=pk)
        else:
            form = ServiceModelForm(instance=service)
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:update-service', args=(pk,)),
        'page_heading': 'Редактиране на техническо обслужване'
    }

    return render(request, 'main/add_update_form.html', context)


class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Service
    success_url = reverse_lazy('main:services-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def users_details_list(request):
    if request.user.is_staff:
        users = get_user_model().objects.filter(is_staff=False, is_active=True)
    else:
        raise PermissionDenied

    context = {
        'users': users,
        'page_heading': 'Документи на шофьори'
    }

    return render(request, 'main/users_details_list.html', context)


@login_required
def user_set_unactive(request, pk=None):
    if request.user.is_staff:
        if request.method == 'POST':
            user = get_object_or_404(get_user_model(), pk=pk)
            user.is_active = False
            user.save()

        return redirect('main:users-details-list')
    else:
        raise PermissionDenied


@login_required
def contractors_list(request):
    if request.user.is_staff:
        contractors = Contractor.objects.all()
    else:
        raise PermissionDenied

    context = {
        'contractors': contractors,
        'page_heading': 'Контрагенти'
    }

    return render(request, 'main/contractors_list.html', context)


@login_required
def add_contractor(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = ContractorsModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('main:contractors-list')
        else:
            form = ContractorsModelForm()
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:add-contractor'),
        'page_heading': 'Добавяне на контрагент'
    }

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_contractor(request, pk):
    if request.user.is_staff:
        contractor = get_object_or_404(Contractor, id=pk)

        if request.method == 'POST':
            form = ContractorsModelForm(
                request.POST, request.FILES, instance=contractor)

            if form.is_valid():
                form.save()
                return redirect('main:update-contractor', pk=pk)
        else:
            form = ContractorsModelForm(instance=contractor)
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:update-contractor', args=(pk,)),
        'page_heading': 'Редактиране на контрагент'
    }

    return render(request, 'main/add_update_form.html', context)


class ContractorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Contractor
    success_url = reverse_lazy('main:contractors-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def add_course(request):
    if request.user.is_staff:

        addresses = Address.objects.all()

        if request.method == 'POST':
            form = CourseModelForm(request.POST)
            formset = CourseAddressAddFormset(request.POST)

            if form.is_valid() and formset.is_valid():
                form_instance = form.save()

                for f in formset:
                    if f.is_valid():
                        f.instance.course = form_instance

                        address_input = f.cleaned_data.get('address_input')
                        save = f.cleaned_data.get('save')

                        address_object = Address.objects.filter(
                            address=address_input)

                        if not address_object:
                            if save:
                                address_object = Address.objects.create(
                                    address=address_input, contact_person=None, contact_phone=None, gps_coordinats=None)
                            else:
                                address_object = None
                        else:
                            address_object = address_object[0]

                        f.instance.address_obj = address_object
                        f.save()

                return redirect('main:add-course')
        else:
            form = CourseModelForm()
            formset = CourseAddressAddFormset()
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'formset': formset,
        'addresses': addresses,
        'url': reverse('main:add-course'),
        'page_heading': 'Добавяне на курс'
    }

    return render(request, 'main/add_course.html', context)


@login_required
def update_course(request, pk):
    if request.user.is_staff:

        addresses = Address.objects.all()
        course = get_object_or_404(Course, id=pk)

        if request.method == 'POST':
            form = CourseModelForm(request.POST, instance=course)
            formset = CourseAddressUpdateFormset(request.POST, instance=course)

            if form.is_valid() and formset.is_valid():
                form_instance = form.save()

                for f in formset:
                    if f.is_valid():
                        f.instance.course = form_instance

                        if 'address_input' in f.changed_data or 'save' in f.changed_data:
                            address_input = f.cleaned_data.get('address_input')
                            save = f.cleaned_data.get('save')

                            address_object = Address.objects.filter(
                                address=address_input)

                            if not address_object:
                                if save:
                                    address_object = Address.objects.create(
                                        address=address_input, contact_person=None, contact_phone=None, gps_coordinats=None)
                                else:
                                    address_object = None
                            else:
                                address_object = address_object[0]

                            f.instance.address_obj = address_object
                            f.save()

                formset.save()
                return redirect('main:update-course', pk=pk)
        else:
            form = CourseModelForm(instance=course)
            formset = CourseAddressUpdateFormset(instance=course)

        context = {
            'form': form,
            'formset': formset,
            'addresses': addresses,
            'url': reverse('main:update-course', args=(pk,)),
            'page_heading': 'Редактиране на курс'
        }

        return render(request, 'main/add_course.html', context)

    else:
        raise PermissionDenied
