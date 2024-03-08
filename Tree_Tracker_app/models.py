from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    
    class Meta():
        abstract=True

class Survey(BaseModel):
    Latitude=models.FloatField()
    Longitude=models.FloatField()
    species=models.CharField(max_length=100)
    tree_height=models.FloatField()
    steam_diameter=models.FloatField()
    crown_height=models.FloatField()
    crown_diameter=models.FloatField()
    spreading=models.CharField(max_length=50)
    crown_damage=models.CharField(max_length=50)
    reason_crown_damage=models.CharField(max_length=1000)
    trunk_damage=models.CharField(max_length=50)
    reason_trunk_damage=models.CharField(max_length=1000)    