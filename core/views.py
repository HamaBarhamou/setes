from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .forms import ContactForm, NewsletterForm
from .models import Service, TeamMember, Testimonial


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: https://setes.net/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def home(request):
    services = Service.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    team_members = TeamMember.objects.filter(is_active=True)
    context = {
        "services": services,
        "testimonials": testimonials,
        "team_members": team_members,
        "contact_form": ContactForm(),
    }
    return render(request, "index.html", context)


def portfolio_details(request):
    return render(request, "portfolio-details.html")


def service_details(request, service_slug):
    service = get_object_or_404(Service, slug=service_slug, is_active=True)
    services = Service.objects.filter(is_active=True)
    return render(
        request,
        "service-details.html",
        {
            "service": service,
            "services": services,
        },
    )


@require_POST
def contact_submit(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse(
            {"success": True, "message": "Votre message a bien été envoyé. Merci !"}
        )
    return JsonResponse(
        {"success": False, "message": "Veuillez corriger les erreurs."},
        status=400,
    )


@require_POST
def newsletter_subscribe(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse(
            {
                "success": True,
                "message": "Votre abonnement a été enregistré. Merci !",
            }
        )
    return JsonResponse(
        {"success": False, "message": "Cet email est déjà abonné ou invalide."},
        status=400,
    )
