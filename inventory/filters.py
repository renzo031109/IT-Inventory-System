import django_filters
from django_filters import DateFilter, CharFilter, ChoiceFilter
from .models import Item, ItemBase, Site, Department
from django import forms


remarks_select = (
    ('IN', 'IN'),
    ('OUT', 'OUT'),
    ('BEGINNING','BEGINNING')
)

#department list
departments = Department.objects.all()
departments_list = []

#get department values
for value in departments:
    departments_list.append((value.id, value.department))



#client list
site = Site.objects.all()
site_list = []

#get client values
for value in site:
    site_list.append((value.id, value.site))




class DateInput(forms.DateInput):
    input_type = 'date'


class ItemFilter(django_filters.FilterSet):
    department= ChoiceFilter(field_name='department', label="DEPARTMENT", choices=departments_list)
    site= ChoiceFilter(field_name='site', label="STORAGE LOCATION", choices=site_list)
    item_name = CharFilter(field_name='item_name', lookup_expr='icontains', label="ITEM NAME")
    brand_name = CharFilter(field_name='brand_name', lookup_expr='icontains', label="BRAND NAME")
    remarks = ChoiceFilter(field_name='remarks', label="REMARKS", choices=remarks_select)
    date_from = DateFilter(field_name='date_added', lookup_expr='date__gte', label="DATE FROM", widget=DateInput(attrs={'type': 'date'}))
    date_to = DateFilter(field_name='date_added', lookup_expr='date__lte', label="DATE TO", widget=DateInput(attrs={'type': 'date'}))
    staff_name = CharFilter(field_name='staff_name', lookup_expr='icontains', label="STAFF NAME")
    staff_name = CharFilter(field_name='ticket', lookup_expr='icontains', label="TICKET NO.")
   
    class Meta:
        model = Item
        fields = ['department','site','item_name','brand_name','remarks','staff_name','date_from','date_to', 'ticket']


class ItemBaseFilter(django_filters.FilterSet):
    department= ChoiceFilter(field_name='department', label="DEPARTMENT", choices=departments_list)
    site= ChoiceFilter(field_name='site', label="STORAGE LOCATION", choices=site_list)
    item_name = CharFilter(field_name='item_name', lookup_expr='icontains', label="ITEM NAME")
    brand_name = CharFilter(field_name='brand_name', lookup_expr='icontains', label="BRAND NAME")
    date_from = DateFilter(field_name='date_added', lookup_expr='date__gte', label="DATE FROM", widget=DateInput(attrs={'type': 'date'}))
    date_to = DateFilter(field_name='date_added', lookup_expr='date__lte', label="DATE TO", widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ItemBase
        fields = ['department','site','item_name','brand_name','date_from','date_to']
