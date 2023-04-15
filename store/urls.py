from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.NormalBlogListView.as_view(template_name="store/blog.html"), name='blog'),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),


	path('register/', views.register, name='register'),
	path('dashboard/', views.user_dashboard, name='user_dashboard'),

	path('add_product/', views.add_product, name='add_product'),
  path('shop/', views.CustomerProductListView.as_view(template_name="store/shop.html"), name='shop'),
  path('products/<int:pk>/', views.productdetail, name='productdetail'),


	path('unauthorized/', views.unauthorized, name="unauthorized"),

  # ADMIN ROUTES
  path('view_products/', views.ProductListView.as_view(template_name="admin/product_list.html"), name="product_list"),
	path('products/<pk>/detail', views.ProductDetailView.as_view(template_name="admin/product_detail_view.html"), name="product_detail_view"),
	path('products/<pk>/update', views.ProductUpdateView.as_view(template_name="admin/product_update_form.html"), name="product_update_form"),
	path('products/<pk>/delete', views.ProductDeleteView.as_view(template_name="admin/product_delete_form.html"), name="product_delete_form"),
	path('view_customers/', views.CustomerListView.as_view(template_name="admin/customers_list.html"), name="customers_list"),
	path('view_orders/', views.OrderListView.as_view(template_name="admin/orders_list.html"), name="orders_list"),

  # ADMIN BLOG ROUTES
  path('all-blogs/', views.BlogListView.as_view(template_name="admin/blog_list.html"), name="blog_list"),
	path('blog/<slug>/detail', views.BlogDetailView.as_view(template_name="admin/blog_detail_view.html"), name="blog_detail_view"),
	path('blog/<slug>/delete', views.BlogDeleteView.as_view(template_name="admin/blog_delete_form.html"), name="blog_delete_form"),
	path('blog/<slug>/update', views.BlogUpdateView.as_view(template_name="admin/blog_update_form.html"), name="blog_update_form"),
	path('blog/add-blog/', views.add_blog, name='add_blog'),


  path ('admin-user/dashboard', views.admin_dashboard, name='admin_dashboard')
]
