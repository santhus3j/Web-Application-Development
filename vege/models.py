from faker import Faker
fake = Faker()
import random
from .models import *
from django.db import models
from django.contrib.auth.models import User
class Department(models.Model):
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name
    
class StudentID(models.Model):
    student_id = models.CharField(max_length=20, unique=True)


    def __str__(self):
        return self.student_id


    
class Student(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    student_id = models.OneToOneField(StudentID, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField(blank=True)

    def __str__(self):
        return self.student_name
    
    class Meta:
        ordering = ['student_name']
        verbose_name = 'student'

from django.utils import timezone

class Receipe(models.Model):
    receipe_name = models.CharField(max_length=200)
    receipe_description = models.TextField(blank=True)
    receipe_image = models.ImageField(upload_to='receipe', blank=True, null=True)
    receipe_view_count = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receipe_name


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subject_name

def seed_db(n=10) -> None:
    try:
        for _ in range(n):
            departments_objs = Department.objects.all()
            random_index = random.randint(0, len(departments_objs) - 1)
            student_id = f'STU-0{random.randint(100, 999)}'
            department = departments_objs[random_index]
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(20, 30)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)

            student_obj = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )
    except Exception as e:
        print(e)

class Subjectmarks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    max_marks = models.IntegerField(default=100)

    def __str__(self):
        return f"{self.student} - {self.subject}"