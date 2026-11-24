from django.contrib import admin
from .models import Product, Category, Brand, Unit, Supplier


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'created_at', 'updated_at']
    search_fields = ['name', 'abbreviation']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'city', 'created_at']
    search_fields = ['name', 'email', 'city']
    list_filter = ['city', 'country']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_code', 'name', 'category', 'selling_price', "image",  'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'brand', 'created_at']
    search_fields = ['product_code', 'barcode', 'name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('product_code', 'barcode', 'name', 'description')
        }),
        ('Classification', {
            'fields': ('category', 'brand', 'unit', 'supplier')
        }),
        ('Pricing', {
            'fields': ('purchase_price', 'selling_price', 'wholesale_price', 'tax_rate', 'discount')
        }),
        ('Stock Management', {
            'fields': ('reorder_level', 'maximum_stock', 'opening_stock', 'opening_stock_date')
        }),
        ('Physical Dimensions', {
            'fields': ('weight', 'length', 'width', 'height')
        }),
        ('Media & Warranty', {
            'fields': ('image', 'warranty_months')
        }),
        ('Tracking Options', {
            'fields': ('expiry_tracking', 'batch_tracking', 'serial_tracking')
        }),
        ('Status & Timestamps', {
            'fields': ('is_active', 'deleted_at', 'created_by', 'updated_by', 'created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

