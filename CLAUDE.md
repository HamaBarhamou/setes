# CLAUDE.md - Guide de Developpement SETES SARL

## Projet
Site vitrine de **SETES SARL** (Energies, Telecommunication et Services), entreprise basee a Niamey, Niger.
- **URL production** : https://setes.net
- **Hebergement** : Render.com
- **Framework** : Django 6.0.3 + Bootstrap 5

## Architecture

```
setes/
├── config/              # Configuration Django (settings, urls, wsgi, asgi)
├── core/                # App principale (models, views, forms, admin, urls, sitemaps)
├── templates/           # Templates HTML (base.html, index.html, service-details.html, etc.)
├── static/assets/       # CSS, JS, images, vendors (Bootstrap, AOS, Swiper, etc.)
├── manage.py
├── build.sh             # Script de deploiement Render
└── requirements.txt
```

## App `core`

- **models.py** : Service, Testimonial, TeamMember, ContactMessage, NewsletterSubscriber
- **views.py** : home, portfolio_details, service_details, contact_submit (AJAX), newsletter_subscribe (AJAX), robots_txt
- **forms.py** : ContactForm, NewsletterForm (ModelForm)
- **admin.py** : Admin complet avec list_display, search, filters, list_editable
- **urls.py** : Toutes les routes du site
- **sitemaps.py** : StaticViewSitemap, ServiceSitemap
- **context_processors.py** : newsletter_form (disponible sur toutes les pages)

## Commandes essentielles

```bash
# Activer le venv
source venv/bin/activate

# Demarrer le serveur de dev
python3 manage.py runserver

# Migrations
python3 manage.py makemigrations core && python3 manage.py migrate

# Collecter les fichiers statiques (production)
python3 manage.py collectstatic --no-input

# Creer un superuser
python3 manage.py createsuperuser
```

## Stack technique

| Composant         | Technologie                              |
|-------------------|------------------------------------------|
| Backend           | Django 6.0.3, Python 3.12                |
| Frontend          | Bootstrap 5, AOS, Swiper, GLightbox     |
| Fichiers statiques| WhiteNoise (compression + cache)         |
| Media (images)    | Cloudinary (gratuit 25GB)                |
| BDD               | PostgreSQL Neon (gratuit) via DATABASE_URL |
| Serveur prod      | Gunicorn                                 |
| Deploiement       | Render.com (build.sh)                    |

## Configuration cle (config/settings.py)

- `DEBUG` = True en local, False sur Render
- `ALLOWED_HOSTS` = `setes.net`, `www.setes.net` en prod ; `127.0.0.1`, `localhost` en dev
- `LANGUAGE_CODE` = `fr`, `TIME_ZONE` = `Africa/Niamey`
- `SECRET_KEY` via variable d'environnement
- PostgreSQL Neon via `DATABASE_URL` (fichier `.env` en local)
- `STORAGES` pour WhiteNoise (syntaxe Django 6.x)
- Cloudinary pour les media (images uploadees via admin)
- Les images existantes restent dans `static/` via les champs `legacy_image`/`legacy_photo`

## Routes

| URL                              | Vue                    | Template                 |
|----------------------------------|------------------------|--------------------------|
| `/`                              | `home()`               | `index.html`             |
| `/admin/`                        | Django admin           | -                        |
| `/portfolio-details/`            | `portfolio_details()`  | `portfolio-details.html` |
| `/service-details/<slug>/`       | `service_details()`    | `service-details.html`   |
| `/contact/`                      | `contact_submit()` POST| JSON response            |
| `/newsletter/`                   | `newsletter_subscribe()` POST | JSON response     |
| `/sitemap.xml`                   | Django sitemap         | XML                      |
| `/robots.txt`                    | `robots_txt()`         | text/plain               |

## Modeles (core/models.py)

- **Service** : title, slug, description, details, icon, image (Cloudinary), legacy_image (static), order, is_active
- **Testimonial** : company_name, person_title, content, rating, order, is_active
- **TeamMember** : name, role, photo (Cloudinary), legacy_photo (static), order, is_active, linkedin_url
- **ContactMessage** : name, email, subject, message, is_read
- **NewsletterSubscriber** : email, is_active

## Templates

- `base.html` : Master layout (header, footer, SEO meta, JSON-LD, preload)
- `index.html` : Page d'accueil (Hero, About, Stats, Services, Portfolio, Testimonials, Team, Contact)
- `service-details.html` : Detail d'un service avec sidebar dynamique
- `portfolio-details.html` : Page realisations (herite de base.html)
- `404.html` / `500.html` : Pages d'erreur en francais

## SEO

- Meta description et keywords avec blocs overridables
- Open Graph tags
- JSON-LD LocalBusiness
- Sitemap XML automatique
- robots.txt

## Formulaires

- Contact : AJAX via `static/assets/js/forms.js`, sauvegarde en BDD, classe CSS `django-form`
- Newsletter : AJAX idem, dans le footer via context processor

## Conventions

- Code Python formate avec `black`
- Templates utilisent `{% static %}` pour les assets
- URLs nommees avec `name=`
- Langue du site : **francais**
- Images below-the-fold : `loading="lazy"` + `decoding="async"`
- Aria-labels sur les elements interactifs

## Variables d'environnement (production Render)

- `SECRET_KEY` - cle secrete Django
- `RENDER_EXTERNAL_HOSTNAME` - ajoute automatiquement aux ALLOWED_HOSTS
- `DATABASE_URL` - **obligatoire** - URL PostgreSQL Neon (gratuit a vie)
- `CLOUDINARY_CLOUD_NAME` - nom du cloud Cloudinary
- `CLOUDINARY_API_KEY` - cle API Cloudinary
- `CLOUDINARY_API_SECRET` - secret API Cloudinary
