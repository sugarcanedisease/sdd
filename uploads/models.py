from django.db import models


class upload(models.Model):
    image = models.ImageField(upload_to='images')
    InfectedRegion = models.ImageField(upload_to='spot_on_org_images')
    
    def __str__(self):
        return str(self.id)

class User(models.Model):
    name =  models.CharField(max_length=200, null=True)
    email = models.CharField (max_length= 200, null=True)



        
         
    