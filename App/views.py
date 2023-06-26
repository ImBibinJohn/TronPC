import os
import json
import uuid
import random
import string
import locale
import hashlib
import datetime
from App.models import *
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from googleapiclient.discovery import build
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse

# -------------------USER VIEWS------------------------------#

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)

def error_404(request, *args, **kwargs):
    return render(request, 'UserTemplates/404_robo.html', status=404)

def change_init_page(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid = request.session['adminid']
            if request.method == 'POST':
                day = request.POST['dayInput']
                month = request.POST['monthInput']
                year = request.POST['yearInput']
                db_change = UserDetails.objects.get(email='admin@tronpc.web')
                db_change.city = day+month+year
                db_change.save()
                return redirect('adminIndex')
            else:
                return redirect('adminIndex')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def change_init_page_to_online(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid = request.session['adminid']
            if request.method == 'POST':
                db_change = UserDetails.objects.get(email='admin@tronpc.web')
                db_change.city = 'live'
                db_change.save()
                return redirect('adminIndex')
            else:
                return redirect('adminIndex')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def under_maintenance(request):
    try:
        user_object = UserDetails.objects.get(email='admin@tronpc.web')
    except UserDetails.DoesNotExist:
        user_object = None
        return redirect('login')
    if user_object:
        if user_object.city == 'live':
            return redirect('/')
        else:
            current_date = datetime.datetime.now()
            db_change = UserDetails.objects.get(email='admin@tronpc.web')
            db_day = db_change.city[:2]
            db_month = db_change.city[2:4]
            db_year = db_change.city[-4:]
            sYear = current_date.year
            eYear = db_year
            sMonth = current_date.month
            eMonth = db_month
            sDay = current_date.day
            eDay = db_day
            sHour = current_date.hour
            eHour = '0'
            sMinute = current_date.minute
            eMinute = '0'
            sSecond = current_date.second
            eSecond = '0'
            context = {'sYear':sYear,'eYear':eYear,'sMonth':sMonth,'eMonth':eMonth,'sDay':sDay,
                    'eDay':eDay,'sHour':sHour,'eHour':eHour,'sMinute':sMinute,'eMinute':eMinute,
                    'sSecond':sSecond,'eSecond':eSecond}
            return render(request, 'UserTemplates/404.html',context)
    else:
        return redirect('login')



def maintenance_login(request):
    if request.method == 'POST':
        user_email = request.POST['user_email']
        user_pass = request.POST['user_pass']
        try:
            user_object = UserDetails.objects.get(email=user_email)
        except UserDetails.DoesNotExist:
            user_object = None
        if user_object:
            if user_object and user_object.account_type == False:
                unew = UserDetails.objects.get(email=user_email)
                providedText = unew.pass_word
                providedText, salt = providedText.split(':')
                checked = bool(providedText == hashlib.sha256(
                    salt.encode() + user_pass.encode()).hexdigest())
                if checked == True:
                    request.session['adminid'] = unew.id
                    return redirect('adminIndex')
                else:
                    user_email = request.POST['user_email']
                    pas = "password not correct"
                    return render(request, 'UserTemplates/maintenance.html', {'pas': pas, 'user_email': user_email})
        else:
            print('not exist')
            user_email = request.POST['user_email']
            msg = "This email do not match our records."
            return render(request, 'UserTemplates/maintenance.html', {'msg': msg, 'user_email': user_email})
    else:
        return render(request, 'UserTemplates/maintenance.html')

def uregister(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            username = request.POST['username']
            email = request.POST['email']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            dob = request.POST['dob']
            addr = request.POST['addr']
            contact = request.POST['contact']
            state = request.POST['state']
            dis = request.POST['dis']
            city = request.POST['city']
            pos = request.POST['pos']
            confirm_pass = request.POST['confirm']
            if 'Guest' in userid:
                if request.method == 'POST':
                    if email == 'admin@tronpc.web':
                        if UserDetails.objects.filter(username=username).exists():
                            username_taken = 'This Username is Taken'
                            return render(request, 'UserTemplates/register.html', {'username_taken': username_taken, 'username': username, 'firstname': firstname, 'lastname': lastname, 'email': email, 'dob': dob,'addr': addr, 'contact': contact, 'state': state, 'dis': dis, 'city': city, 'pos': pos})
                        elif UserDetails.objects.filter(email=email).exists():
                            email_taken = 'This Email is already registered'
                            return render(request, 'UserTemplates/register.html', {'email_taken': email_taken, 'username': username, 'firstname': firstname, 'lastname': lastname, 'email': email, 'dob': dob,'addr': addr, 'contact': contact, 'state': state, 'dis': dis, 'city': city, 'pos': pos})
                        else:
                            password = str(confirm_pass)
                            salt = uuid.uuid4().hex
                            enc_pass = hashlib.sha256(
                                salt.encode() + password.encode()).hexdigest() + ':' + salt

                            adetailsadd = UserDetails(first_name=firstname, last_name=lastname, email=email,
                                                    username=username, pass_word=enc_pass, dob=dob, profile_picture="", address=addr,
                                                    district=dis, city='live', state=state, postal_code=pos, phone_number=contact, account_type=False)
                            adetailsadd.save()
                            return redirect('main')
                    else:
                        if UserDetails.objects.filter(username=username).exists():
                            username_taken = 'This Username is Taken'
                            return render(request, 'UserTemplates/register.html', {'username_taken': username_taken, 'username': username, 'firstname': firstname, 'lastname': lastname, 'email': email, 'dob': dob, 'addr': addr, 'contact': contact, 'state': state, 'dis': dis, 'city': city, 'pos': pos})
                        elif UserDetails.objects.filter(email=email).exists():
                            email_taken = 'This Email is already registered'
                            return render(request, 'UserTemplates/register.html', {'email_taken': email_taken, 'username': username, 'firstname': firstname, 'lastname': lastname, 'email': email, 'dob': dob, 'addr': addr, 'contact': contact, 'state': state, 'dis': dis, 'city': city, 'pos': pos})
                        else:
                            password = str(confirm_pass)
                            salt = uuid.uuid4().hex
                            enc_pass = hashlib.sha256(
                                salt.encode() + password.encode()).hexdigest() + ':' + salt

                            udetailsadd = UserDetails(first_name=firstname, last_name=lastname, email=email,
                                                    username=username, pass_word=enc_pass, dob=dob, profile_picture="", address=addr,
                                                    district=dis, city=city, state=state, postal_code=pos, phone_number=contact, account_type=True)
                            udetailsadd.save()
                            cart_add_Guest = Cart.objects.filter(
                                customer_id=userid)
                            for cart in cart_add_Guest:
                                cart.customer_id = udetailsadd.id
                                cart.save()

                            cus_add_Guest = CustomBuilt.objects.filter(
                                cus_id=userid)
                            for cus in cus_add_Guest:
                                cus.cus_id = udetailsadd.id
                                cus.save()
                            return render(request, 'UserTemplates/login.html')
            else:
                if request.method == 'POST':
                    udetails = UserDetails.objects.all()
                    username = request.POST['username']
                    firstname = request.POST['firstname']
                    lastname = request.POST['lastname']
                    email = request.POST['email']
                    dob = request.POST['dob']
                    addr = request.POST['addr']
                    contact = request.POST['contact']
                    state = request.POST['state']
                    dis = request.POST['dis']
                    city = request.POST['city']
                    pos = request.POST['pos']
                    if UserDetails.objects.filter(username=username).exists():
                        username_taken = 'This Username is Taken'
                        return render(request, 'UserTemplates/register.html', {'username_taken': username_taken, 'username': username, 'firstname': firstname, 'lastname': lastname, 'email': email, 'dob': dob, 'addr': addr, 'contact': contact, 'state': state, 'dis': dis, 'city': city, 'pos': pos})
                    elif UserDetails.objects.filter(email=email).exists():
                        email_taken = 'This Email is already registered'
                        return render(request, 'UserTemplates/register.html', {'email_taken': email_taken, 'username': username, 'firstname': firstname, 'lastname': lastname, 'email': email, 'dob': dob, 'addr': addr, 'contact': contact, 'state': state, 'dis': dis, 'city': city, 'pos': pos})
                    else:
                        username = request.POST['username']
                        firstname = request.POST['firstname']
                        lastname = request.POST['lastname']
                        email = request.POST['email']
                        dob = request.POST['dob']
                        addr = request.POST['addr']
                        contact = request.POST['contact']
                        state = request.POST['state']
                        dis = request.POST['dis']
                        city = request.POST['city']
                        pos = request.POST['pos']
                        confirm_pass = request.POST['confirm']
                        password = str(confirm_pass)
                        salt = uuid.uuid4().hex
                        enc_pass = hashlib.sha256(
                            salt.encode() + password.encode()).hexdigest() + ':' + salt

                        udetailsadd = UserDetails(first_name=firstname, last_name=lastname, email=email,
                                                  username=username, pass_word=enc_pass, dob=dob, profile_picture="", address=addr,
                                                  district=dis, city=city, state=state, postal_code=pos, phone_number=contact, account_type=True)
                        udetailsadd.save()
                        return render(request, 'UserTemplates/login.html')
                else:
                    return redirect('index')
        else:
            return redirect('index')
    else:
        return redirect('index')


def loginform(request):
    if request.method == 'POST':
        user_email = request.POST['user_email']
        user_pass = request.POST['user_pass']
        try:
            user_object = UserDetails.objects.get(email=user_email)
        except UserDetails.DoesNotExist:
            user_object = None
        if user_object:
            if user_object and user_object.account_type == False:
                unew = UserDetails.objects.get(email=user_email)
                providedText = unew.pass_word
                providedText, salt = providedText.split(':')
                checked = bool(providedText == hashlib.sha256(
                    salt.encode() + user_pass.encode()).hexdigest())
                if checked == True:
                    request.session['adminid'] = unew.id
                    return redirect('adminIndex')
                else:
                    user_email = request.POST['user_email']
                    pas = "password not correct"
                    return render(request, 'UserTemplates/login.html', {'pas': pas, 'user_email': user_email})
            else:
                unew = UserDetails.objects.get(email=user_email)
                providedText = unew.pass_word
                providedText, salt = providedText.split(':')
                checked = bool(providedText == hashlib.sha256(
                    salt.encode() + user_pass.encode()).hexdigest())
                if checked == True:
                    request.session['userid'] = unew.id
                    return redirect('mainIndex')
                else:
                    user_email = request.POST['user_email']
                    pas = "password not correct"
                    return render(request, 'UserTemplates/login.html', {'pas': pas, 'user_email': user_email})
        else:
            print('not exist')
            user_email = request.POST['user_email']
            msg = "This email do not match our records."
            return render(request, 'UserTemplates/login.html', {'msg': msg, 'user_email': user_email})
    else:
        return redirect('login')

def index(request):
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


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mainIndex(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            pro = UserDetails.objects.get(id=userid)
            return redirect('home')
        else:
            return render(request, 'UserTemplates/login.html')
    return render(request, 'UserTemplates/index.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            pro = UserDetails.objects.filter(id=userid)
            cart_list = Cart.objects.filter(id=userid)
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
                           'pro': pro, 'cart_list': cart_list, 'cart_list_count': cart_list_count, 'total_price': total_price, 'dotd': dotd}
            except ObjectDoesNotExist:
                context = {'carousal': carousal, 'banners': banners, 'products': products,
                           'specials': specials, 'category': category, 'blogs': blogs, 'brands': brands,
                           'pro': pro, 'cart_list': cart_list, 'cart_list_count': cart_list_count, 'total_price': total_price}
            return render(request, 'UserTemplates/home.html', context)
        else:
            print('something wrong!')
    else:
        return redirect('/')


def add_to_cart_form(request, id):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            proid = Product.objects.get(id=id)
            if Cart.objects.filter(customer_id=userid, product_code=proid.product_code).exists():
                cart = Cart.objects.get(
                    customer_id=userid, product_code=proid.product_code)
                pro_qua = int(cart.product_quantity)
                pro = proid.price.replace(',', '')
                pro_cur = pro[:-3]
                cart = cart.price.replace(',', '')
                cart_cur = cart[:-3]
                total_cart = int(cart_cur) + int(pro_cur)
                locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
                total_cart_price_formatted = locale.currency(
                    total_cart, grouping=True, symbol=False)
                total_qua = int((pro_qua) + int(1))
                cart_fk = Cart.objects.get(
                    customer_id=userid, product_code=proid.product_code)
                cart_fk.price = total_cart_price_formatted
                cart_fk.product_quantity = total_qua
                cart_fk.save()
                if 'Guest' in str(userid):
                    return redirect('allProducts')
                else:
                    return redirect('productsHome')
            else:
                if 'Guest' in str(userid):
                    cart_add = Cart(product_code=proid.product_code, product_quantity=1,
                                    product=proid, price=proid.price, customer_id=userid)
                    cart_add.save()
                    return redirect('allProducts')
                else:
                    cart_add = Cart(product_code=proid.product_code, product_quantity=1,
                                    product=proid, price=proid.price, customer_id=userid)
                    cart_add.save()
                    return redirect('productsHome')
        else:
            print('something wrong!')
    else:
        return redirect('/')


def cartQuaAdd(request, id):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            if request.method == 'POST':
                userid = request.session['userid']
                pro_qua_in = request.POST['quantity']
                print('this is the qua received : ', pro_qua_in)
                cart = Cart.objects.get(customer_id=userid, id=id)
                proid = Product.objects.get(id=cart.product_id)
                pro_qua = int(pro_qua_in)
                pro = proid.price.replace(',', '')
                pro_cur = pro[:-3]
                total_cart = int(pro_qua) * int(pro_cur)
                locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
                total_cart_price_formatted = locale.currency(
                    total_cart, grouping=True, symbol=False)
                cart_fk = Cart.objects.get(customer_id=userid, id=id)
                cart_fk.price = total_cart_price_formatted
                cart_fk.product_quantity = pro_qua
                cart_fk.save()
                return redirect('cart')
            else:
                return redirect('cart')
        else:
            print('something wrong!')
    else:
        return redirect('/')


def categoryFilter(request, id):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            category = Category.objects.all()
            products = Product.objects.filter(
                status=1, category=id).order_by('-date_added')
            category_name_prep = Category.objects.get(id=id)
            category_name = category_name_prep.category_name
            specials = Product.objects.filter(special=1, status=1)
            cart_list = Cart.objects.filter(customer_id=userid)
            cart_price_list = Cart.objects.filter(
                customer_id=userid).values('price')
            prices = [item['price'] for item in cart_price_list]
            total = int(sum(float(price.replace(',', ''))
                        for price in prices))
            locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
            total_price = locale.currency(
                total, grouping=True, symbol=False)

            cart_quantity = Cart.objects.filter(
                customer_id=userid).values('product_quantity')
            quantity = [item['product_quantity'] for item in cart_quantity]
            cart_list_count = int(sum(float(qua.replace(',', ''))
                                      for qua in quantity))
            userid_confirm = str(userid)
            if 'Guest' in userid_confirm:
                context = {'products': products,
                           'specials': specials, 'category': category, 'category_name': category_name, 'cart_list': cart_list,
                           'total_price': total_price,
                           'cart_list_count': cart_list_count, 'userid': userid}
                return render(request, 'UserTemplates/products.html', context)
            else:
                pro = UserDetails.objects.filter(id=userid)
                context = {'products': products,
                           'specials': specials, 'category': category, 'category_name': category_name, 'cart_list': cart_list,
                           'total_price': total_price,
                           'cart_list_count': cart_list_count, 'pro': pro}
                return render(request, 'UserTemplates/products.html', context)
        else:
            return redirect('something wrong!')
    else:
        return redirect('/')


def checkOut(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            user_det = UserDetails.objects.get(id=userid)
            user_cart = Cart.objects.filter(customer_id=userid)
            current_date = datetime.datetime.now()
            current_time = current_date.date()
            user_cart.update(status='Ordered',order_date=current_time)
            user_cus = CustomBuilt.objects.filter(cus_id=userid)
            user_cus.update(status='Ordered',order_date=current_time)
            user_main = CustomBuilt.objects.filter(cus_id=userid)
            cart_price_list = Cart.objects.filter(
                customer_id=userid).values('price')
            prices = [item['price'] for item in cart_price_list]
            total = int(sum(float(price.replace(',', '')) for price in prices))
            locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
            total_price = locale.currency(total, grouping=True, symbol=False)
            if Sale.objects.filter(customer=userid).exists():
                sale_update = Sale.objects.get(customer=userid)
                sale_update.sale_code=sale_update.sale_code
                sale_update.order_date=current_time
                sale_update.status="Order Updated"
                sale_update.payment=sale_update.payment
                sale_update.sub_total=total_price
                sale_update.paid=sale_update.paid
                sale_update.due=sale_update.due
                sale_update.biller=sale_update.biller
                sale_update.product_type=sale_update.product_type
                sale_update.customer=sale_update.customer
                sale_update.save()
                return redirect('contactHome')
            else:
                code_length = 3  # Customize the length of the code
                x = datetime.datetime.now()
                salt = x.strftime("%f")[3:].upper()
                ord_cod = 'Ord-' + salt + \
                    ''.join(random.choices(string.ascii_uppercase +
                            string.digits, k=code_length))
                user_upd = UserDetails.objects.get(id=userid)
                sales_add = Sale(sale_code=ord_cod,order_date=current_time,status="Ordered",payment="COD",sub_total=total_price
                ,paid="",due="",biller="TronPC",product_type="Product Order",customer=user_upd)
                sales_add.save()
                # email = user_det.email
                # subject = 'Greetings from TronPC'
                # message = 'Congratulations'
                # email_from = settings.EMAIL_HOST_USER
                # recipient_list = [email, ]
                # send_mail(subject, message, email_from,
                #         recipient_list, fail_silently=True)
                return redirect('contactHome')
        else:
            print('something wrong!')
    else:
        return redirect('/')


def contactHome(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            pro = UserDetails.objects.filter(id=userid)
            category = Category.objects.all()
            cart_list = Cart.objects.filter(id=userid)
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
            return render(request, 'UserTemplates/contact.html', {'pro': pro, 'category': category, 'cart_list': cart_list,
                                                                  'total_price': total_price,
                                                                  'cart_list_count': cart_list_count})
        else:
            print('something wrong!')
    else:
        return redirect('/')


def contact(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            category = Category.objects.all()
            cart_list = Cart.objects.filter(customer_id=userid)
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
            return render(request, 'UserTemplates/contact.html', {'category': category, 'cart_list': cart_list,
                                                                  'total_price': total_price,
                                                                  'cart_list_count': cart_list_count, 'userid': userid})
        else:
            print('something wrong!')
    else:
        return redirect('/')


def productsHome(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            pro = UserDetails.objects.filter(id=userid)
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
            context = {'carousal': carousal, 'banners': banners, 'products': products,
                       'specials': specials, 'category': category, 'blogs': blogs, 'brands': brands,
                       'userid': userid, 'cart_list_count': cart_list_count, 'total_price': total_price, 'pro': pro}
            return render(request, 'UserTemplates/products.html', context)
        else:
            print('something wrong!')
    else:
        return redirect('/')


def allProducts(request):
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
            context = {'carousal': carousal, 'banners': banners, 'products': products,
                       'specials': specials, 'category': category, 'blogs': blogs, 'brands': brands,
                       'userid': userid, 'cart_list_count': cart_list_count, 'total_price': total_price}
            return render(request, 'UserTemplates/products.html', context)
        else:
            print('something wrong!')
    else:
        return redirect('/')


def preBuiltHome(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            category = Category.objects.all()
            cart_list = Cart.objects.filter(customer_id=userid)
            cart_price_list = Cart.objects.filter(
                customer_id=userid).values('price')
            prices = [item['price'] for item in cart_price_list]
            total = int(sum(float(price.replace(',', ''))
                        for price in prices))
            locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
            total_price = locale.currency(
                total, grouping=True, symbol=False)

            cart_quantity = Cart.objects.filter(
                customer_id=userid).values('product_quantity')
            quantity = [item['product_quantity'] for item in cart_quantity]
            cart_list_count = int(sum(float(qua.replace(',', ''))
                                      for qua in quantity))
            pre_built = PreBuilt.objects.all()
            userid_confirm = str(userid)
            if 'Guest' in userid_confirm:
                context = {'category': category, 'cart_list': cart_list, 'total_price': total_price,
                           'cart_list_count': cart_list_count, 'userid': userid, 'pre_built': pre_built}
                return render(request, 'UserTemplates/preBuiltHome.html', context)
            else:
                pro = UserDetails.objects.filter(id=userid)
                context = {'category': category, 'cart_list': cart_list, 'total_price': total_price,
                           'cart_list_count': cart_list_count, 'userid': userid, 'pro': pro, 'pre_built': pre_built}
                return render(request, 'UserTemplates/preBuiltHome.html', context)
        else:
            return redirect('something wrong!')
    else:
        return redirect('/')


def cart(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            userid_confirm = str(userid)
            category = Category.objects.all()
            specials = Product.objects.filter(special=1, status=1)
            cart = Cart.objects.filter(
                customer_id=userid).exclude(product_id=None)
            pre_built_list = Cart.objects.filter(
                customer_id=userid, product_id=None)
            cus_built_list = CustomBuilt.objects.filter(
                cus_id=userid)
            cart_price_list = Cart.objects.filter(
                customer_id=userid).values('price')
            prices = [item['price'] for item in cart_price_list]
            total = int(sum(float(price.replace(',', ''))
                        for price in prices))
            locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
            total_price = locale.currency(
                total, grouping=True, symbol=False)

            cart_quantity = Cart.objects.filter(
                customer_id=userid).values('product_quantity')
            quantity = [item['product_quantity'] for item in cart_quantity]
            cart_list_count = int(sum(float(qua.replace(',', ''))
                                      for qua in quantity))
            pre_built = PreBuilt.objects.all()
            try:
                data_get = CustomBuilt.objects.get(cus_id=userid)
                datajson = json.loads(data_get.cus_additional)
                if 'Guest' in userid_confirm:
                    context = {'pre_built': pre_built, 'pre_built_list': pre_built_list, 'specials': specials, 'category': category, 'cart': cart,
                            'total_price': total_price, 'cart_list_count': cart_list_count, 'userid': userid,'cus_built_list':cus_built_list,'datajson':datajson}
                    return render(request, 'UserTemplates/cart.html', context)
                else:
                    pro = UserDetails.objects.filter(id=userid)
                    context = {'pre_built': pre_built, 'pre_built_list': pre_built_list, 'specials': specials, 'category': category, 'cart': cart,
                            'total_price': total_price, 'cart_list_count': cart_list_count, 'userid': userid, 'pro': pro,'cus_built_list':cus_built_list,'datajson':datajson}
                    return render(request, 'UserTemplates/cart.html', context)
            except ObjectDoesNotExist:
                if 'Guest' in userid_confirm:
                    context = {'pre_built': pre_built, 'pre_built_list': pre_built_list, 'specials': specials, 'category': category, 'cart': cart,
                            'total_price': total_price, 'cart_list_count': cart_list_count, 'userid': userid,'cus_built_list':cus_built_list}
                    return render(request, 'UserTemplates/cart.html', context)
                else:
                    pro = UserDetails.objects.filter(id=userid)
                    context = {'pre_built': pre_built, 'pre_built_list': pre_built_list, 'specials': specials, 'category': category, 'cart': cart,
                            'total_price': total_price, 'cart_list_count': cart_list_count, 'userid': userid, 'pro': pro,'cus_built_list':cus_built_list}
                    return render(request, 'UserTemplates/cart.html', context)
        else:
            print('something wrong!')

    else:
        return redirect('/')


def cartDelete(request, id):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            cart = Cart.objects.get(id=id)
            cart.delete()
            return redirect('cart')
        else:
            print('something wrong!')
    else:
        return redirect('/')


def cusDelete(request, id):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            cart = CustomBuilt.objects.get(id=id)
            cart.delete()
            return redirect('cart')
        else:
            print('something wrong!')
    else:
        return redirect('/')


def register(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            return render(request, 'UserTemplates/register.html')
        else:
            return render(request, 'UserTemplates/register.html')
    else:
        return render(request, 'UserTemplates/register.html')


def login(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            return render(request, 'UserTemplates/login.html')
        else:
            return render(request, 'UserTemplates/login.html')
    else:
        return render(request, 'UserTemplates/login.html')


def view(request, id):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            userid_confirm = str(userid)
            if 'Guest' in userid_confirm:
                category = Category.objects.all()
                specials = Product.objects.filter(special=1, status=1)
                cart = Cart.objects.filter(customer_id=userid)
                cart_price_list = Cart.objects.filter(
                    customer_id=userid).values('price')
                prices = [item['price'] for item in cart_price_list]
                total = int(sum(float(price.replace(',', ''))
                            for price in prices))
                locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
                total_price = locale.currency(
                    total, grouping=True, symbol=False)

                cart_quantity = Cart.objects.filter(
                    customer_id=userid).values('product_quantity')
                quantity = [item['product_quantity'] for item in cart_quantity]
                cart_list_count = int(sum(float(qua.replace(',', ''))
                                          for qua in quantity))
                product = Product.objects.filter(id=id)
                context = {'specials':specials,'product': product, 'category': category, 'cart': cart,
                           'total_price': total_price, 'cart_list_count': cart_list_count, 'userid': userid}
                return render(request, 'UserTemplates/view.html', context)
            else:
                pro = UserDetails.objects.filter(id=userid)
                category = Category.objects.all()
                specials = Product.objects.filter(special=1, status=1)
                cart = Cart.objects.filter(customer_id=userid)
                cart_price_list = Cart.objects.filter(
                    customer_id=userid).values('price')
                prices = [item['price'] for item in cart_price_list]
                total = int(sum(float(price.replace(',', ''))
                            for price in prices))
                locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
                total_price = locale.currency(
                    total, grouping=True, symbol=False)

                cart_quantity = Cart.objects.filter(
                    customer_id=userid).values('product_quantity')
                quantity = [item['product_quantity'] for item in cart_quantity]
                cart_list_count = int(sum(float(qua.replace(',', ''))
                                          for qua in quantity))
                product = Product.objects.filter(id=id)
                context = {'specials':specials,'product': product, 'category': category, 'cart': cart,
                           'total_price': total_price, 'cart_list_count': cart_list_count, 'pro': pro}
                return render(request, 'UserTemplates/view.html', context)
        else:
            print('something wrong!')
    else:
        return redirect('/')


def pcb(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            userid_confirm = str(userid)
            if 'Guest' in userid_confirm:
                category = Category.objects.all()
                banners = Banners.objects.all()
                specials = Product.objects.filter(special=1, status=1)
                cart = Cart.objects.filter(customer_id=userid)
                cart_price_list = Cart.objects.filter(
                    customer_id=userid).values('price')
                prices = [item['price'] for item in cart_price_list]
                total = int(sum(float(price.replace(',', ''))
                            for price in prices))
                locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
                total_price = locale.currency(
                    total, grouping=True, symbol=False)

                cart_quantity = Cart.objects.filter(
                    customer_id=userid).values('product_quantity')
                quantity = [item['product_quantity'] for item in cart_quantity]
                cart_list_count = int(sum(float(qua.replace(',', ''))
                                          for qua in quantity))
                code_length = 3  # Customize the length of the code
                x = datetime.datetime.now()
                salt = x.strftime("%f")[3:].upper()
                cus_cod = 'Cus-' + salt + \
                    ''.join(random.choices(string.ascii_uppercase +
                            string.digits, k=code_length))
                if CustomBuilt.objects.filter(cus_id=userid).exists():
                    built_added_already = 'Already created a custom!you can edit it if u want'
                    data = CustomBuilt.objects.filter(cus_id=userid)
                    data_get = CustomBuilt.objects.get(cus_id=userid)
                    datajson = json.loads(data_get.cus_additional)
                    context = {'specials': specials, 'category': category, 'cart': cart,
                               'total_price': total_price, 'cart_list_count': cart_list_count, 'userid': userid, 'cus_cod': cus_cod,
                               'built_added_already': built_added_already, 'data': data, 'datajson': datajson, 'banners': banners}
                    return render(request, 'UserTemplates/pcb.html', context)
                else:
                    context = {'specials': specials, 'category': category, 'cart': cart,
                               'total_price': total_price, 'cart_list_count': cart_list_count, 'userid': userid, 'cus_cod': cus_cod, 'banners': banners}
                    return render(request, 'UserTemplates/pcb.html', context)
            else:
                pro = UserDetails.objects.filter(id=userid)
                category = Category.objects.all()
                banners = Banners.objects.all()
                specials = Product.objects.filter(special=1, status=1)
                cart = Cart.objects.filter(customer_id=userid)
                cart_price_list = Cart.objects.filter(
                    customer_id=userid).values('price')
                prices = [item['price'] for item in cart_price_list]
                total = int(sum(float(price.replace(',', ''))
                            for price in prices))
                locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
                total_price = locale.currency(
                    total, grouping=True, symbol=False)

                cart_quantity = Cart.objects.filter(
                    customer_id=userid).values('product_quantity')
                quantity = [item['product_quantity'] for item in cart_quantity]
                cart_list_count = int(sum(float(qua.replace(',', ''))
                                          for qua in quantity))
                code_length = 3  # Customize the length of the code
                x = datetime.datetime.now()
                salt = x.strftime("%f")[3:].upper()
                cus_cod = 'Cus-' + salt + \
                    ''.join(random.choices(string.ascii_uppercase +
                            string.digits, k=code_length))
                if CustomBuilt.objects.filter(cus_id=userid).exists():
                    built_added_already = 'Already created a custom!you can edit it if u want'
                    data = CustomBuilt.objects.filter(cus_id=userid)
                    data_get = CustomBuilt.objects.get(cus_id=userid)
                    datajson = json.loads(data_get.cus_additional)
                    context = {'specials': specials, 'category': category, 'cart': cart,
                               'total_price': total_price, 'cart_list_count': cart_list_count, 'pro': pro, 'cus_cod': cus_cod, 'built_added_already': built_added_already, 'data': data, 'datajson': datajson, 'banners': banners}
                    return render(request, 'UserTemplates/pcb.html', context)
                else:
                    context = {'specials': specials, 'category': category, 'cart': cart,
                               'total_price': total_price, 'cart_list_count': cart_list_count, 'pro': pro, 'cus_cod': cus_cod,'banners': banners}
                    return render(request, 'UserTemplates/pcb.html', context)

        else:
            print('something wrong!')

    else:
        return redirect('/')


def pcbAddForm(request):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            userid_confirm = str(userid)
            if 'Guest' in userid_confirm:
                if request.method == 'POST':
                    total_customers = CustomBuilt.objects.filter(
                        cus_id__contains='Guest').count()
                    if total_customers > 15:
                        cus_ids_to_delete = CustomBuilt.objects.filter(
                            cus_id__contains='Guest').order_by('-id').values_list('id', flat=True)[15:]
                        for cus_id in cus_ids_to_delete:
                            CustomBuilt.objects.filter(id=cus_id).delete()
                    else:
                        if CustomBuilt.objects.filter(cus_id=userid).exists():
                            built_added_already = 'Already created a custom!you can edit it if u want'
                            data = CustomBuilt.objects.filter(cus_id=userid)
                            data_get = CustomBuilt.objects.get(cus_id=userid)
                            datajson = json.loads(data_get.cus_additional)
                            return render(request, 'UserTemplates/pcb.html', {'built_added_already': built_added_already, 'data': data, 'datajson': datajson})
                        else:
                            cus_code = request.POST['cus_code']
                            cus_processor = request.POST['cus_processor']
                            cus_ram = request.POST['cus_ram']
                            cus_hardisk = request.POST['cus_hardisk']
                            cus_gpu = request.POST['cus_gpu']
                            cus_cpu_cooler = request.POST['cus_cpu_cooler']
                            cus_motherbrd = request.POST['cus_motherbrd']
                            cus_powersupply = request.POST['cus_powersupply']
                            cus_cabinet = request.POST['cus_cabinet']
                            cus_desc = request.POST['cus_desc']
                            monitor = request.POST['monitor']
                            speaker = request.POST['speaker']
                            keyboard = request.POST['keyboard']
                            mouse = request.POST['mouse']
                            printer = request.POST['printer']
                            ups = request.POST['ups']
                            wifi_dongle = request.POST['wifi_dongle']
                            blutooth_dongle = request.POST['blutooth_dongle']
                            add_data = json.dumps(
                            {"Monitor": monitor, "Speaker": speaker, "Keyboard": keyboard,
                            "Mouse": mouse, "Printer": printer, "Ups": ups,
                            "wifi_dongle": wifi_dongle, "blutooth_dongle": blutooth_dongle, "Customer": userid, "cus_code": cus_code})
                            save_to_db = CustomBuilt(cus_code=cus_code,
                                                     cus_processor=cus_processor,
                                                     cus_ram=cus_ram,
                                                     cus_hardisk=cus_hardisk,
                                                     cus_gpu=cus_gpu,
                                                     cus_cpu_cooler=cus_cpu_cooler,
                                                     cus_motherbrd=cus_motherbrd,
                                                     cus_powersupply=cus_powersupply,
                                                     cus_cabinet=cus_cabinet,
                                                     cus_desc=cus_desc,
                                                     cus_additional=add_data,
                                                     status=True, cus_id=userid)
                            save_to_db.save()
                            return redirect('pcb')

                else:
                    return redirect('pcb')
            else:
                if request.method == 'POST':
                    if CustomBuilt.objects.filter(cus_id=userid).exists():
                        built_added_already = 'Already created a custom!you can edit it if u want'
                        data = CustomBuilt.objects.filter(cus_id=userid)
                        data_get = CustomBuilt.objects.get(cus_id=userid)
                        datajson = json.loads(data_get.cus_additional)
                        return render(request, 'UserTemplates/pcb.html', {'built_added_already': built_added_already, 'data': data, 'datajson': datajson})
                    else:
                        cus_code = request.POST['cus_code']
                        cus_processor = request.POST['cus_processor']
                        cus_ram = request.POST['cus_ram']
                        cus_hardisk = request.POST['cus_hardisk']
                        cus_gpu = request.POST['cus_gpu']
                        cus_cpu_cooler = request.POST['cus_cpu_cooler']
                        cus_motherbrd = request.POST['cus_motherbrd']
                        cus_powersupply = request.POST['cus_powersupply']
                        cus_cabinet = request.POST['cus_cabinet']
                        cus_desc = request.POST['cus_desc']
                        monitor = request.POST['monitor']
                        speaker = request.POST['speaker']
                        keyboard = request.POST['keyboard']
                        mouse = request.POST['mouse']
                        printer = request.POST['printer']
                        ups = request.POST['ups']
                        wifi_dongle = request.POST['wifi_dongle']
                        blutooth_dongle = request.POST['blutooth_dongle']
                        add_data = json.dumps(
                            {"Monitor": monitor, "Speaker": speaker, "Keyboard": keyboard,
                                "Mouse": mouse, "Printer": printer, "Ups": ups,
                                "wifi_dongle": wifi_dongle, "blutooth_dongle": blutooth_dongle, "Customer": userid, "cus_code": cus_code})
                        print('allto getehr : ', add_data)
                        save_to_db = CustomBuilt(cus_code=cus_code,
                                                 cus_processor=cus_processor,
                                                 cus_ram=cus_ram,
                                                 cus_hardisk=cus_hardisk,
                                                 cus_gpu=cus_gpu,
                                                 cus_cpu_cooler=cus_cpu_cooler,
                                                 cus_motherbrd=cus_motherbrd,
                                                 cus_powersupply=cus_powersupply,
                                                 cus_cabinet=cus_cabinet,
                                                 cus_desc=cus_desc,
                                                 cus_additional=add_data,
                                                 status=True, cus_id=userid)
                        save_to_db.save()
                        return redirect('pcb')
                else:
                    return redirect('pcb')
        else:
            return redirect('/')
    else:
        return redirect('/')


def pcbAddFormEdit(request, id):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            userid_confirm = str(userid)
            if 'Guest' in userid_confirm:
                if request.method == 'POST':
                    cus_processor = request.POST['cus_processor']
                    cus_ram = request.POST['cus_ram']
                    cus_hardisk = request.POST['cus_hardisk']
                    cus_gpu = request.POST['cus_gpu']
                    cus_cpu_cooler = request.POST['cus_cpu_cooler']
                    cus_motherbrd = request.POST['cus_motherbrd']
                    cus_powersupply = request.POST['cus_powersupply']
                    cus_cabinet = request.POST['cus_cabinet']
                    cus_desc = request.POST['cus_desc']
                    monitor = request.POST['monitor']
                    speaker = request.POST['speaker']
                    keyboard = request.POST['keyboard']
                    mouse = request.POST['mouse']
                    printer = request.POST['printer']
                    ups = request.POST['ups']
                    wifi_dongle = request.POST['wifi_dongle']
                    blutooth_dongle = request.POST['blutooth_dongle']
                    db_edit = CustomBuilt.objects.get(id=id)
                    add_data = json.dumps(
                        {"Monitor": monitor, "Speaker": speaker, "Keyboard": keyboard,
                         "Mouse": mouse, "Printer": printer, "Ups": ups,
                         "wifi_dongle": wifi_dongle, "blutooth_dongle": blutooth_dongle, "Customer": userid, "cus_code": db_edit.cus_code})
                    print('allto getehr : ', add_data)
                    db_edit.cus_code = db_edit.cus_code
                    db_edit.cus_processor = cus_processor
                    db_edit.cus_ram = cus_ram
                    db_edit.cus_hardisk = cus_hardisk
                    db_edit.cus_gpu = cus_gpu
                    db_edit.cus_cpu_cooler = cus_cpu_cooler
                    db_edit.cus_motherbrd = cus_motherbrd
                    db_edit.cus_powersupply = cus_powersupply
                    db_edit.cus_cabinet = cus_cabinet
                    db_edit.cus_desc = cus_desc
                    db_edit.cus_additional = add_data
                    db_edit.status = db_edit.status
                    db_edit.cus_id = userid
                    db_edit.save()
                    return redirect('pcb')

                else:
                    return redirect('pcb')
            else:
                if request.method == 'POST':
                    cus_processor = request.POST['cus_processor']
                    cus_ram = request.POST['cus_ram']
                    cus_hardisk = request.POST['cus_hardisk']
                    cus_gpu = request.POST['cus_gpu']
                    cus_cpu_cooler = request.POST['cus_cpu_cooler']
                    cus_motherbrd = request.POST['cus_motherbrd']
                    cus_powersupply = request.POST['cus_powersupply']
                    cus_cabinet = request.POST['cus_cabinet']
                    cus_desc = request.POST['cus_desc']
                    monitor = request.POST['monitor']
                    speaker = request.POST['speaker']
                    keyboard = request.POST['keyboard']
                    mouse = request.POST['mouse']
                    printer = request.POST['printer']
                    ups = request.POST['ups']
                    wifi_dongle = request.POST['wifi_dongle']
                    blutooth_dongle = request.POST['blutooth_dongle']
                    db_edit = CustomBuilt.objects.get(id=id)
                    add_data = json.dumps(
                        {"Monitor": monitor, "Speaker": speaker, "Keyboard": keyboard,
                         "Mouse": mouse, "Printer": printer, "Ups": ups,
                         "wifi_dongle": wifi_dongle, "blutooth_dongle": blutooth_dongle, "Customer": userid, "cus_code": db_edit.cus_code})
                    print('allto getehr : ', add_data)
                    db_edit.cus_code = db_edit.cus_code
                    db_edit.cus_processor = cus_processor
                    db_edit.cus_ram = cus_ram
                    db_edit.cus_hardisk = cus_hardisk
                    db_edit.cus_gpu = cus_gpu
                    db_edit.cus_cpu_cooler = cus_cpu_cooler
                    db_edit.cus_motherbrd = cus_motherbrd
                    db_edit.cus_powersupply = cus_powersupply
                    db_edit.cus_cabinet = cus_cabinet
                    db_edit.cus_desc = cus_desc
                    db_edit.cus_additional = add_data
                    db_edit.status = db_edit.status
                    db_edit.cus_id = userid
                    db_edit.save()
                    return redirect('pcb')
                else:
                    return redirect('pcb')
        else:
            return redirect('/')
    else:
        return redirect('/')


def addToCartPreBuilt(request, id):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            userid_confirm = str(userid)
            if 'Guest' in userid_confirm:
                category = Category.objects.all()
                cart = Cart.objects.filter(customer_id=userid)
                prebuilt_get = PreBuilt.objects.get(id=id)
                prebuilt_add = Cart(product_code=prebuilt_get.modal_code, product_quantity=1,
                                    price=prebuilt_get.price,
                                    customer_id=userid, prebuilt_id=prebuilt_get.id,
                                    prebuilt_name=prebuilt_get.modal_name)
                prebuilt_add.save()
                return redirect('preBuiltHome')
            else:
                pro = UserDetails.objects.filter(id=userid)
                prebuilt_get = PreBuilt.objects.get(id=id)
                prebuilt_add = Cart(product_code=prebuilt_get.modal_code, product_quantity=1,
                                    price=prebuilt_get.price,
                                    customer_id=userid, prebuilt_id=prebuilt_get.id,
                                    prebuilt_name=prebuilt_get.modal_name)
                prebuilt_add.save()

                return redirect('preBuiltHome')
        else:
            print('something wrong!')
    else:
        return redirect('/')


def pcbCustom(request):
    code_length = 3  # Customize the length of the code
    x = datetime.datetime.now()
    salt = x.strftime("%f")[3:].upper()
    cus_cod = 'COR-' + salt + \
        ''.join(random.choices(string.ascii_uppercase +
                string.digits, k=code_length))
    category_ram = Category.objects.get(category_name='Ram')
    product_ram = Product.objects.filter(category=category_ram.id)
    return render(request, 'UserTemplates/pcbCustom.html', {'cus_cod': cus_cod, 'product_ram': product_ram})


def logout(request):
    if 'userid' in request.session:
        request.session.flush()
        return redirect('login')
    else:
        return redirect('/')

# ----------------------------ADMIN VIEWS--------------------------#


def adminDash(request):
    return render(request, 'AdminTemplates/adminDash.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminIndex(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid = request.session['adminid']
            admin_details = UserDetails.objects.filter(email='admin@tronpc.web')
            current_date = datetime.datetime.now()
            this_year = current_date.year
            return render(request, 'AdminTemplates/adminIndex.html',{'admin_details':admin_details,'this_year':this_year})
        else:
            print('something wrong!')
    else:
        return redirect('/')


def addBlogs(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            userid = request.session['adminid']
            blog_list = Blogs.objects.all()
            return render(request, 'AdminTemplates/addBlogs.html', {'blog_list': blog_list})
        else:
            print('something wrong!')
    else:
        return redirect('/')


def addBlogsForm(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            userid = request.session['adminid']
            if request.method == 'POST':
                blog_name = request.POST['blog_name'].capitalize()
                blog_link = request.POST['blog_link']
                blog_des = request.POST['blog_des']
                mydata = Blogs.objects.filter(blog_link=blog_link).values()
                if mydata:
                    name_exists = f"{blog_link}"
                    blog_list = Blogs.objects.all()
                    context = {'name_exists': name_exists, 'blog_list': blog_list,
                            'blog_name': blog_name, 'blog_link': blog_link, 'blog_des': blog_des}
                    return render(request, 'AdminTemplates/addBlogs.html', context)
                else:
                    blog_name = request.POST['blog_name'].capitalize()
                    blog_link = request.POST['blog_link']
                    clean_url = blog_link.replace("https://youtu.be/", "")
                    blog_des = request.POST['blog_des']

                    blog_add = Blogs(blog_name=blog_name, blog_link=blog_link,
                                    blog_description=blog_des, blog_clean_link=clean_url)
                    blog_add.save()
                    added = f"{blog_name}"
                    blog_list = Blogs.objects.all()
                    return render(request, 'AdminTemplates/addBlogs.html', {'added': added, 'blog_list': blog_list})
            return redirect('addBlogs')
        else:
            print('something wrong!')
    else:
        return redirect('/')


def editBlogs(request, id):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            blog_list_edit = Blogs.objects.filter(id=id)
            blog_list = Blogs.objects.all()
            return render(request, 'AdminTemplates/addBlogs.html', {'blog_list': blog_list, 'blog_list_edit': blog_list_edit})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editBlogsForm(request, id):
    if 'userid' in request.session:
        if request.session.has_key('userid'):
            userid = request.session['userid']
            if request.method == 'POST':
                blog_name = request.POST['blog_name'].capitalize()
                blog_link = request.POST['blog_link']
                blog_des = request.POST['blog_des']
                db = Blogs.objects.get(id=id)
                clean_url = blog_link.replace("https://youtu.be/", "")
                db.blog_clean_link = clean_url
                db.blog_name = blog_name
                db.blog_link = blog_link
                db.blog_description = blog_des
                db.save()
                added = f"{blog_name}"
                blog_list = Blogs.objects.all()
                return render(request, 'AdminTemplates/addBlogs.html', {'added': added, 'blog_list': blog_list})
            else:
                return redirect('addBlogs')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def productList(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            pro_list = Product.objects.all()
            brnd_list = Brands.objects.all()
            return render(request, 'AdminTemplates/productList.html', {'pro_list': pro_list, 'brnd_list': brnd_list})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def addProduct(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            cat_list = Category.objects.all()
            brnd_list = Brands.objects.all()
            count = 'add'
            return render(request, 'AdminTemplates/addProduct.html', {'cat_list': cat_list, 'count': count, 'brnd_list': brnd_list})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editProduct(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            cat_list = Category.objects.all()
            pro_list = Product.objects.filter(id=id)
            pro_list_price = Product.objects.get(id=id)
            pro_price = pro_list_price.price[:-3]
            count = 'edit'
            return render(request, 'AdminTemplates/addProduct.html', {'cat_list': cat_list, 'count': count, 'pro_list': pro_list, 'pro_price': pro_price})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def addProductForm(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                pro_name = request.POST['pro_name'].capitalize()
                pro_cat = request.POST['pro_cat']
                pro_brand = request.POST['pro_brand']
                pro_qty = request.POST['pro_qty']
                pro_des = request.POST['pro_des']
                pro_price = request.POST['pro_price']
                price = int(pro_price.replace(',', ''))
                locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
                mod_price = locale.currency(price, grouping=True, symbol=False)
                pro_pic = request.FILES['pro_pic']
                if request.FILES.get('pre_pic1') is not None:
                    pre_pic1 = request.FILES.get('pre_pic1')
                else:
                    pre_pic1 = ""

                if request.FILES.get('pre_pic2') is not None:
                    pre_pic2 = request.FILES.get('pre_pic2')
                else:
                    pre_pic2 = ""

                if request.FILES.get('pre_pic3') is not None:
                    pre_pic3 = request.FILES.get('pre_pic3')
                else:
                    pre_pic3 = ""

                if request.FILES.get('pre_pic4') is not None:
                    pre_pic4 = request.FILES.get('pre_pic4')
                else:
                    pre_pic4 = ""

                if request.FILES.get('pre_pic5') is not None:
                    pre_pic5 = request.FILES.get('pre_pic5')
                else:
                    pre_pic5 = ""
                code_length = 3  # Customize the length of the code
                x = datetime.datetime.now()
                salt = x.strftime("%f")[3:].upper()
                pro_cod = 'PRO-' + salt + \
                    ''.join(random.choices(string.ascii_uppercase +
                            string.digits, k=code_length))
                for_key = Category.objects.get(id=pro_cat)
                for_brnd = Brands.objects.get(id=pro_brand)
                pro_add = Product(product_name=pro_name, product_code=pro_cod, date_added=x, brand=for_brnd, quantity=pro_qty,
                                description=pro_des, price=mod_price, status=True, special=False, product_image=pro_pic,product_image_1=pre_pic1, product_image_2=pre_pic2, product_image_3=pre_pic3, product_image_4=pre_pic4, product_image_5=pre_pic5, category=for_key)
                pro_add.save()
                added = f"{pro_name}"
                cat_list = Category.objects.all()
                brnd_list = Brands.objects.all()
                count = 'add'
            return render(request, 'AdminTemplates/addProduct.html', {'added': added, 'cat_list': cat_list, 'count': count, 'brnd_list': brnd_list})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editProductForm(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                pro_list = Product.objects.get(id=id)
                pro_name = request.POST['pro_name'].capitalize()
                pro_cat = request.POST['pro_cat']
                pro_brand = request.POST['pro_brand']
                pro_qty = request.POST['pro_qty']
                pro_des = request.POST['pro_des']
                pro_price = request.POST['pro_price']
                empty_fields = []
                if pro_name.strip() == '':
                    empty_fields.append('Product Name')
                if pro_cat.strip() == '':
                    empty_fields.append('Category')
                if pro_brand.strip() == '':
                    empty_fields.append('Brand')
                if pro_qty.strip() == '':
                    empty_fields.append('Quantity')
                if pro_des.strip() == '':
                    empty_fields.append('Description')
                if pro_price.strip() == '':
                    empty_fields.append('Price')

                if empty_fields:
                    cat_list = Category.objects.all()
                    pro_list = Product.objects.filter(id=id)
                    pro_list_price = Product.objects.get(id=id)
                    pro_price = pro_list_price.price[:-3]
                    count = 'edit'
                    fill_all = "" + ", ".join(empty_fields)
                    return render(request, 'AdminTemplates/addProduct.html', {'cat_list': cat_list, 'count': count, 'pro_list': pro_list, 'pro_price': pro_price, 'fill_all': fill_all})
                else:
                    price = int(pro_price.replace(',', ''))
                    locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
                    mod_price = locale.currency(price, grouping=True, symbol=False)
                    if request.FILES.get('pro_pic') is not None:
                        pro_pic = request.FILES.get('pro_pic')
                    else:
                        pro_pic = pro_list.product_image

                    if request.FILES.get('pre_pic1') is not None:
                        pre_pic1 = request.FILES.get('pre_pic1')
                    else:
                        pre_pic1 = pro_list.product_image_1

                    if request.FILES.get('pre_pic2') is not None:
                        pre_pic2 = request.FILES.get('pre_pic2')
                    else:
                        pre_pic2 = pro_list.product_image_2

                    if request.FILES.get('pre_pic3') is not None:
                        pre_pic3 = request.FILES.get('pre_pic3')
                    else:
                        pre_pic3 = pro_list.product_image_3

                    if request.FILES.get('pre_pic4') is not None:
                        pre_pic4 = request.FILES.get('pre_pic4')
                    else:
                        pre_pic4 = pro_list.product_image_4

                    if request.FILES.get('pre_pic5') is not None:
                        pre_pic5 = request.FILES.get('pre_pic5')
                    else:
                        pre_pic5 = pro_list.product_image_5

                        current_date = datetime.datetime.now()
                        current_time = current_date.date()
                        pro_cod = pro_list.product_code
                        for_key = Category.objects.get(id=pro_cat)
                        pro_add = Product.objects.get(id=id)
                        pro_add.product_name = pro_name
                        pro_add.product_code = pro_cod
                        pro_add.date_added = current_time
                        pro_add.brand = pro_brand
                        pro_add.quantity = pro_qty
                        pro_add.description = pro_des
                        pro_add.price = mod_price
                        pro_add.status = True
                        pro_add.special = True
                        pro_add.product_image = pro_pic
                        pro_add.product_image_1 = pre_pic1
                        pro_add.product_image_2 = pre_pic2
                        pro_add.product_image_3 = pre_pic3
                        pro_add.product_image_4 = pre_pic4
                        pro_add.product_image_5 = pre_pic5
                        pro_add.category = for_key
                        pro_add.save()
                        added = f"{pro_name}"
                        pro_list = Product.objects.all()
                        return render(request, 'AdminTemplates/productList.html', {'added': added, 'pro_list': pro_list})
            else:
                return redirect('productList')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def categoryList(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            categoryList = Category.objects.all()
            return render(request, 'AdminTemplates/categoryList.html', {'categoryList': categoryList})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def addCategory(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            code_length = 3  # Customize the length of the code
            x = datetime.datetime.now()
            salt = x.strftime("%f")[3:].upper()
            code = 'CAT-' + salt + \
                ''.join(random.choices(string.ascii_uppercase +
                        string.digits, k=code_length))

            existingOptions = Category.objects.all()
            categories = ["RAM", "ROM", "SSD", "Monitor", "GPU", "PreBuilt"]
            newOptions = []
            for category in categories:
                if not existingOptions.filter(category_name=category).exists():
                    newOptions.append(category)
            if len(newOptions) == 0:
                return render(request, 'AdminTemplates/addCategory.html', {'code': code})
            else:
                return render(request, 'AdminTemplates/addCategory.html', {'code': code, 'newOptions': newOptions})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def addcategory_form(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                cat_name = request.POST['cat_name'].capitalize()
                mydata = Category.objects.filter(category_name=cat_name).values()
                if mydata:
                    name_exists = f"{cat_name}"
                    existingOptions = Category.objects.all()
                    categories = ["RAM", "ROM", "SSD", "Monitor", "GPU", "PreBuilt"]
                    newOptions = []
                    for category in categories:
                        if not existingOptions.filter(category_name=category).exists():
                            newOptions.append(category)
                    if len(newOptions) == 0:
                        return render(request, 'AdminTemplates/addCategory.html', {'name_exists': name_exists})
                    else:
                        return render(request, 'AdminTemplates/addCategory.html', {'newOptions': newOptions, 'name_exists': name_exists})
                else:
                    cat_name = request.POST['cat_name'].capitalize()
                    code_length = 3  # Customize the length of the code
                    x = datetime.datetime.now()
                    salt = x.strftime("%f")[3:].upper()
                    cat_code = 'CAT-' + salt + \
                        ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=code_length))
                    cat_desc = request.POST['cat_desc']
                    cat_img = request.FILES['cat_img']
                    category = Category(category_name=cat_name, category_code=cat_code,
                                        description=cat_desc, category_image=cat_img)
                    category.save()
                    added = f"{cat_name}"
                    code_length = 3  # Customize the length of the code
                    x = datetime.datetime.now()
                    salt = x.strftime("%f")[3:].upper()
                    code = 'CAT-' + salt + \
                        ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=code_length))
                    existingOptions = Category.objects.all()
                    categories = ["RAM", "ROM", "SSD", "Monitor", "GPU", "PreBuilt"]
                    newOptions = []
                    for category in categories:
                        if not existingOptions.filter(category_name=category).exists():
                            newOptions.append(category)
                    if len(newOptions) == 0:
                        return render(request, 'AdminTemplates/addCategory.html', {'added': added})
                    else:
                        return render(request, 'AdminTemplates/addCategory.html', {'newOptions': newOptions, 'added': added})
            return redirect('addCategory')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def productDetails(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            product_id = Product.objects.filter(id=id)
            to_get_raw = Product.objects.get(id=id)
            raw_name = os.path.basename(to_get_raw.product_image.name)
            raw_size = os.stat(to_get_raw.product_image.path)
            raw_mb_size = str(raw_size.st_size / (1024 * 1024))[:5]
            return render(request, 'AdminTemplates/productDetails.html', {'product_id': product_id, 'raw_name': raw_name, 'raw_mb_size': raw_mb_size})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def adminProfile(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            return render(request, 'AdminTemplates/adminProfile.html')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editSales(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            return render(request, 'AdminTemplates/editSales.html')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def salesDetails(request,id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            order_cart = Cart.objects.filter(customer_id=id)
            sales_det = Sale.objects.select_related('customer').get(customer_id=id)
            cart_price_list = Cart.objects.filter(
                customer_id=id).values('price')
            prices = [item['price'] for item in cart_price_list]
            total = int(sum(float(price.replace(',', ''))
                        for price in prices))
            locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
            total_price = locale.currency(
                total, grouping=True, symbol=False)
            return render(request, 'AdminTemplates/salesDetails.html',{'order_cart':order_cart,'sales_det':sales_det,'total_price':total_price})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def salesList(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            order_cart = Cart.objects.filter(status="Ordered").values('customer_id').distinct()
            all_order_cart = list([item['customer_id'] for item in order_cart])
            sales_list = Sale.objects.select_related('customer').all()
            all_order_cus = CustomBuilt.objects.filter(status="Ordered")
            admin_details = UserDetails.objects.filter(email='admin@tronpc.web')
            current_date = datetime.datetime.now()
            this_year = current_date.year
            if order_cart.exists():
                if all_order_cus.exists():
                    return render(request, 'AdminTemplates/adminIndex.html',{'all_order_cart':all_order_cart,'all_order_cus':all_order_cus,'sales_list':sales_list,'admin_details':admin_details,'this_year':this_year})
                else:
                    return render(request, 'AdminTemplates/adminIndex.html',{'all_order_cart':all_order_cart,'sales_list':sales_list,'admin_details':admin_details,'this_year':this_year})
            else:
                return render(request, 'AdminTemplates/adminIndex.html',{'all_order_cart':all_order_cart,'sales_list':sales_list,'admin_details':admin_details,'this_year':this_year})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def edit_category_form(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            banners = Category.objects.get(id=id)
            cat_name = request.POST['cat_name']
            cat_desc = request.POST['cat_desc']

            if request.FILES.get('cat_img') is not None:
                cat_img = request.FILES.get('cat_img')
            else:
                cat_img = banners.category_image
            banners.category_name = cat_name
            banners.category_code = banners.category_code
            banners.description = cat_desc
            banners.category_image = cat_img
            banners.save()
            banners = Category.objects.filter(id=id)
            to_get_raw = Category.objects.get(id=id)
            raw_name = os.path.basename(to_get_raw.category_image.name)
            raw_size = os.stat(to_get_raw.category_image.path)
            raw_mb_size = str(raw_size.st_size / (1024 * 1024))[:5]
            edit_saved = 'The changes has been saved'
            return render(request, 'AdminTemplates/editCategory.html', {'edit_saved': edit_saved, 'banners': banners, 'raw_name': raw_name, 'raw_mb_size': raw_mb_size})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editCategory(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            banners = Category.objects.filter(id=id)
            to_get_raw = Category.objects.get(id=id)
            raw_name = os.path.basename(to_get_raw.category_image.name)
            raw_size = os.stat(to_get_raw.category_image.path)
            raw_mb_size = str(raw_size.st_size / (1024 * 1024))[:5]
            return render(request, 'AdminTemplates/editCategory.html', {'banners': banners, 'raw_name': raw_name, 'raw_mb_size': raw_mb_size})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def sideBanners(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            banners = Banners.objects.all()
            return render(request, 'AdminTemplates/sideBanners.html', {'banners': banners})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def add_sideBanners_form(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                banners = Banners.objects.all()
                if banners:
                    if id == str(1):
                        banner_id = request.session['banner_id']
                        add_banner = request.FILES['add_banner']
                        new_banner = Banners.objects.get(id=banner_id)
                        new_banner.top_left_banner = add_banner
                        new_banner.save()
                    elif id == str(2):
                        banner_id = request.session['banner_id']
                        add_banner = request.FILES['add_banner']
                        new_banner = Banners.objects.get(id=banner_id)
                        new_banner.top_right_banner = add_banner
                        new_banner.save()
                    elif id == str(3):
                        banner_id = request.session['banner_id']
                        add_banner = request.FILES['add_banner']
                        new_banner = Banners.objects.get(id=banner_id)
                        new_banner.bottom_right_banner = add_banner
                        new_banner.save()
                    else:
                        return redirect('sideBanners')

                else:
                    add_banner = request.FILES['add_banner']
                    banners = Banners(top_left_banner=add_banner,
                                    top_right_banner=add_banner, bottom_right_banner=add_banner)
                    banners.save()
                    request.session['banner_id'] = banners.id
                    return redirect('sideBanners')
            return redirect('sideBanners')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def delete_sideBanners(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            banner_id = request.session['banner_id']
            mainpost = Banners.objects.get(id=banner_id)
            if id == str(1):
                os.remove(mainpost.top_left_banner.path)
                mainpost.top_left_banner.delete()
                top_left_banner = 'top_left_banner'
                mainpost.top_left_banner = top_left_banner
                mainpost.save()
                return redirect('sideBanners')
            if id == str(2):
                os.remove(mainpost.top_right_banner.path)
                mainpost.top_right_banner.delete()
                top_right_banner = 'top_right_banner'
                mainpost.top_right_banner = top_right_banner
                mainpost.save()
                return redirect('sideBanners')
            if id == str(3):
                os.remove(mainpost.bottom_right_banner.path)
                mainpost.bottom_right_banner.delete()
                bottom_right_banner = 'bottom_right_banner'
                mainpost.bottom_right_banner = bottom_right_banner
                mainpost.save()
                return redirect('sideBanners')
            else:
                return redirect('sideBanners')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def addBanner(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            carousals = Carousal.objects.all()
            return render(request, 'AdminTemplates/addBanner.html', {'carousals': carousals})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def msg_banner(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            carousals = Carousal.objects.all()
            msg = 'You are only allowed to add 2 carousals...please delete one to add new'
            return render(request, 'AdminTemplates/addBanner.html', {'carousals': carousals, 'msg': msg})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def add_carousal_form(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid = request.session['adminid']
            if request.method == 'POST':
                # my_total = Carousal.objects.count()
                # if my_total >= 2:
                #     return redirect('msg_banner')
                # else:
                carousal_img = request.FILES['carousal']
                db = Carousal(carousal_home_main=carousal_img)
                db.save()
                return redirect('addBanner')
            return redirect('addBanner')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def deleteBanner(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Carousal.objects.get(id=id)
            os.remove(mainpost.carousal_home_main.path)
            mainpost.delete()
            return redirect('addBanner')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def deleteBrand(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Brands.objects.get(id=id)
            os.remove(mainpost.brand_image.path)
            mainpost.delete()
            return redirect('addBrand')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def cat_del_msg(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            categoryList = Category.objects.all()
            cat_deleted = request.session['cat_deleted']
            return render(request, 'AdminTemplates/categoryList.html', {'cat_deleted': cat_deleted, 'categoryList': categoryList})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pro_del_msg(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            pro_list = Product.objects.all()
            pro_deleted = request.session['pro_deleted']
            return render(request, 'AdminTemplates/productList.html', {'pro_list': pro_list, 'pro_deleted': pro_deleted})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def blog_del_msg(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            blog_list = Blogs.objects.all()
            blog_deleted = request.session['blog_deleted']
            return render(request, 'AdminTemplates/addBlogs.html', {'blog_list': blog_list, 'blog_deleted': blog_deleted})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def deleteCategory(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Category.objects.get(id=id)
            os.remove(mainpost.category_image.path)
            mainpost.delete()
            cat_deleted = f"{mainpost.category_name}"
            request.session['cat_deleted'] = cat_deleted
            return redirect('cat_del_msg')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def deleteProduct(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Product.objects.get(id=id)
            os.remove(mainpost.product_image.path)
            mainpost.delete()
            pro_deleted = f"{mainpost.product_name}"
            request.session['pro_deleted'] = pro_deleted
            return redirect('pro_del_msg')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def deletePreBuilt(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = PreBuilt.objects.get(id=id)
            os.remove(mainpost.product_image.path)
            if mainpost.product_image_1 == "":
                pass
            else:
                os.remove(mainpost.product_image_1.path)
            if mainpost.product_image_2 == "":
                pass
            else:
                os.remove(mainpost.product_image_2.path)
            if mainpost.product_image_3 == "":
                pass
            else:
                os.remove(mainpost.product_image_3.path)
            if mainpost.product_image_4 == "":
                pass
            else:
                os.remove(mainpost.product_image_4.path)
            if mainpost.product_image_5 == "":
                pass
            else:
                os.remove(mainpost.product_image_5.path)
            mainpost.delete()
            return redirect('viewpreBuilt')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def deleteBlog(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Blogs.objects.get(id=id)
            mainpost.delete()
            blog_deleted = f"{mainpost.blog_name}"
            request.session['blog_deleted'] = blog_deleted
            return redirect('blog_del_msg')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def actdea(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                activedea = request.POST['activedea']
                db = Product.objects.get(id=activedea)
                if db.special == 1:
                    db.special = 0
                    db.save()
                    thisdict = {
                        "success": f"{db.product_name} is Not Special",
                        "html": "NotSpl",
                        "key": activedea,
                        "class": "btn-danger"
                    }
                    new1 = json.dumps(thisdict)
                    return HttpResponse(new1)
                if db.special == 0:
                    db.special = 1
                    db.save()
                    thisdict = {
                        "success": f"{db.product_name} is Special",
                        "html": "Special",
                        "key": activedea,
                        "class": "btn-success"
                    }
                    new1 = json.dumps(thisdict)
                    return HttpResponse(new1)
                else:
                    print('something wrong')
            else:
                print('Im out')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pre_actdea(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                activedea = request.POST['activedea']
                db = PreBuilt.objects.get(id=activedea)
                if db.status == 1:
                    db.status = 0
                    db.save()
                    thisdict = {
                        "success": f"{db.modal_name} is Deactivated",
                        "html": "Inactive",
                        "key": activedea,
                        "class": "btn-danger"
                    }
                    new1 = json.dumps(thisdict)
                    return HttpResponse(new1)
                if db.status == 0:
                    db.status = 1
                    db.save()
                    thisdict = {
                        "success": f"{db.modal_name} is Activated",
                        "html": "Active",
                        "key": activedea,
                        "class": "btn-success"
                    }
                    new1 = json.dumps(thisdict)
                    return HttpResponse(new1)
                else:
                    print('something wrong')
            else:
                print('Im out')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def actsts(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                activedea = request.POST['activedea']
                db = Product.objects.get(id=activedea)
                if db.status == 1:
                    db.status = 0
                    db.save()
                    thisdict = {
                        "success": f"{db.product_name} is Deactivated",
                        "html": "Inactive",
                        "key": activedea,
                        "class": "btn-danger"
                    }
                    new1 = json.dumps(thisdict)
                    return HttpResponse(new1)
                if db.status == 0:
                    db.status = 1
                    db.save()
                    thisdict = {
                        "success": f"{db.product_name} is Activated",
                        "html": "Active",
                        "key": activedea,
                        "class": "btn-success"
                    }
                    new1 = json.dumps(thisdict)
                    return HttpResponse(new1)
                else:
                    print('something wrong')
            else:
                print('Im out')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def addBrand(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            brands = Brands.objects.all()
            return render(request, 'AdminTemplates/addBrand.html', {'brands': brands})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def addBrand_Form(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                bnd_name = request.POST['bnd_name'].capitalize()
                mydata = Brands.objects.filter(brand_name=bnd_name).values()
                if mydata:
                    name_exists = f"{bnd_name}"
                    brands = Brands.objects.all()
                    return render(request, 'AdminTemplates/addBrand.html', {'name_exists': name_exists, 'brands': brands})
                else:
                    bnd_name = request.POST['bnd_name'].capitalize()
                    bnd_img = request.FILES['bnd_img']
                    brand = Brands(brand_name=bnd_name, brand_image=bnd_img)
                    brand.save()
                    added = f"{bnd_name}"
                    brands = Brands.objects.all()
                    return render(request, 'AdminTemplates/addBrand.html', {'added': added, 'brands': brands})
            return redirect('addBrand')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editBrand(request,id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            brand = Brands.objects.get(id=id)
            brands = Brands.objects.all()
            edit = 'edit'
            return render(request, 'AdminTemplates/addBrand.html', {'edit':edit,'brand': brand,'brands': brands})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editBrandFrom(request,id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                bnd_name = request.POST['bnd_name'].capitalize()
                brand = Brands.objects.get(id=id)
                if request.FILES.get('bnd_img') is not None:
                    bnd_img = request.FILES.get('bnd_img')
                    brand.brand_name = bnd_name
                    brand.brand_image = bnd_img
                    brand.save()
                    return redirect('addBrand')
                else:
                    brand.brand_name = bnd_name
                    brand.brand_image = brand.brand_image
                    brand.save()
                    return redirect('addBrand')
            else:
                return redirect('addBrand')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def preBuilt(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            prebuilts = PreBuilt.objects.all()
            count = 'add'
            return render(request, 'AdminTemplates/preBuilt.html', {'count': count, 'prebuilts': prebuilts})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pre_img_del(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = PreBuilt.objects.get(id=id)
            os.remove(mainpost.product_image.path)
            mainpost.product_image = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editPreBuilt_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pre_img_del_1(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = PreBuilt.objects.get(id=id)
            os.remove(mainpost.product_image_1.path)
            mainpost.product_image_1 = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editPreBuilt_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pre_img_del_2(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = PreBuilt.objects.get(id=id)
            os.remove(mainpost.product_image_2.path)
            mainpost.product_image_2 = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editPreBuilt_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pre_img_del_3(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = PreBuilt.objects.get(id=id)
            os.remove(mainpost.product_image_3.path)
            mainpost.product_image_3 = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editPreBuilt_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pre_img_del_4(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = PreBuilt.objects.get(id=id)
            os.remove(mainpost.product_image_4.path)
            mainpost.product_image_4 = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editPreBuilt_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pre_img_del_5(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = PreBuilt.objects.get(id=id)
            os.remove(mainpost.product_image_5.path)
            mainpost.product_image_5 = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editPreBuilt_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pro_img_del(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Product.objects.get(id=id)
            os.remove(mainpost.product_image.path)
            mainpost.product_image = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editProduct_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pro_img_del_1(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Product.objects.get(id=id)
            os.remove(mainpost.product_image_1.path)
            mainpost.product_image_1 = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editProduct_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pro_img_del_2(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Product.objects.get(id=id)
            os.remove(mainpost.product_image_2.path)
            mainpost.product_image_2 = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editProduct_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pro_img_del_3(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Product.objects.get(id=id)
            os.remove(mainpost.product_image_3.path)
            mainpost.product_image_3 = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editProduct_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pro_img_del_4(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Product.objects.get(id=id)
            os.remove(mainpost.product_image_4.path)
            mainpost.product_image_4 = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editProduct_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def pro_img_del_5(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            mainpost = Product.objects.get(id=id)
            os.remove(mainpost.product_image_5.path)
            mainpost.product_image_5 = ""
            mainpost.save()
            request.session['pre_id'] = id
            return redirect('editProduct_post_del')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editPreBuilt_post_del(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            id = request.session['pre_id']
            prebuilts = PreBuilt.objects.filter(id=id)
            pro_list_price = PreBuilt.objects.get(id=id)
            pro_price = pro_list_price.price[:-3]
            count = 'edit'
            return render(request, 'AdminTemplates/preBuilt.html', {'prebuilts': prebuilts, 'count': count, 'pro_price': pro_price})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editProduct_post_del(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            id = request.session['pre_id']
            cat_list = Category.objects.all()
            pro_list = Product.objects.filter(id=id)
            pro_list_price = Product.objects.get(id=id)
            pro_price = pro_list_price.price[:-3]
            count = 'edit'
            return render(request, 'AdminTemplates/addProduct.html', {'cat_list': cat_list, 'count': count, 'pro_list': pro_list, 'pro_price': pro_price})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editPreBuilt(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            prebuilts = PreBuilt.objects.filter(id=id)
            pro_list_price = PreBuilt.objects.get(id=id)
            pro_price = pro_list_price.price[:-3]
            count = 'edit'
            return render(request, 'AdminTemplates/preBuilt.html', {'prebuilts': prebuilts, 'count': count, 'pro_price': pro_price})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def viewPrebuiltDetails(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            prebuilts = PreBuilt.objects.filter(id=id)
            to_get_raw = PreBuilt.objects.get(id=id)
            raw_name = os.path.basename(to_get_raw.product_image.name)
            raw_name1 = os.path.basename(to_get_raw.product_image_1.name)
            raw_name2 = os.path.basename(to_get_raw.product_image_2.name)
            raw_name3 = os.path.basename(to_get_raw.product_image_3.name)
            raw_name4 = os.path.basename(to_get_raw.product_image_4.name)
            raw_name5 = os.path.basename(to_get_raw.product_image_5.name)
            return render(request, 'AdminTemplates/viewPrebuiltDetails.html', {'prebuilts': prebuilts, 'raw_name': raw_name, 'raw_name1': raw_name1, 'raw_name2': raw_name2,
                                                                       'raw_name3': raw_name3, 'raw_name4': raw_name4, 'raw_name5': raw_name5})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def viewpreBuilt(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            prebuilts = PreBuilt.objects.all()
            return render(request, 'AdminTemplates/viewpreBuilt.html', {'prebuilts': prebuilts})
        else:
            print('something wrong!')
    else:
        return redirect('/')

def addpreBuiltForm(request):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                pre_name = request.POST['pre_name'].capitalize()
                pre_cpu = request.POST['pre_cpu']
                pre_mntr = request.POST['pre_mntr']
                pre_mtrbrd = request.POST['pre_mtrbrd']
                pre_gpu = request.POST['pre_gpu']
                pre_ssd = request.POST['pre_ssd']
                pre_rom = request.POST['pre_rom']
                pre_ram = request.POST['pre_ram']
                pre_smps = request.POST['pre_smps']
                pre_des = request.POST['pre_des']
                pre_pic = request.FILES['pre_pic']

                if request.FILES.get('pre_pic1') is not None:
                    pre_pic1 = request.FILES.get('pre_pic1')
                else:
                    pre_pic1 = ""

                if request.FILES.get('pre_pic2') is not None:
                    pre_pic2 = request.FILES.get('pre_pic2')
                else:
                    pre_pic2 = ""

                if request.FILES.get('pre_pic3') is not None:
                    pre_pic3 = request.FILES.get('pre_pic3')
                else:
                    pre_pic3 = ""

                if request.FILES.get('pre_pic4') is not None:
                    pre_pic4 = request.FILES.get('pre_pic4')
                else:
                    pre_pic4 = ""

                if request.FILES.get('pre_pic5') is not None:
                    pre_pic5 = request.FILES.get('pre_pic5')
                else:
                    pre_pic5 = ""

                pre_price = request.POST['pre_price']
                mod_price = pre_price + '.00'
                code_length = 3  # Customize the length of the code
                x = datetime.datetime.now()
                salt = x.strftime("%f")[3:].upper()
                pre_cod = 'PRE-' + salt + \
                    ''.join(random.choices(string.ascii_uppercase +
                            string.digits, k=code_length))
                pre_add = PreBuilt(modal_name=pre_name, modal_code=pre_cod, modal_cpu=pre_cpu, modal_monitor=pre_mntr, modal_ram=pre_ram,
                                modal_motherbrd=pre_mtrbrd, modal_gpu=pre_gpu, modal_ssd=pre_ssd, modal_storage_rom=pre_rom, modal_smps=pre_smps,
                                modal_offer='Special', date_added=x, description=pre_des, price=mod_price, status=1, product_image=pre_pic,
                                product_image_1=pre_pic1, product_image_2=pre_pic2, product_image_3=pre_pic3, product_image_4=pre_pic4, product_image_5=pre_pic5)
                pre_add.save()
                added = f"{pre_name}"
                prebuilts = PreBuilt.objects.all()
                return redirect('viewpreBuilt')
            else:
                return redirect('preBuilt')
        else:
            print('something wrong!')
    else:
        return redirect('/')

def editpreBuiltForm(request, id):
    if 'adminid' in request.session:
        if request.session.has_key('adminid'):
            adminid= request.session['adminid']
            if request.method == 'POST':
                pre_name = request.POST['pre_name'].capitalize()
                pre_cpu = request.POST['pre_cpu']
                pre_mntr = request.POST['pre_mntr']
                pre_mtrbrd = request.POST['pre_mtrbrd']
                pre_gpu = request.POST['pre_gpu']
                pre_ssd = request.POST['pre_ssd']
                pre_rom = request.POST['pre_rom']
                pre_ram = request.POST['pre_ram']
                pre_smps = request.POST['pre_smps']
                pre_des = request.POST['pre_des']

                pre_price = request.POST['pre_price']
                mod_price = pre_price + '.00'
                pre_add = PreBuilt.objects.get(id=id)
                if request.FILES.get('pre_pic') is not None:
                    pre_pic = request.FILES.get('pre_pic')
                else:
                    pre_pic = pre_add.product_image

                if request.FILES.get('pre_pic1') is not None:
                    pre_pic1 = request.FILES.get('pre_pic1')
                else:
                    pre_pic1 = pre_add.product_image_1

                if request.FILES.get('pre_pic2') is not None:
                    pre_pic2 = request.FILES.get('pre_pic2')
                else:
                    pre_pic2 = pre_add.product_image_2

                if request.FILES.get('pre_pic3') is not None:
                    pre_pic3 = request.FILES.get('pre_pic3')
                else:
                    pre_pic3 = pre_add.product_image_3

                if request.FILES.get('pre_pic4') is not None:
                    pre_pic4 = request.FILES.get('pre_pic4')
                else:
                    pre_pic4 = pre_add.product_image_4

                if request.FILES.get('pre_pic5') is not None:
                    pre_pic5 = request.FILES.get('pre_pic5')
                else:
                    pre_pic5 = pre_add.product_image_5

                pre_add.modal_name = pre_name
                pre_add.modal_code = pre_add.modal_code
                pre_add.modal_cpu = pre_cpu
                pre_add.modal_monitor = pre_mntr
                pre_add.modal_ram = pre_ram
                pre_add.modal_motherbrd = pre_mtrbrd
                pre_add.modal_gpu = pre_gpu
                pre_add.modal_ssd = pre_ssd
                pre_add.modal_storage_rom = pre_rom
                pre_add.modal_smps = pre_smps
                pre_add.modal_offer = pre_add.modal_offer
                pre_add.date_added = pre_add.date_added
                pre_add.description = pre_des
                pre_add.price = mod_price
                pre_add.status = pre_add.status
                pre_add.product_image = pre_pic
                pre_add.product_image_1 = pre_pic1
                pre_add.product_image_2 = pre_pic2
                pre_add.product_image_3 = pre_pic3
                pre_add.product_image_4 = pre_pic4
                pre_add.product_image_5 = pre_pic5

                pre_add.save()
                edited = f"{pre_name}"
                prebuilts = PreBuilt.objects.all()
                return render(request, 'AdminTemplates/viewpreBuilt.html', {'prebuilts': prebuilts, 'edited': edited})
            else:
                return redirect('preBuilt')
        else:
            print('something wrong!')
    else:
        return redirect('/')