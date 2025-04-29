from django.contrib import admin
from .models import Item, ItemBase, ItemCode, UOM, Site, Department, TeamMember


class ItemCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'site')


admin.site.site_header = "S360 Inventory System"
# admin.site.register(Item)
# admin.site.register(ItemBase)
admin.site.register(ItemCode, ItemCodeAdmin)
admin.site.register(UOM)
admin.site.register(Site)
admin.site.register(Department)
admin.site.register(TeamMember)


# Customizing the Clinic_Record admin view
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'brand_name', 'site','department')  # Fields displayed in the admin list view
    search_fields = ('item_name', 'brand_name', 'site','department')  # Enables search functionality
    list_filter = ('item_name', 'brand_name', 'site','department')  # Optional: Filters for better usability


# Customizing the Clinic_Record admin view
@admin.register(ItemBase)
class ItemBaseAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'brand_name', 'site','department')  # Fields displayed in the admin list view
    search_fields = ('item_name', 'brand_name', 'site','department')  # Enables search functionality
    list_filter = ('item_name', 'brand_name', 'site','department')  # Optional: Filters for better usability
