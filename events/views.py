import qrcode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.template import loader
from django.contrib import messages
from django.db.models import Q
from events.form import EventCreateForm, ImageForm
from events.models import Event, Image
from user.models import Photographer
from io import BytesIO
from PIL import Image as im,ImageDraw
from django.core.files import File


@login_required
def CreateEvent(request):
     context = {}
     template = loader.get_template('../templates/create_event.html')
     if request.method == "POST":
          form = EventCreateForm(request.POST, request.FILES)
          if form.is_valid():
               event=form.save()
               event.link="https://smartshooting.herokuapp.com/event/"+str(event.id)+"/images/"
               qrcode_img = qrcode.make(event.link)
               canvas = im.new('RGB', (400,400), 'white')
               draw = ImageDraw.Draw(canvas)
               canvas.paste(qrcode_img)
               fname = f'qr_code-{event.name}' + '.png'
               buffer = BytesIO()
               canvas.save(buffer, 'PNG')
               event.qrcode.save(fname, File(buffer), save=False)
               canvas.close()
               event.save()
               messages.success(request, ('Your event was successfully create!'))
               return redirect('event_detail',pk=event.pk)
          else:
               messages.error(request, 'Error saving form')

          return redirect("/")
     else:
          form=EventCreateForm(initial={'author': request.user})
          events = Event.objects.all()
          context['form'] = form
          context['evensts'] = events
          return HttpResponse(template.render(context, request))



def index():
     pass



class SearchPhotographer(ListView):
    model = Photographer
    template_name = "../templates/result.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Photographer.objects.filter(
            Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(user__user_name__icontains=query)
            | Q(user__email__icontains=query)
        ).distinct()
        return queryset

def showImage(request,pke, pk):
    if request.user.is_authenticated:
        template = loader.get_template('../templates/showImage.html')
        event = Event.objects.get(pk=pke)
        image=Image.objects.get(pk=pk)
        context = {'event': event,'image':image}
        return HttpResponse(template.render(context, request))
    else:
        return render(request, '../templates/login.html', context={'form': AuthenticationForm()})


def EventEdit(request, pk):
    if request.user.is_authenticated:
        pass

    else:
        return render(request, '../templates/login.html',context={'form':AuthenticationForm()})




def GetEvent(request,pk):
    if request.user.is_authenticated:
        template = loader.get_template('../templates/event_details.html')
        event = Event.objects.get(pk=pk)
        context = {'event':event}
        return HttpResponse(template.render(context, request))
    else:
        return render(request, '../templates/login.html',context={'form':AuthenticationForm()})


def GetEventImage(request,pk):
    if request.user.is_authenticated:
        template = loader.get_template('../templates/events_images_view.html')
        event = Event.objects.get(pk=pk)
        images=Image.objects.filter(event=event)
        context = {'event':event,'images':images}
        return HttpResponse(template.render(context, request))
    else:
        return render(request, '../templates/login.html',context={'form':AuthenticationForm()})


def GetAllEvent(request):
    if request.user.is_authenticated:
        template = loader.get_template('../templates/events_view.html')
        events = Event.objects.filter(author=request.user)
        context = {'event':events}
        return HttpResponse(template.render(context, request))
    else:
        return render(request, '../templates/login.html',context={'form':AuthenticationForm()})



@login_required
def addImages(request,pk):
    template = loader.get_template('../templates/events_images_view.html')
    if request.method == 'POST':
        form = ImageForm(request.POST or None, request.FILES or None)
        images = request.FILES.getlist('images')
        event = Event.objects.get(pk=pk)
        for image in images:
            print("for file valid ")
            Image.objects.create(images=image,event=event)
            print("create image ok ")
        images = Image.objects.filter(event=event)
        context = {'event':event,'images': images}
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse('/')


@login_required()
class SearchEvent(ListView):
    """Class to render search results"""
    model = Event
    template_name = "../templates/event_details.html"

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Event.objects.filter(
            Q(name__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()
        return queryset
