from django.urls import path
from django.contrib.auth.decorators import login_required

from .views_PDF_1 import print_ticket_old
from . import views

urlpatterns = [
    path('', login_required(views.DoctorView.as_view()), name='list_doctors'),
    path('add_doctor/', login_required(views.DoctorCreate.as_view()), name='add_doctor'),
    path('detail_doctor/<int:pk>/', login_required(views.DoctorDetail.as_view()), name='detail_doctor'),
    path('detail_doctor/<int:pk>/update/', login_required(views.DoctorUpdate.as_view()), name='update_doctor'),
    path('detail_doctor/<int:pk>/update_cmvp/', login_required(views.DoctorCMVPUpdate.as_view()), name='update_cmvp'),
    path('detail_doctor/<int:pk>/pay_quota/', login_required(views.DoctorPayUpdate.as_view()), name='pay_quota'),

    path('print_ticket_old/<int:pk>/', print_ticket_old, name='print_ticket_old'),

    path('pay_doctor/', views.pay_doctor, name='pay_doctor'),

]
