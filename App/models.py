from django.db import models
import uuid

# Create your models here.


class UserDetails(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    pass_word = models.CharField(max_length=100, default="")
    dob = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True, default="")
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)

    account_type = models.IntegerField(blank=True, null=True, default=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=255)
    category_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    category_image = models.ImageField(
        upload_to='category_images/', null=True, blank=True, default="")

    def __str__(self):
        return self.category_name

class Brands(models.Model):
    brand_name = models.CharField(max_length=255)
    brand_image = models.ImageField(
        upload_to='category_images/', null=True, blank=True, default="")

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_code = models.CharField(max_length=50, unique=True)
    date_added = models.DateField(auto_now_add=True)
    brand = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=20, null=True, blank=True, default="")
    status = models.BooleanField(default=True)
    special = models.BooleanField(default=True)
    product_image = models.ImageField(
        upload_to='product_images/', null=True, blank=True, default="")

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Sale(models.Model):
    sale_code = models.CharField(max_length=50, unique=True)
    order_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50)
    payment = models.CharField(max_length=50)
    sub_total = models.CharField(max_length=15, null=True, blank=True, default="")
    paid = models.CharField(max_length=15, null=True, blank=True, default="")
    due = models.CharField(max_length=15, null=True, blank=True, default="")
    biller = models.CharField(max_length=255)
    product_type = models.CharField(max_length=50, null=True, blank=True, default="")
    customer = models.ForeignKey(UserDetails, on_delete=models.CASCADE)

    def __str__(self):
        return self.sale_code


class Cart(models.Model):
    product_code = models.CharField(max_length=50)
    product_quantity = models.CharField(max_length=500)
    price = models.CharField(max_length=20, null=True, blank=True, default="")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    customer_id = models.CharField(max_length=50)
    prebuilt_id = models.CharField(max_length=50, null=True, blank=True, default="NoID")
    prebuilt_name = models.CharField(max_length=50, null=True, blank=True, default="")
    status = models.CharField(max_length=50, null=True, blank=True, default="In Cart")
    order_date = models.DateField(blank=True, null=True)


class Carousal(models.Model):
    carousal_home_main = models.ImageField(
        upload_to='banners/', null=True, blank=True, default="")


class Banners(models.Model):
    top_left_banner = models.ImageField(
        upload_to='banners/', null=True, blank=True, default="top_left_banner")
    top_right_banner = models.ImageField(
        upload_to='banners/', null=True, blank=True, default="top_right_banner")
    bottom_right_banner = models.ImageField(
        upload_to='banners/', null=True, blank=True, default="bottom_right_banner")


class Blogs(models.Model):
    blog_name = models.CharField(
        max_length=100, null=True, blank=True, default="")
    blog_link = models.CharField(max_length=500, unique=True, default="")
    blog_clean_link = models.CharField(max_length=500, default="")
    blog_description = models.CharField(max_length=500)

    def __str__(self):
        return self.blog_name


class PreBuilt(models.Model):
    modal_name = models.CharField(max_length=255)
    modal_code = models.CharField(max_length=50, unique=True)
    modal_cpu = models.CharField(max_length=50)
    modal_monitor = models.CharField(max_length=50)
    modal_ram = models.CharField(max_length=50)
    modal_motherbrd = models.CharField(max_length=50)
    modal_gpu = models.CharField(max_length=50)
    modal_ssd = models.CharField(max_length=50)
    modal_storage_rom = models.CharField(max_length=50)
    modal_smps = models.CharField(max_length=50)
    modal_offer = models.CharField(max_length=50)
    date_added = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=20, null=True, blank=True, default="")
    status = models.BooleanField(default=True)
    product_image = models.ImageField(
        upload_to='product_images/', null=True, blank=True, default="")
    product_image_1 = models.ImageField(
        upload_to='product_images/', null=True, blank=True, default="")
    product_image_2 = models.ImageField(
        upload_to='product_images/', null=True, blank=True, default="")
    product_image_3 = models.ImageField(
        upload_to='product_images/', null=True, blank=True, default="")
    product_image_4 = models.ImageField(
        upload_to='product_images/', null=True, blank=True, default="")
    product_image_5 = models.ImageField(
        upload_to='product_images/', null=True, blank=True, default="")

    def __str__(self):
        return self.modal_name

class CustomBuilt(models.Model):
    cus_code = models.CharField(max_length=50, unique=True)
    cus_processor = models.CharField(max_length=255, null=True, blank=True, default="")
    cus_cpu_cooler = models.CharField(max_length=255, null=True, blank=True, default="")
    cus_motherbrd = models.CharField(max_length=255, null=True, blank=True, default="")
    cus_ram = models.CharField(max_length=255, null=True, blank=True, default="")
    cus_hardisk = models.CharField(max_length=255, null=True, blank=True, default="")
    cus_gpu = models.CharField(max_length=255, null=True, blank=True, default="")
    cus_powersupply = models.CharField(max_length=255, null=True, blank=True, default="")
    cus_cabinet = models.CharField(max_length=255, null=True, blank=True, default="")
    cus_desc = models.CharField(max_length=1000, null=True, blank=True, default="")
    cus_additional = models.CharField(max_length=1000, null=True, blank=True, default="")
    status = models.CharField(max_length=50, null=True, blank=True, default="In Cart")
    order_date = models.DateField(blank=True, null=True)
    cus_id = models.CharField(max_length=100)

    def __str__(self):
        return self.cus_name