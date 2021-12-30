from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main.models import Car, Reminder, Service, Contractor, Address, Course
from main import forms


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
            form = forms.CarModelForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('main:cars-list')
        else:
            form = forms.CarModelForm()
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
            form = forms.CarModelForm(request.POST, instance=car)

            if form.is_valid():
                form.save()
                return redirect('main:update-car', pk=pk)
        else:
            form = forms.CarModelForm(instance=car)
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
            form = forms.ReminderModelForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('main:reminders-list')
        else:
            form = forms.ReminderModelForm()
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
            form = forms.ReminderModelForm(request.POST, instance=reminder)

            if form.is_valid():
                form.save()
                return redirect('main:update-reminder', pk=pk)
        else:
            form = forms.ReminderModelForm(instance=reminder)
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
            form = forms.ServiceModelForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('main:services-list')
        else:
            form = forms.ServiceModelForm()
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
            form = forms.ServiceModelForm(request.POST, instance=service)

            if form.is_valid():
                form.save()
                return redirect('main:update-service', pk=pk)
        else:
            form = forms.ServiceModelForm(instance=service)
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
            form = forms.ContractorsModelForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                return redirect('main:contractors-list')
        else:
            form = forms.ContractorsModelForm()
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
            form = forms.ContractorsModelForm(
                request.POST, request.FILES, instance=contractor)

            if form.is_valid():
                form.save()
                return redirect('main:update-contractor', pk=pk)
        else:
            form = forms.ContractorsModelForm(instance=contractor)
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
def courses_list(request):
    if request.user.is_staff:
        courses = Course.objects.all()
    else:
        raise PermissionDenied

    context = {
        'courses': courses,
        'page_heading': 'Курсове'
    }

    return render(request, 'main/courses_list.html', context)


@login_required
def add_course(request):
    if request.user.is_staff:

        addresses = Address.objects.all()

        if request.method == 'POST':
            form = forms.CourseModelForm(request.POST)
            formset = forms.CourseAddressAddFormset(request.POST)

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
                                    address=address_input, contact_person=None, contact_phone=None, gps_coordinates=None)
                            else:
                                address_object = None
                        else:
                            address_object = address_object[0]

                        f.instance.address_obj = address_object
                        f.save()

                return redirect('main:courses-list')
        else:
            form = forms.CourseModelForm()
            formset = forms.CourseAddressAddFormset()
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
            form = forms.CourseModelForm(request.POST, instance=course)
            formset = forms.CourseAddressUpdateFormset(
                request.POST, instance=course)

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
                                        address=address_input, contact_person=None, contact_phone=None, gps_coordinates=None)
                                else:
                                    address_object = None
                            else:
                                address_object = address_object[0]

                            f.instance.address_obj = address_object
                            f.save()

                formset.save()
                return redirect('main:update-course', pk=pk)
        else:
            form = forms.CourseModelForm(instance=course)
            formset = forms.CourseAddressUpdateFormset(instance=course)

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


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Course
    success_url = reverse_lazy('main:courses-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def addresses_list(request):
    if request.user.is_staff:
        addresses = Address.objects.all()
    else:
        raise PermissionDenied

    context = {
        'addresses': addresses,
        'page_heading': 'Адреси'
    }

    return render(request, 'main/addresses_list.html', context)


@login_required
def add_address(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.AddressModelForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('main:addresses-list')
        else:
            form = forms.AddressModelForm()
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:add-address'),
        'page_heading': 'Добавяне на адрес'
    }

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_address(request, pk):
    if request.user.is_staff:
        address = get_object_or_404(Address, id=pk)

        if request.method == 'POST':
            form = forms.AddressModelForm(request.POST, instance=address)

            if form.is_valid():
                form.save()
                return redirect('main:update-address', pk=pk)
        else:
            form = forms.AddressModelForm(instance=address)
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:update-address', args=(pk,)),
        'page_heading': 'Редактиране на адрес'
    }

    return render(request, 'main/add_update_form.html', context)


class AddressDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Address
    success_url = reverse_lazy('main:addresses-list')

    def test_func(self):
        return self.request.user.is_staff
