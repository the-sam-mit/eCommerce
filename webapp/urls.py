from django.urls import path
from django.conf.urls import url
from . import views
from .views import SignUpView

app_name = 'webapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/detail/', views.ResultsView.as_view(), name='detail'),
    path('<int:product_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>/add_to_cart/<int:delete_id>/delete_pro/', views.delete_pro, name='delete_pro'),
    path('add_to_cart/<int:delete_id>/delete_pro/', views.deleted_p, name='deleted_p'),
    path('add_to_cart/', views.added_cart, name='added_cart'),
    path('order/', views.order_it, name='order_it'),
    path('add_order/', views.add_order, name='add_order'),
]