import os
from django.conf import settings
from django.views.generic import DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from openpyxl import load_workbook
from num2cyrillic import NumberToWords
from main import models
from main import forms


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
        car = get_object_or_404(models.Car, id=pk)

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
        reminder = get_object_or_404(models.Reminder, id=pk)

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
        service = get_object_or_404(models.Service, id=pk)

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
        contractors = models.Contractor.objects.all()
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
        contractor = get_object_or_404(models.Contractor, id=pk)

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

    model = models.Contractor
    success_url = reverse_lazy('main:contractors-list')

    def test_func(self):
        return self.request.user.is_staff


@login_required
def courses_list(request):
    if request.user.is_staff:
        courses = models.Course.objects.all().order_by('-pk')
    else:
        courses = models.Course.objects.filter(
            user=request.user).order_by('-pk')

    context = {
        'courses': courses,
        'page_heading': 'Курсове'
    }

    return render(request, 'main/courses_list.html', context)


@login_required
def add_course(request):
    if request.user.is_staff:

        addresses = models.Address.objects.all()

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

                        address_object = models.Address.objects.filter(
                            address=address_input)

                        if not address_object:
                            if save:
                                address_object = models.Address.objects.create(
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

        addresses = models.Address.objects.all()
        course = get_object_or_404(models.Course, id=pk)

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

                            address_object = models.Address.objects.filter(
                                address=address_input)

                            if not address_object:
                                if save:
                                    address_object = models.Address.objects.create(
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


@login_required
def course_information(request, pk):
    course = get_object_or_404(models.Course, id=pk)
    expenses = models.Expense.objects.filter(course=course)

    context = {
        'course': course,
        'expenses': expenses,
        'page_heading': 'Информация за курс'
    }

    return render(request, 'main/course_information.html', context)


@login_required
def course_expenses_xlsx(request, pk):
    if request.user.is_staff:
        course = get_object_or_404(models.Course, id=pk)
        trip_order = course.triporder_set.all()[0]

        xlsx_path = os.path.join(
            settings.BASE_DIR, 'main/xlsx_files/course_expenses.xlsx')

        wb = load_workbook(filename=xlsx_path)
        ws = wb.active
        ws['B1'] = trip_order.id
        ws['E1'] = trip_order.from_date
        ws['B2'] = course.car.number_plate
        ws['G2'] = course.driver.__str__()
        ws['G17'] = course.driver.debit_card_number

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Course {course.id} Expenses.xlsx"'

        wb.save(response)

        return response
    else:
        raise PermissionDenied


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = models.Course
    success_url = reverse_lazy('main:courses-list')

    def test_func(self):
        return self.request.user.is_staff


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
        address = get_object_or_404(models.Address, id=pk)

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
        trip_orders = models.TripOrder.objects.all().order_by('-pk')
    else:
        raise PermissionDenied

    context = {
        'trip_orders': trip_orders,
        'page_heading': 'Командировъчни заповеди'
    }

    return render(request, 'main/trip_orders_list.html', context)


@login_required
def add_trip_order(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.TripOrderModelForm(request.POST)

            if form.is_valid():
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
def load_course_options(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')

        if driver_id != '':
            courses = models.Course.objects.filter(driver__id=int(driver_id))
        else:
            courses = models.Course.objects.none()

        context = {
            'courses': courses
        }

        return render(request, 'main/course_select_options.html', context)
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
                load_type='loading_address').order_by('date')
            to_date = course_addresses.filter(
                load_type='unloading_address').order_by('date')

            if (from_date):
                data['from_date'] = from_date.first().date

            if (to_date):
                data['to_date'] = to_date.last().date

        return JsonResponse(data)
    else:
        raise PermissionDenied


@login_required
def trip_order_xlsx(request, pk):
    if request.user.is_staff:
        trip_order = get_object_or_404(models.TripOrder, id=pk)
        duration_time = (trip_order.to_date - trip_order.from_date).days
        xlsx_path = os.path.join(
            settings.BASE_DIR, 'main/xlsx_files/trip_order.xlsx')

        wb = load_workbook(filename=xlsx_path)
        ws = wb.active
        ws['E3'] = trip_order.id
        ws['G3'] = trip_order.creation_date
        ws['A8'] = trip_order.driver.__str__()
        ws['B12'] = trip_order.destination
        ws['C13'] = trip_order.from_date
        ws['E13'] = trip_order.to_date
        ws['I13'] = duration_time
        ws['F15'] = trip_order.course.car.number_plate
        ws['A29'] = trip_order.driver.__str__()

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Trip Order {trip_order.id}.xlsx"'

        wb.save(response)

        return response
    else:
        raise PermissionDenied


@login_required
def expense_orders_list(request):
    if request.user.is_staff:
        expense_orders = models.ExpenseOrder.objects.all().order_by('-pk')
    else:
        raise PermissionDenied

    context = {
        'expense_orders': expense_orders,
        'page_heading': 'Разходни ордери'
    }

    return render(request, 'main/expense_orders_list.html', context)


@login_required
def add_expense_order(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.ExpenseOrderModelForm(request.POST)

            if form.is_valid():
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
        duration_time = (expense_order.trip_order.to_date -
                         expense_order.trip_order.from_date).days
        xlsx_path = os.path.join(
            settings.BASE_DIR, 'main/xlsx_files/expense_order.xlsx')

        wb = load_workbook(filename=xlsx_path)
        ws = wb.active
        ws['E3'] = expense_order.id
        ws['G3'] = expense_order.creation_date
        ws['D5'] = expense_order.trip_order.driver.__str__()

        if expense_order.BGN_amount:
            ws['B7'] = expense_order.BGN_amount

        if expense_order.EUR_amount:
            ws['E7'] = expense_order.EUR_amount

        ws['F10'] = expense_order.trip_order.id
        ws['H10'] = expense_order.trip_order.from_date
        ws['G12'] = expense_order.trip_order.driver.debit_card_number
        ws['A19'] = expense_order.trip_order.driver.__str__()
        ws['C21'] = expense_order.trip_order.from_date
        ws['C23'] = expense_order.trip_order.to_date
        ws['C25'] = duration_time

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Expense Order {expense_order.id}.xlsx"'

        wb.save(response)

        return response
    else:
        raise PermissionDenied


@login_required
def course_invoices_list(request):
    if request.user.is_staff:
        course_invoices = models.CourseInvoice.objects.all().order_by('-pk')
    else:
        raise PermissionDenied

    context = {
        'course_invoices': course_invoices,
        'page_heading': 'Фактури за курсове'
    }

    return render(request, 'main/course_invoices_list.html', context)


@login_required
def add_course_invoice(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = forms.CourseInvoiceModelForm(request.POST)

            if form.is_valid():
                form.instance.creator = request.user
                form.save()

                return redirect('main:course-invoices-list')
        else:
            form = forms.CourseInvoiceModelForm()
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
        xlsx_path = os.path.join(
            settings.BASE_DIR, 'main/xlsx_files/course_invoice.xlsx')

        contractor = course_invoice.course.contractor
        bank = course_invoice.course.bank
        company = course_invoice.course.company

        price_sum = round(course_invoice.price * course_invoice.quantity, 2)

        if course_invoice.tax_type == 'Стандартна фактура':
            calculated_price = round(price_sum + price_sum * 0.2, 2)
        else:
            calculated_price = price_sum

        whole_part = int(calculated_price)
        fractional_part = int(((calculated_price - whole_part) * 100))
        price_in_words = NumberToWords()

        wb = load_workbook(filename=xlsx_path)
        ws = wb.active

        ws['V5'] = str(course_invoice.id).zfill(10)
        ws['V6'] = course_invoice.creation_date

        ws['G9'] = contractor.name
        ws['G11'] = contractor.bulstat

        if contractor.client_type == 'Български':
            ws['G12'] = contractor.bulstat[2:]
        else:
            ws['G12'] = contractor.bulstat

        ws['G13'] = contractor.city
        ws['G14'] = contractor.address
        ws['G16'] = contractor.mol
        ws['G17'] = contractor.phone_number

        ws['R9'] = company.name
        ws['R11'] = company.bulstat
        ws['R12'] = company.bulstat[2:]
        ws['R13'] = company.city
        ws['R14'] = company.address
        ws['R16'] = company.mol
        ws['R17'] = company.phone_number

        ws['M21'] = course_invoice.measure_type
        ws['Q21'] = course_invoice.quantity
        ws['T21'] = round(course_invoice.price, 2)
        ws['X21'] = price_sum

        if course_invoice.tax_type == 'Стандартна фактура':
            ws['X24'] = price_sum
            ws['X25'] = round(price_sum * 0.2, 2)
        else:
            ws['X24'] = None
            ws['X25'] = None

        ws['X26'] = calculated_price
        ws['G24'] = f'{price_in_words.cyrillic(whole_part)} лева и {price_in_words.cyrillic(fractional_part)} стотинки'

        from_destination = course_invoice.course.from_to.split(' ')[0]
        to_destination = course_invoice.course.from_to.split(' ')[2]
        from_to = f'Транспорт от {from_destination} до {to_destination} с камион'

        ws['H27'] = course_invoice.additional_information

        ws['C21'] = from_to
        ws['I22'] = course_invoice.course.car.number_plate
        ws['H23'] = course_invoice.course.request_number

        ws['J28'] = course_invoice.creation_date
        ws['J29'] = course_invoice.tax_transaction_basis.__str__()

        ws['R28'] = course_invoice.payment_type
        ws['R29'] = bank.iban
        ws['R31'] = bank.name
        ws['R33'] = bank.bank_code

        ws['I35'] = course_invoice.course.contact_person
        ws['S35'] = course_invoice.creator.__str__()

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Course Invoice {course_invoice.id}.xlsx"'

        wb.save(response)

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

    return render(request, 'main/companies_list.html', context)


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

    return render(request, 'main/banks_list.html', context)


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
