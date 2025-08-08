from django.shortcuts import render
from .models import Service
# Create your views here.
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Employee, Firma, SocialLink, PrivacyPolicySection, PrivacyPolicySubsection

def index(request):
    services = Service.objects.all()
    employees = Employee.objects.all()
    company = Firma.objects.first()
    links = SocialLink.objects.all()
    social_links = {link.name.lower(): link.url for link in links}
    return render(request, 'main/index.html',{'services': services,'employees':employees,'company':company,'social_links':social_links})

def privacy_policy(request):
    company = Firma.objects.first()
    sections = PrivacyPolicySection.objects.prefetch_related("subsections")
    return render(request, 'main/privacy_policy.html',{'company':company,"sections": sections})

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
