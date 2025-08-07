from django.shortcuts import render
from .models import Service
# Create your views here.
from django.shortcuts import render, redirect
from .forms import ContactForm

def index(request):
    services = Service.objects.all()
    return render(request, 'main/index.html',{'services': services})

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})
