from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'employee'

urlpatterns = [
    path('token', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('sign-up', views.SignUpView.as_view(), name='sign-up'),
    path('list/', views.EmployeeListView.as_view(), name='employee-list'),
    path('detail/<int:national_code>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('create/', views.EmployeeCreateView.as_view(), name='employee-create'),

]
