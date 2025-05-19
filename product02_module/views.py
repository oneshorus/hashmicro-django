from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from hashmicro.decorators import role_required
from module_engine.models import ModuleRegistry
from module_engine.libs.permissions import get_product_access_permissions
from django.http import JsonResponse
from .models import Product
from .forms import ProductForm, ProductModelForm


def list_products(request, module_name=None):
    title = 'HASHMICRO | ' + module_name

    products = Product.objects.all()
    modules = ModuleRegistry.objects.filter(is_installed=True)
    access = access = get_product_access_permissions(request.user)
    
    return render(request, 'product_module/product_list.html', {
        'title': title,
        'current_module': module_name,
        'products': products, 
        'modules': modules,
        'access': access
    })


def create_product(request, module_name=None):
    title = 'HASHMICRO | ' + module_name

    modules = ModuleRegistry.objects.filter(is_installed=True)
    access = access = get_product_access_permissions(request.user)

    if not access['allowed_create']:
        return redirect(f'/{module_name}/')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # form.save()
            Product.objects.create(
                name=form.cleaned_data['name'],
                barcode=form.cleaned_data['barcode'],
                price=form.cleaned_data['price'],
                stock=form.cleaned_data['stock']
            )
            return redirect(f'/{module_name}/')
    else:
        # form = ProductModelForm()
        # return render(request, 'product_module/product_form.html', { form: form })
        form = ProductForm()
    return render(request, 'product_module/product_form.html', {
        'title': title,
        'current_module': module_name,
        'modules': modules,
        'access': access,
        'form': form
    })


def update_product(request, pk, module_name=None):
    title = 'HASHMICRO | ' + module_name

    product = get_object_or_404(Product, pk=pk)
    modules = ModuleRegistry.objects.filter(is_installed=True)
    access = access = get_product_access_permissions(request.user)

    if not access['allowed_update']:
        return redirect(f'/{module_name}/')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.update_instance(product)
            return redirect(f'/{module_name}/')
    else:
        form = ProductForm()
        form.from_instance(product)
    return render(request, 'product_module/product_form.html', {
        'title': title,
        'current_module': module_name,
        'modules': modules,
        'access': access,
        'form': form,
        'is_edit': True
    })


@csrf_exempt
def delete_product(request, pk, module_name=None):
    if request.method == 'POST':
        Product.objects.filter(pk=pk).delete()
        return JsonResponse({'message': 'Product deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=405)