from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from Store.models import Sanpham,UserProfileInfo,KhuyenMai
from .cart import Cart
from django.utils import timezone

from .forms import CartAddProductForm
# from orders.models import OrderItem, Order


@require_POST
# def cart_add(request, product_id):
#     cart = Cart(request)
#     product = get_object_or_404(Sanpham, id=product_id)
   
#     form = CartAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(product=product,
#                  quantity=cd['quantity'],
#                  override_quantity=cd['override'])
#     return redirect('cart:cart_detail')
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Sanpham, id=product_id)
    
    form = CartAddProductForm(request.POST)
        
    if form.is_valid():
            # Kiểm tra xem sản phẩm có khuyến mãi không
            cd = form.cleaned_data
            current_time = timezone.now()
            khuyen_mai = KhuyenMai.objects.filter(
                san_pham=product,
                start_date__lte=current_time,
                end_date__gte=current_time
            ).first()

            # Tính giá đã giảm nếu có khuyến mãi
            if khuyen_mai:
                original_price = product.price
                discounted_price = original_price * (1 - khuyen_mai.discount / 100)
                price_to_add = discounted_price
            else:
                price_to_add = product.price

            # Thêm sản phẩm vào giỏ hàng
            cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'],
                 price=price_to_add)

    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Sanpham, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    username = request.session.get('username', 0)
    for item in cart:
        print(item)
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    return render(request, 'cart/detail.html',
                   {'cart': cart,
                    'username':username,
                    })

 