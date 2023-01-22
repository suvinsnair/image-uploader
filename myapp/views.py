from django.shortcuts import render
from .forms import UserRegsitrationForm
from .models import ImageUploader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from PIL import Image, UnidentifiedImageError
# Create your views here.


class HomeListView(generic.TemplateView):
    """ To see the complete images as a list"""
    model = ImageUploader
    template_name = 'home.html'

    def get_context_data(self, request, *args, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['images'] = ImageUploader.objects.filter(user=request.user,is_deleted=False)
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data(request))

    def post(self, request, *args, **kwargs):
        image_id = request.POST.get('image_id', None)
        if image_id:
            self.delete_image(int(image_id))
            messages.success(request,'Image has been deleted Successfully !!')
        else:
            img_name = request.POST.get('img_name', None)
            files = request.FILES.getlist('img')
            for img in files:
                try:
                    _ = Image.open(img)
                except (UnidentifiedImageError, AttributeError):
                    messages.error(request,'Please upload Valid Image Files !!')
                    return HttpResponseRedirect(reverse('home')) 
            description = request.POST.get('img_desc', None)
            if img_name and img:
                for img in files:
                    img_uploader = ImageUploader(image_name=img_name,
                                            image=img,
                                            description=description,
                                            user=request.user
                    )
                    img_uploader.save()
                messages.success(request,'Your Images Uploaded Successfully !!')
            else:
                messages.error(request,'Form Contains Errors !!')
        return HttpResponseRedirect(reverse('home'))
        
    def delete_image(self, image_id):
        ImageUploader.objects.filter(id=image_id).update(is_deleted=True)
        return

class SignUp(generic.TemplateView):
    form = UserRegsitrationForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        fm  = self.form()
        context = {'fm':fm}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        fm = self.form(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Signup Done !!')
        else:
            fm  = self.form()

        context = {'fm':fm}
        return render(request, self.template_name, context)
