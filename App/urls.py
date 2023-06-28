from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from App import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_to_cart_form/<int:id>', views.add_to_cart_form, name='add_to_cart_form'),
    path('addToCartPreBuilt/<int:id>', views.addToCartPreBuilt, name='addToCartPreBuilt'),
    path('allProducts/', views.allProducts, name='allProducts'),
    path('cart/', views.cart, name='cart'),
    path('cartDelete/<int:id>', views.cartDelete, name='cartDelete'),
    path('cartQuaAdd/<int:id>', views.cartQuaAdd, name='cartQuaAdd'),
    path('categoryFilter/<int:id>', views.categoryFilter, name='categoryFilter'),
    path('change_init_page/', views.change_init_page, name='change_init_page'),
    path('change_init_page_to_online/', views.change_init_page_to_online, name='change_init_page_to_online'),
    path('checkOut/', views.checkOut, name='checkOut'),
    path('contact/', views.contact, name='contact'),
    path('contactHome/', views.contactHome, name='contactHome'),
    path('cusDelete/<int:id>', views.cusDelete, name='cusDelete'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('loginform/', views.loginform, name='loginform'),
    path('logout/', views.logout, name='logout'),
    path('mainIndex/', views.mainIndex, name='mainIndex'),
    path('pcbAddForm/', views.pcbAddForm, name='pcbAddForm'),
    path('pcbAddFormEdit/<int:id>', views.pcbAddFormEdit, name='pcbAddFormEdit'),
    path('preBuiltHome/', views.preBuiltHome, name='preBuiltHome'),
    path('productsHome/', views.productsHome, name='productsHome'),
    path('register/', views.register, name='register'),
    path('under_maintenance/', views.under_maintenance, name='under_maintenance'),
    path('uregister/', views.uregister, name='uregister'),
    path('view/<int:id>', views.view, name='view'),


    # ------------------ADMIN MODULE URLS------------------------------------#

    path('actdea/', views.actdea, name='actdea'),
    path('actsts/', views.actsts, name='actsts'),
    path('addBanner/', views.addBanner, name='addBanner'),
    path('addBlogs/', views.addBlogs, name='addBlogs'),
    path('addBlogsForm/', views.addBlogsForm, name='addBlogsForm'),
    path('addBrand/', views.addBrand, name='addBrand'),
    path('addBrand_Form/', views.addBrand_Form, name='addBrand_Form'),
    path('addCategory/', views.addCategory, name='addCategory'),
    path('addCategoryForm/', views.addCategoryForm, name='addCategoryForm'),
    path('addCarousalForm/', views.addCarousalForm, name='addCarousalForm'),
    path('addPreBuiltForm/', views.addPreBuiltForm, name='addPreBuiltForm'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('addProductForm/', views.addProductForm, name='addProductForm'),
    path('add_sideBanners_form/<int:id>', views.add_sideBanners_form, name='add_sideBanners_form'),
    path('adminDash/', views.adminDash, name='adminDash'),
    path('adminIndex/', views.adminIndex, name='adminIndex'),
    path('adminProfile/', views.adminProfile, name='adminProfile'),
    path('blog_del_msg/', views.blog_del_msg, name='blog_del_msg'),
    path('cat_del_msg/', views.cat_del_msg, name='cat_del_msg'),
    path('categoryList/', views.categoryList, name='categoryList'),
    path('deleteBanner/<int:id>', views.deleteBanner, name='deleteBanner'),
    path('deleteBlog/<int:id>', views.deleteBlog, name='deleteBlog'),
    path('deleteBrand/<int:id>', views.deleteBrand, name='deleteBrand'),
    path('deleteCategory/<int:id>', views.deleteCategory, name='deleteCategory'),
    path('deletePreBuilt/<int:id>', views.deletePreBuilt, name='deletePreBuilt'),
    path('deleteProduct/<int:id>', views.deleteProduct, name='deleteProduct'),
    path('delete_sideBanners/<int:id>', views.delete_sideBanners, name='delete_sideBanners'),
    path('editBlogs/<int:id>', views.editBlogs, name='editBlogs'),
    path('editBlogsForm/<int:id>', views.editBlogsForm, name='editBlogsForm'),
    path('editBrand/<int:id>', views.editBrand, name='editBrand'),
    path('editBrandFrom/<int:id>', views.editBrandFrom, name='editBrandFrom'),
    path('editCategory/<int:id>', views.editCategory, name='editCategory'),
    path('edit_category_form/<int:id>', views.edit_category_form, name='edit_category_form'),
    path('editPreBuilt/<int:id>', views.editPreBuilt, name='editPreBuilt'),
    path('editPreBuilt_post_del/', views.editPreBuilt_post_del, name='editPreBuilt_post_del'),
    path('editpreBuiltForm/<int:id>', views.editpreBuiltForm, name='editpreBuiltForm'),
    path('editProduct/<int:id>', views.editProduct, name='editProduct'),
    path('editProductForm/<int:id>', views.editProductForm, name='editProductForm'),
    path('editProduct_post_del/', views.editProduct_post_del, name='editProduct_post_del'),
    path('editSales/', views.editSales, name='editSales'),
    path('msg_banner/', views.msg_banner, name='msg_banner'),
    path('preBuilt/', views.preBuilt, name='preBuilt'),
    path('pre_actdea/', views.pre_actdea, name='pre_actdea'),
    path('pre_img_del/<int:id>', views.pre_img_del, name='pre_img_del'),
    path('pre_img_del_1/<int:id>', views.pre_img_del_1, name='pre_img_del_1'),
    path('pre_img_del_2/<int:id>', views.pre_img_del_2, name='pre_img_del_2'),
    path('pre_img_del_3/<int:id>', views.pre_img_del_3, name='pre_img_del_3'),
    path('pre_img_del_4/<int:id>', views.pre_img_del_4, name='pre_img_del_4'),
    path('pre_img_del_5/<int:id>', views.pre_img_del_5, name='pre_img_del_5'),
    path('pcb/', views.pcb, name='pcb'),
    path('pcbCustom/', views.pcbCustom, name='pcbCustom'),
    path('productDetails/<int:id>', views.productDetails, name='productDetails'),
    path('productList/', views.productList, name='productList'),
    path('pro_del_msg/', views.pro_del_msg, name='pro_del_msg'),
    path('pro_img_del_1/<int:id>', views.pro_img_del_1, name='pro_img_del_1'),
    path('pro_img_del_2/<int:id>', views.pro_img_del_2, name='pro_img_del_2'),
    path('pro_img_del_3/<int:id>', views.pro_img_del_3, name='pro_img_del_3'),
    path('pro_img_del_4/<int:id>', views.pro_img_del_4, name='pro_img_del_4'),
    path('pro_img_del_5/<int:id>', views.pro_img_del_5, name='pro_img_del_5'),
    path('salesDetails/<int:id>', views.salesDetails, name='salesDetails'),
    path('salesList/', views.salesList, name='salesList'),
    path('sideBanners/', views.sideBanners, name='sideBanners'),
    path('viewPrebuiltDetails/<int:id>', views.viewPrebuiltDetails, name='viewPrebuiltDetails'),
    path('viewpreBuilt/', views.viewpreBuilt, name='viewpreBuilt')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^maintenance_login/$', views.maintenance_login,
            name='maintenance_login'),
    path('<path:invalid_path>', views.error_404),
]
