from secrets import choice
from statistics import mode

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True, default="admin")
	email = models.CharField(max_length=200, default="admin@admin.com")

	def __str__(self):
		return self.name


class Product(models.Model):
	SKINCARE="skincare"
	PRODUCT_TAGS = (
		(SKINCARE, "Fiction"),
		("makeup", "Non-Fiction"),
		("bath&body", "Study")
	)
	name = models.CharField(max_length=200)
	tag= models.CharField(max_length=100, choices=PRODUCT_TAGS,default=SKINCARE,null=True,blank=True)
	price = models.FloatField()
	description = models.TextField()
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		product = self.product
		total = product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

class Blog(models.Model):
	BLOG_TAGS = (
		("design", "Design"),
		("fashion", "Fashion")
	)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, null=False)
	description = models.TextField()
	tag= models.CharField(max_length=10, choices=BLOG_TAGS)
	slug = models.SlugField(unique=True, max_length=100)
	published_at = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.title
