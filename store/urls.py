from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import PasswordsChangeView

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('about/', views.about, name="about"),
	path('contact/', views.contact, name="contact"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('my_orders/', views.myOrders, name="my_orders"),
	path('order_details/<int:id>', views.order_details, name="order_details"),
	path('view_product/<int:id>', views.viewProduct, name="view_product"),
	path('register', views.register, name="register"),
	path('log_in', views.log_in, name="log_in"),
	path('log_out', views.log_out, name="log_out"),
	path('myProfile', views.my_profile, name="myProfile"),
	path('editProfile', views.edit_profile, name="editProfile"),
	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"), name="reset_password"),
	path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_sent.html"), name="password_reset_done"),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_complete.html"), name='password_reset_confirm'),
	path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_done.html"), name='password_reset_complete'),
	# path('password/', auth_views.PasswordChangeView.as_view(template_name="store/change_password.html")),
	path('password/', PasswordsChangeView.as_view(template_name="store/change_password.html")),

	

]