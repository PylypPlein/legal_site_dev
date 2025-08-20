from django.shortcuts import render
from .models import Service
# Create your views here.
from django.shortcuts import render, redirect
from .forms import ContactRequestForm
from .models import Employee, Firma, SocialLink, PrivacyPolicySection, PrivacyPolicySubsection, JobOffer, BlacklistedCountry
from ipware import get_client_ip

def index(request):
    services = Service.objects.all()
    employees = Employee.objects.all()
    company = Firma.objects.first()
    links = SocialLink.objects.all()
    social_links = {link.name.lower(): link.url for link in links}

    return render(
        request,
        'main/index.html',
        {
            'services': services,
            'employees': employees,
            'company': company,
            'social_links': social_links,
            'isBlackListed': getattr(request, "is_blacklisted", False),
        }
    )

def privacy_policy(request):
    company = Firma.objects.first()
    sections = PrivacyPolicySection.objects.prefetch_related("subsections")
    return render(request, 'main/privacy_policy.html',{'company':company,"sections": sections})

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваше сообщение отправлено!")
            return redirect(reverse('index'))  # Можно изменить на страницу, куда хотите редиректить
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = ContactRequestForm()

    services = Service.objects.all()
    return render(request, 'index.html', {'form': form, 'services': services})
    '''
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})
    

def job_list(request):
    jobs = JobOffer.objects.filter(status='published')
    company = Firma.objects.first()
    return render(request, 'main/job_offers.html', {'jobs': jobs,'company':company})
    '''
def job_list(request):
    # Pobranie IP
    ip, is_routable = get_client_ip(request)
    if ip is None:
        ip = "Не удалось определить IP"

    # Pobranie kraju
    country = "Неизвестно"
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = response.get("country", "None")
    except Exception:
        pass

    # Sprawdzenie w bazie
    is_blacklisted = BlacklistedCountry.objects.filter(name__iexact=country).exists()

    if is_blacklisted:
        # Jeśli zablokowany – renderujemy index.html
        services = Service.objects.all()
        employees = Employee.objects.all()
        company = Firma.objects.first()
        links = SocialLink.objects.all()
        social_links = {link.name.lower(): link.url for link in links}

        return render(
            request,
            'main/index.html',
            {
                'services': services,
                'employees': employees,
                'company': company,
                'social_links': social_links,
                'isBlackListed': True
            }
        )

    # Jeśli nie zablokowany – normalny widok job_list
    jobs = JobOffer.objects.filter(status='published')
    company = Firma.objects.first()
    return render(request, 'main/job_offers.html', {'jobs': jobs, 'company': company})

# views.py
from django.shortcuts import render, redirect
from .forms import ContactRequestForm
from .models import Service
from django.urls import reverse
from django.contrib import messages


def contact_view(request):
    if request.method == "POST":
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваше сообщение отправлено!")
            return redirect(reverse('home'))  # Можно изменить на страницу, куда хотите редиректить
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = ContactRequestForm()

    services = Service.objects.all()
    return render(request, 'contact_modal.html', {'form': form, 'services': services})

