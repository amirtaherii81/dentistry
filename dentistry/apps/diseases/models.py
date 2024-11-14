from django.db import models
from django.utils import timezone
from jalali_date import datetime2jalali, date2jalali
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Disease(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان بیماری')
    
    summary_description = models.TextField(max_length=100, default="", null=True, blank=True, verbose_name='خلاصه شرح')
    description = RichTextUploadingField(config_name='special',blank=True, null=True, verbose_name='توضیحات کامل')
    
    is_priority = models.BooleanField(default=False, verbose_name='اولویت بودن / نبودن')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن / نبودن')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    slug = models.SlugField(null=False)
    
    def get_shamsi_date(self):
        return datetime2jalali(self.publication_date).strftime('%H:%M:%S _ %y/%m/%d')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = 'بیماری'
        verbose_name_plural = 'بیماری ها'
        

    