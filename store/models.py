
from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Collection(models.Model):
    title = models.CharField(max_length=250)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    description = models.CharField(max_length=300)
    discount = models.FloatField()
    # product_set


class Product(models.Model):
    title = models.CharField(max_length=270)
    slug = models.SlugField(default='')
    description = models.TextField()
    unit_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    inventory = models.IntegerField(
        validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)  # optional

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    MEMBERSHIP_STANDARD = 'S'
    MEMBERSHIP_PREMIUM = 'P'
    MEMEBERSHIP_DELUXE = 'D'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_STANDARD, 'Standard'),
        (MEMBERSHIP_PREMIUM, 'Premium'),
        (MEMEBERSHIP_DELUXE, 'Deluxe'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_STANDARD)

    def __str__(self):
        return f'{self.first_name}  {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name']

    # class Meta:
    #     db_table = 'store_customers'
    #     indexes = [
    #         models.Index(fields=['last_name', 'first_name'])
    #     ]


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_SUCCESS = 'S'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_SUCCESS, "Success"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]

    ordered_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='OrderItem')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)


class Address(models.Model):
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    zipcode = models.IntegerField(null=True)
    customers = models.ForeignKey(
        Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
