from django.db import models


class Client(models.Model):
    client = models.CharField(max_length=200)

    def __str__(self):
        return self.client

    class Meta:
        ordering = ["client"]
    
    #Save data to upper case
    def save(self, *args, **kwargs):
        self.client = self.client.upper()
        super(Client, self).save()


class Department(models.Model):
    department = models.CharField(max_length=200)

    def __str__(self):
        return self.department

    class Meta:
        ordering = ["department"]

    #Save data to upper case
    def save(self, *args, **kwargs):
        self.department = self.department.upper()
        super(Department, self).save(*args, **kwargs)

class UOM(models.Model):
    uom = models.CharField(max_length=30)
    
    def __str__(self):
        return self.uom
    
    class Meta:
        ordering = ["uom"]

    #Save data to upper case
    def save(self, *args, **kwargs):
        self.uom= self.uom.upper()
        super(UOM, self).save(*args, **kwargs)



class Site(models.Model):
    site = models.CharField(max_length=200)

    def __str__(self):
        return self.site

    class Meta:
        ordering = ["site"]
    
    #Save data to upper case
    def save(self, *args, **kwargs):
        self.site = self.site.upper()
        super(Site, self).save(*args, **kwargs)


# class Floor(models.Model):
#     floor = models.CharField(max_length=200)
#     site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return self.floor

#     class Meta:
#         ordering = ["floor"]
    
#     #Save data to upper case
#     def save(self):
#         self.floor = self.floor.upper()
#         super(Floor, self).save()



class ItemCode(models.Model):
    code = models.CharField(max_length=200, null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True) 

    class Meta:
        ordering = ["code"]
    
    #Save data to upper case
    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super(ItemCode, self).save(*args, **kwargs)

    def __str__(self): 
        return self.code


class ItemBase(models.Model):
    item_name = models.CharField(max_length=200, null=True, blank=True)
    brand_name = models.CharField(max_length=200, null=True, blank=True)
    soh = models.IntegerField(null=True, blank=True)
    item_code = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=50, null=True, blank=True)
    uom = models.ForeignKey(UOM, on_delete=models.CASCADE, null=True, blank=True)
    critical_value = models.IntegerField(null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True) 
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True) 
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True) 

    class Meta:
        ordering = ["item_name"]

    def __str__(self):
        return self.item_code
    
    #save input to uppercase
    def save(self, *args, **kwargs):
        self.item_name = self.item_name.upper()
        self.brand_name = self.brand_name.upper()
        self.item_code = self.item_code.upper()
        super(ItemBase, self).save(*args, **kwargs)
        
    # #computation of total price per item
    # @property
    # def totalPrice(self):
    #     return self.soh * self.price
    

class TeamMember(models.Model):
    member = models.CharField(max_length=200)

    class Meta:
        ordering = ["member"]
        verbose_name_plural = "Staff Name"

    def __str__(self):
        return self.member

    #save input to uppercase
    def save(self, *args, **kwargs):
        self.member = self.member.upper()
        super(TeamMember, self).save(*args, **kwargs)


class Item(models.Model):
    item_code = models.ForeignKey(ItemCode, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True, blank=True) 
    remarks = models.CharField(max_length=50, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True)
    uom = models.CharField(max_length=20, null=True, blank=True)
    item_name = models.CharField(max_length=200, blank=True, null=True)
    brand_name = models.CharField(max_length=200, blank=True, null=True)
    staff_name = models.CharField(max_length=100, null=True, blank=True)
    client_name = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    member = models.ForeignKey(TeamMember, on_delete=models.CASCADE, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True) 
    # purpose = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return str(self.item_name)
    
    def save(self, *args, **kwargs):
        self.item_name = self.item_name.upper()
        self.brand_name = self.brand_name.upper()
        super(Item, self).save(*args, **kwargs)

    # #computation of total price per item
    # @property
    # def totalAmt(self):
    #     return self.quantity * self.price
    
    # @property
    # def fullname(self):
    #     return f"{self.lastName}, {self.firstName} {self.middleName}"
    



    
    



      


    
    

    
    
        
