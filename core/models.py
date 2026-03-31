from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    details = models.TextField()
    icon = models.CharField(max_length=50)
    image = models.ImageField(upload_to="services/", blank=True)
    legacy_image = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def display_image(self):
        """Retourne l'URL de l'image Cloudinary ou le chemin static legacy."""
        if self.image:
            return self.image.url
        return None

    class Meta:
        ordering = ["order"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    company_name = models.CharField(max_length=200)
    person_title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Temoignage"
        verbose_name_plural = "Temoignages"

    def __str__(self):
        return self.company_name


class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="team/", blank=True)
    legacy_photo = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    linkedin_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def display_photo(self):
        """Retourne l'URL de la photo Cloudinary ou le chemin static legacy."""
        if self.photo:
            return self.photo.url
        return None

    class Meta:
        ordering = ["order"]
        verbose_name = "Membre de l'equipe"
        verbose_name_plural = "Membres de l'equipe"

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.name} - {self.subject}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Abonne newsletter"
        verbose_name_plural = "Abonnes newsletter"

    def __str__(self):
        return self.email
