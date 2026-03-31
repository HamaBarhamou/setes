from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ContactMessage,
    NewsletterSubscriber,
    Service,
    TeamMember,
    Testimonial,
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "order", "is_active", "apercu_image"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title", "description"]
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "description",
                    "details",
                    "icon",
                    "order",
                    "is_active",
                )
            },
        ),
        (
            "Image",
            {
                "fields": ("image", "legacy_image"),
                "description": "Uploadez une image via Cloudinary. Le champ 'legacy' est pour les anciennes images statiques.",
            },
        ),
    ]

    def apercu_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:4px;">', obj.image.url
            )
        return "-"

    apercu_image.short_description = "Apercu"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["company_name", "person_title", "rating", "order", "is_active"]
    list_editable = ["order", "is_active"]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["name", "role", "order", "is_active", "apercu_photo"]
    list_editable = ["order", "is_active"]
    fieldsets = [
        (None, {"fields": ("name", "role", "order", "is_active", "linkedin_url")}),
        (
            "Photo",
            {
                "fields": ("photo", "legacy_photo"),
                "description": "Uploadez une photo via Cloudinary. Le champ 'legacy' est pour les anciennes photos statiques.",
            },
        ),
    ]

    def apercu_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:40px;border-radius:50%;">', obj.photo.url
            )
        return "-"

    apercu_photo.short_description = "Apercu"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "created_at", "is_read"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["name", "email", "subject", "message", "created_at"]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "subscribed_at", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["email"]
