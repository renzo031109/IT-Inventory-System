import django_filters
from django_filters import DateFilter, CharFilter, ChoiceFilter
from .models import Item, ItemBase, Department, Client, Site
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
clients = Client.objects.all()
clients_list = []

#get client values
for value in clients:
    clients_list.append((value.id, value.client))


#client list
site = Site.objects.all()
site_list = []

#get client values
for value in site:
    site_list.append((value.id, value.site))




class DateInput(forms.DateInput):
    input_type = 'date'


class ItemFilter(django_filters.FilterSet):
    site= ChoiceFilter(field_name='site', label="STORAGE LOCATION", choices=site_list)
    item_name = CharFilter(field_name='item_name', lookup_expr='icontains', label="ITEM NAME")
    brand_name = CharFilter(field_name='brand_name', lookup_expr='icontains', label="BRAND NAME")
    remarks = ChoiceFilter(field_name='remarks', label="REMARKS", choices=remarks_select)
    date_from = DateFilter(field_name='date_added', lookup_expr='date__gte', label="DATE FROM", widget=DateInput(attrs={'type': 'date'}))
    date_to = DateFilter(field_name='date_added', lookup_expr='date__lte', label="DATE TO", widget=DateInput(attrs={'type': 'date'}))
    staff_name = CharFilter(field_name='staff_name', lookup_expr='icontains', label="STAFF NAME")
    department= ChoiceFilter(field_name='department_name', label="DEPARTMENT", choices=departments_list)
    client= ChoiceFilter(field_name='client_name', label="CLIENT", choices=clients_list)
   
    class Meta:
        model = Item
        fields = ['site','item_name','brand_name','remarks','staff_name','department','client','date_from','date_to']


class ItemBaseFilter(django_filters.FilterSet):
    site= ChoiceFilter(field_name='site', label="STORAGE LOCATION", choices=site_list)
    item_name = CharFilter(field_name='item_name', lookup_expr='icontains', label="ITEM NAME")
    brand_name = CharFilter(field_name='brand_name', lookup_expr='icontains', label="BRAND NAME")
    date_from = DateFilter(field_name='date_added', lookup_expr='date__gte', label="DATE FROM", widget=DateInput(attrs={'type': 'date'}))
    date_to = DateFilter(field_name='date_added', lookup_expr='date__lte', label="DATE TO", widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = ItemBase
        fields = ['site','item_name','brand_name','date_from','date_to']
