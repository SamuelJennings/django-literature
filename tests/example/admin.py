from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
    # formfield_overrides = {
    #     models.JSONField: {"widget": JSONFormWidget(schema=schema)},
    # }
