from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from .models import Product, Category, Brand, Unit, Supplier
from .forms import ProductForm, CategoryForm, BrandForm, UnitForm, SupplierForm


@login_required(login_url='login:login')
def products_list(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')
    stock_filter = request.GET.get('stock', '')

    # Valid sort fields map
    valid_sorts = {
        'code': 'product_code',
        '-code': '-product_code',
        'name': 'name',
        '-name': '-name',
        'category': 'category__name',
        '-category': '-category__name',
        'price': 'selling_price',
        '-price': '-selling_price',
        'status': 'is_active',
        '-status': '-is_active',
    }
    
    products = Product.objects.filter(deleted_at__isnull=True)

    if query:
        products = products.filter(
            Q(product_code__icontains=query) |
            Q(name__icontains=query) |
            Q(barcode__icontains=query)
        )

    # Stock filter took place
    if stock_filter == 'in_stock':
        products = products.filter(opening_stock__gt=0)
    elif stock_filter == 'out_of_stock':
        products = products.filter(opening_stock=0)
    elif stock_filter == 'low_stock':
        products = products.filter(opening_stock__lte=F('reorder_level'), opening_stock__gt=0)
    elif stock_filter == 'overstock':
        products = products.filter(opening_stock__gte=F('maximum_stock'))

    if sort_by in valid_sorts:
        products = products.order_by(valid_sorts[sort_by])
    else:
        # Default order
        products = products.order_by('-created_at')

    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'Products',
        'page_obj': page_obj,
        'query': query,
        'sort_by': sort_by,
        'stock_filter': stock_filter,
    }
    return render(request, 'products/product_table.html', context)


@login_required(login_url='login:login')
def products_page(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')
    stock_filter = request.GET.get('stock', '')

    # Valid sort fields map
    valid_sorts = {
        'code': 'product_code',
        '-code': '-product_code',
        'name': 'name',
        '-name': '-name',
        'category': 'category__name',
        '-category': '-category__name',
        'price': 'selling_price',
        '-price': '-selling_price',
        'status': 'is_active',
        '-status': '-is_active',
    }

    products = Product.objects.filter(deleted_at__isnull=True)

    if query:
        products = products.filter(
            Q(product_code__icontains=query) |
            Q(name__icontains=query) |
            Q(barcode__icontains=query)
        )

    # Stock filter
    if stock_filter == 'in_stock':
        products = products.filter(opening_stock__gt=0)
    elif stock_filter == 'out_of_stock':
        products = products.filter(opening_stock=0)
    elif stock_filter == 'low_stock':
        products = products.filter(opening_stock__lte=F('reorder_level'), opening_stock__gt=0)
    elif stock_filter == 'overstock':
        products = products.filter(opening_stock__gte=F('maximum_stock'))

    if sort_by in valid_sorts:
        products = products.order_by(valid_sorts[sort_by])
    else:
        # Default order
        products = products.order_by('-created_at')

    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'Products',
        'page_obj': page_obj,
        'query': query,
        'sort_by': sort_by,
        'stock_filter': stock_filter,
    }
    return render(request, 'products/products.html', context)



@login_required(login_url='login:login')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, deleted_at__isnull=True)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    context = {
        'page_title': f'Product - {product.name}',
        'product': product,
        'is_ajax': is_ajax,
        'base_template': 'base/blank.html' if is_ajax else 'base/base.html',
    }
    return render(request, 'products/product_detail.html', context)


from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required(login_url='login:login')
def product_create(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        products = Product.objects.filter(deleted_at__isnull=True)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            if is_ajax:
                return JsonResponse({'success': True})

            # return redirect('products:detail', pk=product.pk)
            response = render(
                request,
                "products/product_table.html",
                {"page_obj": products},
            )
            response["HX-Trigger"] = "productCreated"
            return response
        else:
            if is_ajax:
                context = {
                    'form': form,
                    'is_ajax': is_ajax,
                    'base_template': 'base/blank.html',
                }
                html = render_to_string('products/product_form.html', context, request=request)
                return JsonResponse({'success': False, 'html': html})
    else:
        form = ProductForm()

    context = {
        'page_title': 'Add Product',
        'form': form,
        'is_ajax': is_ajax,
        'base_template': 'base/blank.html' if is_ajax else 'base/base.html',
    }
    return render(request, 'products/product_form.html', context)


@login_required(login_url='login:login')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, deleted_at__isnull=True)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    products = Product.objects.filter(deleted_at__isnull=True)


    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.updated_by = request.user
            prod.save()
            messages.success(request, f'Product "{prod.name}" updated successfully!')
            if is_ajax:
                return JsonResponse({'success': True})
            # return redirect('products:detail', pk=prod.pk)

            # response = redirect('products:list')
            response = render(
                request,
                "products/product_table.html",
                {"page_obj": products},
            )
            response["HX-Trigger"] = "productUpdated"
            return response
        else:
            if is_ajax:
                context = {
                    'form': form,
                    'product': product,
                    'is_ajax': is_ajax,
                    'base_template': 'base/blank.html',
                }
                html = render_to_string('products/product_form.html', context, request=request)
                return JsonResponse({'success': False, 'html': html})
    else:
        form = ProductForm(instance=product)

    context = {
        'page_title': f'Edit Product - {product.name}',
        'form': form,
        'product': product,
        'is_ajax': is_ajax,
        'base_template': 'base/blank.html' if is_ajax else 'base/base.html',
    }
    return render(request, 'products/product_form.html', context)


@login_required(login_url='login:login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, deleted_at__isnull=True)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    products = Product.objects.filter(deleted_at__isnull=True)


    if request.method == 'POST':
        product_name = product.name
        from django.utils import timezone
        product.deleted_at = timezone.now()
        product.save()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        if is_ajax:
            return JsonResponse({'success': True})
        # return redirect('products:list')
        response = render(
            request,
            "products/product_table.html",
            {"page_obj": products},
        )
        response["HX-Trigger"] = "productDeleted"
        return response

    context = {
        'page_title': f'Delete Product - {product.name}',
        'product': product,
        'is_ajax': is_ajax,
        'base_template': 'base/blank.html' if is_ajax else 'base/base.html',
    }
    return render(request, 'products/product_confirm_delete.html', context)

