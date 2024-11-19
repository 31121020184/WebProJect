import datetime
import pytz
from django.contrib import admin
from django.db.models import F

# Register your models here.
from .models import Danhmuc, Thuonghieu, Sanpham, Lienhe,UserProfileInfo,KhuyenMai,TinTuc

def change_public_day(modeladmin, request, queryset):
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time_vn = datetime.datetime.now(vn_tz)
    queryset.update(public_day=current_time_vn)
change_public_day.short_description = "Cập nhật ngày giờ"

def change_viewd(modeladmin,request,queryset):
    queryset.update(viewed = F('viewed') +  1)

def change_start_date(modeladmin, request, queryset):
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time_vn = datetime.datetime.now(vn_tz)
    queryset.update(start_date=current_time_vn)
change_start_date.short_description = "Ngày bắt đầu"

def change_end_date(modeladmin, request, queryset):
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time_vn = datetime.datetime.now(vn_tz)
    queryset.update(end_date=current_time_vn)
change_end_date.short_description = "Ngày kết thúc"

change_viewd.short_description ="Cập nhật viewed"
# moduleadmin class
class ProductA(admin.ModelAdmin):
    # exclude=('name',)
    list_display=('name','price','viewed','public_day')
    list_filter=('public_day',)
    search_fields=("name",)
    actions =[change_public_day,change_viewd]

class ThuonghieuA(admin.ModelAdmin):
    list_display=('name','country')
    search_fields=("name",)

# class KhuyenmaiA(admin.ModelAdmin):
#     list_display=('san_pham','discount','start_date','end_date')
#     actions =[change_start_date,change_end_date]

class KhuyenmaiA(admin.ModelAdmin):
    list_display = ('san_pham', 'formatted_discount', 'start_date', 'end_date')
    actions = [change_start_date, change_end_date]

    def formatted_discount(self, obj):
        return f"{int(obj.discount)}%"

    formatted_discount.short_description = 'Discount'
    
def change_ngay_dang(modeladmin, request, queryset):
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time_vn = datetime.datetime.now(vn_tz)
    queryset.update(ngay_dang=current_time_vn)
change_ngay_dang.short_description = "Cập nhật ngày đăng"
class TintucA(admin.ModelAdmin):
    list_display=('tieu_de','ngay_dang','nguoi_dang')
    search_fields=("tieu_de",)
    actions =[change_ngay_dang]

class LienheA(admin.ModelAdmin):
    list_display=('name','email','phone_number','subject')
    search_fields=("name",)

class UserProfileInfoA(admin.ModelAdmin):
    list_display=('user','address','phone')

admin.site.register(Sanpham,ProductA)
admin.site.register(Danhmuc)
admin.site.register(Thuonghieu,ThuonghieuA)
admin.site.register(KhuyenMai, KhuyenmaiA)
admin.site.register(Lienhe,LienheA)
admin.site.register(TinTuc,TintucA)
admin.site.register(UserProfileInfo,UserProfileInfoA)

admin.site.site_header="HỆ THỐNG QUẢN LÝ BÁN HÀNG"

