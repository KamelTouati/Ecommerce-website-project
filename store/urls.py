from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.updateItem, name='update-item'),
    path('process-order/', views.processOrder, name='process-order'),
    path('view-product/<int:id>', views.view_product, name='view-product'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/login/', views.login, name='account_login'),
    path('add-to-favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorite_product/', views.favorite_product, name='favorite_product'),
    path('remove-from-favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),

]