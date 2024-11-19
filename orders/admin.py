from django.contrib import admin
import datetime
import pytz
from django.utils import timezone
# Register your models here.
from orders.models import Order,OrderItem

class OrderItemInline(admin.TabularInline):
    model=OrderItem
    raw_id_fields=['product']

def mark_as_paid(modeladmin, request, queryset):
    queryset.update(paid=True)

def mark_as_unpaid(modeladmin, request, queryset):
    queryset.update(paid=False)

mark_as_paid.short_description = "Đã thanh toán"
mark_as_unpaid.short_description = "Chưa thanh toán"

def change_public_day(modeladmin, request, queryset):
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time_vn = timezone.now().astimezone(vn_tz)
    queryset.update(updated=current_time_vn)
change_public_day.short_description = "Cập nhật ngày giờ"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','username','first_name','last_name','email','address','paid','created','updated']
    list_filter=['paid','created','updated']
    search_fields=("username",)
    actions = [mark_as_paid, mark_as_unpaid,change_public_day]
    inlines=[OrderItemInline]


