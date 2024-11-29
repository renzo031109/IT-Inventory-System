from django import forms
from django.forms import modelformset_factory, BaseFormSet
from .models import Item, ItemBase, ItemCode

        
class ItemNewForm(forms.ModelForm):
    class Meta:
        model = ItemBase
        fields = [ 
            'site',
            'item_name',
            'brand_name',
            'soh','uom',
            'item_code',
            'remarks',
            'critical_value'
            ]
        labels = {
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
            'site': forms.Select(attrs={'class':'ItemNewForm', 'autocomplete': 'off'}),
            'item_name': forms.TextInput(attrs={'class':'ItemNewForm','autocomplete': 'off'}),
            'brand_name': forms.TextInput(attrs={'class':'ItemNewForm', 'value':'NONE', 'autocomplete': 'off'}),
            'soh': forms.TextInput(attrs={'class':'ItemNewForm', 'autocomplete': 'off'}),
            'uom': forms.Select(attrs={'class':'ItemNewForm', 'autocomplete': 'off'}),
            'item_code': forms.TextInput(attrs={'class':'ItemNewForm','autocomplete': 'off','type':'hidden'}),
            'remarks': forms.TextInput(attrs={'value': 'OUT', 'type':'hidden'}),
            'critical_value': forms.TextInput(attrs={'class':'ItemNewForm', 'autocomplete': 'off'})
        }




#Formset for Get Item
class ItemGetForm(forms.ModelForm):
    class Meta:
        Item

        fields= ['item_code',
                'quantity',
                'item_name',
                'brand_name',
                'client_name',
                'department_name',
                'member',
                'site',
                'remarks',

        ]

        labels={
            # 'firstName':'FIRST NAME',
            # 'middleName': 'MIDDLE NAME',
            # 'lastName': 'LAST NAME',
            'member': 'STAFF NAME',
            'client_name': 'CLIENT NAME',
            'dapartment_name': 'DEPARTMENT NAME',
            'site': 'SITE',
            'floor': 'FLOOR',

        }

        widgets={
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
                'required':True
                }),
            'client_name': forms.Select(attrs={
                'class':'form-control',
                'required':True
                }),
            'department_name': forms.Select(attrs={
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

        if 'form-0-site' in self.data:
            try:
                site_id = int(self.data.get('form-0-site'))
                self.fields['item_code'].queryset = ItemCode.objects.filter(site_id=site_id).order_by('code')
            except (ValueError, TypeError):
                pass # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['item_code'].queryset = self.instance.site.itemcode_set.order_by('code')
            

ItemModelFormSet = modelformset_factory(Item, form=ItemGetForm, extra=1) 


#Formset for Add Item


ItemModelFormSetAdd = modelformset_factory(
    Item, 
    fields=(
        'item_code',
        'quantity',
        'item_name',
        'brand_name',
        'staff_name',
        'client_name',
        'department_name',
        # 'price'
        ),
    extra=1,
    labels={
        'staff_name': 'STAFF NAME',
        'client_name': 'CLIENT NAME',
        'dapartment_name': 'DEPARTMENT NAME',
        # 'price': 'PRICE'
    },
    widgets={
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
        'client_name': forms.Select(attrs={
            'class':'form-control',
            }),
        'department_name': forms.Select(attrs={
            'class':'form-control',
       
            }),
        # 'price': forms.TextInput(attrs={
        #     'class':'form-control',
        #     'required':True
        #     }),

    }
)

