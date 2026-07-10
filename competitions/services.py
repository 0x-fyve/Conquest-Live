from .models import Competition
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError

class CompetitionService():
    @staticmethod
    def _generate_unique_slug(project, base_slug):
        base_slug = slugify(base_slug)
        candidate = base_slug

        counter = 2

        while Competition.objects.filter(slug=candidate, project=project).exists():
            candidate = f"{base_slug}-{counter}"

            counter += 1
               
        return candidate
    
    @staticmethod
    def create_competition(name, project, description="", slug=None, rules=None, starts_at=None, ends_at=None):
        if slug:
            slug = slugify(slug) 

            if Competition.objects.filter(project=project, slug=slug).exists():
                slug = CompetitionService._generate_unique_slug(project, slug)
        else:
            slug = CompetitionService._generate_unique_slug(project, name)       

        if starts_at and ends_at:
            if ends_at < starts_at:
                raise ValidationError({
                    "ends_at": [
                        "End date must be after the start date."
                    ]
                })   
            
        if rules is None:
            rules = {}    

        competition = Competition.objects.create(
            name=name,
            project=project,
            description=description,
            slug=slug,
            rules=rules,
            starts_at=starts_at,
            ends_at=ends_at
        )

        return competition
