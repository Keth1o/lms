from django.db import models
from users.models import User


class Course(models.Model):

    title = models.CharField(max_length=255)

    description = models.TextField()

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Schedule(models.Model):
    def __str__(self):
        return self.title

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)

    date = models.DateField()

    description = models.TextField()

class Subject(models.Model):
    def __str__(self):
        return self.title

    name = models.CharField(max_length=255)

    description = models.TextField()

    courses = models.ManyToManyField(Course)

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subjects'
    )

    def __str__(self):
        return self.name


class Assignment(models.Model):

    title = models.CharField(max_length=255)

    description = models.TextField()

    image = models.ImageField(
        upload_to='assignments/',
        blank=True,
        null=True
    )

    deadline = models.DateField()

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='assignments'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments'
    )



class SubjectTask(models.Model):

    subject = models.ForeignKey(
    Subject,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    title = models.CharField(max_length=255)

    description = models.TextField()

class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submission')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField(blank=True)
    submitted = models.BooleanField(default=False)  
    grade = models.IntegerField(blank=True, null=True)