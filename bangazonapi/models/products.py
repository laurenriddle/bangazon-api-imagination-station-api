from django.db import models
from .customers import Customer
from .producttypes import ProductType
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE

class Product(SafeDeleteModel):
    """
    This represents a product object

    foreign keys: customer, product_type

    Author: Ken Boyd
    """
    _safedelete_policy = SOFT_DELETE
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField()
    location = models.CharField(max_length=75)
    image_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name="customers")

    # The related_name attribute specifies the name of the reverse relation
    product_type = models.ForeignKey(
        ProductType, on_delete=models.DO_NOTHING, related_name="products")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = ("product")
        verbose_name_plural = ("products")

    def __str__(self):
        return f'{self.name} costs ${self.price} and was posted by {self.customer.user.first_name} {self.customer.user.last_name}.'
