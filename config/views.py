from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def portfolio_details(request):
    return render(request, "portfolio-details.html")


""" def service_details(request):
    return render(request, 'service-details.html')
 """


def service_details(request, service_slug):
    services = {
        "etudes-techniques": {
            "title": "Études et conception de sites techniques",
            "description": "Des études personnalisées pour la conception et l’installation de sites techniques répondant aux normes industrielles.",
            "icon": "bi-diagram-3",
            "details": "Chez SETES SARL, nous réalisons des études techniques approfondies pour concevoir des infrastructures adaptées aux besoins spécifiques de chaque client. Nos équipes d'ingénieurs et de techniciens expérimentés effectuent une analyse complète des paramètres techniques, environnementaux et économiques avant de concevoir un projet. Grâce à notre expertise, nous assurons une optimisation des performances tout en respectant les normes les plus strictes de l'industrie. Nos solutions couvrent la conception de réseaux, la planification d'installations techniques, ainsi que l'ingénierie des systèmes complexes.",
            "image": "assets/img/services/etudes-techniques.jpg",
        },
        "systemes-solaires": {
            "title": "Fourniture et pose de systèmes solaires photovoltaïques",
            "description": "Des solutions d’énergie renouvelable pour vos besoins en électricité durable et économique.",
            "icon": "bi-sun",
            "details": "Nous proposons des systèmes solaires photovoltaïques qui répondent aux besoins énergétiques des entreprises et des particuliers. Nos solutions incluent l'étude de faisabilité, la fourniture des équipements de haute qualité, l'installation sur site et la maintenance continue. Nous offrons une expertise complète allant de l'intégration des panneaux solaires à la gestion des batteries et des onduleurs, garantissant ainsi une production d'énergie propre et stable. En choisissant SETES SARL, vous optez pour une autonomie énergétique et une réduction significative de votre empreinte carbone.",
            "image": "assets/img/services/systemes-solaires.jpg",
        },
        "systemes-securite": {
            "title": "Fourniture et installation de systèmes de sécurité",
            "description": "Sécurisez vos installations avec nos systèmes de surveillance et de protection incendie.",
            "icon": "bi-shield-lock",
            "details": "Nous offrons des solutions de sécurité intégrées comprenant des systèmes de surveillance par caméras, des dispositifs de détection d'incendie, des contrôles d'accès sécurisés, et bien plus encore. Chaque système est conçu pour s'adapter à vos besoins spécifiques, que ce soit pour une entreprise, une industrie ou un espace résidentiel. Nos solutions incluent la fourniture, l'installation et la configuration des équipements, ainsi que la formation pour une utilisation optimale. Nous assurons également la maintenance préventive et corrective afin de garantir une protection continue.",
            "image": "assets/img/services/systemes-securite.jpg",
        },
        "maintenance-telecoms": {
            "title": "Maintenance et exploitation des systèmes télécoms",
            "description": "Nous assurons l’audit, la maintenance et l’exploitation des systèmes FH, VSAT, FO et autres infrastructures télécom.",
            "icon": "bi-wifi",
            "details": "Nos services de maintenance télécom comprennent l'audit des infrastructures, la maintenance préventive et corrective, ainsi que l'exploitation continue des systèmes télécoms. Nous intervenons sur des technologies telles que les faisceaux hertziens (FH), les systèmes VSAT, la fibre optique (FO) et d'autres équipements critiques. Notre expertise garantit la disponibilité et la performance optimales de vos réseaux télécoms, réduisant ainsi les interruptions de service. Nous offrons des solutions sur-mesure, que ce soit pour des opérateurs télécoms, des institutions gouvernementales ou des entreprises privées.",
            "image": "assets/img/services/maintenance-telecoms.jpg",
        },
        "groupes-electrogenes": {
            "title": "Fourniture de groupes électrogènes",
            "description": "Nous proposons des solutions fiables pour assurer la continuité de l’alimentation électrique.",
            "icon": "bi-lightning",
            "details": "Nos solutions de fourniture de groupes électrogènes incluent la vente, l'installation et la maintenance d’équipements de différentes puissances adaptés à vos besoins spécifiques. Que ce soit pour une alimentation de secours, pour des sites industriels ou pour des installations temporaires, nous vous fournissons des générateurs robustes et fiables. Nos équipes d'experts vous accompagnent dans le choix des équipements, en assurant une configuration optimale pour garantir une disponibilité continue de l’énergie. Nos services incluent également la gestion de l’entretien préventif et des réparations pour prolonger la durée de vie des équipements.",
            "image": "assets/img/services/groupes-electrogenes.jpg",
        },
        "audit-pylones": {
            "title": "Audit et maintenance des pylônes",
            "description": "Nos services incluent l’audit, l’installation et la maintenance des pylônes télécoms pour une performance optimale.",
            "icon": "bi-tower",
            "details": """Nous offrons des services complets pour l’audit, l’installation et la maintenance des pylônes de communication. Nos experts réalisent des inspections approfondies pour évaluer l’intégrité structurelle et la conformité des pylônes aux normes de sécurité. Nos services incluent également la modernisation des infrastructures existantes, l’installation de nouveaux pylônes et la gestion des systèmes de fixation d’équipements télécoms. Grâce à notre expertise, nous garantissons une performance optimale et une sécurité accrue de vos installations télécoms.""",
            "image": "assets/img/services/audit-pylones.jpg",
        },
        "solutions-numeriques": {
            "title": "Développement de solutions numériques",
            "description": "Ingénierie logicielle pour la gestion de l'énergie, l'analyse de données, la gestion des réseaux intelligents, et plus encore.",
            "icon": "bi-laptop",
            "details": """SETES SARL se positionne en tant qu'acteur clé dans le développement de solutions numériques sur-mesure. Nos services incluent la conception de logiciels de gestion de l'énergie, des systèmes de contrôle de la production d’énergies renouvelables, ainsi que des plateformes pour la gestion de réseaux intelligents. Nous offrons des solutions évolutives et performantes adaptées aux besoins spécifiques de chaque client. Notre expertise couvre également l’analyse de données, la prévision de consommation énergétique, et l’intégration de systèmes IoT pour une optimisation continue.""",
            "image": "assets/img/services/solutions-numeriques.jpg",
        },
    }

    service = services.get(service_slug, None)
    if service is None:
        return render(request, "404.html")  # Vous pouvez personnaliser la page d'erreur

    return render(
        request,
        "service-details.html",
        {
            "service": service,
            "services": services,  # Pour rendre la liste des services accessible dans le template
        },
    )
