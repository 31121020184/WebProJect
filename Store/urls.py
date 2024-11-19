
from django.urls import path
from . import views
app_name ='Store'
urlpatterns = [
    path('', views.index,name='index'),
    path('nuoc-hoa-nam/', views.nuochoanam,name='nuoc-hoa-nam'),
    path('nuoc-hoa-nu/', views.nuochoanu,name='nuoc-hoa-nu'),
    path('unisex/', views.unisex,name='unisex'),
    path('san-pham/<int:pk>/', views.sanpham,name='san-pham'),
    path('khuyen-mai/', views.khuyenmai,name='khuyen-mai'),
    path('thuong-hieu/', views.thuonghieu,name='thuong-hieu'),
    path('tin-tuc/', views.tintuc,name='tin-tuc'),
    path('lien-he/', views.lienhe,name='lien-he'),
    path('brand/<int:pk>/', views.brand,name='brand'),
    path('news/<int:id>/', views.News,name='news'),
    path('dang-ky/', views.dangky,name='dang-ky'),
    path('dang-nhap/', views.dangnhap,name='dang-nhap'),
    path('dang-xuat/', views.dangxuat, name='dang-xuat'),
    path('profile/', views.profile_view, name='profile'),
    path('purchase/', views.purchase, name='purchase'),
    path('search/', views.search_form, name='search'),
    path('shop/', views.shop, name='shop'),
    path('price_filter/', views.filter_by_prices, name='price_filter'),
    path('dieu-khoan/', views.dieukhoan, name='dieu-khoan'),
    path('phuong-thuc-thanh-toan/', views.phuongthuc, name='phuong-thuc-thanh-toan'),  
]
