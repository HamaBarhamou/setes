import json

from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from .admin import (
    ContactMessageAdmin,
    NewsletterSubscriberAdmin,
    ServiceAdmin,
    TeamMemberAdmin,
    TestimonialAdmin,
)
from .context_processors import newsletter_form
from .forms import ContactForm, NewsletterForm
from .models import (
    ContactMessage,
    NewsletterSubscriber,
    Service,
    TeamMember,
    Testimonial,
)
from .sitemaps import ServiceSitemap, StaticViewSitemap


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_service(**kwargs):
    defaults = {
        "title": "Test Service",
        "slug": "test-service",
        "description": "Description",
        "details": "Details",
        "icon": "bi-star",
        "legacy_image": "assets/img/services/test.webp",
        "order": 1,
    }
    defaults.update(kwargs)
    return Service.objects.create(**defaults)


def _make_testimonial(**kwargs):
    defaults = {
        "company_name": "TestCorp",
        "person_title": "CEO",
        "content": "Great work!",
        "rating": 5,
        "order": 1,
    }
    defaults.update(kwargs)
    return Testimonial.objects.create(**defaults)


def _make_team_member(**kwargs):
    defaults = {
        "name": "John Doe",
        "role": "Developer",
        "legacy_photo": "assets/img/team/team-1.jpg",
        "order": 1,
    }
    defaults.update(kwargs)
    return TeamMember.objects.create(**defaults)


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------
class ServiceModelTest(TestCase):
    def setUp(self):
        Service.objects.all().delete()

    def test_str(self):
        service = _make_service()
        self.assertEqual(str(service), "Test Service")

    def test_ordering(self):
        s2 = _make_service(slug="b-service", order=2, title="B")
        s1 = _make_service(slug="a-service", order=1, title="A")
        qs = Service.objects.all()
        self.assertEqual(list(qs), [s1, s2])

    def test_is_active_default(self):
        service = _make_service()
        self.assertTrue(service.is_active)

    def test_verbose_names(self):
        self.assertEqual(Service._meta.verbose_name, "Service")
        self.assertEqual(Service._meta.verbose_name_plural, "Services")


class TestimonialModelTest(TestCase):
    def setUp(self):
        Testimonial.objects.all().delete()

    def test_str(self):
        t = _make_testimonial()
        self.assertEqual(str(t), "TestCorp")

    def test_ordering(self):
        t2 = _make_testimonial(company_name="B", order=2)
        t1 = _make_testimonial(company_name="A", order=1)
        self.assertEqual(list(Testimonial.objects.all()), [t1, t2])

    def test_verbose_names(self):
        self.assertEqual(Testimonial._meta.verbose_name, "Temoignage")
        self.assertEqual(Testimonial._meta.verbose_name_plural, "Temoignages")


class TeamMemberModelTest(TestCase):
    def setUp(self):
        TeamMember.objects.all().delete()

    def test_str(self):
        m = _make_team_member()
        self.assertEqual(str(m), "John Doe")

    def test_ordering(self):
        m2 = _make_team_member(name="B", order=2)
        m1 = _make_team_member(name="A", order=1)
        self.assertEqual(list(TeamMember.objects.all()), [m1, m2])

    def test_blank_photo(self):
        m = _make_team_member(photo="")
        self.assertEqual(m.photo, "")

    def test_blank_linkedin(self):
        m = _make_team_member(linkedin_url="")
        self.assertEqual(m.linkedin_url, "")

    def test_verbose_names(self):
        self.assertEqual(TeamMember._meta.verbose_name, "Membre de l'equipe")
        self.assertEqual(TeamMember._meta.verbose_name_plural, "Membres de l'equipe")


class ContactMessageModelTest(TestCase):
    def test_str(self):
        msg = ContactMessage.objects.create(
            name="Ali", email="ali@test.com", subject="Hello", message="Bonjour"
        )
        self.assertEqual(str(msg), "Ali - Hello")

    def test_ordering(self):
        m1 = ContactMessage.objects.create(
            name="A", email="a@t.com", subject="S1", message="M1"
        )
        m2 = ContactMessage.objects.create(
            name="B", email="b@t.com", subject="S2", message="M2"
        )
        # newest first
        self.assertEqual(list(ContactMessage.objects.all()), [m2, m1])

    def test_is_read_default(self):
        msg = ContactMessage.objects.create(
            name="A", email="a@t.com", subject="S", message="M"
        )
        self.assertFalse(msg.is_read)

    def test_verbose_names(self):
        self.assertEqual(ContactMessage._meta.verbose_name, "Message de contact")
        self.assertEqual(
            ContactMessage._meta.verbose_name_plural, "Messages de contact"
        )


class NewsletterSubscriberModelTest(TestCase):
    def test_str(self):
        sub = NewsletterSubscriber.objects.create(email="test@test.com")
        self.assertEqual(str(sub), "test@test.com")

    def test_unique_email(self):
        NewsletterSubscriber.objects.create(email="dup@test.com")
        with self.assertRaises(Exception):
            NewsletterSubscriber.objects.create(email="dup@test.com")

    def test_is_active_default(self):
        sub = NewsletterSubscriber.objects.create(email="a@t.com")
        self.assertTrue(sub.is_active)

    def test_verbose_names(self):
        self.assertEqual(NewsletterSubscriber._meta.verbose_name, "Abonne newsletter")
        self.assertEqual(
            NewsletterSubscriber._meta.verbose_name_plural, "Abonnes newsletter"
        )


# ---------------------------------------------------------------------------
# Form tests
# ---------------------------------------------------------------------------
class ContactFormTest(TestCase):
    def test_valid(self):
        form = ContactForm(
            data={
                "name": "Ali",
                "email": "ali@test.com",
                "subject": "Test",
                "message": "Bonjour",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = ContactForm(
            data={
                "name": "Ali",
                "email": "not-an-email",
                "subject": "Test",
                "message": "Bonjour",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_missing_name(self):
        form = ContactForm(
            data={
                "name": "",
                "email": "ali@test.com",
                "subject": "Test",
                "message": "Bonjour",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_missing_subject(self):
        form = ContactForm(
            data={
                "name": "Ali",
                "email": "ali@test.com",
                "subject": "",
                "message": "Bonjour",
            }
        )
        self.assertFalse(form.is_valid())

    def test_missing_message(self):
        form = ContactForm(
            data={
                "name": "Ali",
                "email": "ali@test.com",
                "subject": "Test",
                "message": "",
            }
        )
        self.assertFalse(form.is_valid())

    def test_widgets(self):
        form = ContactForm()
        self.assertIn("form-control", form.fields["name"].widget.attrs["class"])
        self.assertIn("form-control", form.fields["email"].widget.attrs["class"])
        self.assertEqual(form.fields["message"].widget.attrs["rows"], 6)

    def test_save(self):
        form = ContactForm(
            data={
                "name": "Ali",
                "email": "ali@test.com",
                "subject": "Test",
                "message": "Bonjour",
            }
        )
        form.save()
        self.assertEqual(ContactMessage.objects.count(), 1)


class NewsletterFormTest(TestCase):
    def test_valid(self):
        form = NewsletterForm(data={"email": "test@test.com"})
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = NewsletterForm(data={"email": "bad"})
        self.assertFalse(form.is_valid())

    def test_empty_email(self):
        form = NewsletterForm(data={"email": ""})
        self.assertFalse(form.is_valid())

    def test_duplicate_email(self):
        NewsletterSubscriber.objects.create(email="dup@test.com")
        form = NewsletterForm(data={"email": "dup@test.com"})
        self.assertFalse(form.is_valid())

    def test_widget(self):
        form = NewsletterForm()
        self.assertEqual(
            form.fields["email"].widget.attrs["placeholder"], "Votre email"
        )

    def test_save(self):
        form = NewsletterForm(data={"email": "new@test.com"})
        form.save()
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)


# ---------------------------------------------------------------------------
# View tests
# ---------------------------------------------------------------------------
class RobotsTxtViewTest(TestCase):
    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertIn("User-agent", response.content.decode())
        self.assertIn("Sitemap", response.content.decode())


class HomeViewTest(TestCase):
    def setUp(self):
        self.service = _make_service()
        self.testimonial = _make_testimonial()
        self.member = _make_team_member()

    def test_status_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_context_services(self):
        response = self.client.get(reverse("home"))
        self.assertIn(self.service, response.context["services"])

    def test_context_testimonials(self):
        response = self.client.get(reverse("home"))
        self.assertIn(self.testimonial, response.context["testimonials"])

    def test_context_team_members(self):
        response = self.client.get(reverse("home"))
        self.assertIn(self.member, response.context["team_members"])

    def test_context_contact_form(self):
        response = self.client.get(reverse("home"))
        self.assertIsInstance(response.context["contact_form"], ContactForm)

    def test_inactive_service_excluded(self):
        inactive = _make_service(slug="inactive", is_active=False)
        response = self.client.get(reverse("home"))
        self.assertNotIn(inactive, response.context["services"])

    def test_inactive_testimonial_excluded(self):
        inactive = _make_testimonial(company_name="Gone", is_active=False)
        response = self.client.get(reverse("home"))
        self.assertNotIn(inactive, response.context["testimonials"])

    def test_inactive_team_member_excluded(self):
        inactive = _make_team_member(name="Gone", is_active=False)
        response = self.client.get(reverse("home"))
        self.assertNotIn(inactive, response.context["team_members"])

    def test_template_used(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "index.html")


class PortfolioDetailsViewTest(TestCase):
    def test_status_200(self):
        response = self.client.get(reverse("portfolio-details"))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse("portfolio-details"))
        self.assertTemplateUsed(response, "portfolio-details.html")


class ServiceDetailsViewTest(TestCase):
    def setUp(self):
        Service.objects.all().delete()
        self.service = _make_service()
        _make_service(slug="other-service", title="Other", order=2)

    def test_status_200(self):
        response = self.client.get(reverse("service-details", args=["test-service"]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse("service-details", args=["test-service"]))
        self.assertTemplateUsed(response, "service-details.html")

    def test_context_service(self):
        response = self.client.get(reverse("service-details", args=["test-service"]))
        self.assertEqual(response.context["service"], self.service)

    def test_context_services_list(self):
        response = self.client.get(reverse("service-details", args=["test-service"]))
        self.assertEqual(response.context["services"].count(), 2)

    def test_404_unknown_slug(self):
        response = self.client.get(reverse("service-details", args=["nonexistent"]))
        self.assertEqual(response.status_code, 404)

    def test_404_inactive_service(self):
        _make_service(slug="hidden", is_active=False)
        response = self.client.get(reverse("service-details", args=["hidden"]))
        self.assertEqual(response.status_code, 404)


class ContactSubmitViewTest(TestCase):
    def test_post_valid(self):
        data = {
            "name": "Ali",
            "email": "ali@test.com",
            "subject": "Test",
            "message": "Bonjour",
        }
        response = self.client.post(reverse("contact-submit"), data)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertTrue(body["success"])
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_post_invalid(self):
        response = self.client.post(
            reverse("contact-submit"),
            {"name": "", "email": "bad", "subject": "", "message": ""},
        )
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertFalse(body["success"])
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_get_not_allowed(self):
        response = self.client.get(reverse("contact-submit"))
        self.assertEqual(response.status_code, 405)


class NewsletterSubscribeViewTest(TestCase):
    def test_post_valid(self):
        response = self.client.post(
            reverse("newsletter-subscribe"), {"email": "new@test.com"}
        )
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertTrue(body["success"])
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)

    def test_post_duplicate(self):
        NewsletterSubscriber.objects.create(email="dup@test.com")
        response = self.client.post(
            reverse("newsletter-subscribe"), {"email": "dup@test.com"}
        )
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertFalse(body["success"])

    def test_post_invalid_email(self):
        response = self.client.post(
            reverse("newsletter-subscribe"), {"email": "invalid"}
        )
        self.assertEqual(response.status_code, 400)

    def test_get_not_allowed(self):
        response = self.client.get(reverse("newsletter-subscribe"))
        self.assertEqual(response.status_code, 405)


# ---------------------------------------------------------------------------
# Context processor tests
# ---------------------------------------------------------------------------
class NewsletterContextProcessorTest(TestCase):
    def test_returns_newsletter_form(self):
        request = HttpRequest()
        ctx = newsletter_form(request)
        self.assertIn("newsletter_form", ctx)
        self.assertIsInstance(ctx["newsletter_form"], NewsletterForm)


# ---------------------------------------------------------------------------
# Sitemap tests
# ---------------------------------------------------------------------------
class StaticViewSitemapTest(TestCase):
    def test_items(self):
        sitemap = StaticViewSitemap()
        self.assertEqual(sitemap.items(), ["home"])

    def test_location(self):
        sitemap = StaticViewSitemap()
        self.assertEqual(sitemap.location("home"), "/")

    def test_changefreq(self):
        self.assertEqual(StaticViewSitemap.changefreq, "monthly")

    def test_priority(self):
        self.assertEqual(StaticViewSitemap.priority, 1.0)


class ServiceSitemapTest(TestCase):
    def setUp(self):
        Service.objects.all().delete()
        self.service = _make_service()
        _make_service(slug="inactive", is_active=False)

    def test_items_only_active(self):
        sitemap = ServiceSitemap()
        items = list(sitemap.items())
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0], self.service)

    def test_location(self):
        sitemap = ServiceSitemap()
        self.assertEqual(
            sitemap.location(self.service), "/service-details/test-service/"
        )

    def test_changefreq(self):
        self.assertEqual(ServiceSitemap.changefreq, "monthly")

    def test_priority(self):
        self.assertEqual(ServiceSitemap.priority, 0.8)


class SitemapXMLViewTest(TestCase):
    def setUp(self):
        _make_service()

    def test_sitemap_xml(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("xml", response["Content-Type"])


# ---------------------------------------------------------------------------
# Admin tests
# ---------------------------------------------------------------------------
class AdminConfigTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_service_admin(self):
        ma = ServiceAdmin(Service, self.site)
        self.assertEqual(
            ma.list_display, ["title", "slug", "order", "is_active", "apercu_image"]
        )
        self.assertEqual(ma.list_editable, ["order", "is_active"])
        self.assertEqual(ma.prepopulated_fields, {"slug": ("title",)})
        self.assertEqual(ma.search_fields, ["title", "description"])

    def test_testimonial_admin(self):
        ma = TestimonialAdmin(Testimonial, self.site)
        self.assertEqual(
            ma.list_display,
            ["company_name", "person_title", "rating", "order", "is_active"],
        )
        self.assertEqual(ma.list_editable, ["order", "is_active"])

    def test_team_member_admin(self):
        ma = TeamMemberAdmin(TeamMember, self.site)
        self.assertEqual(
            ma.list_display, ["name", "role", "order", "is_active", "apercu_photo"]
        )
        self.assertEqual(ma.list_editable, ["order", "is_active"])

    def test_contact_message_admin(self):
        ma = ContactMessageAdmin(ContactMessage, self.site)
        self.assertEqual(
            ma.list_display, ["name", "email", "subject", "created_at", "is_read"]
        )
        self.assertEqual(ma.list_filter, ["is_read", "created_at"])
        self.assertIn("name", ma.readonly_fields)
        self.assertIn("message", ma.readonly_fields)

    def test_newsletter_subscriber_admin(self):
        ma = NewsletterSubscriberAdmin(NewsletterSubscriber, self.site)
        self.assertEqual(ma.list_display, ["email", "subscribed_at", "is_active"])
        self.assertEqual(ma.list_filter, ["is_active"])


# ---------------------------------------------------------------------------
# Error page tests
# ---------------------------------------------------------------------------
class ErrorPageTest(TestCase):
    def test_404_page(self):
        response = self.client.get("/nonexistent-page-xyz/")
        self.assertEqual(response.status_code, 404)

    def test_service_404_page(self):
        response = self.client.get("/service-details/nonexistent/")
        self.assertEqual(response.status_code, 404)


# ---------------------------------------------------------------------------
# URL routing tests
# ---------------------------------------------------------------------------
class URLRoutingTest(TestCase):
    def test_home_url(self):
        self.assertEqual(reverse("home"), "/")

    def test_portfolio_url(self):
        self.assertEqual(reverse("portfolio-details"), "/portfolio-details/")

    def test_service_details_url(self):
        self.assertEqual(
            reverse("service-details", args=["test"]), "/service-details/test/"
        )

    def test_contact_url(self):
        self.assertEqual(reverse("contact-submit"), "/contact/")

    def test_newsletter_url(self):
        self.assertEqual(reverse("newsletter-subscribe"), "/newsletter/")

    def test_robots_url(self):
        self.assertEqual(reverse("robots-txt"), "/robots.txt")
