from django.views import View
from django.shortcuts import render
from django.db.models import Max, Sum, Avg, Count, F, FloatField
from django.db.models.functions import Cast
from apps.shop.models import ProductDiscount, Category, Brand, ShoppingCartProduct, ShoppingCart

class Discounts(View):

    def get(self, request):

        # User
        user = request.user

        # Obtener todos los productos
        products = ProductDiscount.objects.prefetch_related(
            'product__photos'
            ).select_related(
            'product'
            ).annotate(
            average_rating=Avg('product__reviews__rating'),
            review_count=Count('product__reviews')
            ).filter(
            product__is_active=True
            ).order_by(
            '-product__created_at'
            )

        # Obtener las categorías y marcas para los filtros
        categories = Category.objects.all()
        brands = Brand.objects.all()

        # Obtener los parámetros de filtro de la URL
        category_id = request.GET.get('category')
        brand_id = request.GET.get('brand')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # Aplicar filtros si están presentes en la URL
        if category_id:
            products = products.filter(product__category_id=category_id)
        if brand_id:
            products = products.filter(product__brand_id=brand_id)
        if min_price:
            products = products.annotate(min_price_discounted=Cast(F('product__price') - F('discount_value'), output_field=FloatField()))
            products = products.filter(min_price_discounted__gte=min_price)
        if max_price:
            products = products.annotate(max_price_discounted=Cast(F('product__price') - F('discount_value'), output_field=FloatField()))
            products = products.filter(max_price_discounted__lte=max_price)

        if user.is_authenticated:
            # Obtener el carrito del usuario
            try:
                shopping_cart = ShoppingCart.objects.get(user=user, is_active=True)
            except ShoppingCart.DoesNotExist:
                shopping_cart = None
            
            # Obtener la cantidad de productos en el carrito
            if shopping_cart:
                product_count = ShoppingCartProduct.objects.filter(cart=shopping_cart).count()
            else:
                product_count = 0
        else:
            product_count = None

        context = {
            'products': products,
            'categories': categories,
            'brands': brands,
            'selected_category': int(category_id) if category_id else None,
            'selected_brand': int(brand_id) if brand_id else None,
            'min_price': min_price,
            'max_price': max_price,
            'products_cart_count': product_count,
            'path': request.path
        }

        return render(request, 'shop/discounts_list.html', context)