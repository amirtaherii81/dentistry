from django.db import models
from khayyam import JalaliDatetime
from django.utils import timezone
# Create your models here.

class Disease(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان بیماری')
    description = models.TextField(verbose_name='شرح بیماری')
    is_priority = models.BooleanField(default=False, verbose_name='اولویت بودن / نبودن')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن / نبودن')
    publication_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار') 
    # slug = models.SlugField()

    def get_shamsi_date(self):
        jalali_datetime = JalaliDatetime(self.publication_date)
        return str(jalali_datetime.todate())
        
        
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'بیماری'
        verbose_name_plural = 'بیماری ها'
        