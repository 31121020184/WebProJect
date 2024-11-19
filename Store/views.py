from django.shortcuts import redirect, render,get_object_or_404
from Shopnuochoa import settings
from Store import models
import datetime
import requests
from django.utils import timezone
import feedparser
from django.contrib import messages
from bs4 import BeautifulSoup
import os
import re
import pandas as pd
from cart.forms import CartAddProductForm
from . import forms
from .models import UserProfileInfo
from orders.models import Order,OrderItem
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from Shopnuochoa.settings import EMAIL_HOST_USER
from cart.cart import Cart
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, F, Value
from django.contrib.auth.decorators import login_required
# Create your views here.
subcategory_list = models.Danhmuc.objects.all()
danhmuc = 0
now = datetime.datetime.now()
search_str = ''
subcategory = 0
def index(request):
    cart = Cart(request)
    nuochoanu = models.Danhmuc.objects.filter(id=2)
    unisex = models.Danhmuc.objects.filter(id=3)
    nuochoanam = models.Danhmuc.objects.filter(id=1)
    username = request.session.get('username', 0)
    danhsachsp_new = models.Sanpham.objects.order_by("-public_day")
    danhsachsp_nam = models.Sanpham.objects.filter(category_id=1).order_by("-public_day")[:20]
    danhsachsp_nu = models.Sanpham.objects.filter(category_id=2).order_by("-public_day")[:20]
    danhsachsp_unisex = models.Sanpham.objects.filter(category_id=3).order_by("-public_day")[:20]
    twenty_newest = danhsachsp_new[:20]

    respone = render(request,"Store/index.html",{'twenty_newest':twenty_newest,
                                            'twenty_newest_nam': danhsachsp_nam,
                                            'twenty_newest_nu': danhsachsp_nu,
                                            'twenty_newest_unisex': danhsachsp_unisex,
                                             'subcategories':subcategory_list,
                                             'nuochoanu':nuochoanu,
                                             'unisex':unisex,
                                             'username':username,
                                             'nuochoanam':nuochoanam,
                                             'today':now,
                                             'cart': cart,
                                             })
    return respone


# def sanpham(request,pk):
#     cart = Cart(request)
#     product_select = models.Sanpham.objects.get(pk=pk)
#     username = request.session.get('username', 0)
#     # Khi người dùng chọn xem 1 sp tăng view của sp lên 1
#     models.Sanpham.objects.filter(pk=product_select.pk).update(viewed =F('viewed')+ 1)
#     thuonghieu = product_select.brand
#     product_select.refresh_from_db()
#     return render(request,"Store/san-pham.html",
#                   {'product':product_select,
#                    'thuonghieu':thuonghieu,
#                     'username':username,
#                     'cart': cart,
#                    'subcategories':subcategory_list,
#                    })

def sanpham(request,pk):
    cart = Cart(request)
    product_select = models.Sanpham.objects.get(pk=pk)
    username = request.session.get('username', 0)
    # Khi người dùng chọn xem 1 sp tăng view của sp lên 1
    models.Sanpham.objects.filter(pk=product_select.pk).update(viewed =F('viewed')+ 1)
    thuonghieu = product_select.brand
    product_select.refresh_from_db()
    cart_product_form = CartAddProductForm()
    # Đọc rules
    #rules = pd.read_csv(os.path.join(settings.MEDIA_ROOT,'store/rules.csv'), squeeze=True, index_col=0)
    rules = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'Store/rules.csv'), index_col=0)

    lst = rules.values.tolist()
    list_rules =[]
    for item in lst:
        result = item
        if str(pk) in re.findall('\d+[, \d+]*', item[0])[0].split(','):
            list_rules = re.findall('\d+[, \d+]*', item[1])[0].split(',')


    list_asc_products=[]
    for i in list_rules:
        list_asc_products.append(models.Sanpham.objects.get(pk=int(i)))
    return render(request,"Store/san-pham.html",
                  {'product':product_select,
                   'thuonghieu':thuonghieu,
                    'username':username,
                    'cart_product_form':cart_product_form,
                    'cart': cart,
                    'list_asc_products':list_asc_products,
                   'subcategories':subcategory_list,
                   })

def gioithieu(request):
    cart = Cart(request)
    username = request.session.get('username', 0)
    return render(request,'Store/gioi-thieu.html',
                  {'username':username,
                   'subcategories':subcategory_list,
                    'cart': cart,
                   })

def dieukhoan(request):
    cart = Cart(request)
    username = request.session.get('username', 0)
    return render(request,'Store/dieu-khoan.html',
                  {'username':username,
                   'subcategories':subcategory_list,
                    'cart': cart,
                   })
def phuongthuc(request):
    cart = Cart(request)
    username = request.session.get('username', 0)
    return render(request,'Store/phuong-thuc-thanh-toan.html',
                  {'username':username,
                   'subcategories':subcategory_list,
                    'cart': cart,
                   })

def nuochoanam(request):
    # Danh sách sản phẩm
    cart = Cart(request)
    username = request.session.get('username', 0)
    category_id = 1  
    danhsachsp_nam = models.Sanpham.objects.filter(category_id=category_id).order_by("-public_day")
    three_newest = danhsachsp_nam[:3]

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(danhsachsp_nam, 9)  

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)  
    except EmptyPage:
        products = paginator.page(paginator.num_pages) 

    return render(request, "Store/nuoc-hoa-nam.html", {
        'products': products,
        'subcategories': subcategory_list,  
        'username': username,
        'cart': cart,
        'three_newest': three_newest,
        'category_id': category_id,
    })


def nuochoanu(request):
    cart = Cart(request)
    category_id = 2
    danhsachsp_nu = models.Sanpham.objects.filter(category_id=category_id).order_by("-public_day")
    username = request.session.get('username', 0)
    three_newest = danhsachsp_nu[:3]
   

    page = request.GET.get('page', 1)
    paginator = Paginator(danhsachsp_nu, 9)  

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)  
    except EmptyPage:
        products = paginator.page(paginator.num_pages) 
    return render(request,'Store/nuoc-hoa-nu.html',{
        'products': products,
        'username':username,
        'subcategories':subcategory_list,
        'cart': cart,
        'category_id': category_id,
        'three_newest':three_newest
    })

def unisex(request):
    cart = Cart(request)
    category_id = 3
    danhsachsp_unisex = models.Sanpham.objects.filter(category_id=category_id).order_by("-public_day")
    username = request.session.get('username', 0)
    three_newest = danhsachsp_unisex[:3]
    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(danhsachsp_unisex, 9)  

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)  
    except EmptyPage:
        products = paginator.page(paginator.num_pages) 
    return render(request,'Store/unisex.html',{
        'products': products,
        'username':username,
        'subcategories':subcategory_list,
        'cart': cart,
        'category_id': category_id,
        'three_newest':three_newest
    })

def shop(request):
    cart = Cart(request)
    product_list = models.Sanpham.objects.all().order_by("-public_day")
    three_newest = product_list[:3]
    page = request.GET.get('page', 1) # Trang bắt đầu
    paginator = Paginator(product_list, 9) # số product/trang

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    username = request.session.get('username', 0)
    return render(request,"Store/shop.html",{'three_newest':three_newest,
                                             'products':products,
                                             'subcategories':subcategory_list,
                                             'username':username,
                                             'cart': cart,
                                             })

def thuonghieu(request):
    cart = Cart(request)
    thuong_hieu_list = models.Thuonghieu.objects.all()
    username = request.session.get('username', 0)
    return render(request, 'Store/thuong-hieu.html', {
            'thuong_hieu_list': thuong_hieu_list,
            'cart': cart,
            'subcategories':subcategory_list,
            'username':username,})
def khuyenmai(request):
    cart = Cart(request)
    current_time = timezone.now()
    username = request.session.get('username', 0)
    # Lấy các khuyến mãi đang hoạt động
    khuyen_mai = models.KhuyenMai.objects.filter(start_date__lte=current_time, end_date__gte=current_time)

    # Lấy danh sách sản phẩm liên quan đến khuyến mãi và tính giá sau giảm giá
    products = []
    for km in khuyen_mai:
        product = km.san_pham
        original_price = product.price
        discounted_price = int(original_price * (1 - km.discount / 100))  # Tính giá sau giảm giá
        products.append({
            'id': product.id,  # Lấy product.id
            'product': product,
            'original_price': original_price,
            'discounted_price': discounted_price,
            'subcategories':subcategory_list,
            'discount': km.discount,
            'start_date': km.start_date, 
            'end_date': km.end_date,   
            
        })
    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)

    try:
        products_paginated = paginator.page(page)
    except PageNotAnInteger:
        products_paginated = paginator.page(1)
    except EmptyPage:
        products_paginated = paginator.page(paginator.num_pages)

    return render(request, 'Store/khuyen-mai.html', {
        'cart': cart,
        'username':username,
        'khuyen_mai': khuyen_mai,
        'products': products_paginated,
    })

def tintuc(request):
    cart = Cart(request)
    tintuc = models.TinTuc.objects.all().order_by("-ngay_dang")
    four_newest = tintuc[:4]
    username = request.session.get('username', 0)
    return render(request, "Store/tin-tuc.html", {
        'username': username,
        'tintucs': tintuc,
        'subcategories':subcategory_list,
        'four_newest':four_newest,
        'cart': cart,
    })

def News(request,id):
    cart = Cart(request)
    tin_tuc = get_object_or_404(models.TinTuc, id=id)
    tintuc = models.TinTuc.objects.all().order_by("-ngay_dang")
    four_newest = tintuc[:4]
    username = request.session.get('username', 0)
    return render(request, "Store/news.html", {
        'username': username,
        'cart': cart,
        'subcategories':subcategory_list,
        'four_newest':four_newest,
        'tin_tuc':tin_tuc
    })

def lienhe(request):
    cart = Cart(request)
    resutl = '...'
    form = forms.FormContact()
    if request.method == 'POST':
        resutl="Form đã có POST"
        form = forms.FormContact(request.POST)
        resutl="Form đã có contact"
        # Thêm validation cho form
        if form.is_valid():
           resutl="Form đã valid!"
        #    request.POST._mutable = True
           post = form.save(commit=False)
           post.name = form.cleaned_data['name']
           post.phone_number = form.cleaned_data['phone_number']
           post.email = form.cleaned_data['email']
           post.subject = form.cleaned_data['subject']
           post.message = form.cleaned_data['message']
           post.save()
           resutl = "Chúng tôi đã nhận thông tin quý khách và sẽ phản hồi sớm. Cảm ơn quý khách"
   
           form =None # ẩn form
        #    form = forms.FormContact()
    last_visit =  request.session.get('last_visit', False)
    username = request.session.get('username', 0)
    return render(request,"Store/lien-he.html",
                  {'form': form,
                   'resutl':resutl,
                   'last_visit':last_visit,
                   'cart': cart,
                   'subcategories':subcategory_list,
                   'username':username,
                   })

def brand(request,pk):
    cart = Cart(request)
    if pk !=0:
        product_list = models.Sanpham.objects.filter(brand_id=pk).order_by("-public_day")
    username = request.session.get('username', 0)
    page = request.GET.get('page', 1) # Trang bắt đầu
    paginator = Paginator(product_list, 9) # số product/trang

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request,"store/brand.html",{
                                             'products':products,
                                             'subcategories':subcategory_list,
                                             'pk':pk,
                                             'cart': cart,
                                             'subcategories':subcategory_list,
                                             'username':username,
                                             })

def dangky(request):
    registered = False
    if request.method == "POST":
        form_user = forms.UserForm(data=request.POST)
        form_por = forms.UserProfileInfoForm(data=request.POST)

        if (form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']):
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            profile = form_por.save(commit=False)
            profile.user = user
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()

            registered = True

              # Lấy email và username trước khi reset biểu mẫu
            email_address = form_user.cleaned_data['email']
            username = form_user.cleaned_data['username']
            # Reset lại biểu mẫu sau khi đăng ký thành công
            form_user = forms.UserForm() 
            form_por = forms.UserProfileInfoForm()

            subject ='Tài khoản của quý khách tại K&T PERFURM đã được tạo.'
            message ='Hãy trải nghiệm việc mua sắm online các sản phẩm nước hoa tại K&T PERFURM.<br/> Trân trọng'
            recpient = str(email_address)

            html_content ='<h2 style="color:blue"><i>Kính chào '+ username +',</i></h2>'\
                     + '<p> Cám ơn bạn sữ dụng dịch vụ <strong>Web của chúng tôi</strong>.</p>'\
                     +'<h4 style=" color:red">'+ message +'</h4>'
        
            msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER,[recpient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        elif form_user.cleaned_data['password'] != form_user.cleaned_data['confirm']:
            form_user.add_error(
                'confirm', 'Password và confirm password không giống nhau!')
            print(form_user.errors, form_por.errors)
    else:
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()

    last_visit =  request.session.get('last_visit', False)
    username = request.session.get('username', 0)
    return render(request, 'Store/dang-ky.html',
                  {'subcategories': subcategory_list,
                   'form_user': form_user,
                   'form_por': form_por,
                   'registered': registered,
                   'username': username,
                   'last_visit':last_visit
                   })
    

def search_form(request):
    cart = Cart(request)
    global subcategory
    product_items = 0
    three_newest = models.Sanpham.objects.all().order_by("-public_day")[:3]
    product_list = []
    search_str = ''  # Khởi tạo search_str là rỗng

    if request.method == 'GET':
        form = forms.FormSearch(request.GET, models.Sanpham)
        if form.is_valid():
            category = form.cleaned_data['category_id']  
            search_str = form.cleaned_data['name']  
            print(f"Danh mục: {category}, Chuỗi tìm kiếm: '{search_str}'") 

            if category != 0:  # khi ng dùng chọn 1 mục cụ thể
                product_list = models.Sanpham.objects.filter(
                    category=category, name__icontains=search_str
                ).order_by("-public_day")
            else:  # khi người dùng chọn tất cả
                product_list = models.Sanpham.objects.filter(
                    name__icontains=search_str).order_by("-public_day")

    product_items = len(product_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 9)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    username = request.session.get('username', 0)
    return render(request, "Store/search.html",
                  {
                      'three_newest': three_newest,
                      'subcategories': subcategory_list,
                      'products': products,
                      'pk': subcategory,
                      'cart': cart,
                      'username': username,
                      'product_items': product_items,
                      'subcategory': subcategory,
                      'search_str': search_str  
                  })

def dangnhap(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # result = "Hello " + username
            request.session['username'] = username
           
            username = request.session.get('username', 0)
            return redirect('Store:index')
        else:
            print("You can't login.")
            print("Username: {} and password: {}".format(username, password))
            login_result = "Username hoặc password không chính xác!"
            return render(request, "Store/dang-nhap.html", {'login_result': login_result})
    else:
        return render(request, "Store/dang-nhap.html")

@login_required
def dangxuat(request):
    logout(request)
    return redirect('Store:index')
    # result = "Quý khách đã logout. Quý khách có thể login trở lại"
    # return render(request, "store/login.html", {'logout_result': result})



def purchase(request):
    cart = Cart(request)
    username = request.session.get('username', 0)
    orders = Order.objects.filter(username=request.user.username).order_by('-created')
    
    # Tạo danh sách chi tiết đơn hàng
    order_details = {}
    for order in orders:
        items = order.items1.all()  # Lấy tất cả các mục trong đơn hàng
        total_order_price = 0  # Khởi tạo tổng tiền cho đơn hàng
        for item in items:
            total_price = item.price * item.quantity
            total_order_price += total_price  # Cộng dồn tổng tiền cho đơn hàng
            
            # Nếu order_id chưa có trong order_details, khởi tạo một danh sách
            if order.id not in order_details:
                order_details[order.id] = {
                     'order_id': f"{order.id}{order.created.strftime('%Y%m%d')}",  # Tạo mã đơn hàng
                    'order_date': order.created_vn,
                    'products': [],  # Danh sách sản phẩm
                    'total_price': 0,  # Tổng tiền cho đơn hàng
                    'paid': order.paid,
                }
            
            # Thêm sản phẩm vào danh sách sản phẩm của đơn hàng
            order_details[order.id]['products'].append({
                'product_name': item.product.name,
                'product_image': item.product.image.url,
                'quantity': item.quantity,
                'price': item.price,
                'total_price': total_price,
                'category_name': item.product.category.name,
            })
        
        # Cập nhật tổng tiền cho đơn hàng
        order_details[order.id]['total_price'] = total_order_price

    if not orders.exists():
        message = "Bạn chưa có lịch sử mua nào...!"
    else:
        message = None  # Không có thông báo nếu có đơn hàng

    # Chuyển đổi order_details từ dict sang list để dễ dàng render
    order_details_list = list(order_details.values())

    return render(request, 'Store/purchase.html', {
        'orders': order_details_list,
        'username': username,
        'subcategories':subcategory_list,
        'message': message,
        'cart': cart,
    })
def profile_view(request):
    cart = Cart(request)
    username = request.session.get('username', 0)
    success_message = None
    user = request.user  # Lấy đối tượng người dùng hiện tại

    # In ra thông tin để kiểm tra
    print("Username:", user.username)  # Kiểm tra tên đăng nhập
    print("Email:", user.email)  # Kiểm tra email

    user_profile = UserProfileInfo.objects.get(user=user)

    # Khởi tạo biểu mẫu với dữ liệu hiện tại
    form_user = forms.UserForm(instance=user)
    form_por = forms.UserProfileInfoForm(instance=user_profile)

    if request.method == "POST":
        form_user = forms.UserForm(data=request.POST, instance=user)
        form_por = forms.UserProfileInfoForm(data=request.POST, instance=user_profile)

        if form_user.is_valid() and form_por.is_valid():
            user = form_user.save(commit=False)
            password = form_user.cleaned_data.get('password')

            # Cập nhật mật khẩu nếu có
            if password:
                user.set_password(password)  # Cập nhật mật khẩu
            user.save()  # Lưu thông tin người dùng

            # Cập nhật thông tin hồ sơ
            user_profile.phone = form_por.cleaned_data['phone']
            user_profile.address = form_por.cleaned_data['address']
            user_profile.save()  # Lưu thông tin hồ sơ

            success_message = "Cập nhật thành công!"  # Thông báo thành công
        else:
            print(form_user.errors)  # In ra lỗi nếu có
            print(form_por.errors)  # In ra lỗi nếu có

    return render(request, 'Store/profile.html', {
        'form_user': form_user,
        'form_por': form_por,
        'subcategories':subcategory_list,
        'cart': cart,
        'username': username,
        'success_message': success_message, 
        'phone_number': user_profile.phone,
        'address': user_profile.address,
    })


def filter_by_prices(request):
    username = request.session.get('username', 0)
    three_newest = models.Sanpham.objects.all().order_by("-public_day")[:3]
    
    # Lấy các tham số từ yêu cầu GET
    category_id = request.GET.get('category_id', '0')  
    search_str = request.GET.get('name_1', '')
    result = "" 

    # Xử lý giá
    try:
        price_from = float(request.GET.get('price_from', 0))
        price_to = float(request.GET.get('price_to', float('inf')))
        if price_from > price_to:
            price_from, price_to = price_to, price_from
    except (ValueError, TypeError):
        price_from, price_to = 0, float('inf')

    # Lọc sản phẩm
    product_list = models.Sanpham.objects.all()  # Lấy tất cả sản phẩm

    # Nếu category_id không phải là 0, lọc theo category_id
    if category_id != '0':
        product_list = product_list.filter(category_id=category_id)

    # Lọc theo tên sản phẩm nếu có từ khóa tìm kiếm
    if search_str:
        product_list = product_list.filter(name__icontains=search_str)

    # Lọc theo khoảng giá
    product_list = product_list.filter(price__gte=price_from, price__lte=price_to)
    
    # Tính số lượng sản phẩm tìm thấy
    product_items = product_list.count()  # Sử dụng count() để đếm số lượng sản phẩm

    # Tạo kết quả cho thông báo
    if product_items > 0:
        result = f"Tìm thấy {product_items} sản phẩm"
        if search_str:
            result += f" có từ '{search_str}'"
        result += f" trong khoảng giá từ {price_from:,.0f} đ đến {price_to:,.0f} đ."
    else:
        result = "Không tìm thấy sản phẩm nào!"

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(product_list, 9)  # số sản phẩm trên mỗi trang

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, "Store/shop.html", {
        'three_newest': three_newest,
        'products': products,
        'username': username,
        'subcategories':subcategory_list,
        'category_id': category_id, 
        'search_str': search_str,
        'result': result,  
        'product_items': product_items,  
    })
# def filter_by_prices(request):
#     username = request.session.get('username', 0)
#     three_newest = models.Sanpham.objects.all().order_by("-public_day")[:3]
    
#     # Lấy các tham số từ yêu cầu GET
#     category_id = request.GET.get('category_id', '0')  # Lấy category_id từ form
#     search_str = request.GET.get('name_1', '')
#     result = "" 
#     # subcategory_name = ""  

#     # Xử lý giá
#     try:
#         price_from = float(request.GET.get('price_from', 0))
#         price_to = float(request.GET.get('price_to', float('inf')))
#         if price_from > price_to:
#             price_from, price_to = price_to, price_from
#     except (ValueError, TypeError):
#         price_from, price_to = 0, float('inf')

#     # Lọc sản phẩm theo category_id
#     product_list = models.Sanpham.objects.filter(category_id=category_id)  # Lọc theo category_id

#     if search_str:
#         product_list = product_list.filter(name__icontains=search_str)

#     product_list = product_list.filter(price__gte=price_from, price__lte=price_to)
#     result += f" Khoảng giá: từ {price_from:,.0f} đ đến {price_to:,.0f} đ."

   
#     product_items = len(product_list)

#     # Phân trang
#     page = request.GET.get('page', 1)
#     paginator = Paginator(product_list, 9) 

#     try:
#         products = paginator.page(page)
#     except PageNotAnInteger:
#         products = paginator.page(1)
#     except EmptyPage:
#         products = paginator.page(paginator.num_pages)

#     return render(request, "Store/shop.html", {
#         'three_newest': three_newest,
#         'products': products,
#         'username': username,
#         'category_id': category_id,  
#         'search_str': search_str,
#         'result': result,  
#         'product_items': product_items,  
#     })