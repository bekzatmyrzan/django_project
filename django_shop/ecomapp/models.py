from django.db import models

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 150)
    slug = models.SlugField(blank=True)

    def get_absolute_url(self):
        return reverse('category_detail',kwargs={'category_slug':self.slug})

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length = 150)

    def __str__(self):
        return self.name

class ProductManager(models.Manager):# сами написали "Manager" для "Products"

    def all(self, *args, **kwargs):
        return super(ProductManager,self).get_queryset().filter(available=True)

def pre_save_category_slug(sender,instance,*args,**kwargs):
    if not instance.slug:
        slug = slugify(instance.name)
        instance.name = slug

pre_save.connect(pre_save_category_slug,sender=Category)



def image_folder(instance, filename):
    filename = instance.slug + '.' +filename.split('.')[1]
    return "{0}/{1}".format(instance.slug,filename)

class Product(models.Model):
    category = models.ForeignKey('Category',on_delete = models.PROTECT)
    brand = models.ForeignKey('Brand',on_delete = models.PROTECT)
    title = models.CharField(max_length = 150)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to=image_folder)
    price = models.DecimalField(max_digits = 9,decimal_places =2)
    available = models.BooleanField(default=True)
    objects = ProductManager() #переопределили какую-то функция и видны только те продукты которые "available"

    def get_absolute_url(self):
        return reverse('product_detail',kwargs={'product_slug':self.slug})

    def __str__(self):
        return self.title
