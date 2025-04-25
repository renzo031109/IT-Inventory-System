from typing import Any
from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Item, ItemBase, ItemCode, UOM, TeamMember, Site, Department
from .forms import ItemNewForm, ItemModelFormSet, ItemModelFormSetAdd
from .filters import ItemFilter, ItemBaseFilter
from django.http import HttpResponse
# from django.core.paginator import Paginator

#for export excel imports
from openpyxl.styles.borders import Border, Side, BORDER_THIN
from openpyxl import Workbook
from datetime import datetime
from openpyxl.styles import *

from django.http import JsonResponse
import json




@login_required
def summary_item(request):
    items = ItemBase.objects.all()
    # item_count_total= items.count()

    itemFilter = ItemBaseFilter(request.GET, queryset=items)
    items = itemFilter.qs
    item_count = items.count()

    if item_count > 0 :
        messages.info(request, f"Found '{item_count}' item(s) in the database")
    else:
        messages.info(request, f"Item not Found in the database ")

    # #pagination show 50 items per page
    # paginator = Paginator(items, 25)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    global filter_itembase_val
    def filter_itembase_val():
        return items

    # # Compute Total Value
    # total_value = 0
    # for value in items:
    #     total_value += float(value.total_value)

    context = {
        'items': items,
        'item_count': item_count,
        'itemFilter': itemFilter,
        # 'total_value': total_value
        # 'page_obj':page_obj
        }
    return render(request, 'inventory/summary.html', context)


@login_required
def inventory_item(request):
    
    items = Item.objects.all()
    # item_count_total= items.count()
    
    itemFilter = ItemFilter(request.GET, queryset=items)
    items = itemFilter.qs
    
    item_count = items.count()
    
    if item_count > 0 :
        messages.info(request, f"Found '{item_count}' transaction in the database")
    else:
        messages.info(request, f"Item not Found in the database ")
    
    # #pagination show 50 items per page
    # paginator = Paginator(items, 25)
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    #this will get the current filter in the report
    global filter_item_val
    def filter_item_val():
        return items
    
    
    itembase = ItemBase.objects.all()

    context = {
        'items': items, 
        'itembase': itembase,
        'item_count': item_count, 
        'itemFilter': itemFilter,
        # 'page_obj': page_obj
        }
    return render(request,'inventory/inventory.html', context)


@login_required
def delete_item(request, id):
    if request.method == 'POST':

        try:
            #get the selected value
            item = Item.objects.get(id=id)
            item_soh = ItemBase.objects.get(item_code=item.item_code)

            #return the quantity of the deleted item
            if int(item.quantity) > 0:
                #computation on positive value
                updated_soh = int(item_soh.soh) - int(item.quantity) 

                # # updated_total_price = updated_soh * item_soh.price
                # total = item.quantity * item_soh.price
                # item_val = item_soh.total_value - total

                print("posive")
            else:
                #computation on negative value
                updated_soh = int(item_soh.soh) - int(item.quantity)

                # updated_total_price = updated_soh * item_soh.price
                # total = item.quantity * item_soh.price
                # item_val = item_soh.total_value - total

                print("negative")

            item_soh.soh = updated_soh
            # item_soh.total_price = updated_total_price
            # item_soh.total_value = item_val

            #update Total value and save
            item_soh.save()
            item.delete()
            messages.success(request, "Item is deleted successfully")
        except:
            messages.error(request, "Unable to delete this item, please try again later")
    return redirect('inventory_item')



def delete_itembase(request, item_code):
    if request.method == 'POST':
        item = ItemBase.objects.get(item_code=item_code)
        itemcode = ItemCode.objects.get(code=item)

        print(item)
        print(itemcode)

        item.delete()
        itemcode.delete()

        messages.success(request, f"{item.item_name} is deleted successfully")
    return redirect('summary_item')



@login_required
def new_item(request):
    if request.method == 'POST':
        form = ItemNewForm(request.POST)

        if form.is_valid():
            # Get the values from the form
            form_item_department = request.POST.get('department')
            form_item_site = request.POST.get('site')
            form_item_name = request.POST.get('item_name')
            form_item_brand = request.POST.get('brand_name')
            form_item_soh = request.POST.get('soh')
            form_item_uom = request.POST.get('uom')

            # Convert id to values of foreign keys
            uom_value = UOM.objects.get(id=form_item_uom)
            site_value = Site.objects.get(id=form_item_site)
            department_value = Department.objects.get(id=form_item_department)

            # Formulate the item code
            concat = f"{form_item_name} | {form_item_brand} | {department_value} | {site_value}"

            # Check if the item code already exists
            if ItemBase.objects.filter(item_code__iexact=concat).exists():
                messages.error(request, f"The value '{concat}' already exists in the database. Please enter a different value.")
                return redirect('new_item')
            
            # Create the item code using the create method
            itemcode = ItemCode.objects.create(code=concat, site=site_value, department=department_value)
            
            # Assign form to a variable and save the main form data
            itemNewForm = form.save(commit=False)

            # Define user for the staff name
            try:
                user = request.user
                member = TeamMember.objects.get(member=user)
            except TeamMember.DoesNotExist:
                member = TeamMember.objects.get(member="ADMIN")

            # Copy new item to Item Transaction
            itemTransaction = Item(
                item_code=itemcode, 
                item_name=form_item_name, 
                brand_name=form_item_brand, 
                quantity=form_item_soh, 
                remarks="BEGINNING",
                uom=uom_value, 
                member=member,
                site=site_value,
                department=department_value,
                user=request.user
            )
            
            # Assign the generated code value to item_code
            itemNewForm.item_code = concat

            try:
                # Save tables if no error found
                itemNewForm.save()
                itemTransaction.save()
                itemcode.save()

                messages.success(request, "New Item added successfully!")
                return redirect('summary_item')
            except Exception as e:
                messages.error(request, f"Invalid Input: {e}")

    else:
        form = ItemNewForm()

    context = {'form': form}
    return render(request, 'inventory/new_item.html', context)




@login_required
def add_item(request):

    if request.method == 'POST':
        formset = ItemModelFormSetAdd(request.POST)
        if formset.is_valid():
            for form in formset:
                
                # check if itemcode is selected
                if form.cleaned_data.get('item_code') and form.cleaned_data.get('quantity'):  
                    
                    #get the item name from the form 
                    add_item_code = form.cleaned_data.get('item_code')
                    #get the item qty from the form
                    add_item_qty = form.cleaned_data.get('quantity')
                    # #get the price from the form
                    # add_item_price = form.cleaned_data.get('price')
                    
                    try:
                        #get the item SOH from model table
                        item_soh = ItemBase.objects.get(item_code=add_item_code)

    
                        #compute add soh
                        soh = int(item_soh.soh) + int(add_item_qty)
                        #get the updated soh after add
                        item_soh.soh = int(soh)
                        
                        # #compute item price
                        # added_item_amount = add_item_qty * add_item_price
                        
                        # #update Total value and price
                        # grand_total_value = item_soh.total_value + added_item_amount

                        # item_soh.total_value = grand_total_value
                        # item_soh.price = add_item_price
                        # item_soh.total_price = soh * item_soh.price

                        #save tables
                        item_soh.save()
                    except:
                        item_soh = 0
                        soh = int(item_soh) + int(add_item_qty)

                    #assign default values  
                    itemAddForm = form.save(commit=False)    
                    itemAddForm.remarks = "IN"
                    itemAddForm.item_name = item_soh.item_name
                    itemAddForm.brand_name = item_soh.brand_name
                    itemAddForm.uom = item_soh.uom
                    # itemAddForm.item_value = added_item_amount

                    #get the current user
                    try:
                        user = request.user
                        member = TeamMember.objects.get(member=user)
                        itemAddForm.member = member
                    except:
                        member = TeamMember.objects.get(member="ADMIN")
                        itemAddForm.member = member

  
                    itemAddForm.save()          
                
                else:

                    messages.error(request, "Invalid Input. Form is incomplete.")
                    return redirect('add_item')
                
            messages.success(request, "You added stock successfully!")
                
            return redirect('inventory_item')
        else:
            messages.error(request, "Invalid Input!")

    else:
        formset = ItemModelFormSetAdd(queryset=Item.objects.none())

    context = {'formset': formset}
    return render(request, 'inventory/add_item.html', context)


@login_required
def get_item(request):

    #Initiate a list variable for the input select fields
    department_name_list = []
    member_name_list = []
    site_name_list = []
    ticket_name_list = []

    #list for validation checking
    item_error_list = []
    item_success_list = []

    if request.method == 'POST':
        formset = ItemModelFormSet(request.POST)
        if formset.is_valid():          
            for form in formset:
    
                # only save if name is present
                if form.cleaned_data.get('item_code') and form.cleaned_data.get('quantity'): 

                    #get the item name from the form 
                    get_item_code = str(form.cleaned_data.get('item_code'))
                    item_soh = ItemBase.objects.get(item_code=get_item_code)

                    #get the item qty from the form
                    get_qty = form.cleaned_data.get('quantity')

                    # #get the item SOH from model table       
                    item_soh = ItemBase.objects.get(item_code=get_item_code)

                    # # get the staff name values
                    # get_firstName = form.cleaned_data.get('firstName')
                    # get_middleName = form.cleaned_data.get('middleName')
                    # get_lastName = form.cleaned_data.get('lastName')

                    get_department_name = form.cleaned_data.get('department')
                    get_member_name = form.cleaned_data.get('member')
                    get_site_name = form.cleaned_data.get('site')
                    get_ticket = form.cleaned_data.get('ticket')

                    # #populate the list from the user input
                    # staff_name_list.append(get_staff_name)
                    department_name_list.append(get_department_name)
                    member_name_list.append(get_member_name)
                    site_name_list.append(get_site_name)
                    ticket_name_list.append(get_ticket)
    
                    
                    #get the first value of the form
                    department_name = department_name_list[0]
                    member_name = member_name_list[0]
                    site_name = site_name_list[0]
                    ticket_name = ticket_name_list[0]

                  
                    if item_soh.soh < get_qty:
                        messages.error(request, f"Ooops, Your available stock for '{item_soh.item_name}' is only '{item_soh.soh}")
                        item_error_list.append(item_soh.item_name)
                    else:
                        item_success_list.append(item_soh.item_name)
                        #compute add soh
                        soh = int(item_soh.soh) - int(get_qty)
                        #get the updated soh after add
                        item_soh.soh = int(soh)
                        #update Total value
                        # total = get_qty * item_soh.price
                        # total_val = item_soh.total_value - total
                        # item_soh.total_price = soh * item_soh.price
                        # item_soh.total_value = total_val
                        #save tables
                        item_soh.save()

                        #Convert qty value to negative for get
                        qtyToNegative = (get_qty) * -1

                        #assign default value to remarks 
                        itemGetForm = form.save(commit=False)    
                        itemGetForm.remarks = "OUT"
                        itemGetForm.item_name = item_soh.item_name
                        itemGetForm.brand_name = item_soh.brand_name
                        # itemGetForm.price = item_soh.price
                        itemGetForm.quantity = qtyToNegative
                        itemGetForm.uom = item_soh.uom
                        itemGetForm.member = member_name
                        itemGetForm.department = department_name
                        itemGetForm.site = site_name
                        itemGetForm.ticket = ticket_name
    

                        # itemGetForm.item_value = total
                        itemGetForm.save()
                 
                else:
                    messages.error(request, "Invalid Input. Form is incomplete.")

            #assign length variables
            invalid_form = len(item_error_list)
            valid_form = len(item_success_list)

            # if values are valid send to submitted template
            if invalid_form == 0 and valid_form != 0:
                return redirect('submitted')

            # if 1 of the values are valid 
            elif invalid_form > 0 and valid_form > 0:
                messages.info(request, f"'{valid_form}' item(s) is/are submitted. Please re-input the item(s) with insufficient stock on hand.")
                return redirect('get_item')    
            # re input the items     
            else:
                return redirect('get_item')
            
        else:
            messages.error(request, "Invalid Input!")

    else:
        formset = ItemModelFormSet(queryset=Item.objects.none())


    context = {'formset': formset}
    return render(request, 'inventory/get_item.html', context)


@login_required
def export_excel_inventory(request):

    #Export excel function
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="DETAILED REPORT.xlsx"'

    thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))


    # Declare Workbook
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.merge_cells('A1:I1')

    first_cell = worksheet['A1']
    first_cell.value = "DETAILED REPORT"
    first_cell.font = Font(bold=True)
    first_cell.alignment = Alignment(horizontal="center", vertical="center")


    worksheet.title = "DETAILED REPORT"

    # Add headers
    headers =   [
                'SITE',
                'ITEM NAME',	
                'BRAND NAME',
                'QUANTITY',	
                'UOM',	
                'DATE',
                'REMARKS',	
                'STAFF NAME',
                ]
    row_num = 2


    for col_num, column_title in enumerate(headers, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
        cell.fill = PatternFill("solid", fgColor="CFE2FF")
        cell.font = Font(bold=True, color="0B5ED7")
        cell.border = thin_border


    # Add data from the model
    # items = Item.objects.all()
    # check if filtered items if not set default to all
    if filter_item_val():
        items = filter_item_val()
    else:
        items = Item.objects.all()

    for item in items:
        
        #convert object fields to string
        department = str(item.department)
        site = str(item.site)
        member = str(item.member)
        date_added = datetime.strftime(item.date_added,'%m/%d/%Y %H:%M:%S')

        worksheet.append(
            [
            department,
            site,
            item.item_name,
            item.brand_name,
            item.quantity,
            item.uom,
            date_added,
            item.remarks,
            item.user

        ])
    
    workbook.save(response)
    return response


@login_required
def export_excel_summary(request):

    #Export excel function
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="INVENTORY REPORT.xlsx"'

    thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))


    # Declare Workbook
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.merge_cells('A1:G1')

    first_cell = worksheet['A1']
    first_cell.value = "INVENTORY REPORT"
    first_cell.font = Font(bold=True)
    first_cell.alignment = Alignment(horizontal="center", vertical="center")


    worksheet.title = "INVENTORY REPORT"

    # Add headers
    headers =   [
                'DEPARTMENT',
                'SITE',
                'ITEM NAME',	
                'BRAND NAME',
                'UOM',	
                'SOH',
                # 'PRICE',	
                # 'TOTAL PRICE',
                # 'TOTAL BALANCE',
                'DATE'
                ]
    row_num = 2


    for col_num, column_title in enumerate(headers, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
        cell.fill = PatternFill("solid", fgColor="CFE2FF")
        cell.font = Font(bold=True, color="0B5ED7")
        cell.border = thin_border


    # Add data from the model
    # items = ItemBase.objects.all()
    # check if it was filtered if not set default to all
    if filter_itembase_val():
        items = filter_itembase_val()
        print("With filter value")
    else:
        items = ItemBase.objects.all()
        print("filter no value")

    for item in items:
        
        #convert object fields to string
        department = str(item.department)
        site = str(item.site)
        uom = str(item.uom)
        date_added = datetime.strftime(item.date_added,'%m/%d/%Y %H:%M:%S')

        worksheet.append([
            department,
            site,
            item.item_name,
            item.brand_name,
            uom,
            item.soh,
            date_added,
        ])
    
    workbook.save(response)
    return response




@login_required
def submitted(request):
    return render(request, 'inventory/submitted.html')



# #This is connected to itemcode ajax value
# def get_load_items(request, site_id):
#     items = list(ItemCode.objects.filter(site_id=site_id).values('id', 'code'))
#     return JsonResponse({'items': items})

def get_load_items(request, site_id, department_id):
    print(f"Filtering items for Site ID: {site_id}, Department ID: {department_id}")

    items = ItemCode.objects.filter(site_id=site_id, department_id=department_id).values('id', 'code')

    if not items:
        print("No items found!")  # Debugging output

    return JsonResponse({'items': list(items)})



