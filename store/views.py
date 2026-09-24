from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Product
from .forms import ProductForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, CartItem
import stripe
from django.conf import settings
from django.urls import reverse
from .models import Order, OrderItem
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm, CheckoutForm

stripe.api_key = settings.STRIPE_SECRET_KEY

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


@login_required
def product_create_view(request):
    if not request.user.is_approved:
        messages.error(request, "Only approved users can list products.")
        return redirect('store:product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, "Product listed successfully.")
            return redirect('store:product_detail', pk=product.pk)
    else:
        form = ProductForm()

    return render(request, 'store/product_form.html', {'form': form, 'action': 'Add'})


@login_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        raise PermissionDenied("You can only edit your own products.")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('store:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/product_form.html', {'form': form, 'action': 'Edit'})


@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.owner != request.user:
        raise PermissionDenied("You can only delete your own products.")

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect('store:product_list')

    return render(request, 'store/product_confirm_delete.html', {'product': product})

@login_required
def add_to_cart_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f'"{product.name}" added to your cart.')
    return redirect('store:product_detail', pk=product.pk)


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
def update_cart_item_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            item.delete()
            messages.success(request, "Item removed from cart.")
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, "Cart updated.")

    return redirect('store:cart')


@login_required
def remove_from_cart_view(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('store:cart')

@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('store:cart')

    form = CheckoutForm(initial={'email': request.user.email})
    return render(request, 'store/checkout.html', {
        'form': form,
        'cart': cart,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })


@login_required
def create_payment_intent_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        return JsonResponse({'error': 'Your cart is empty.'}, status=400)

    data = json.loads(request.body)
    form = CheckoutForm(data)

    if not form.is_valid():
        return JsonResponse({'error': 'Please fill in all fields correctly.', 'form_errors': form.errors}, status=400)

    order = form.save(commit=False)
    order.user = request.user
    order.total_price = cart.total_price()
    order.save()

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )

    intent = stripe.PaymentIntent.create(
        amount=int(order.total_price * 100),
        currency='usd',
        metadata={'order_id': order.id},
    )
    order.stripe_payment_intent_id = intent.id
    order.save()

    cart.items.all().delete()

    return JsonResponse({'client_secret': intent.client_secret, 'order_id': order.id})


@login_required
def checkout_complete_view(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id, user=request.user)

    intent = stripe.PaymentIntent.retrieve(order.stripe_payment_intent_id)

    if intent.status == 'succeeded':
        order.status = Order.Status.PAID
        order.save()
        messages.success(request, "Payment successful! Your order is confirmed.")
    else:
        messages.warning(request, "Payment was not completed.")

    return redirect('store:order_detail', pk=order.id)
@login_required
def order_list_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})