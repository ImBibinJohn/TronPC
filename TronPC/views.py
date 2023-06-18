from django.shortcuts import redirect,render
from App.models import *
import locale
from django.core.exceptions import ObjectDoesNotExist
import datetime
import random
import string

# for maintenance

# def main(request):
#     return render(request, 'UserTemplates/404.html')


def main(request):
    try:
        user_object = UserDetails.objects.get(email='admin@tronpc.web')
    except UserDetails.DoesNotExist:
        user_object = None
    if user_object:
        if server_status.city == 'live':
            if 'userid' in request.session:
                if request.session.has_key('userid'):
                    userid = request.session['userid']
                    cart_price_list = Cart.objects.filter(
                        customer_id=userid).values('price')
                    prices = [item['price'] for item in cart_price_list]
                    total = int(sum(float(price.replace(',', '')) for price in prices))
                    locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
                    total_price = locale.currency(total, grouping=True, symbol=False)

                    cart_quantity = Cart.objects.filter(
                        customer_id=userid).values('product_quantity')
                    quantity = [item['product_quantity'] for item in cart_quantity]
                    cart_list_count = int(sum(float(qua.replace(',', ''))
                                        for qua in quantity))
                    carousal = Carousal.objects.all()
                    banners = Banners.objects.all()
                    category = Category.objects.all()
                    blogs = Blogs.objects.all()
                    brands = Brands.objects.all()
                    products = Product.objects.filter(status=1).order_by('-date_added')
                    specials = Product.objects.filter(special=1, status=1)
                    try:
                        dotd = Product.objects.latest('id')
                        context = {'carousal': carousal, 'banners': banners, 'products': products,
                                'specials': specials, 'category': category, 'blogs': blogs, 'brands': brands,
                                'userid': userid, 'cart_list_count': cart_list_count, 'total_price': total_price, 'dotd': dotd}
                    except ObjectDoesNotExist:
                        context = {'carousal': carousal, 'banners': banners, 'products': products,
                                'specials': specials, 'category': category, 'blogs': blogs, 'brands': brands,
                                'userid': userid, 'cart_list_count': cart_list_count, 'total_price': total_price}
                    return render(request, 'UserTemplates/index.html', context)
                else:
                    return render(request, 'UserTemplates/login.html')
            else:
                total_customers = Cart.objects.filter(
                customer_id__contains='Guest').count()
            if total_customers > 15:
                customer_ids_to_delete = Cart.objects.filter(
                    customer_id__contains='Guest').order_by('-id').values_list('id', flat=True)[15:]
                for customer_id in customer_ids_to_delete:
                    Cart.objects.filter(id=customer_id).delete()

                code_length = 3
                x = datetime.datetime.now()
                salt = x.strftime("%f")[3:]
                pro_cod = 'Guest-' + salt + \
                    ''.join(random.choices(string.ascii_letters +
                            string.digits, k=code_length))
                request.session['userid'] = pro_cod
                return redirect('index')
            else:
                code_length = 3
                x = datetime.datetime.now()
                salt = x.strftime("%f")[3:]
                pro_cod = 'Guest-' + salt + \
                    ''.join(random.choices(string.ascii_letters +
                            string.digits, k=code_length))
                request.session['userid'] = pro_cod
                return redirect('index')
        else:
            return redirect('under_maintenance')
    else:
        return redirect('login')