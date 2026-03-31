from django.urls import path
from . import views

urlpatterns = [
    path("robots.txt", views.robots_txt, name="robots-txt"),
    path("", views.home, name="home"),
    path("portfolio-details/", views.portfolio_details, name="portfolio-details"),
    path(
        "service-details/<str:service_slug>/",
        views.service_details,
        name="service-details",
    ),
    path("contact/", views.contact_submit, name="contact-submit"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter-subscribe"),
]
