from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone



User = get_user_model()




# class CategoryManager(models.Manager):

#     CATEGORY_NAME_COUNT_NAME = {
#         'Брюки': 'trouser__count',
#         'Шорты': 'shorts__count'
#     }

#     def get_queryset(self):
#         return super().get_queryset()

#     def get_categories_for_left_sidebar(self):
#         models = get_models_for_count('product_set')
#         qs = list(self.get_queryset().annotate(*models))
#         data = [
#             dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
#             for c in qs
#         ]
#         return data


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    # objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('mp:category_detail', kwargs={'slug': self.slug})


class Color(models.Model):
    name = models.CharField('Цвета', max_length = 100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    cloth = models.CharField(max_length=150, verbose_name='Ткань')
    avaliable = models.BooleanField(default = True)
    def __str__(self):
        return self.title



# class Image(models.Model):
#     trouser = models.ForeignKey(Trouser, related_name = 'photo', on_delete = models.CASCADE)
#     photo = models.ImageField(upload_to='images', blank=True)

#     class Meta:
#         verbose_name = 'Фото'
#         verbose_name_plural = 'Фото'

class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name = 'Пользователь', on_delete = models.CASCADE)
    phone = models.CharField(max_length = 50, verbose_name = 'Номер телефона')
    
    def __str__(self):
        return 'Покупатель: {} {}'.format(self.user.first_name, self.user.last_name)

class Cart(models.Model):

    owner = models.ForeignKey(Customer, null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class CartProduct(models.Model):

    user = models.ForeignKey(Customer, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    count = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.count * self.content_object.price
        super().save(*args, **kwargs)




class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)
