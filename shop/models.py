from django.db import models
from django.urls import reverse


class Category(models.Model):
	name=models.CharField(max_length=250, unique=True)
	slug=models.SlugField(max_length=250, unique=True)
	description=models.TextField(blank=True)
	image=models.ImageField(upload_to='category', blank=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering=('name',)
		verbose_name='Category'
		verbose_name_plural='Categories'

	def get_url(self):
		return reverse('product_by_category', args=[self.slug])

class Product(models.Model):
	name=models.CharField(max_length=250, unique=True)
	slug=models.SlugField(max_length=250, unique=True)
	description=models.TextField(blank=True)
	category=models.ForeignKey(Category, on_delete=models.CASCADE)
	price=models.DecimalField(max_digits=10, decimal_places=2)
	image=models.ImageField(upload_to='product', blank=True)
	stock=models.IntegerField()
	available=models.BooleanField(default=True)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering=('name',)
		verbose_name='Product'
		verbose_name_plural='Products'

	def get_url(self):
		return reverse('product_detail', args=[self.category.slug, self.slug])

class Cart(models.Model):
	cart_id=models.CharField(max_length=250, blank=True)
	date_added=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.cart_id

class CartItem(models.Model):
	cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
	product=models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity=models.IntegerField()
	active=models.BooleanField(default=True)

	def __str__(self):
		return self.product

	def sub_total(self):
		return self.product.price*self.quantity

	class Meta:
		db_table='CartItem'