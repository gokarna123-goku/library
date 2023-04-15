
import datetime
import json
from random import choice

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.defaultfilters import slugify
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import AddBlogForm, AddProductForm, RegisterForm
from .models import *
from .models import Customer
from .utils import cartData, guestOrder


def about(request):
   return render(request, 'store/about.html')

def contact(request):
   return render(request, 'store/contact.html')


class NormalBlogListView(ListView):
	paginate_by = 10
	model = Blog
	filter = ['published_by']
	
	
def blog(request):
   return render(request, 'store/blog.html')
   
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username = username, password = password)
            customer = Customer(user = user, name=username, email=email)
            customer.save()
            login(request, user)
            return redirect('store')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def unauthorized(request):
	return render(request, "store/unauthorized.html")

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def productdetail(request,pk):
	product = Product.objects.get(id = pk)
	# Ref: https://stackoverflow.com/questions/22816704/django-get-a-random-object
	pks = Product.objects.values_list('pk', flat=True)
	random_pks = [choice(pks), choice(pks), choice(pks), choice(pks)]
	random_products = Product.objects.filter(id__in= random_pks)

	data = cartData(request)

	cartItems = data['cartItems']


	return render(request, 'store/product.html', {'product': product, 'others': random_products, 'cartItems': cartItems})


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']


	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def add_product(request):
	if request.user.is_superuser:
		if request.method == "POST":
			form = AddProductForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				return redirect('/')
		else:
			form = AddProductForm()

		return render(request, "admin/add_product.html",{
			'form':form
		})
	return redirect('unauthorized')

class CustomerProductListView(ListView):
	model = Product
	paginate_by = 4

	# REF: https://stackoverflow.com/questions/13416502/django-search-form-in-class-based-listview
	def get_queryset(self):
		query = self.request.GET.get('q')

		if query:
			objects = self.model.objects.filter(Q(name__icontains=query) | Q(tag__icontains=query))
		else:
			objects = self.model.objects.all()
		return objects


class ProductListView(LoginRequiredMixin, ListView):
	login_url = "/login/"
	model = Product
	paginate_by = 4
class ProductDetailView(LoginRequiredMixin, DetailView):
	login_url = "/login/"
	model = Product
	paginate_by = 4

class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	login_url = "/login/"
	model = Product
	fields = ["name", "price", "description",  "image", 'tag']
	template_name_suffix: str = "_update_form"
	success_url = '/view_products/'
	success_message = "Product updated successfully"

class ProductDeleteView(LoginRequiredMixin,SuccessMessageMixin, DeleteView):
	login_url = "/login/"
	model = Product
	success_url = "/view_products/"
	success_message = "Deleted Product Successfully"


class OrderListView(LoginRequiredMixin, ListView):
	login_url = "/login/"
	model = Order
	paginate_by = 10


class CustomerListView(LoginRequiredMixin, ListView):
	login_url = "/login/"
	model = Customer
	paginate_by = 10


######### BLOG SECTION #########
class BlogListView(LoginRequiredMixin, ListView):
	login_url = "/login/"
	model= Blog
	paginate_by = 10


class BlogDetailView(LoginRequiredMixin, DetailView):
	login_url = "/login/"
	model= Blog
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

class BlogDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
	login_url = "/login/"
	model = Blog
	success_url = "/all-blogs/"
	success_message = "Deleted Blog Successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


def add_blog(request):
	if request.user.is_superuser:
		if request.method == "POST":
			form = AddBlogForm(request.POST)
			if form.is_valid():
				newpost = form.save(commit=False)
				newpost.user = request.user
				newpost.slug = slugify(newpost.title)
				newpost.save()
				form.save_m2m()
				return redirect('/all-blogs/')
		else:
			form = AddBlogForm()
		return render(request, "admin/add_blog.html",{
			'form':form
		})
	return redirect('unauthorized')


class BlogUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	login_url = "/login/"
	model = Blog
	fields = ["title", "tag", "description", ]
	template_name_suffix: str = "_update_form"
	success_url = '/all-blogs/'
	success_message = "Updated Blog Successfully"


@login_required(login_url='/login/')
def admin_dashboard(request):
	if request.user.is_superuser:
		blog_count = Blog.objects.count()
		customers_count = Customer.objects.count()
		orders_count = Order.objects.count()
		products_count = Product.objects.count()
		context = {
			"blog_count": blog_count,
			"customers_count": customers_count,
			"orders_count": orders_count,
			"products_count": products_count
		}
		return render(request, "admin/dashboard.html",context)
	else:
		return redirect('unauthorized')


@login_required(login_url='/login/')
def user_dashboard(request):
	customer = Customer.objects.get(user=request.user)
	orders_count = Order.objects.filter(customer=customer)
	context = {
		"orders": orders_count,
		"customer": customer
	}
	return render(request, "store/dashboard.html",context)
