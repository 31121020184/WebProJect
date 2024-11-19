from django.db import models
from Store.models import Sanpham
import pytz


class Order(models.Model):
    username = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    @property
    def created_vn(self):
        return self.created.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))

    @property
    def updated_vn(self):
        return self.updated.astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))

        
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items1', on_delete=models.CASCADE)
    product = models.ForeignKey(Sanpham, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
         return str(self.id)