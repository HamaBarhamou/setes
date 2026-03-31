from django.db import migrations


def copy_to_legacy(apps, schema_editor):
    """Copie les chemins static existants vers les champs legacy."""
    Service = apps.get_model("core", "Service")
    for service in Service.objects.all():
        if not service.legacy_image and not service.image:
            pass
        elif not service.legacy_image:
            service.legacy_image = service.image.name if service.image else ""
            service.image = ""
            service.save()

    TeamMember = apps.get_model("core", "TeamMember")
    for member in TeamMember.objects.all():
        if not member.legacy_photo and not member.photo:
            pass
        elif not member.legacy_photo:
            member.legacy_photo = member.photo.name if member.photo else ""
            member.photo = ""
            member.save()


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_service_legacy_image_teammember_legacy_photo_and_more"),
    ]

    operations = [
        migrations.RunPython(copy_to_legacy, migrations.RunPython.noop),
    ]
