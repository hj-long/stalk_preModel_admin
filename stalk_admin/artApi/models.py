# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class StrawData1(models.Model):
    material_ts = models.CharField(blank=True, null=True, max_length=20)
    material_vs = models.CharField(blank=True, null=True, max_length=20)
    carbon = models.CharField(blank=True, null=True, max_length=20)
    hydrogen = models.CharField(blank=True, null=True, max_length=20)
    nitrogen = models.CharField(blank=True, null=True, max_length=20)
    is_add = models.IntegerField(blank=True, null=True)
    is_pre = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    ch4 = models.CharField(blank=True, null=True, max_length=30)
    gas = models.CharField(blank=True, null=True, max_length=30)

    def __int__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'straw_data1'


class StrawData2(models.Model):
    material_ts = models.CharField(blank=True, null=True, max_length=20)
    material_vs = models.CharField(blank=True, null=True, max_length=20)
    is_add = models.IntegerField(blank=True, null=True)
    is_pre = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    ch4 = models.CharField(blank=True, null=True, max_length=30)
    gas = models.CharField(blank=True, null=True, max_length=30)

    def __int__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'straw_data2'


class StrawData3(models.Model):
    material_ts = models.CharField(blank=True, null=True, max_length=20)
    material_vs = models.CharField(blank=True, null=True, max_length=20)
    carbon = models.CharField(blank=True, null=True, max_length=20)
    hydrogen = models.CharField(blank=True, null=True, max_length=20)
    oxygen = models.CharField(blank=True, null=True, max_length=20)
    nitrogen = models.CharField(blank=True, null=True, max_length=20)
    is_add = models.IntegerField(blank=True, null=True)
    is_pre = models.IntegerField(blank=True, null=True)
    days = models.IntegerField(blank=True, null=True)
    ch4 = models.CharField(blank=True, null=True, max_length=30)
    gas = models.CharField(blank=True, null=True, max_length=30)

    def __int__(self):
        return self.id

    class Meta:
        managed = False
        db_table = 'straw_data3'