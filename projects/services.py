from django.utils.text import slugify
from .models import Project

class ProjectService:
    @staticmethod
    def _generate_unique_slug(owner, base_slug):
        base_slug = slugify(base_slug)
        candidate = base_slug

        counter = 2

        while Project.objects.filter(slug=candidate, owner=owner).exists():
            candidate = f"{base_slug}-{counter}"

            counter += 1
               
        return candidate
    
    @staticmethod
    def create_project(owner, name, description="", slug=None):
        if slug:
            slug = slugify(slug)

            if Project.objects.filter(owner=owner, slug=slug).exists():
                slug = ProjectService._generate_unique_slug(owner, slug)
    
        else:
            slug = ProjectService._generate_unique_slug(owner, name)

        project = Project.objects.create(
            owner=owner,
            name=name,
            description=description,
            slug=slug
            )
            

        return project    
        