from django.db import models
from django.contrib.auth.models import User

class Guest(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.name


class Order(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id 


class Product(models.Model):
    category = models.CharField(max_length=50,blank=True, null=True)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    size = models.IntegerField()
    photo = models.ImageField(upload_to='media', blank=True, null=True)
    slug = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_pub = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def comments_count(self):
        return self.comments.all().count()
    
    def comments_order(self):
        return self.comments.order_by('-created_at')


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    authored_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.message


