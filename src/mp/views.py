from django.db import transaction
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View

from .utils import calc_cart
from .forms import OrderForm
from .mixins import CategoryDetailMixin, CartMixin
from django.shortcuts import render, redirect, get_object_or_404
from .models import Color, Category, Customer, Cart, CartProduct, Product

# class BaseView(CartMixin, View):

#     def get(self, request, *args, **kwargs):
#         categories = Category.objects.get_categories_for_left_sidebar()
#         products = LatestProducts.objects.get_products_for_main_page(
#             'trouser', 'shorts', with_respect_to='trouser'
#         )
#         context = {
#             'categories': categories,
#             'products': products,
#             'cart': self.cart
#         }
#         return render(request, 'base.html', context)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(avaliable=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'base.html', 
                {
                    'category':category,
                    'categories':categories, 
                    'products':products
                })

class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):


    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


# class AddToCartView(CartMixin, View):

def add(self, product, quantity=1, update_quantity=False):
    
    """
    ?????????????????? ?????????? ?? ?????????????? ?????? ?????????????????? ?????? ????????????????????.
    """
    product_id = str(product.id)
    if product_id not in self.cart:
        self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
    if update_quantity:
        self.cart[product_id]['quantity'] = quantity
    else:
        self.cart[product_id]['quantity'] += quantity
    self.save()
    # def get(self, request, *args, **kwargs):
        # ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        # content_type = Cart.objects.get(model=ct_model)
        # product = content_type.model_class().objects.get(slug=product_slug)
        # cart_product, created = CartProduct.objects.get_or_create(
        #     user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        # )
    #     if created:
    #         self.cart.products.add(cart_product)
    #     calc_cart(self.cart)
    #     messages.add_message(request, messages.INFO, "?????????? ?????????????? ????????????????")
    #     return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        calc_cart(self.cart)
        messages.add_message(request, messages.INFO, "?????????? ?????????????? ????????????")
        return HttpResponseRedirect('/cart/')


class ChangeCountView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        count = int(request.POST.get('qty'))
        cart_product.count = count
        cart_product.save()
        calc_cart(self.cart)
        messages.add_message(request, messages.INFO, "??????-???? ?????????????? ????????????????")
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, '?????????????? ???? ??????????! ???????????????? ?? ???????? ????????????????')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


def index(request):
    products = Trouser.objects.order_by('id')
    return render(request, 'index.html', {'title': '?????????????? ???????????????? ??????????', 'products': products})


def about(request):
    return render(request, 'about.html')

def detail(request, trouser_id):
    trouser = Product.objects.get(id = trouser_id)
    colors = Color.objects.filter(trouser = trouser)
    print(colors)
    return render(request, 'detail.html', {'trouser': trouser, 'colors': colors})

