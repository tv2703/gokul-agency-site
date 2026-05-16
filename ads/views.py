# ads/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, ProductImage
from .forms import ProductForm


def home(request):
    # Prefetch related images to keep queries fast
    products = Product.objects.prefetch_related('images').all()
    return render(request, 'ads/index.html', {'products': products})


@login_required(login_url='login')
def owner_dashboard(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        files = request.FILES.getlist('extra_images')

        if form.is_valid():
            if len(files) > 10:
                form.add_error('extra_images', 'Maximum limit exceeded! You can only upload up to 10 images.')
            else:
                product = form.save()
                for f in files:
                    ProductImage.objects.create(product=product, image=f)
                return redirect('dashboard')
    else:
        form = ProductForm()

    products = Product.objects.prefetch_related('images').all()
    return render(request, 'ads/dashboard.html', {'form': form, 'products': products})


@login_required(login_url='login')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        files = request.FILES.getlist('extra_images')

        if form.is_valid():
            if len(files) > 10:
                form.add_error('extra_images', 'Maximum limit exceeded! You can only upload up to 10 images.')
            else:
                form.save()
                # If new images are uploaded, clean out the old ones and update
                if files:
                    product.images.all().delete()
                    for f in files:
                        ProductImage.objects.create(product=product, image=f)
                return redirect('dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'ads/edit_product.html', {'form': form, 'product': product})


@login_required(login_url='login')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
    return redirect('dashboard')


def owner_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')