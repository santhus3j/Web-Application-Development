from faker import Faker
fake = Faker()
import random
from vege.models import SubjectMarks, Student, Subject
from django.db import IntegrityError, transaction
import uuid


def create_subject_marks(n):
    try:
        student_objs = Student.objects.all()
        subjects = Subject.objects.all()
        
        marks_to_create = []
        
        for student in student_objs:
            for subject in subjects:
                marks_to_create.append(
                    SubjectMarks(
                        subject=subject,
                        student=student,
                        marks=random.randint(0, 100)
                    )
                )

        with transaction.atomic():
            SubjectMarks.objects.bulk_create(marks_to_create)

    except Exception as e:
        print(e)

def seed_db(n=10) -> None:
    from vege.models import StudentID, Student, Department
    # ensure faker unique state is fresh
    fake.unique.clear()

    for _ in range(n):
        # option A: UUID-based unique id
        sid_value = f"S-{uuid.uuid4().hex[:8]}"

        # option B (alternative): fake.unique.bothify(text='S####??')
        # sid_value = fake.unique.bothify(text='S####??')

        try:
            with transaction.atomic():
                student_id_obj, created = StudentID.objects.get_or_create(student_id=sid_value)
                dept, _ = Department.objects.get_or_create(department_name=fake.word().title())
                Student.objects.create(
                    department=dept,
                    student_id=student_id_obj,
                    student_name=fake.name(),
                    student_email=fake.unique.email(),
                    student_age=fake.random_int(min=18, max=30),
                    student_address=fake.address()
                )
        except IntegrityError:
            # skip and continue on any race/uniqueness issue
            continue
