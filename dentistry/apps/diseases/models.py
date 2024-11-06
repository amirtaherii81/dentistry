from django.db import models
# Create your models here.

class Disease(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان بیماری')
    description = models.TextField(verbose_name='شرح بیماری')
    is_priority = models.BooleanField(default=False, verbose_name='اولویت بودن / نبودن')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن / نبودن')
    publication_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ انتشار') 

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'بیماری'
        verbose_name_plural = 'بیماری ها'