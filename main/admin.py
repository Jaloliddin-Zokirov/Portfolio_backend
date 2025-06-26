from django.contrib import admin
from .models import Sertificate, Skill, Portfolio

@admin.register(Sertificate)
class SerticateAdmin(admin.ModelAdmin):
    list_display = ('id', 'img')
    search_fields = ('id',) 
    list_filter = ('id',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'image')
    search_fields = ('title', 'description')
    list_filter = ('title',)    

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):     
    list_display = ('id', 'title', 'description', 'features','techstack', 'image', 'github_link', 'in_link', 'tg_link', 'linkedin_link', 'link')
    search_fields = ('title', 'description', 'features', 'techstack','github_link', 'in_link', 'tg_link', 'linkedin_link', 'link')
    list_filter = ('title',)    
    ordering = ('id',)
    
