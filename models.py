from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductInstance(models.Model):
    product = models.ForeignKey(Product, related_name='instances', on_delete=models.CASCADE)
    barcode = models.CharField(max_length=100)
    item_count = models.PositiveIntegerField()

    def __str__(self):
        return self.barcode
