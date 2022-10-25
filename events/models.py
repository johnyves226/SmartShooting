import os

from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.core.files import File
import qrcode
from io import BytesIO
from PIL import Image as im,ImageDraw
from django.utils import timezone

from user.models import User

def user_directory_path(instance,filename):
    base_name = os.path.basename(filename)
    name,ext = os.path.splitext(base_name)
    return "event/user/"+ str(instance.event.user.id) + "/"+ str(instance.event.id)+ "/"+"IMG_" + str(instance.event.id)+ext


class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(null=False,unique=True)
    class Meta:
        ordering= ['name']

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Event(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    name = models.CharField(max_length=200, null=False);
    description = models.TextField()
    qrcode = models.ImageField(upload_to='images/codes', blank=True);
    created_date = models.DateField(default=timezone.now())
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(null=True,unique_for_date='published')
    tags = models.ManyToManyField(Tag)
    link=models.CharField(max_length=300, null=True);

    class Meta:
        ordering = ['-last_modified']

    def getEventTags(self):
        return self.tags.all()

    def __str__(self):
        return self.name


    # def save(self,*args,**kwargs):
    #     qrcode_img = qrcode.make(self.name)
    #     canvas= im.new('RGB',(290,290),'white')
    #     draw = ImageDraw.Draw(canvas)
    #     canvas.paste(qrcode_img)
    #     fname=f'qr_code-{self.name}'+'.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer,'PNG')
    #     self.qrcode.save(fname,File(buffer),save=False)
    #     canvas.close()
    #     super().save(*args,**kwargs)

def get_image_filename(names,instance=None):
    if instance:
        name = instance.user.name
        slug = slugify(name)
        return "images/event/%s-%s" % (slug,names)
    else:
        return "images/event/%s" % (names)


class Image(models.Model):
    price = models.IntegerField(max_length=4,null=True,blank=True);
    images=models.ImageField(upload_to="images/event",null=True,blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.event.name + " Img"

def get_unique_slug(sender, instance, **kwargs):
    num = 1
    slug = slugify(instance.name)
    unique_slug = slug
    while Event.objects.filter(slug=unique_slug).exists():
        unique_slug = '{}-{}'.format(slug, num)
        num += 1
    instance.slug=unique_slug


pre_save.connect(get_unique_slug,sender=Event)