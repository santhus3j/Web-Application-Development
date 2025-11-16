from django.contrib import admin
from django.db.models import Sum
from . import models
from .models import Receipe, Department, StudentID, Student, Subject, Subjectmarks

class SubjectmarksAdmin(admin.ModelAdmin):
    list_display = ('student_id_display', 'student_display', 'department_display', 'subject', 'marks')
    list_select_related = ('student', 'student__student_id', 'student__department', 'subject')
    list_per_page = 25
    search_fields = (
        'student__student_name',
        'student__student_id__student_id',
        'student__department__department_name',
        'subject__subject_name',
    )

    @admin.display(description='Student ID', ordering='student__student_id__student_id')
    def student_id_display(self, obj):
        try:
            return obj.student.student_id.student_id
        except Exception:
            return ''

    @admin.display(description='Student')
    def student_display(self, obj):
        return getattr(obj.student, 'student_name', '')

    @admin.display(description='Department')
    def department_display(self, obj):
        try:
            return obj.student.department.department_name
        except Exception:
            return ''

admin.site.register(Receipe)
admin.site.register(Department)
admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Subjectmarks, SubjectmarksAdmin)

# Optional: register ReportCard admin if ReportCard model exists in models.py
ReportCard = getattr(models, 'ReportCard', None)
if ReportCard:
    class ReportCardAdmin(admin.ModelAdmin):
        list_display = ('student', 'student_rank', 'total_marks_display', 'date_generated')
        readonly_fields = ('total_marks_display',)

        def total_marks_display(self, obj):
            # prefer an explicit field on the model if present
            if hasattr(obj, 'total_marks'):
                return getattr(obj, 'total_marks')
            # otherwise aggregate related Subjectmarks if available
            try:
                return obj.subjectmarks_set.aggregate(total=Sum('marks'))['total'] or 0
            except Exception:
                return ''
        total_marks_display.short_description = 'Total Marks'

    admin.site.register(ReportCard, ReportCardAdmin)