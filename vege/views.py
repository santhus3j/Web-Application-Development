from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipe, Student, Subjectmarks
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator

def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        Receipe.objects.create(
            receipe_image=receipe_image,
            receipe_name=receipe_name,
            receipe_description=receipe_description
        )
        return redirect('/receipes')
    queryset = Receipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains=request.GET.get('search'))
    context = {"receipes": queryset}
    return render(request, 'receipes.html', context)

def update_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    if request.method == "POST":
        data = request.POST
        receipe_image = request.FILES.get('receipe_image')
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        if receipe_image:
            queryset.receipe_image = receipe_image
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
        queryset.save()
        return redirect('/receipes')
    context = {'receipe': queryset}
    return render(request, 'update_receipe.html', context)

def delete_receipe(request, id):
    queryset = Receipe.objects.get(id=id)
    queryset.delete()
    return redirect('receipes')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username or Password")
            return redirect('/login/')
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid Username or Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/receipes/')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect("/register/")
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        messages.info(request, "User created successfully")
        return redirect('/register/')
    return render(request, 'register.html')

def get_students(request):
    queryset = Student.objects.select_related('student_id', 'department').all()
    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(student_name__icontains=search) |
            Q(department__department_name__icontains=search) |
            Q(student_id__student_id__icontains=search) |
            Q(student_email__icontains=search) |
            Q(student_age__icontains=search)
        )
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'report/students.html', {'page_obj': page_obj})

students = get_students

def see_marks(request, student_id):
    # find the student object
    student = get_object_or_404(Student, student_id__student_id=student_id)

    # marks queryset for the student
    queryset = Subjectmarks.objects.filter(student=student).select_related('subject')

    # total marks for this student (handle NULLs)
    total_agg = queryset.aggregate(total_marks=Coalesce(Sum('marks'), 0))
    total_marks = total_agg.get('total_marks', 0) or 0

    # compute rank: annotate all students with their total marks and order desc
    students_totals = Student.objects.annotate(
        total_marks=Coalesce(Sum('subjectmarks__marks'), 0)
    ).order_by('-total_marks')

    current_rank = None
    for idx, s in enumerate(students_totals, start=1):
        if s.id == student.id:
            current_rank = idx
            break

    context = {
        'queryset': queryset,        # old name you used in templates
        'marks': queryset,           # also provide 'marks' for templates that expect it
        'total_marks': total_marks,
        'current_rank': current_rank,
        'student': student,
    }
    return render(request, 'report/see_marks.html', context)

def student_report(request, student_id):
    # get student
    student = get_object_or_404(Student, student_id__student_id=student_id)

    # per-subject marks
    marks_qs = Subjectmarks.objects.filter(student=student).select_related('subject').order_by('subject__subject_name')

    # totals
    total = marks_qs.aggregate(total=Coalesce(Sum('marks'), 0))['total'] or 0
    max_total = marks_qs.aggregate(max_total=Coalesce(Sum('max_marks'), 0))['max_total'] or 0
    percentage = round((total / max_total * 100) if max_total else 0, 2)

    # simple grading
    def grade_from_pct(p):
        if p >= 90: return 'A+'
        if p >= 80: return 'A'
        if p >= 70: return 'B'
        if p >= 60: return 'C'
        if p >= 50: return 'D'
        return 'F'
    grade = grade_from_pct(percentage)

    # rank: compute total for every student and determine position
    students_totals = Student.objects.annotate(
        total_marks=Coalesce(Sum('subjectmarks__marks'), 0)
    ).order_by('-total_marks', 'student_name')

    rank = None
    for idx, s in enumerate(students_totals, start=1):
        if s.id == student.id:
            rank = idx
            break

    # class average (of students who have marks)
    class_total = students_totals.aggregate(class_sum=Coalesce(Sum('total_marks'), 0))['class_sum'] or 0
    class_count = students_totals.count() or 1
    class_average = round(class_total / class_count, 2)

    context = {
        'student': student,
        'marks': marks_qs,
        'total': total,
        'max_total': max_total,
        'percentage': percentage,
        'grade': grade,
        'rank': rank,
        'class_average': class_average,
    }
    return render(request, 'report/student_report.html', context)

def success_page(request):
    return render(request, 'success_page.html')