from django.contrib import admin
from .models import HowItWorksStep, ServicePlan, FAQCategory, FAQItem, Testimonial,SchoolClass, Stream, Subject, Teacher, StreamSubjectTeacher


class FAQItemInline(admin.TabularInline):
    model = FAQItem
    extra = 1

class FAQCategoryAdmin(admin.ModelAdmin):
    inlines = [FAQItemInline]

admin.site.register(HowItWorksStep)
admin.site.register(ServicePlan)
admin.site.register(FAQCategory, FAQCategoryAdmin)
admin.site.register(Testimonial)

admin.site.register(SchoolClass)
admin.site.register(Stream)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(StreamSubjectTeacher)
