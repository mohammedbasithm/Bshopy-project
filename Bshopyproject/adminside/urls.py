from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.adminhome,name='adminhome'),
    path('user/',views.user,name='user'),
    path('products/',views.products,name='product'),
    path('block_user/<int:user_id>',views.block_user,name='block_user'),
    path('unblock_user/<int:user_id>',views.unblock_user,name='unblock_user'),
    path('delete_user/<int:user_id>',views.delete_user,name='delete_user'),
    path('edit_product/<int:product_id>',views.edit_product,name='edit_product'),
    path('enable_product/<int:product_id>',views.enable_product,name='enable_product'),
    path('disable_product/<int:product_id>',views.disable_product,name='disable_product'),
    path('category/',views.category,name='category'),
    path('add-product/',views.add_product,name='add-product'),
    path('add-category',views.add_category,name='add-category'),
    path('productview/<int:product_id>/',views.product_view,name='product-view'),
    path('enablevariant/<int:variant_id>',views.enable_variant,name='enable_variant'),
    path('disablevariant/<int:variant_id>',views.disable_variant,name='disable_variant'),
    path('add-variant/<int:product_id>',views.add_variant,name='add-variant'),
    path('uploadimages',views.upload_images,name='upload-images'),
    path('edit-variant/<int:variant_id>',views.edit_variants,name='edit-variant'),
    path('disable-category/<int:category_id>',views.disable_category,name='disable-category'),
    path('enable-category/<int:category_id>',views.enable_category,name='enable-category'),
    path('edit-category/<int:category_id>',views.edit_category,name='edit-category'),
    path('delete-image/<int:img_id>',views.delete_image,name='delete-image'),

    path('order-list/',views.order_list,name='order-list'),
    path('admin-order-view/<int:order_id>',views.admin_order_view,name='admin-order-view'),
    path('add-brand',views.add_brand,name='add-brand'),
    path('add-size',views.add_size,name='add-size'),

    path('coupon-list',views.coupon_list,name='coupon-list'),
    path('disable-coupon/<int:coupon_id>',views.disable_coupon,name='disable-coupon'),
    path('enable-coupon/<int:coupon_id>',views.enable_coupon,name='enable-coupon'),
    path('add-coupon',views.add_coupon,name='add-coupon'),
    path('edit-coupon/<int:coupon_id>',views.edit_coupon,name='edit-coupon'),

    path('order-shipped/<int:order_id>',view=views.order_shipped,name='order-shipped'),
    path('order-deliverd/<int:order_id>',views.order_delivered,name='order-deilverd'),
    path('cancel-order/<int:order_id>',views.admin_order_cancel,name='cancel-order'),
    path('return-order/<int:order_id>',views.return_orders,name='return-order'),

    path('sales-report',views.sales_report,name='sales-report'),
    path('sales-report-pdf',views.generate_pdf,name='generate-pdf'),
    path('admin-profile',views.admin_profile,name='admin-profile'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)