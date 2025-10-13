from django.db import models
from .helpers import SaveMediaFile
from .validators import validate_image_or_svg


class Sertificate(models.Model):
    img = models.FileField(
        upload_to=SaveMediaFile.sertificate_image,
        blank=True,
        null=True,
        validators=[validate_image_or_svg],
        max_length=500,
    )

    class Meta:
        verbose_name = "Sertificate"
        verbose_name_plural = "Sertificates"

    def __str__(self):
        return f"Sertificate {self.id}"
    

class Skill(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(
        upload_to=SaveMediaFile.skill_image,
        blank=True,
        null=True,
        validators=[validate_image_or_svg],
    )

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return f'{self.id} - {self.title or "No Title"} - {self.description or "No Description"}'



class Portfolio(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    features = models.JSONField(blank=True, null=True)
    tech_stack = models.JSONField(blank=True, default=list, db_column='techstack')
    image = models.FileField(
        upload_to=SaveMediaFile.portfolio_image,
        blank=True,
        null=True,
        validators=[validate_image_or_svg],
    )
    github_link = models.URLField(max_length=255, blank=True, null=True)
    in_link = models.URLField(max_length=255, blank=True, null=True)
    tg_link = models.URLField(max_length=255, blank=True, null=True)
    linkedin_link = models.URLField(max_length=255, blank=True, null=True)
    link = models.URLField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"  

    def __str__(self):
        return f'{self.id} - {self.title} - {self.description} - {self.features} - {self.tech_stack} - {self.github_link} - {self.in_link} - {self.tg_link} - {self.linkedin_link} - {self.link}'

    
