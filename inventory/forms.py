from django import forms
from django.forms import modelformset_factory, BaseFormSet
from .models import Item, ItemBase, ItemCode

        
class ItemNewForm(forms.ModelForm):
    class Meta:
        model = ItemBase
        fields = [ 
            'department',
            'site',
            'item_name',
            'brand_name',
            'soh','uom',
            'item_code',
            'remarks',
            'critical_value'
            ]
        labels = {
            'department': 'DEPARTMENT',
            'site': 'SITE',
            'item_name': 'ITEM NAME',
            'brand_name': 'BRAND NAME (NONE if N/A)',
            'soh': 'BEGINNING BALANCE',
            'item_code': 'ITEM CODE',
            'uom':'UOM',
            'remarks' : 'REMARKS',
            'critical_value': 'CRITICAL VALUE'

        }
        widgets = {
            'department': forms.Select(attrs={'class':'ItemNewForm', 'autocomplete': 'off', 'required':True}),
            'site': forms.Select(attrs={'class':'ItemNewForm', 'autocomplete': 'off', 'required':True}),
            'item_name': forms.TextInput(attrs={'class':'ItemNewForm','autocomplete': 'off', 'required':True}),
            'brand_name': forms.TextInput(attrs={'class':'ItemNewForm', 'value':'NONE', 'autocomplete': 'off', 'required':True}),
            'soh': forms.TextInput(attrs={'class':'ItemNewForm', 'autocomplete': 'off', 'required':True}),
            'uom': forms.Select(attrs={'class':'ItemNewForm', 'autocomplete': 'off', 'required':True}),
            'item_code': forms.TextInput(attrs={'class':'ItemNewForm','autocomplete': 'off','type':'hidden'}),
            'remarks': forms.TextInput(attrs={'value': 'OUT', 'type':'hidden'}),
            'critical_value': forms.TextInput(attrs={'class':'ItemNewForm', 'autocomplete': 'off','required':True})
        }




#Formset for Get Item
class ItemGetForm(forms.ModelForm):
    class Meta:
        model = Item

        fields= [
                'department',    
                'item_code',
                'quantity',
                'item_name',
                'brand_name',
                'member',
                'site',
                'remarks',
                'ticket'

        ]

        labels={
            # 'firstName':'FIRST NAME',
            # 'middleName': 'MIDDLE NAME',
            # 'lastName': 'LAST NAME',
            'department': 'DEPARTMENT',
            'member': 'STAFF NAME',
            'site': 'SITE',
            'floor': 'FLOOR',
            'ticket': 'TICKET NUMBER'

        }

        widgets={
            'department': forms.Select(attrs={
                'class':'form-control', 
                'required':True
                }),
            'item_code': forms.Select(attrs={
                'class':'form-control form-select',
                'autocomplete': 'off',
                'required':True
                }),
            'quantity': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': '0',
                'autocomplete': 'off',
                'required':True
                }),
            'remarks': forms.TextInput(attrs={
                'class':'form-control',
                'type':'hidden'
            }),
            'item_name': forms.TextInput(attrs={
                'class':'form-control',
                'type':'hidden'
                }),
            'brand_name': forms.TextInput(attrs={
                'class':'form-control',
                'type':'hidden'
                }),
            'staff_name': forms.TextInput(attrs={
                'class':'form-control',
                'type':'hidden'
                }),
            'member': forms.Select(attrs={
                'class':'form-control',
                }),

            'site': forms.Select(attrs={
                'class':'form-control', 
                'required':True
                }),

            'ticket': forms.TextInput(attrs={
                'class':'form-control',
                'autocomplete': 'off',
                }),
 

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_code'].queryset = ItemCode.objects.none()

        print("this site", self.data)

        if 'form-0-site' in self.data and 'form-0-department' in self.data:
            try:
                site_id = int(self.data.get('form-0-site'))
                department_id = int(self.data.get('form-0-department'))
                self.fields['item_code'].queryset = ItemCode.objects.filter(site_id=site_id, department_id=department_id).order_by('code')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['item_code'].queryset = ItemCode.objects.filter(site=self.instance.site, department=self.instance.department).order_by('code')
            

ItemModelFormSet = modelformset_factory(Item, form=ItemGetForm, extra=1) 



#Formset for Add Item

class ItemAddForm(forms.ModelForm):

    class Meta:
        model = Item

        fields=[
            'item_code',
            'quantity',
            'item_name',
            'brand_name',
            'staff_name',
            'site',
            'department'
        ]
     
        labels={
            'staff_name': 'STAFF NAME',
            'site': 'SITE',
            'department': 'DEPARTMEMT'
        }

        widgets={
            'department': forms.Select(attrs={
                'class':'form-control', 
                'required':True
                }),
            'item_code': forms.Select(attrs={
                'class':'form-control form-select',
                'autocomplete': 'off',
                'required':True
                }),
            'quantity': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': '0',
                'autocomplete': 'off',
                'id':'id_add_form-0-quantity',
                'required':True
                }),
            'remarks': forms.TextInput(attrs={
                'class':'form-control',
                'type':'hidden'
                }),
            'item_name': forms.TextInput(attrs={
                'class':'form-control',
                'type':'hidden'
                }),
            'brand_name': forms.TextInput(attrs={
                'class':'form-control',
                'type':'hidden'
                }),
            'staff_name': forms.TextInput(attrs={
                'class':'form-control',
        
                }),

            'site': forms.Select(attrs={
                'class':'form-control', 
                'required':True
                }),

        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_code'].queryset = ItemCode.objects.none()

        print("this site", self.data)

        if 'form-0-site' in self.data and 'form-0-department' in self.data:
            try:
                site_id = int(self.data.get('form-0-site'))
                department_id = int(self.data.get('form-0-department'))
                self.fields['item_code'].queryset = ItemCode.objects.filter(site_id=site_id, department_id=department_id).order_by('code')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['item_code'].queryset = ItemCode.objects.filter(site=self.instance.site, department=self.instance.department).order_by('code')

            

ItemModelFormSetAdd = modelformset_factory(Item, form=ItemAddForm, extra=1) 

