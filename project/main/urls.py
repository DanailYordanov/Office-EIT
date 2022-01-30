from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('cars/', views.cars_list, name='cars-list'),
    path('add-car/', views.add_car, name='add-car'),
    path('update-car/<int:pk>/', views.update_car, name='update-car'),
    path('delete-car/<int:pk>/', views.CarDeleteView.as_view(), name='delete-car'),
    path('reminders/', views.reminders_list, name='reminders-list'),
    path('add-reminder/', views.add_reminder, name='add-reminder'),
    path('update-reminder/<int:pk>/',
         views.update_reminder, name='update-reminder'),
    path('delete-reminder/<int:pk>/',
         views.ReminderDeleteView.as_view(), name='delete-reminder'),
    path('services/', views.services_list, name='services-list'),
    path('add-service/', views.add_service, name='add-service'),
    path('update-service/<int:pk>/', views.update_service, name='update-service'),
    path('delete-service/<int:pk>/',
         views.ServiceDeleteView.as_view(), name='delete-service'),
    path('users-details/', views.users_details_list, name='users-details-list'),
    path('set-unactive-user/<int:pk>/',
         views.user_set_unactive, name='user-set-unactive'),
    path('contractors/', views.contractors_list, name='contractors-list'),
    path('add-contractor/', views.add_contractor, name='add-contractor'),
    path('update-contractor/<int:pk>/',
         views.update_contractor, name='update-contractor'),
    path('delete-contractor/<int:pk>/',
         views.ContractorDeleteView.as_view(), name='delete-contractor'),
    path('', views.courses_list, name='courses-list'),
    path('add-course/', views.add_course, name='add-course'),
    path('update-course/<int:pk>/',
         views.update_course, name='update-course'),
    path('delete-course/<int:pk>/',
         views.CourseDeleteView.as_view(), name='delete-course'),
    path('course/<int:pk>/', views.course_information, name='course-information'),
    path('course/<int:pk>/add-expense/',
         views.add_expense, name='add-expense'),
    path('course/update-expense/<int:pk>/',
         views.update_expense, name='update-expense'),
    path('course/<int:course_pk>/delete-expense/<int:pk>/',
         views.ExpenseDeleteView.as_view(), name='delete-expense'),
    path('download/course-expenses/<int:pk>/',
         views.course_expenses_xlsx, name='course-expenses-xlsx'),
    path('addresses/', views.addresses_list, name='addresses-list'),
    path('add-address/', views.add_address, name='add-address'),
    path('update-address/<int:pk>/',
         views.update_address, name='update-address'),
    path('delete-address/<int:pk>/',
         views.AddressDeleteView.as_view(), name='delete-address'),
    path('trip-orders/', views.trip_orders_list, name='trip-orders-list'),
    path('add-trip-order/', views.add_trip_order, name='add-trip-order'),
    path('update-trip-order/<int:pk>/',
         views.update_trip_order, name='update-trip-order'),
    path('delete-trip-order/<int:pk>/',
         views.TripOrderDeleteView.as_view(), name='delete-trip-order'),
    path('download/trip-order/<int:pk>/',
         views.trip_order_xlsx, name='trip-order-xlsx'),
    path('load/course-options/', views.load_course_options,
         name='load-course-options'),
    path('load/dates/', views.load_dates,
         name='load-dates'),
    path('expense-orders/', views.expense_orders_list, name='expense-orders-list'),
    path('add-expense-order/', views.add_expense_order, name='add-expense-order'),
    path('update-expense-order/<int:pk>/',
         views.update_expense_order, name='update-expense-order'),
    path('delete-expense-order/<int:pk>/',
         views.ExpenseOrderDeleteView.as_view(), name='delete-expense-order'),
    path('download/expense-order/<int:pk>/',
         views.expense_order_xlsx, name='expense-order-xlsx'),
    path('course-invoices-list/', views.course_invoices_list,
         name='course-invoices-list'),
    path('add-course-invoice/', views.add_course_invoice,
         name='add-course-invoice'),
    path('update-course-invoice/<int:pk>/',
         views.update_course_invoice, name='update-course-invoice'),
    path('delete-course-invoice/<int:pk>/',
         views.CourseInvoiceDeleteView.as_view(), name='delete-course-invoice'),
    path('download/course-invoice/<int:pk>/',
         views.course_invoice_xlsx, name='course-invoice-xlsx'),
    path('companies-list/', views.companies_list,
         name='companies-list'),
    path('add-company/', views.add_company,
         name='add-company'),
    path('update-company/<int:pk>/',
         views.update_company, name='update-company'),
    path('delete-company/<int:pk>/',
         views.CompanyDeleteView.as_view(), name='delete-company'),
    path('banks-list/', views.banks_list,
         name='banks-list'),
    path('add-bank/', views.add_bank,
         name='add-bank'),
    path('update-bank/<int:pk>/',
         views.update_bank, name='update-bank'),
    path('delete-bank/<int:pk>/',
         views.BankDeleteView.as_view(), name='delete-bank'),
    path('instructions-list/', views.instructions_list,
         name='instructions-list'),
    path('add-instruction/', views.add_instruction,
         name='add-instruction'),
    path('update-instruction/<int:pk>/',
         views.update_instruction, name='update-instruction'),
    path('delete-instruction/<int:pk>/',
         views.InstructionDeleteView.as_view(), name='delete-instruction')
]
