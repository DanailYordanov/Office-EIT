from django.utils import dateformat, formats
from deep_translator import GoogleTranslator


def trip_order_xlsx_populate(ws, trip_order):
    company = trip_order.course.company
    heading = f'{company.name}, {company.city}, ЕИК {company.bulstat}'
    duration_time = 0

    if trip_order.to_date and trip_order.from_date:
        duration_time = (trip_order.to_date - trip_order.from_date).days + 1

    ws['A1'] = heading
    ws['E3'] = trip_order.number
    ws['G3'] = dateformat.format(
        trip_order.creation_date, formats.get_format('SHORT_DATE_FORMAT'))
    ws['A8'] = trip_order.driver.__str__()
    ws['B12'] = trip_order.destination

    if trip_order.from_date:
        ws['C13'] = dateformat.format(
            trip_order.from_date, formats.get_format('SHORT_DATE_FORMAT'))

    if trip_order.to_date:
        ws['E13'] = dateformat.format(
            trip_order.to_date, formats.get_format('SHORT_DATE_FORMAT'))

    ws['I13'] = duration_time
    ws['F15'] = trip_order.course.car.number_plate
    ws['F18'] = f'{company.name}'
    ws['A29'] = trip_order.driver.__str__()
    ws['F29'] = trip_order.creator.__str__()


def trip_order_expenses_xlsx_populate(ws, trip_order):
    ws['B1'] = trip_order.number
    ws['E1'] = trip_order.from_date
    ws['B2'] = trip_order.course.car.number_plate
    ws['G2'] = trip_order.driver.__str__()
    ws['G17'] = trip_order.driver.debit_card_number


def expense_order_xlsx_populate(ws, expense_order):
    company = expense_order.trip_order.course.company
    heading = f'{company.name}, {company.city}, ЕИК {company.bulstat}'

    ws['A1'] = heading
    ws['E3'] = expense_order.number
    ws['G3'] = dateformat.format(
        expense_order.creation_date, formats.get_format('SHORT_DATE_FORMAT'))
    ws['D5'] = expense_order.trip_order.driver.__str__()
    ws['B7'] = expense_order.BGN_amount
    ws['E7'] = expense_order.EUR_amount
    ws['F10'] = expense_order.trip_order.number

    if expense_order.trip_order.from_date:
        ws['H10'] = dateformat.format(
            expense_order.trip_order.from_date, formats.get_format('SHORT_DATE_FORMAT'))

    ws['G12'] = expense_order.trip_order.driver.debit_card_number

    if expense_order.trip_order.driver.bank:
        ws['E13'] = expense_order.trip_order.driver.bank.iban

    ws['B15'] = dateformat.format(
        expense_order.creation_date, formats.get_format('SHORT_DATE_FORMAT'))
    ws['A19'] = expense_order.trip_order.driver.__str__()
    ws['F19'] = expense_order.creator.__str__()


def course_invoice_xlsx_populate(ws, course_invoice):
    course = course_invoice.course
    bank = course.bank
    company = course.company
    contractor = course.contractor
    prices = course_invoice.get_prices()

    ws['V5'] = str(course_invoice.number).zfill(10)
    ws['V6'] = dateformat.format(
        course_invoice.creation_date, formats.get_format('SHORT_DATE_FORMAT'))

    ws['G9'] = contractor.name
    ws['G11'] = contractor.bulstat

    if contractor.bulstat:
        if contractor.client_type == 'Български':
            ws['G12'] = contractor.bulstat[2:]
        else:
            ws['G12'] = contractor.bulstat

    ws['G13'] = contractor.city
    ws['G14'] = contractor.address
    ws['G16'] = contractor.mol
    ws['G17'] = contractor.phone_number

    ws['R9'] = company.name

    if company.bulstat:
        ws['R11'] = company.bulstat
        ws['R12'] = company.bulstat[2:]

    ws['R13'] = company.city
    ws['R14'] = company.address
    ws['R16'] = company.mol
    ws['R17'] = company.phone_number

    ws['T21'] = prices['price']

    if course_invoice.tax_type == 'Стандартна фактура':
        ws['X24'] = prices['price']
        ws['X25'] = prices['vat_price']

    ws['X26'] = prices['calculated_price']

    ws['G24'] = prices['price_in_words']

    from_to = f'Транспорт от {course.from_to.__str__()} с камион'

    ws['H27'] = course_invoice.additional_information

    ws['C21'] = from_to
    ws['I22'] = course.car.number_plate
    ws['H23'] = course.request_number.__str__()

    ws['J28'] = course_invoice.creation_date
    ws['J29'] = course_invoice.tax_transaction_basis.__str__()

    ws['R28'] = course_invoice.payment_type
    ws['R29'] = bank.iban
    ws['R31'] = bank.name
    ws['R33'] = bank.bank_code

    ws['I35'] = course.contact_person.__str__()
    ws['S35'] = course_invoice.creator.__str__()


def course_invoice_translated_xlsx_populate(ws, course_invoice):
    course = course_invoice.course
    bank = course.bank
    company = course.company
    contractor = course.contractor
    prices = course_invoice.get_prices()

    translator = GoogleTranslator(source='bg', target='en')

    ws['B2'] = translator.translate(company.name)
    ws['Q2'] = str(course_invoice.number).zfill(10)
    ws['C3'] = company.bulstat

    if company.address:
        ws['B4'] = translator.translate(company.address)

    if company.city:
        ws['B5'] = translator.translate(company.city)

    ws['C17'] = contractor.name
    ws['C18'] = contractor.address
    ws['C19'] = contractor.bulstat

    ws['O17'] = dateformat.format(
        course_invoice.creation_date, formats.get_format('SHORT_DATE_FORMAT'))
    ws['O18'] = course.car.number_plate

    ws['D41'] = translator.translate(course.from_to.__str__())
    ws['E42'] = course.car.number_plate
    ws['N40'] = prices['price']

    if course_invoice.tax_type == 'Стандартна фактура':
        ws['P52'] = prices['vat_price']

    ws['P53'] = prices['calculated_price']

    ws['D73'] = dateformat.format(
        course_invoice.creation_date, formats.get_format('SHORT_DATE_FORMAT'))

    ws['C82'] = translator.translate(course_invoice.payment_type)
    ws['B83'] = translator.translate(bank.name)
    ws['C84'] = bank.iban
    ws['C85'] = bank.bank_code


def instruction_xlsx_populate(ws, instruction):
    company = instruction.course.company

    ws['A2'] = company.name
    ws['A3'] = f'{company.city}, {company.address}'
    ws['A4'] = company.bulstat
    ws['E7'] = instruction.number
    ws['B9'] = instruction.driver.__str__()
    ws['G9'] = instruction.driver.personal_id
    ws['B11'] = instruction.course.car.number_plate
    ws['G18'] = instruction.driver.__str__()
    ws['G21'] = instruction.creator.__str__()
    ws['B20'] = dateformat.format(
        instruction.creation_date, formats.get_format('SHORT_DATE_FORMAT'))


def receipt_letter_xlsx_populate(ws, course):
    company = course.company
    contractor = course.contractor

    ws['C8'] = contractor.name
    ws['E10'] = contractor.correspondence_address

    if contractor.postal_code:
        ws['C12'] = contractor.postal_code[0]
        ws['D12'] = contractor.postal_code[1]
        ws['E12'] = contractor.postal_code[2]
        ws['F12'] = contractor.postal_code[3]

    ws['J12'] = contractor.city
    ws['D15'] = course.contact_person.__str__()

    ws['AC20'] = company.name
    ws['AE21'] = company.correspondence_address
    ws['AE23'] = company.province

    if company.postal_code:
        ws['AC25'] = company.postal_code[0]
        ws['AD25'] = company.postal_code[1]
        ws['AE25'] = company.postal_code[2]
        ws['AF25'] = company.postal_code[3]

    ws['AJ25'] = company.city

    ws['A30'] = company.name
    ws['A31'] = f'{company.postal_code} {company.city} {company.correspondence_address}'
    ws['E32'] = company.phone_number
    ws['E33'] = company.email

    ws['Z46'] = contractor.name
    ws['Z47'] = contractor.correspondence_address
    ws['Z48'] = f'{contractor.postal_code} {contractor.city}'
    ws['AD49'] = contractor.phone_number


def technical_inspection_xlsx_populate(ws, technical_inspection):
    course = technical_inspection.course
    company = course.company

    ws['A1'] = company.name
    ws['A2'] = f'{company.city}, {company.address}'
    ws['A3'] = company.bulstat
    ws['E9'] = technical_inspection.number
    ws['B12'] = course.car.number_plate
    ws['B13'] = technical_inspection.driver.__str__()
    ws['C15'] = technical_inspection.perpetrator.perpetrator
    ws['B18'] = dateformat.format(
        course.creation_date, formats.get_format('SHORT_DATE_FORMAT'))


def medical_examination_xlsx_populate(ws, medical_examination):
    course = medical_examination.course
    company = course.company

    ws['A1'] = company.name
    ws['A2'] = f'{company.city}, {company.address}'
    ws['A3'] = company.bulstat
    ws['E9'] = medical_examination.number
    ws['A12'] = medical_examination.driver.__str__()
    ws['B13'] = course.car.number_plate
    ws['C17'] = medical_examination.perpetrator.perpetrator
    ws['B20'] = dateformat.format(
        course.creation_date, formats.get_format('SHORT_DATE_FORMAT'))
