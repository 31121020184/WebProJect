from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from ckeditor_uploader.fields import RichTextUploadingField

class Danhmuc(models.Model):
    name = models.CharField(max_length=150,unique=True)
    def __str__(self):
        return self.name
        
class Thuonghieu(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    image = models.ImageField(upload_to="Store/images",default="Store/images/default.png")

    def __str__(self):
        return self.name 
    
class Sanpham(models.Model):
    GIOI_TINH_CHOICES = [
        ('Nam', 'Nam'),     
        ('Nữ', 'Nữ'),    
        ('Unisex', 'Unisex'), 
    ]
    NONG_DO_CHOICES = [
        ('EDT', 'EDT'),     
        ('EDP', 'EDP'), 
        ('Parfum', 'Parfum'), 
    ]
    DUNG_TICH_CHOICES = [
        ('30ml', '30ml'),
        ('50ml', '50ml'),
        ('100ml', '100ml'),
        ('125ml', '125ml'),
        ('150ml', '150ml'),
        ('200ml', '200ml'),
    ]
    category = models.ForeignKey(Danhmuc, on_delete=models.PROTECT)
    brand = models.ForeignKey(Thuonghieu, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    price = models.FloatField(default=0.0)
    price_origin = models.FloatField(null=True)
    image = models.ImageField(upload_to="Store/images", default="Store/images/default.png")
    content = RichTextUploadingField(blank=True, null=True)
    gioi_tinh = models.CharField(max_length=50, choices=GIOI_TINH_CHOICES, null=True, blank=True)
    nam_san_xuat = models.CharField(max_length=50, null=True, blank=True)
    huong_dau = models.CharField(max_length=100, blank=True, null=True)
    huong_giua = models.CharField(max_length=100, blank=True, null=True)
    huong_cuoi = models.CharField(max_length=100, blank=True, null=True)
    nhom_nuoc_hoa = models.CharField(max_length=100, null=True, blank=True)  
    phong_cach = models.CharField(max_length=100, null=True, blank=True)
    thoi_gian_luu_huong = models.CharField(max_length=50, null=True, blank=True)
    dung_tich = models.CharField(max_length=50,choices=DUNG_TICH_CHOICES, null=True, blank=True)
    nong_do = models.CharField(max_length=50, choices=NONG_DO_CHOICES, null=True, blank=True) 
    viewed = models.IntegerField(default=0)
    public_day = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.name

class Lienhe(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True)
    subject = models.CharField(max_length=264)
    message = models.TextField()

    def __str__(self):
        return self.name +", " + self.subject
    
class UserProfileInfo(models.Model):
    # Create relationship from this class to User
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    # Add any more attribute you want    
    address = models.CharField(max_length=250, unique=False)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to = "Store/images/", default="Store/images/people_default.png")    
    
    def __str__(self):
        return self.user.username 
    

class KhuyenMai(models.Model):
    san_pham = models.ForeignKey(Sanpham, on_delete=models.CASCADE)
    discount = models.FloatField()  
    start_date = models.DateTimeField(default=timezone.now) 
    end_date = models.DateTimeField() 

    def __str__(self):
        return f"{self.san_pham.name} - Giảm {self.discount}%"
    

class TinTuc(models.Model):
    tieu_de = models.CharField(max_length=255) 
    image = models.ImageField(upload_to = "Store/images/", default="Store/images/people_default.png")
    noi_dung = RichTextUploadingField(blank=True, null=True)
    ngay_dang = models.DateTimeField(auto_now_add=True)  
    nguoi_dang = models.ForeignKey(User, on_delete=models.CASCADE) 

    def __str__(self):
        return self.tieu_de