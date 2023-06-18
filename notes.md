# code to add to cart using ajax edited

# python

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product, Cart

def add_to_cart(request):
if request.is_ajax():
product_id = request.POST.get('product_id')
quantity = request.POST.get('quantity')
product = get_object_or_404(Product, pk=product_id)
cart, created = Cart.objects.get_or_create(user=request.user)
cart.add_to_cart(product, quantity)
return JsonResponse({'success': True})
else:
return JsonResponse({'success': False})

# javascript

$(document).on('submit', '#add-to-cart-form', function(e) {
    e.preventDefault();
    var form = $(this);
    $.ajax({
    type: form.attr('method'),
    url: form.attr('action'),
    data: form.serialize(),
    success: function(response) {
    if (response.success) {
        alert('Product added to cart!');
    } else {
        alert('Error adding product to cart!');
        }
    }
    });
});

# code for random generation

import random
import string
import datetime

code_length = 3 # Customize the length of the code
x = datetime.datetime.now()
salt = x.strftime("%f")[3:].upper()

code = 'PRO-' + salt + ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length))

print(code)

# email encryption

from cryptography.fernet import Fernet

email = 'www.test@gmail.com'
print(email)

key = Fernet.generate_key()
f = Fernet(key)
encrypted_email = f.encrypt(email.encode())
print('encrypted email : ',encrypted_email)

print('-------------------------------------------------------------------------')

decrypted_email = f.decrypt(encrypted_email.decode())
double_decription = str(decrypted_email)[1:]
print('normal email : ',email)
print('decrypted email : ',decrypted_email)
print('double decrypted email : ',double_decription)

if f"'{email}'" == double_decription:
print('YES! its the same!')
else:
print('Not Same!')

# mask email or phone number

email = 'tw@gmail.com'
phone = '9876543210'
print(email)
print(phone)

this = email.find('@')
if this>0:
print("masked email : " + email[:1]+ "\*\*\*\*" + email[this-2:])
else:
print("enter valid email address")

print("masked phone : " + phone[:2]+ "**\*\***" + phone[-2:])

# Carousal Codes

<!DOCTYPE html>
<html>

<head>
  <!-- Include Bootstrap CSS -->
  <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
</head>
<style>
  /* Custom CSS for smaller main container */
  .container {
    max-width: 800px;
  }

  /* Custom CSS for responsive feedback on interaction */
  .carousel-control.left,
  .carousel-control.right {
    background: rgba(0, 0, 0, 0.5);
    top: 50%;
    transform: translateY(-50%);
  }

  .carousel-control.left {
    left: 0;
  }

  .carousel-control.right {
    right: 0;
  }

  .carousel-control.left:hover,
  .carousel-control.right:hover {
    background: rgba(0, 0, 0, 0.7);
  }
</style>

<body>
  <!-- Your HTML content goes here -->
  <div class="container"><br><br>
    <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
      <!-- Indicators -->
      <ol class="carousel-indicators">
        <li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>
        <li data-target="#carousel-example-generic" data-slide-to="1"></li>
        <li data-target="#carousel-example-generic" data-slide-to="2"></li>
      </ol>
      <!-- Wrapper for slides -->
      <div class="carousel-inner" role="listbox">
        <div class="item active">
          <img src="https://unsplash.it/1400/600?image=62" alt="Image">
        </div>
        <div class="item">
          <img src="https://unsplash.it/1400/600?image=62" alt="Image">
          <div class="carousel-caption">
          </div>
        </div>
        <div class="item">
          <img src="https://unsplash.it/1400/600?image=315" alt="Image">
          <div class="carousel-caption">
            <h5>Lorem, ipsum dolor.</h5>
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus labore quidem, ducimus
              cumque
              omnis architecto.</p>
          </div>
        </div>
      </div>
      <!-- Controls -->
      <a class="left carousel-control" href="#carousel-example-generic" role="button" data-slide="prev"
        style="background: rgba(0,0,0,0);">
        <span class="glyphicon glyphicon-chevron-left"></span>
        <span class="sr-only">Previous</span>
      </a>
      <a class="right carousel-control" href="#carousel-example-generic" role="button" data-slide="next"
        style="background: rgba(0,0,0,0);">
        <span class="glyphicon glyphicon-chevron-right"></span>
        <span class="sr-only">Next</span>
      </a>
    </div>
  </div>
  <!-- Include jQuery and Bootstrap JavaScript -->
  <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
  <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>

  <!-- Include Bootstrap JavaScript and jQuery -->
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>

  <script>
    $(document).ready(function () {
      // Activate Carousel
      $('#carousel-example-generic').carousel();

      // Enable Carousel Indicators
      $('.carousel-indicators li').click(function () {
        $('.carousel-indicators li').removeClass('active');
        $(this).addClass('active');
      });

      // Enable Carousel Controls
      $('.carousel-control-prev').click(function () {
        $('#carousel-example-generic').carousel('prev');
      });

      $('.carousel-control-next').click(function () {
        $('#carousel-example-generic').carousel('next');
      });
    });
  </script>

</body>

</html>


<div class="container mt-5 mb-5">
    <div class="d-flex justify-content-center row">
        <div class="col-md-10">
            <div class="row p-2 bg-white border rounded">
                <div class="col-md-3 mt-1"><img class="img-fluid img-responsive rounded product-image" src="https://i.imgur.com/QpjAiHq.jpg"></div>
                <div class="col-md-6 mt-1">
                    <h5>Quant olap shirts</h5>
                    <div class="d-flex flex-row">
                        <div class="ratings mr-2"><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i><i class="fa fa-star"></i></div><span>310</span>
                    </div>
                    <div class="mt-1 mb-1 spec-1"><span>100% cotton</span><span class="dot"></span><span>Light weight</span><span class="dot"></span><span>Best finish<br></span></div>
                    <div class="mt-1 mb-1 spec-1"><span>Unique design</span><span class="dot"></span><span>For men</span><span class="dot"></span><span>Casual<br></span></div>
                    <p class="text-justify text-truncate para mb-0">There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable.<br><br></p>
                </div>
                <div class="align-items-center align-content-center col-md-3 border-left mt-1">
                    <div class="d-flex flex-row align-items-center">
                        <h4 class="mr-1">$13.99</h4><span class="strike-text">$20.99</span>
                    </div>
                    <h6 class="text-success">Free shipping</h6>
                    <div class="d-flex flex-column mt-4"><button class="btn btn-primary btn-sm" type="button">Details</button><button class="btn btn-outline-primary btn-sm mt-2" type="button">Add to wishlist</button></div>
                </div>
            </div>
        </div>
    </div>
</div>


C:\Users\ROBIN\Desktop\TronPC\static\images\cache\catalog\banners

## code for two rows and two cols

<div id="content" class="col-sm-9">
    <div class="row">
        <div class="col-sm-6">
            <div class="containerz">
                <div class="containerz__item">
                    <input type="email" class="form__field" placeholder="Preferred RAM" />
                    <button type="button" class="btn btn--primary btn--inside uppercase">RAM</button>
                </div>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="containerz">
                <div class="containerz__item">
                    <input type="email" class="form__field" placeholder="Preferred ROM" />
                    <button type="button" class="btn btn--primary btn--inside uppercase">ROM</button>
                </div>
            </div>
        </div>
    </div><br>
    <div class="row">
        <div class="col-sm-6">
            <div class="containerz">
                <div class="containerz__item">
                    <input type="email" class="form__field" placeholder="Preferred GPU" />
                    <button type="button" class="btn btn--primary btn--inside uppercase">GPU</button>
                </div>
            </div>
        </div>
        <div class="col-sm-6">
            <div class="containerz">
                <div class="containerz__item">
                    <input type="email" class="form__field" placeholder="Preferred GPU" />
                    <button type="button" class="btn btn--primary btn--inside uppercase">GPU</button>
                </div>
            </div>
        </div>
    </div><br>
    <div class="modal-footer">
        <button type="button" class="btn btn-primary">Add to Cart</button>
    </div>
</div>




## Issues:

1.Brand Logo not showing (Admin)
2.No Images Showing (All)
3.