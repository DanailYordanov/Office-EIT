from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import reverse
from django.core.validators import RegexValidator
from num2cyrillic import NumberToWords


CLIENT_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Български', 'Български'),
    ('Чуждестранен', 'Чуждестранен')
]

CURRENCY_CHOICES = [
    ('', 'Избери'),
    ('BGN', 'BGN'),
    ('EUR', 'EUR'),
    ('USD', 'USD'),
    ('GBP', 'GBP'),
    ('CAD', 'CAD')
]

LOADING_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Адрес на товарене', 'Адрес на товарене'),
    ('Адрес на разтоварване', 'Адрес на разтоварване'),
    ('Адрес на митница', 'Адрес на митница')
]

PAYMENT_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Кеш', 'Кеш'),
    ('Дебитна карта', 'Дебитна карта'),
    ('Кредитна карта', 'Кредитна карта'),
    ('Банков превод', 'Банков превод')
]


MEASURE_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Тон', 'Тон'),
    ('Курс', 'Курс'),
    ('Брой', 'Брой'),
    ('Километър', 'Километър')
]


INVOICE_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Фактура', 'Фактура'),
    ('Кредитно известие', 'Кредитно известие'),
    ('Дебитно известие', 'Дебитно известие')
]


TAX_TYPE_CHOICES = [
    ('', 'Избери'),
    ('Стандартна фактура', 'Стандартна фактура'),
    ('Фактура без начисление на ДДС', 'Фактура без начисление на ДДС')
]


class CarType(models.Model):
    car_type = models.CharField('Вид автомобил', max_length=50)

    class Meta:
        ordering = ['car_type']
        verbose_name = 'Вид автомобил'
        verbose_name_plural = 'Видове автомобили'

    def __str__(self):
        return self.car_type


class Car(models.Model):
    car_type = models.ForeignKey(
        CarType, verbose_name='Вид автомобил', related_name='cars', null=True, on_delete=models.CASCADE)
    brand = models.CharField('Марка', max_length=50)
    number_plate = models.CharField('Регистрационен номер', max_length=50)
    vin = models.CharField(
        'Номер на рама', max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['brand']
        verbose_name = 'Автомобил'
        verbose_name_plural = 'Автомобили'

    def __str__(self):
        return self.number_plate


class ReminderType(models.Model):
    reminder_type = models.CharField('Вид напомняне', max_length=50)

    class Meta:
        ordering = ['reminder_type']
        verbose_name = 'Вид напомняне'
        verbose_name_plural = 'Видове напомняния'

    def __str__(self):
        return self.reminder_type


class Reminder(models.Model):
    reminder_type = models.ForeignKey(
        ReminderType, verbose_name='Вид напомняне', related_name='reminders', null=True, on_delete=models.CASCADE)
    car = models.ForeignKey(
        Car, verbose_name='Автомобил', on_delete=models.CASCADE)
    expiration_date = models.DateField('Дата на изтичнане')

    class Meta:
        verbose_name = 'Напомняне'
        verbose_name_plural = 'Напомняния'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('reminders_notifications')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete('reminders_notifications')

    def __str__(self):
        return f'{self.car.number_plate} - {self.reminder_type.reminder_type}'


class ServiceType(models.Model):
    service_type = models.CharField('Вид обслужване', max_length=100)

    class Meta:
        ordering = ['service_type']
        verbose_name = 'Вид техническо обслужване'
        verbose_name_plural = 'Видове технически обслужвания'

    def __str__(self):
        return self.service_type


class Service(models.Model):
    car = models.ForeignKey(
        Car, verbose_name='Автомобил', related_name='services', on_delete=models.CASCADE)
    service_type = models.ForeignKey(
        ServiceType, verbose_name='Вид обслужване', related_name='services', null=True, on_delete=models.CASCADE)
    run = models.CharField('Пробег', max_length=20)
    date = models.DateField('Дата')
    additional_information = models.CharField(
        'Допълнителна информация', max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = 'Техническо обслужване'
        verbose_name_plural = 'Технически обслужвания'

    def __str__(self):
        return f'{self.car.brand} - {self.car.number_plate} - {self.service_type}'


class Contractor(models.Model):
    client_type = models.CharField(
        'Тип клиент', max_length=100, choices=CLIENT_TYPE_CHOICES)
    name = models.CharField('Име', max_length=100)
    bulstat = models.CharField(
        'Булстат', max_length=100, null=True, blank=True)
    mol = models.CharField('МОЛ', max_length=100, null=True, blank=True)
    country = models.CharField(
        'Държава', max_length=100, null=True, blank=True)
    city = models.CharField('Град', max_length=100, null=True, blank=True)
    address = models.CharField('Адрес', max_length=100, null=True, blank=True)
    postal_code = models.CharField(
        'Пощенски код', max_length=20, null=True, blank=True)
    correspondence_address = models.CharField(
        'Адрес за кореспонденция', max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        'Телефонен номер', max_length=100, null=True, blank=True)
    email = models.CharField('E-mail', max_length=100, null=True, blank=True)
    maturity_date = models.CharField(
        'Падеж', max_length=50, null=True, blank=True)
    cmr_photo = models.FileField(
        'Прикачи ЧМР Застраховка', upload_to='cmr_photos', null=True, blank=True)
    cmr_expiration_date = models.DateField(
        'Дата на изтичане', null=True, blank=True)
    license_photo = models.FileField(
        'Прикачи лиценз или друг документ', upload_to='license_photos', null=True, blank=True)
    license_expiration_date = models.DateField(
        'Дата на изтичане', null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенти'

    def __str__(self):
        return self.name


class Bank(models.Model):
    name = models.CharField('Име', max_length=50)
    bank_code = models.CharField(
        'Банков код', max_length=50, null=True, blank=True)
    iban = models.CharField('IBAN', max_length=50)

    class Meta:
        ordering = ['name']
        verbose_name = 'Банка'
        verbose_name_plural = 'Банки'

    def __str__(self):
        return f'{self.name} - {self.bank_code} - {self.iban}'


class Company(models.Model):
    name = models.CharField('Име', max_length=100)
    bulstat = models.CharField(
        'Булстат', max_length=100, null=True, blank=True)
    mol = models.CharField('МОЛ', max_length=100, null=True, blank=True)
    city = models.CharField('Град', max_length=100, null=True, blank=True)
    postal_code = models.CharField(
        'Пощенски код', max_length=20, null=True, blank=True)
    province = models.CharField(
        'Област', max_length=50, null=True, blank=True)
    address = models.CharField('Адрес', max_length=100, null=True, blank=True)
    correspondence_address = models.CharField(
        'Адрес за кореспонденция', max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        'Телефонен номер', max_length=100, null=True, blank=True)
    email = models.EmailField('E-mail', max_length=100, null=True, blank=True)
    course_id = models.IntegerField('Курс №', default=1)
    course_invoice_id = models.IntegerField('Фактура №', default=1)
    trip_order_id = models.IntegerField('Командировъчна заповед №', default=1)
    expense_order_id = models.IntegerField('Разходен Ордер №', default=1)
    instruction_id = models.IntegerField('Инструкция №', default=1)
    course_technical_inspection_id = models.IntegerField(
        'Технически преглед към курс №', default=1)
    course_medical_examination_id = models.IntegerField(
        'Медицински преглед към курс №', default=1)

    class Meta:
        ordering = ['name']
        verbose_name = 'Компания'
        verbose_name_plural = 'Комапнии'

    def __str__(self):
        return self.name


class TaxTransactionBasis(models.Model):
    name = models.CharField('Име', max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Основание на сделка'
        verbose_name_plural = 'Основание на сделка'

    def __str__(self):
        return self.name


from_to_regex = '^.+ {1}до{1} {1}.+$'
from_to_error_message = """
    Невалиден формат! Използвайте следния формат: "{Дестинация} до {Дестинация}",
    с празни места и думата "до" между дестинациите.
    """
from_to_validator = RegexValidator(
    regex=from_to_regex,
    message=from_to_error_message
)


class FromTo(models.Model):
    from_to = models.CharField(
        'Релация', max_length=100, validators=[from_to_validator])

    class Meta:
        ordering = ['from_to']
        verbose_name = 'Релация'
        verbose_name_plural = 'Релации'

    def __str__(self):
        return self.from_to


class RequestNumber(models.Model):
    request_number = models.CharField('Номер на заявка', max_length=100)

    class Meta:
        ordering = ['request_number']
        verbose_name = 'Номер на заявка'
        verbose_name_plural = 'Номера на заявки'

    def __str__(self):
        return self.request_number


class CargoType(models.Model):
    cargo_type = models.CharField('Вид и тегло на товара', max_length=100)

    class Meta:
        ordering = ['cargo_type']
        verbose_name = 'Вид и тегло на товара'
        verbose_name_plural = 'Видове и тегла на товари'

    def __str__(self):
        return self.cargo_type


class ContactPerson(models.Model):
    contact_person = models.CharField('Лице за контакт', max_length=100)

    class Meta:
        ordering = ['contact_person']
        verbose_name = 'Лице за контакт'
        verbose_name_plural = 'Лица за контакти'

    def __str__(self):
        return self.contact_person


class Description(models.Model):
    description = models.CharField('Описание', max_length=1000)

    class Meta:
        verbose_name = 'Описание'
        verbose_name_plural = 'Описания'

    def __str__(self):
        return self.description


class Course(models.Model):
    number = models.IntegerField('№')
    driver = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='courses', verbose_name='Шофьор')
    car = models.ForeignKey(
        Car, verbose_name='Автомобил', related_name='courses', null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(
        Company, verbose_name='Фирма', related_name='courses', null=True, on_delete=models.SET_NULL)
    contractor = models.ForeignKey(
        Contractor, verbose_name='Контрагент', null=True, on_delete=models.SET_NULL)
    bank = models.ForeignKey(Bank, verbose_name='Банка', related_name='courses',
                             null=True, on_delete=models.SET_NULL)
    request_number = models.ForeignKey(
        RequestNumber, verbose_name='Номер на заявка', null=True, blank=True, on_delete=models.SET_NULL)
    from_to = models.ForeignKey(
        FromTo, verbose_name='Релация', null=True, on_delete=models.SET_NULL)
    description = models.ForeignKey(
        Description, verbose_name='Описание', null=True, blank=True, on_delete=models.SET_NULL)
    course_price = models.FloatField('Цена за курс')
    course_price_currency = models.CharField(
        'Валута', choices=CURRENCY_CHOICES, max_length=5)
    driver_salary = models.FloatField('Цена за командировка')
    driver_salary_currency = models.CharField(
        'Валута', choices=CURRENCY_CHOICES, max_length=5)
    cargo_type = models.ForeignKey(
        CargoType, verbose_name='Вид и тегло на товара', null=True, on_delete=models.SET_NULL)
    export = models.BooleanField('За износ', default=False)
    mileage = models.FloatField('Километраж')
    contact_person = models.ForeignKey(
        ContactPerson, verbose_name='Лице за контакт', null=True, blank=True, on_delete=models.SET_NULL)
    other_conditions = models.CharField(
        'Други условия', max_length=1000, null=True, blank=True)
    file = models.FileField(
        'Прикачи файл', upload_to='course_files', null=True, blank=True)
    creation_date = models.DateField('Дата на създаване', auto_now_add=True)

    class Meta:
        ordering = ['-number']
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсове'

    def __str__(self):
        drivers = self.get_drivers()
        return f'№{self.number} - {drivers} - {self.contractor} - {self.from_to}'

    def save(self, *args, **kwargs):
        if not self.id:
            company = self.company
            self.number = company.course_id
            company.course_id += 1
            company.save()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:course-information', kwargs={
            'pk': self.id,
        })

    def get_drivers(self):
        return ', '.join(map(str, self.driver.all()))


class Address(models.Model):
    address = models.CharField('Адрес', max_length=200)
    contact_person = models.CharField(
        'Лице за контакт', max_length=50, null=True, blank=True)
    contact_phone = models.CharField(
        'Телефон за връзка', max_length=30, null=True, blank=True)
    gps_coordinates = models.CharField(
        'GPS координати', max_length=100, null=True, blank=True)
    email = models.EmailField('E-mail', null=True, blank=True)

    class Meta:
        ordering = ['address']
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреси'

    def __str__(self):
        return self.address


class CourseAddress(models.Model):
    course = models.ForeignKey(
        Course, verbose_name='Курс', related_name='addresses', on_delete=models.CASCADE)
    address = models.ForeignKey(
        Address, verbose_name='Свързан адрес', null=True, blank=True, on_delete=models.SET_NULL)
    load_type = models.CharField('Товарен/Разтоварен/Митница',
                                 choices=LOADING_TYPE_CHOICES, max_length=30)
    date = models.DateField('Дата', null=True, blank=True)

    class Meta:
        verbose_name = 'Адрес към курс'
        verbose_name_plural = 'Адреси към курсове'

    def __str__(self):
        return f'{self.course} - {self.address} - {self.date}'


class ExpenseType(models.Model):
    expense_type = models.CharField('Вид разход', max_length=50)

    class Meta:
        ordering = ['expense_type']
        verbose_name = 'Вид разход'
        verbose_name_plural = 'Видове разходи'

    def __str__(self):
        return self.expense_type


class Expense(models.Model):
    course = models.ForeignKey(
        Course, verbose_name='Курс', related_name='expenses', on_delete=models.CASCADE)
    expense_type = models.ForeignKey(
        ExpenseType, verbose_name='Вид разход', related_name='expenses', on_delete=models.CASCADE)
    price = models.FloatField('Цена')
    currency = models.CharField(
        'Валута', choices=CURRENCY_CHOICES, max_length=5)
    payment_type = models.CharField(
        'Вид плащане', max_length=50, choices=PAYMENT_TYPE_CHOICES)
    additional_information = models.CharField(
        'Допълнителна информация', max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = 'Разход към курс'
        verbose_name_plural = 'Разходи към курсове'

    def __str__(self):
        return f'{self.course} - {self.expense_type} - {self.price}'


class TripOrder(models.Model):
    number = models.IntegerField('№')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Създател', related_name='trip_orders_creator', null=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Шофьор', related_name='trip_orders_driver', null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(
        Course, verbose_name='Курс за износ', related_name='trip_orders', on_delete=models.CASCADE)
    destination = models.CharField('Дестинация', max_length=100)
    from_date = models.DateField('Начална дата', null=True, blank=True)
    to_date = models.DateField('Крайна дата', null=True, blank=True)
    creation_date = models.DateField('Дата на създаване', auto_now_add=True)

    class Meta:
        ordering = ['-number']
        verbose_name = 'Командировъчна заповед'
        verbose_name_plural = 'Командировъчни заповеди'

    def __str__(self):
        return f'Командировъчна заповед № - {self.number}'

    def save(self, *args, **kwargs):
        if not self.id:
            company = self.course.company
            self.number = company.trip_order_id
            company.trip_order_id += 1
            company.save()

        super().save(*args, **kwargs)


class ExpenseOrder(models.Model):
    number = models.IntegerField('№')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Създател', related_name='expense_orders', null=True, on_delete=models.SET_NULL)
    trip_order = models.ForeignKey(
        TripOrder, verbose_name='Командировъчна заповед', related_name='expense_orders', null=True, on_delete=models.CASCADE)
    BGN_amount = models.FloatField('Сума в лева', null=True, blank=True)
    EUR_amount = models.FloatField('Сума в евро', null=True, blank=True)
    creation_date = models.DateField('Дата на създаване', auto_now_add=True)

    class Meta:
        ordering = ['-number']
        verbose_name = 'Разходен ордер'
        verbose_name_plural = 'Разходни ордери'

    def __str__(self):
        return f'Разходен ордер № - {self.number}'

    def save(self, *args, **kwargs):
        if not self.id:
            company = self.trip_order.course.company
            self.number = company.expense_order_id
            company.expense_order_id += 1
            company.save()

        super().save(*args, **kwargs)


class CourseInvoice(models.Model):
    number = models.IntegerField('№')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Създател', related_name='invoices', null=True, on_delete=models.SET_NULL)
    course = models.OneToOneField(
        Course, verbose_name='Курс', related_name='invoice', null=True, on_delete=models.CASCADE)
    payment_type = models.CharField(
        'Вид плащане', max_length=50, choices=PAYMENT_TYPE_CHOICES)
    invoice_type = models.CharField(
        'Вид документ', max_length=30, choices=INVOICE_TYPE_CHOICES)
    tax_type = models.CharField(
        'ДДС', max_length=30, choices=TAX_TYPE_CHOICES)
    tax_transaction_basis = models.ForeignKey(
        TaxTransactionBasis, verbose_name='Основане на сделка', null=True, on_delete=models.SET_NULL)
    additional_information = models.CharField(
        'Допълнителна информация', max_length=500, null=True, blank=True)
    creation_date = models.DateField('Дата на създаване', auto_now_add=True)

    class Meta:
        ordering = ['-number']
        verbose_name = 'Фактура за курс'
        verbose_name_plural = 'Фактури за курсове'

    def __str__(self):
        return f'Фактура за курс № - {self.number}'

    def get_prices(self):
        price = round(self.course.course_price, 2)

        if self.tax_type == 'Стандартна фактура':
            vat_price = round(self.course.course_price * 0.2, 2)
        else:
            vat_price = 0

        calculated_price = price + vat_price
        whole_part = int(calculated_price)
        fractional_part = int(((calculated_price - whole_part) * 100))
        price_in_words = NumberToWords()

        if fractional_part != 0:
            price_in_words = f'{price_in_words.cyrillic(whole_part)} лева и {price_in_words.cyrillic(fractional_part)} стотинки'
        else:
            price_in_words = f'{price_in_words.cyrillic(whole_part)} лева'

        currency = self.course.course_price_currency

        price = f'{price} {currency}'
        vat_price = f'{vat_price} {currency}'
        calculated_price = f'{calculated_price} {currency}'

        prices = {
            'price': price,
            'vat_price': vat_price,
            'price_in_words': price_in_words,
            'calculated_price': calculated_price
        }

        return prices

    def save(self, *args, **kwargs):
        if not self.id:
            company = self.course.company
            self.number = company.course_invoice_id
            company.course_invoice_id += 1
            company.save()

        super().save(*args, **kwargs)


class Instruction(models.Model):
    number = models.IntegerField('№')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Създател', related_name='instructions_creator', null=True, on_delete=models.SET_NULL)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Шофьор', related_name='instructions_driver', null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, verbose_name='Курс',
                               related_name='instructions', on_delete=models.CASCADE)
    creation_date = models.DateField('Дата на създаване', auto_now_add=True)

    class Meta:
        ordering = ['-number']
        verbose_name = 'Инструкция'
        verbose_name_plural = 'Инструкции'

    def __str__(self):
        return f'Инструкция на {self.driver} № - {self.number}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.number = self.course.company.instruction_id
            self.course.company.instruction_id += 1
            self.course.company.save()

        super().save(*args, **kwargs)


class TechnicalInspectionPerpetrator(models.Model):
    perpetrator = models.CharField('Извършител', max_length=100)

    class Meta:
        ordering = ['perpetrator']
        verbose_name = 'Извършител на технически преглед'
        verbose_name_plural = 'Извършители на технически прегледи'

    def __str__(self):
        return self.perpetrator


class CourseTechnicalInspection(models.Model):
    number = models.IntegerField('№')
    course = models.ForeignKey(
        Course, verbose_name='Курс', related_name='technical_inspections', on_delete=models.CASCADE)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Шофьор', related_name='technical_inspections', null=True, on_delete=models.SET_NULL)
    perpetrator = models.ForeignKey(
        TechnicalInspectionPerpetrator, verbose_name='Извършител', on_delete=models.CASCADE)
    creation_date = models.DateField('Дата на създаване', auto_now_add=True)

    class Meta:
        ordering = ['-number']
        verbose_name = 'Технически преглед'
        verbose_name_plural = 'Технически прегледи'

    def __str__(self):
        return f'Технически преглед № - {self.number}'

    def save(self, *args, **kwargs):
        if not self.id:
            company = self.course.company
            self.number = company.course_technical_inspection_id
            company.course_technical_inspection_id += 1
            company.save()

        super().save(*args, **kwargs)


class MedicalExaminationPerpetrator(models.Model):
    perpetrator = models.CharField('Извършител', max_length=100)

    class Meta:
        ordering = ['perpetrator']
        verbose_name = 'Извършител на медицински преглед'
        verbose_name_plural = 'Извършители на медицински прегледи'

    def __str__(self):
        return self.perpetrator


class CourseMedicalExamination(models.Model):
    number = models.IntegerField('№')
    course = models.ForeignKey(
        Course, verbose_name='Курс', related_name='medical_examinations', on_delete=models.CASCADE)
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Шофьор', related_name='medical_examinations', null=True, on_delete=models.SET_NULL)
    perpetrator = models.ForeignKey(
        MedicalExaminationPerpetrator, verbose_name='Извършител', on_delete=models.CASCADE)
    creation_date = models.DateField('Дата на създаване', auto_now_add=True)

    class Meta:
        ordering = ['-number']
        verbose_name = 'Медицински преглед'
        verbose_name_plural = 'Медицински прегледи'

    def __str__(self):
        return f'Медицински преглед № - {self.number}'

    def save(self, *args, **kwargs):
        if not self.id:
            company = self.course.company
            self.number = company.course_medical_examination_id
            company.course_medical_examination_id += 1
            company.save()

        super().save(*args, **kwargs)
