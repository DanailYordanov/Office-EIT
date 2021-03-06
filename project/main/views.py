import os
import shutil
import secrets
from django.conf import settings
from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from django.utils import timezone, dateformat, formats
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from pyVies import api
from openpyxl import load_workbook
from django_select2.views import AutoResponseView
from main import models
from main import forms
from . import xlsx_populate


@login_required
def cars_list(request):
    if request.user.is_staff:
        cars = models.Car.objects.all()
    else:
        raise PermissionDenied

    context = {
        'cars': cars,
        'page_heading': 'Автомобили'
    }

    return render(request, 'main/lists/cars_list.html', context)


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
        car = get_object_or_404(models.Car, id=pk)

        if request.method == 'POST':
            form = forms.CarModelForm(request.POST, instance=car)

            if form.is_valid():
                form.save()
                return redirect('main:cars-list')
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

    model = models.Car
    success_url = reverse_lazy('main:cars-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def reminders_list(request):
    if request.user.is_staff:
        reminders = models.Reminder.objects.all()
    else:
        raise PermissionDenied

    context = {
        'reminders': reminders,
        'page_heading': 'Напомняния'
    }

    return render(request, 'main/lists/reminders_list.html', context)


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
        reminder = get_object_or_404(models.Reminder, id=pk)

        if request.method == 'POST':
            form = forms.ReminderModelForm(request.POST, instance=reminder)

            if form.is_valid():
                form.save()
                return redirect('main:reminders-list')
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

    model = models.Reminder
    success_url = reverse_lazy('main:reminders-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def services_list(request):
    if request.user.is_staff:
        services = models.Service.objects.all()
    else:
        raise PermissionDenied

    context = {
        'services': services,
        'page_heading': 'Технически обслужвания'
    }

    return render(request, 'main/lists/services_list.html', context)


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
        service = get_object_or_404(models.Service, id=pk)

        if request.method == 'POST':
            form = forms.ServiceModelForm(request.POST, instance=service)

            if form.is_valid():
                form.save()
                return redirect('main:services-list')
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

    model = models.Service
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

    return render(request, 'main/lists/users_details_list.html', context)


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
        contractors = models.Contractor.objects.all()
    else:
        raise PermissionDenied

    context = {
        'contractors': contractors,
        'page_heading': 'Контрагенти'
    }

    return render(request, 'main/lists/contractors_list.html', context)


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
        contractor = get_object_or_404(models.Contractor, id=pk)

        if request.method == 'POST':
            form = forms.ContractorsModelForm(
                request.POST, request.FILES, instance=contractor)

            if form.is_valid():
                form.save()
                return redirect('main:contractors-list')
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

    model = models.Contractor
    success_url = reverse_lazy('main:contractors-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def populate_vat_info(request):
    if request.method == 'POST':
        bulstat = request.POST.get('bulstat')

        data = {
            'name': None,
            'city': None,
            'address': None,
            'postal_code': None
        }

        if bulstat != '':
            try:
                vies = api.Vies()
                result = vies.request(bulstat, extended_info=True)

                data['name'] = result['traderName']
                data['city'] = result['traderCity']
                data['address'] = result['traderAddress']
                data['postal_code'] = result['traderPostcode']
            except Exception:
                pass

        return JsonResponse(data)
    else:
        raise PermissionDenied


@login_required
def courses_list(request):
    if request.user.is_staff:
        courses = models.Course.objects.all()
    else:
        courses = models.Course.objects.filter(
            driver=request.user)

    context = {
        'courses': courses,
        'page_heading': 'Курсове'
    }

    return render(request, 'main/lists/courses_list.html', context)


@login_required
def add_course(request, pk=None):
    if request.user.is_staff:

        initial_form = dict()
        initial_formset = list()

        if pk:
            initial_course = get_object_or_404(models.Course, id=pk)

            initial_form['driver'] = initial_course.driver.all()
            initial_form['car'] = initial_course.car
            initial_form['company'] = initial_course.company
            initial_form['contractor'] = initial_course.contractor
            initial_form['bank'] = initial_course.bank
            initial_form['from_to'] = initial_course.from_to
            initial_form['cargo_type'] = initial_course.cargo_type
            initial_form['export'] = initial_course.export
            initial_form['contact_person'] = initial_course.contact_person
            initial_form['other_conditions'] = initial_course.other_conditions

            medical_examination = initial_course.medical_examinations.all().first()
            technical_inspection = initial_course.technical_inspections.all().first()

            if medical_examination:
                initial_form['medical_examination_perpetrator'] = medical_examination.perpetrator

            if technical_inspection:
                initial_form['technical_inspection_perpetrator'] = technical_inspection.perpetrator

            for address in initial_course.addresses.all():
                initial_formset.append(
                    {
                        'load_type': address.load_type,
                        'address': address.address
                    }
                )

            forms.CourseAddressAddFormset.extra = len(initial_formset)

        else:
            medical_examination_perpetrator = models.MedicalExaminationPerpetrator.objects.all().last()
            initial_form['medical_examination_perpetrator'] = medical_examination_perpetrator

            technical_inspection_perpetrator = models.TechnicalInspectionPerpetrator.objects.all().last()
            initial_form['technical_inspection_perpetrator'] = technical_inspection_perpetrator

        if request.method == 'POST':
            form = forms.CourseModelForm(
                request.POST, request.FILES, initial=initial_form)
            formset = forms.CourseAddressAddFormset(
                request.POST, initial=initial_formset)

            if form.is_valid() and formset.is_valid():
                form_instance = form.save()

                for f in formset:
                    if f.is_valid():
                        f.instance.course = form_instance
                        f.save()

                if form_instance.export:
                    from_date = next((
                        form for form in formset.cleaned_data if form['load_type'] == 'Адрес на товарене'), None
                    )

                    if from_date:
                        from_date = from_date['date']

                    to_date = form.cleaned_data['trip_order_to_date']

                    destination = (
                        form_instance.from_to.from_to.split('до')[-1]).strip().capitalize()

                    medical_examination_perpetrator = form.cleaned_data[
                        'medical_examination_perpetrator']

                    technical_inspection_perpetrator = form.cleaned_data[
                        'technical_inspection_perpetrator']

                    for driver in form.cleaned_data['driver']:
                        models.Instruction.objects.create(
                            creator=request.user,
                            course=form_instance,
                            driver=driver,
                        )

                        models.TripOrder.objects.create(
                            creator=request.user,
                            driver=driver,
                            course=form_instance,
                            destination=destination,
                            from_date=from_date,
                            to_date=to_date
                        )

                        models.CourseMedicalExamination.objects.create(
                            course=form_instance,
                            driver=driver,
                            perpetrator=medical_examination_perpetrator
                        )

                        models.CourseTechnicalInspection.objects.create(
                            course=form_instance,
                            driver=driver,
                            perpetrator=technical_inspection_perpetrator
                        )

                return redirect('main:add-course-invoice', pk=form_instance.id)
        else:
            form = forms.CourseModelForm(initial=initial_form)
            formset = forms.CourseAddressAddFormset(initial=initial_formset)
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'formset': formset,
        'url': reverse('main:add-course'),
        'page_heading': 'Добавяне на курс'
    }

    return render(request, 'main/add_update_course.html', context)


@login_required
def update_course(request, pk):
    if request.user.is_staff:
        course = get_object_or_404(models.Course, id=pk)

        if request.method == 'POST':
            form = forms.CourseModelForm(
                request.POST, request.FILES, instance=course)
            formset = forms.CourseAddressUpdateFormset(
                request.POST, instance=course)

            if form.is_valid() and formset.is_valid():
                form_instance = form.save()

                for f in formset:
                    if f.is_valid():
                        f.instance.course = form_instance
                        f.save()

                formset.save()

                if form_instance.export:
                    from_date = next((
                        form for form in formset.cleaned_data if form['load_type'] == 'Адрес на товарене'), None
                    )

                    if from_date:
                        from_date = from_date['date']

                    to_date = form.cleaned_data['trip_order_to_date']

                    destination = (
                        form_instance.from_to.from_to.split('до')[-1]).strip().capitalize()

                    medical_examination_perpetrator = form.cleaned_data[
                        'medical_examination_perpetrator']

                    technical_inspection_perpetrator = form.cleaned_data[
                        'technical_inspection_perpetrator']

                    trip_orders = form_instance.trip_orders.all()
                    instructions = form_instance.instructions.all()
                    course_medical_examinations = form_instance.medical_examinations.all()
                    course_technical_inspections = form_instance.technical_inspections.all()

                    if not instructions:
                        for driver in form.cleaned_data['driver']:
                            models.Instruction.objects.create(
                                creator=request.user,
                                course=form_instance,
                                driver=driver,
                            )

                    if not trip_orders:
                        for driver in form.cleaned_data['driver']:
                            models.TripOrder.objects.create(
                                creator=request.user,
                                driver=driver,
                                course=form_instance,
                                destination=destination,
                                from_date=from_date,
                                to_date=to_date
                            )

                    if not course_medical_examinations:
                        for driver in form.cleaned_data['driver']:
                            models.CourseMedicalExamination.objects.create(
                                course=form_instance,
                                driver=driver,
                                perpetrator=medical_examination_perpetrator
                            )

                    if not course_technical_inspections:
                        for driver in form.cleaned_data['driver']:
                            models.CourseTechnicalInspection.objects.create(
                                course=form_instance,
                                driver=driver,
                                perpetrator=technical_inspection_perpetrator
                            )

                    else:
                        if 'trip_order_to_date' in form.changed_data:
                            for trip_order in trip_orders:
                                trip_order.to_date = to_date
                                trip_order.save()

                        if 'from_to' in form.changed_data:
                            for trip_order in trip_orders:
                                trip_order.destination = destination
                                trip_order.save()

                        if 'medical_examination_perpetrator' in form.changed_data:
                            for medical_examination in course_medical_examinations:
                                medical_examination.perpetrator = form.cleaned_data[
                                    'medical_examination_perpetrator']
                                medical_examination.save()

                        if 'technical_inspection_perpetrator' in form.changed_data:
                            for technical_inspection in course_technical_inspections:
                                technical_inspection.perpetrator = form.cleaned_data[
                                    'technical_inspection_perpetrator']
                                technical_inspection.save()

                        if formset.has_changed():
                            for f in formset:
                                if 'date' in f.changed_data and f.cleaned_data['load_type'] == 'Адрес на товарене':
                                    for trip_order in trip_orders:
                                        trip_order.from_date = f.cleaned_data['date']
                                        trip_order.save()
                                        break

                        if 'driver' in form.changed_data:
                            while len(form.cleaned_data['driver']) > len(form_instance.trip_orders.all()):
                                trip_order = trip_orders.first()

                                if trip_order:
                                    trip_order.pk = None
                                    trip_order.save()

                            while len(form.cleaned_data['driver']) > len(form_instance.instructions.all()):
                                instruction = instructions.first()

                                if instruction:
                                    instruction.pk = None
                                    instruction.save()

                            while len(form.cleaned_data['driver']) > len(form_instance.medical_examinations.all()):
                                medical_examination = course_medical_examinations.first()

                                if medical_examination:
                                    medical_examination.pk = None
                                    medical_examination.save()

                            while len(form.cleaned_data['driver']) > len(form_instance.technical_inspections.all()):
                                technical_inspection = course_technical_inspections.first()

                                if technical_inspection:
                                    technical_inspection.pk = None
                                    technical_inspection.save()

                            trip_orders = form_instance.trip_orders.all()
                            instructions = form_instance.instructions.all()
                            course_medical_examinations = form_instance.medical_examinations.all()
                            course_technical_inspections = form_instance.technical_inspections.all()

                            for i in range(0, len(form.cleaned_data['driver'])):
                                trip_order = trip_orders[i]
                                instruction = instructions[i]
                                medical_examination = course_medical_examinations[i]
                                technical_inspection = course_technical_inspections[i]

                                trip_order.driver = form.cleaned_data['driver'][i]
                                trip_order.save()

                                instruction.driver = form.cleaned_data['driver'][i]
                                instruction.save()

                                medical_examination.driver = form.cleaned_data['driver'][i]
                                medical_examination.save()

                                technical_inspection.driver = form.cleaned_data['driver'][i]
                                technical_inspection.save()

                return redirect('main:courses-list')
        else:
            form = forms.CourseModelForm(instance=course)
            formset = forms.CourseAddressUpdateFormset(instance=course)

        context = {
            'form': form,
            'formset': formset,
            'url': reverse('main:update-course', args=(pk,)),
            'page_heading': 'Редактиране на курс'
        }

        return render(request, 'main/add_update_course.html', context)
    else:
        raise PermissionDenied


@login_required
def course_information(request, pk):
    course = get_object_or_404(models.Course, id=pk)
    expenses = models.Expense.objects.filter(course=course)
    addresses = models.CourseAddress.objects.filter(course=course)

    context = {
        'course': course,
        'expenses': expenses,
        'addresses': addresses,
        'page_heading': 'Информация за курс'
    }

    return render(request, 'main/course_information.html', context)


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = models.Course
    success_url = reverse_lazy('main:courses-list')

    def test_func(self):
        return self.request.user.is_staff


def load_contractor_reminder(request):
    if request.method == 'POST':
        contractor_id = request.POST.get('contractor_id')

        data = {
            'cmr_reminder': None,
            'license_reminder': None
        }

        if contractor_id != '':
            contractor = get_object_or_404(
                models.Contractor, id=int(contractor_id))

            if contractor.cmr_expiration_date:
                if contractor.cmr_expiration_date <= (timezone.now().date() + timezone.timedelta(days=5)):
                    data['cmr_reminder'] = f'ЧМР Застраховката изтича на {contractor.cmr_expiration_date}'

            if contractor.license_expiration_date:
                if contractor.license_expiration_date <= (timezone.now().date() + timezone.timedelta(days=5)):
                    data['license_reminder'] = f'Лиценза изтича на {contractor.license_expiration_date}'

        return JsonResponse(data)
    else:
        raise PermissionDenied


@login_required
def addresses_list(request):
    if request.user.is_staff:
        addresses = models.Address.objects.all()
    else:
        raise PermissionDenied

    context = {
        'addresses': addresses,
        'page_heading': 'Адреси'
    }

    return render(request, 'main/lists/addresses_list.html', context)


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
        address = get_object_or_404(models.Address, id=pk)

        if request.method == 'POST':
            form = forms.AddressModelForm(request.POST, instance=address)

            if form.is_valid():
                form.save()
                return redirect('main:addresses-list')
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

    model = models.Address
    success_url = reverse_lazy('main:addresses-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def add_expense(request, pk):
    course = get_object_or_404(models.Course, id=pk)

    if request.method == 'POST':
        form = forms.ExpenseModelForm(request.POST)

        if form.is_valid():
            form.instance.course = course
            form.save()
            return redirect('main:course-information', pk=pk)
    else:
        form = forms.ExpenseModelForm()

    context = {
        'form': form,
        'url': reverse('main:add-expense', args=(pk,)),
        'page_heading': 'Добавяне на разход'
    }

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_expense(request, pk):
    expense = get_object_or_404(models.Expense, id=pk)

    if request.method == 'POST':
        form = forms.ExpenseModelForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            return redirect('main:course-information', pk=expense.course.id)
    else:
        form = forms.ExpenseModelForm(instance=expense)

    context = {
        'form': form,
        'url': reverse('main:update-expense', args=(pk,)),
        'page_heading': 'Редактиране на разход'
    }

    return render(request, 'main/add_update_form.html', context)


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):

    model = models.Expense

    def get_success_url(self):
        return reverse_lazy('main:course-information', kwargs={'pk': self.kwargs['course_pk']})


@login_required
def trip_orders_list(request):
    if request.user.is_staff:
        trip_orders = models.TripOrder.objects.all()
    else:
        raise PermissionDenied

    context = {
        'trip_orders': trip_orders,
        'page_heading': 'Командировъчни заповеди'
    }

    return render(request, 'main/lists/trip_orders_list.html', context)


@login_required
def add_trip_order(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.TripOrderModelForm(request.POST)

            if form.is_valid():
                form.instance.creator = request.user
                form.save()

                return redirect('main:trip-orders-list')
        else:
            form = forms.TripOrderModelForm()
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:add-trip-order'),
        'page_heading': 'Добавяне на командировъчна заповед'
    }

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_trip_order(request, pk):
    trip_order = get_object_or_404(models.TripOrder, id=pk)

    if request.method == 'POST':
        form = forms.TripOrderModelForm(request.POST, instance=trip_order)

        if form.is_valid():
            form.save()
            return redirect('main:trip-orders-list')
    else:
        form = forms.TripOrderModelForm(instance=trip_order)

    context = {
        'form': form,
        'url': reverse('main:update-trip-order', args=(pk,)),
        'page_heading': 'Редактиране на командировъчна заповед'
    }

    return render(request, 'main/add_update_form.html', context)


class TripOrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = models.TripOrder
    success_url = reverse_lazy('main:trip-orders-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def trip_order_xlsx(request, pk):
    if request.user.is_staff:
        trip_order = get_object_or_404(models.TripOrder, id=pk)

        unique_token = secrets.token_hex(32)

        xlsx_path = os.path.join(
            settings.BASE_DIR, 'main/xlsx_files/trip_order.xlsx')

        unique_xlsx_path = os.path.join(
            settings.BASE_DIR, f'main/xlsx_files/trip_order_{unique_token}.xlsx')

        shutil.copy(xlsx_path, unique_xlsx_path)

        wb = load_workbook(filename=unique_xlsx_path)
        ws = wb['trip_order']

        xlsx_populate.trip_order_xlsx_populate(ws, trip_order)

        ws = wb['expenses']

        xlsx_populate.trip_order_expenses_xlsx_populate(ws, trip_order)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Trip Order {trip_order.number}.xlsx"'

        wb.save(response)

        os.remove(unique_xlsx_path)

        return response
    else:
        raise PermissionDenied


@login_required
def load_dates(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')

        data = {
            'from_date': None,
            'to_date': None
        }

        if course_id != '':
            course_addresses = models.CourseAddress.objects.filter(
                course__id=int(course_id))

            from_date = course_addresses.filter(
                load_type='Адрес на товарене').order_by('date')
            to_date = course_addresses.filter(
                load_type='Адрес на разтоварване').order_by('date')

            if (from_date):
                data['from_date'] = from_date.first().date

            if (to_date):
                data['to_date'] = to_date.last().date

        return JsonResponse(data)
    else:
        raise PermissionDenied


@login_required
def expense_orders_list(request):
    if request.user.is_staff:
        expense_orders = models.ExpenseOrder.objects.all()
    else:
        raise PermissionDenied

    context = {
        'expense_orders': expense_orders,
        'page_heading': 'Разходни ордери'
    }

    return render(request, 'main/lists/expense_orders_list.html', context)


@login_required
def add_expense_order(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.ExpenseOrderModelForm(request.POST)

            if form.is_valid():
                form.instance.creator = request.user
                form.save()

                return redirect('main:expense-orders-list')
        else:
            form = forms.ExpenseOrderModelForm()

        context = {
            'form': form,
            'url': reverse('main:add-expense-order'),
            'page_heading': 'Добавяне на разходен ордер'
        }

        return render(request, 'main/add_update_form.html', context)
    else:
        raise PermissionDenied


@login_required
def update_expense_order(request, pk):
    if request.user.is_staff:
        expense_order = get_object_or_404(models.ExpenseOrder, id=pk)

        if request.method == 'POST':
            form = forms.ExpenseOrderModelForm(
                request.POST, instance=expense_order)

            if form.is_valid():
                form.save()
                return redirect('main:expense-orders-list')
        else:
            form = forms.ExpenseOrderModelForm(instance=expense_order)

        context = {
            'form': form,
            'url': reverse('main:update-expense-order', args=(pk,)),
            'page_heading': 'Редактиране на разходен ордер'
        }

        return render(request, 'main/add_update_form.html', context)
    else:
        raise PermissionDenied


class ExpenseOrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = models.ExpenseOrder
    success_url = reverse_lazy('main:expense-orders-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def expense_order_xlsx(request, pk):
    if request.user.is_staff:
        expense_order = get_object_or_404(models.ExpenseOrder, id=pk)

        unique_token = secrets.token_hex(32)

        xlsx_path = os.path.join(
            settings.BASE_DIR, 'main/xlsx_files/expense_order.xlsx')

        unique_xlsx_path = os.path.join(
            settings.BASE_DIR, f'main/xlsx_files/expense_order_{unique_token}.xlsx')

        shutil.copy(xlsx_path, unique_xlsx_path)

        wb = load_workbook(filename=unique_xlsx_path)
        ws = wb.active

        xlsx_populate.expense_order_xlsx_populate(ws, expense_order)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Expense Order {expense_order.number}.xlsx"'

        wb.save(response)

        os.remove(unique_xlsx_path)

        return response
    else:
        raise PermissionDenied


@login_required
def course_invoices_list(request):
    if request.user.is_staff:
        course_invoices = models.CourseInvoice.objects.all()
    else:
        raise PermissionDenied

    context = {
        'course_invoices': course_invoices,
        'page_heading': 'Фактури за курсове'
    }

    return render(request, 'main/lists/course_invoices_list.html', context)


@login_required
def add_course_invoice(request, pk=None):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.CourseInvoiceModelForm(request.POST)

            if form.is_valid():
                form.instance.creator = request.user
                form.save()

                return redirect('main:course-invoices-list')
        else:
            initial_data = dict()

            if pk:
                initial_data['course'] = get_object_or_404(
                    models.Course, pk=pk)

            form = forms.CourseInvoiceModelForm(initial=initial_data)
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:add-course-invoice'),
        'page_heading': 'Добавяне на фактура за курс'
    }

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_course_invoice(request, pk):
    course_invoice = get_object_or_404(models.CourseInvoice, id=pk)

    if request.method == 'POST':
        form = forms.CourseInvoiceModelForm(
            request.POST, instance=course_invoice)

        if form.is_valid():
            form.save()
            return redirect('main:course-invoices-list')
    else:
        form = forms.CourseInvoiceModelForm(instance=course_invoice)

    context = {
        'form': form,
        'url': reverse('main:update-course-invoice', args=(pk,)),
        'page_heading': 'Редактиране на фактура за курс'
    }

    return render(request, 'main/add_update_form.html', context)


class CourseInvoiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = models.CourseInvoice
    success_url = reverse_lazy('main:course-invoices-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def course_invoice_xlsx(request, pk):
    if request.user.is_staff:
        course_invoice = get_object_or_404(models.CourseInvoice, id=pk)

        unique_token = secrets.token_hex(32)

        xlsx_path = os.path.join(
            settings.BASE_DIR, 'main/xlsx_files/course_invoice.xlsx')

        unique_xlsx_path = os.path.join(
            settings.BASE_DIR, f'main/xlsx_files/course_invoice_{unique_token}.xlsx')

        shutil.copy(xlsx_path, unique_xlsx_path)

        wb = load_workbook(filename=unique_xlsx_path)
        ws = wb['original']

        xlsx_populate.course_invoice_xlsx_populate(ws, course_invoice)

        if course_invoice.course.export:
            ws = wb['translated']

            xlsx_populate.course_invoice_translated_xlsx_populate(
                ws, course_invoice)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Course Invoice {course_invoice.course.number}.xlsx"'

        wb.save(response)

        os.remove(unique_xlsx_path)

        return response
    else:
        raise PermissionDenied


@login_required
def companies_list(request):
    if request.user.is_staff:
        companies = models.Company.objects.all()
    else:
        raise PermissionDenied

    context = {
        'companies': companies,
        'page_heading': 'Фирми'
    }

    return render(request, 'main/lists/companies_list.html', context)


@login_required
def add_company(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.CompanyModelForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('main:companies-list')
        else:
            form = forms.CompanyModelForm()
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:add-company'),
        'page_heading': 'Добавяне на фирма'
    }

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_company(request, pk):
    company = get_object_or_404(models.Company, id=pk)

    if request.method == 'POST':
        form = forms.CompanyModelForm(
            request.POST, instance=company)

        if form.is_valid():
            form.save()
            return redirect('main:companies-list')
    else:
        form = forms.CompanyModelForm(instance=company)

    context = {
        'form': form,
        'url': reverse('main:update-company', args=(pk,)),
        'page_heading': 'Редактиране на фирма'
    }

    return render(request, 'main/add_update_form.html', context)


class CompanyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = models.Company
    success_url = reverse_lazy('main:companies-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def banks_list(request):
    if request.user.is_staff:
        banks = models.Bank.objects.all()
    else:
        raise PermissionDenied

    context = {
        'banks': banks,
        'page_heading': 'Банки'
    }

    return render(request, 'main/lists/banks_list.html', context)


@login_required
def add_bank(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.BankModelForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('main:banks-list')
        else:
            form = forms.BankModelForm()
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:add-bank'),
        'page_heading': 'Добавяне на банка'
    }

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_bank(request, pk):
    bank = get_object_or_404(models.Bank, id=pk)

    if request.method == 'POST':
        form = forms.BankModelForm(
            request.POST, instance=bank)

        if form.is_valid():
            form.save()
            return redirect('main:banks-list')
    else:
        form = forms.BankModelForm(instance=bank)

    context = {
        'form': form,
        'url': reverse('main:update-bank', args=(pk,)),
        'page_heading': 'Редактиране на банка'
    }

    return render(request, 'main/add_update_form.html', context)


class BankDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = models.Bank
    success_url = reverse_lazy('main:banks-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def instructions_list(request):
    if request.user.is_staff:
        instructions = models.Instruction.objects.all()
    else:
        raise PermissionDenied

    context = {
        'instructions': instructions,
        'page_heading': 'Инструкции'
    }

    return render(request, 'main/lists/instructions_list.html', context)


@login_required
def add_instruction(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.InstructionModelForm(request.POST)

            if form.is_valid():
                form.instance.creator = request.user
                form.save()

                return redirect('main:instructions-list')
        else:
            form = forms.InstructionModelForm()
    else:
        raise PermissionDenied

    context = {
        'form': form,
        'url': reverse('main:add-instruction'),
        'page_heading': 'Добавяне на инструкция'
    }

    return render(request, 'main/add_update_form.html', context)


@login_required
def update_instruction(request, pk):
    instruction = get_object_or_404(models.Instruction, id=pk)

    if request.method == 'POST':
        form = forms.InstructionModelForm(
            request.POST, instance=instruction)

        if form.is_valid():
            form.save()
            return redirect('main:instructions-list')
    else:
        form = forms.InstructionModelForm(instance=instruction)

    context = {
        'form': form,
        'url': reverse('main:update-instruction', args=(pk,)),
        'page_heading': 'Редактиране на инструкция'
    }

    return render(request, 'main/add_update_form.html', context)


class InstructionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = models.Instruction
    success_url = reverse_lazy('main:instructions-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def instruction_xlsx(request, pk):
    if request.user.is_staff:
        instruction = get_object_or_404(models.Instruction, id=pk)

        unique_token = secrets.token_hex(32)

        xlsx_path = os.path.join(
            settings.BASE_DIR, 'main/xlsx_files/instruction.xlsx')

        unique_xlsx_path = os.path.join(
            settings.BASE_DIR, f'main/xlsx_files/instruction_{unique_token}.xlsx')

        shutil.copy(xlsx_path, unique_xlsx_path)

        wb = load_workbook(filename=unique_xlsx_path)
        ws = wb.active

        xlsx_populate.instruction_xlsx_populate(ws, instruction)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Instruction {instruction.number}.xlsx"'

        wb.save(response)

        os.remove(unique_xlsx_path)

        return response
    else:
        raise PermissionDenied


def receipt_letter_xlsx(course):
    unique_token = secrets.token_hex(32)

    xlsx_path = os.path.join(
        settings.BASE_DIR, 'main/xlsx_files/receipt_letter.xlsx')

    unique_xlsx_path = os.path.join(
        settings.BASE_DIR, f'main/xlsx_files/receipt_letter_{unique_token}.xlsx')

    shutil.copy(xlsx_path, unique_xlsx_path)

    wb = load_workbook(filename=unique_xlsx_path)
    ws = wb.active

    xlsx_populate.receipt_letter_xlsx_populate(ws, course)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="Receipt Letter.xlsx"'

    wb.save(response)

    os.remove(unique_xlsx_path)

    return response


def official_notices_xlsx(course):
    medical_examinations = course.medical_examinations.all()
    technical_inspections = course.technical_inspections.all()

    unique_token = secrets.token_hex(32)

    xlsx_path = os.path.join(
        settings.BASE_DIR, 'main/xlsx_files/official_notices.xlsx')

    unique_xlsx_path = os.path.join(
        settings.BASE_DIR, f'main/xlsx_files/official_notices_{unique_token}.xlsx')

    shutil.copy(xlsx_path, unique_xlsx_path)

    wb = load_workbook(filename=unique_xlsx_path)
    ws = wb['technical_inspection']

    worksheets = 1

    for technical_inspection in technical_inspections:
        xlsx_populate.technical_inspection_xlsx_populate(
            ws, technical_inspection)

        if len(technical_inspections) > worksheets:
            ws = wb.copy_worksheet(ws)
            worksheets += 1

    ws = wb['medical_examination']

    worksheets = 1

    for medical_examination in medical_examinations:
        xlsx_populate.medical_examination_xlsx_populate(
            ws, medical_examination)

        if len(medical_examinations) > worksheets:
            ws = wb.copy_worksheet(ws)
            worksheets += 1

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="Official Notices.xlsx"'

    wb.save(response)

    os.remove(unique_xlsx_path)

    return response


@login_required
def course_documents_xlsx(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.CourseDocumentsForm(request.POST)
            if form.is_valid():
                course = form.cleaned_data.get('course')
                document_type = form.cleaned_data.get('document_type')

                if document_type == 'official_notices':
                    response = official_notices_xlsx(course)
                elif document_type == 'receipt_letter':
                    response = receipt_letter_xlsx(course)

                return response
        else:
            form = forms.CourseDocumentsForm()

        context = {
            'form': form,
            'page_heading': 'Документи за курс'
        }

        return render(request, 'main/add_update_form.html', context)
    else:
        raise PermissionDenied


@login_required
def course_date_journals_xlsx(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.CourseDateJournalForm(request.POST)

            if form.is_valid():
                journal_type = form.cleaned_data['journal_type']
                from_date = form.cleaned_data['from_date']
                to_date = form.cleaned_data['to_date']
                company = form.cleaned_data['company']

                if journal_type == 'technical_inspection':
                    technical_inspections = models.CourseTechnicalInspection.objects.filter(
                        creation_date__range=[from_date, to_date]
                    )

                    unique_token = secrets.token_hex(32)

                    xlsx_path = os.path.join(
                        settings.BASE_DIR, 'main/xlsx_files/course_technical_inspection_journal.xlsx')

                    unique_xlsx_path = os.path.join(
                        settings.BASE_DIR, f'main/xlsx_files/course_technical_inspection_journal_{unique_token}.xlsx')

                    shutil.copy(xlsx_path, unique_xlsx_path)

                    heading = f'{company.name}, {company.city}, ЕИК {company.bulstat}'

                    wb = load_workbook(filename=unique_xlsx_path)
                    ws = wb.active

                    ws['A2'] = heading

                    for i in range(0, len(technical_inspections)):
                        ws[f'A{i + 6}'] = technical_inspections[i].number
                        ws[f'B{i + 6}'] = technical_inspections[i].course.car.__str__()
                        ws[f'C{i + 6}'] = dateformat.format(
                            technical_inspections[i].creation_date, formats.get_format('SHORT_DATE_FORMAT'))
                        ws[f'F{i + 6}'] = technical_inspections[i].perpetrator.perpetrator

                    response = HttpResponse(
                        content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = f'attachment; filename="Technical Inspections Journal.xlsx"'

                    wb.save(response)

                    os.remove(unique_xlsx_path)

                elif journal_type == 'medical_examination':
                    medical_examinations = models.CourseMedicalExamination.objects.filter(
                        creation_date__range=[from_date, to_date]
                    )

                    unique_token = secrets.token_hex(32)

                    xlsx_path = os.path.join(
                        settings.BASE_DIR, 'main/xlsx_files/course_medical_examination_journal.xlsx')

                    unique_xlsx_path = os.path.join(
                        settings.BASE_DIR, f'main/xlsx_files/course_medical_examination_journal_{unique_token}.xlsx')

                    shutil.copy(xlsx_path, unique_xlsx_path)

                    heading = f'{company.name}, {company.city}, ЕИК {company.bulstat}'

                    wb = load_workbook(filename=unique_xlsx_path)
                    ws = wb.active

                    ws['A2'] = heading

                    for i in range(0, len(medical_examinations)):
                        ws[f'A{i + 6}'] = medical_examinations[i].number
                        ws[f'B{i + 6}'] = medical_examinations[i].driver.__str__()
                        ws[f'C{i + 6}'] = dateformat.format(
                            medical_examinations[i].creation_date, formats.get_format('SHORT_DATE_FORMAT'))
                        ws[f'F{i + 6}'] = medical_examinations[i].perpetrator.perpetrator

                    response = HttpResponse(
                        content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = f'attachment; filename="Medical Examinations Journal.xlsx"'

                    wb.save(response)

                    os.remove(unique_xlsx_path)

                elif journal_type == 'instruction':
                    instructions = models.Instruction.objects.filter(
                        creation_date__range=[from_date, to_date]
                    )

                    unique_token = secrets.token_hex(32)

                    xlsx_path = os.path.join(
                        settings.BASE_DIR, 'main/xlsx_files/instruction_journal.xlsx')

                    unique_xlsx_path = os.path.join(
                        settings.BASE_DIR, f'main/xlsx_files/instruction_journal_{unique_token}.xlsx')

                    shutil.copy(xlsx_path, unique_xlsx_path)

                    wb = load_workbook(filename=unique_xlsx_path)
                    ws = wb.active

                    for i in range(0, len(instructions)):
                        ws[f'A{i + 2}'] = instructions[i].number
                        ws[f'B{i + 2}'] = instructions[i].driver.__str__()
                        ws[f'C{i + 2}'] = instructions[i].course.car.number_plate
                        ws[f'G{i + 2}'] = dateformat.format(
                            instructions[i].creation_date, formats.get_format('SHORT_DATE_FORMAT'))

                    response = HttpResponse(
                        content_type='application/vnd.ms-excel')
                    response['Content-Disposition'] = f'attachment; filename="Instructions Journal.xlsx"'

                    wb.save(response)

                    os.remove(unique_xlsx_path)

                return response
        else:
            form = forms.CourseDateJournalForm()

        context = {
            'form': form,
            'page_heading': 'Сваляне на дневник'
        }

        return render(request, 'main/add_update_form.html', context)
    else:
        raise PermissionDenied


class TagAutoResponseView(AutoResponseView):
    def get(self, request, *args, **kwargs):
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get('term', request.GET.get('term', ''))
        self.object_list = self.get_queryset()

        context = self.get_context_data()
        field_name = self.kwargs['field_name']

        return JsonResponse({
            'results': [
                {
                    'text': self.widget.label_from_instance(obj),
                    'id': getattr(obj, field_name),
                }
                for obj in context['object_list']
            ],
            'more': context['page_obj'].has_next()
        })


def all_course_documents_xlsx(request, pk):
    if request.user.is_staff:
        course = get_object_or_404(models.Course, id=pk)

        if hasattr(course, 'invoice'):
            course_invoice = course.invoice

        if hasattr(course, 'trip_orders'):
            trip_orders = course.trip_orders.all()

        if hasattr(course, 'instructions'):
            instructions = course.instructions.all()

        if hasattr(course, 'medical_examinations'):
            medical_examinations = course.medical_examinations.all()

        if hasattr(course, 'technical_inspections'):
            technical_inspections = course.technical_inspections.all()

        unique_token = secrets.token_hex(32)

        xlsx_path = os.path.join(
            settings.BASE_DIR, 'main/xlsx_files/all_course_documents.xlsx')

        unique_xlsx_path = os.path.join(
            settings.BASE_DIR, f'main/xlsx_files/all_course_documents_{unique_token}.xlsx')

        shutil.copy(xlsx_path, unique_xlsx_path)

        wb = load_workbook(filename=unique_xlsx_path)

        if course_invoice:
            ws = wb['original']

            xlsx_populate.course_invoice_xlsx_populate(ws, course_invoice)

            if course_invoice.course.export:
                ws = wb['translated']

                xlsx_populate.course_invoice_translated_xlsx_populate(
                    ws, course_invoice)

        if trip_orders:
            ws = wb['trip_order']

            worksheets = 1

            for trip_order in trip_orders:
                xlsx_populate.trip_order_xlsx_populate(ws, trip_order)

                if len(trip_orders) > worksheets:
                    ws = wb.copy_worksheet(ws)
                    worksheets += 1

            ws = wb['expenses']

            xlsx_populate.trip_order_expenses_xlsx_populate(ws, trip_orders[0])

            worksheets = 1
            expense_orders_sum = 0
            blank_file_populated = False

            ws = wb['expense_order']

            for trip_order in trip_orders:
                if hasattr(trip_order, 'expense_orders'):
                    expense_orders = trip_order.expense_orders.all()
                    expense_orders_sum += len(expense_orders)

                    for expense_order in expense_orders:
                        if not blank_file_populated:
                            xlsx_populate.expense_order_xlsx_populate(
                                ws, expense_order)

                            if expense_orders_sum > worksheets:
                                ws = wb.copy_worksheet(ws)
                                worksheets += 1

                            blank_file_populated = True
                        else:
                            if expense_orders_sum > worksheets:
                                ws = wb.copy_worksheet(ws)
                                worksheets += 1

                            xlsx_populate.expense_order_xlsx_populate(
                                ws, expense_order)

        if instructions:
            ws = wb['instruction']

            worksheets = 1

            for instruction in instructions:
                xlsx_populate.instruction_xlsx_populate(ws, instruction)

                if len(instructions) > worksheets:
                    ws = wb.copy_worksheet(ws)
                    worksheets += 1

        if medical_examinations:
            ws = wb['medical_examination']

            worksheets = 1

            for medical_examination in medical_examinations:
                xlsx_populate.medical_examination_xlsx_populate(
                    ws, medical_examination)

                if len(medical_examinations) > worksheets:
                    ws = wb.copy_worksheet(ws)
                    worksheets += 1

        if technical_inspections:
            ws = wb['technical_inspection']

            worksheets = 1

            for technical_inspection in technical_inspections:
                xlsx_populate.technical_inspection_xlsx_populate(
                    ws, technical_inspection)

                if len(technical_inspections) > worksheets:
                    ws = wb.copy_worksheet(ws)
                    worksheets += 1

        ws = wb['receipt_letter']
        xlsx_populate.receipt_letter_xlsx_populate(ws, course)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="All Course Documents.xlsx"'

        wb.save(response)

        os.remove(unique_xlsx_path)

        return response

    else:
        raise PermissionDenied
