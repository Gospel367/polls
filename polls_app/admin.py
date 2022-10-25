import profile
from django.contrib import admin
from .models import Newsletter, Profile


'''class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
           ( 'Question Information', {'fields': ['title'],}),
           ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)'''
admin.site.register(Profile)
admin.site.register(Newsletter)
