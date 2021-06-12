from django.urls import path
from .views import ProductDetailView, index, about, detail, CategoryDetailView, CartView, add, DeleteFromCartView, product_list, ChangeCountView

app_name = 'mp'
urlpatterns = [
    path('', product_list, name='base'),
    # path('', index, name='home'),
    # path('about', about, name='about'),
    # path('detail/<int:trouser_id>', detail, name="detail"),
    # path('index', index, name='index'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name = 'product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', add, name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-count/<str:ct_model>/<str:slug>/', ChangeCountView.as_view(), name='change_qty'),

]
