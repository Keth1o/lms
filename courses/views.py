from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Schedule, Assignment, Subject, SubjectTask, Submission
from .forms import CourseForm, SubjectForm, ScheduleForm, AssignmentForm
from users.models import User


@login_required
def redirect_after_login(request):

    if request.user.role == 'student':

        enrollment = Enrollment.objects.filter(student=request.user).first()

        if enrollment:
            return redirect('course_detail', pk=enrollment.course.id)

    return redirect('course_list')


@login_required
def course_list(request):

    courses = Course.objects.all()

    return render(request, 'course_list.html', {
        'courses': courses
    })


@login_required
def add_course(request):

    if not request.user.is_teacher():
        return redirect('course_list')

    form = CourseForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('course_list')

    return render(request, 'add_course.html', {'form': form})


@login_required
def course_detail(request, pk):

    course = get_object_or_404(Course, id=pk)

    tab = request.GET.get('tab', 'schedule')

    schedule = Schedule.objects.filter(course=course)

    subjects = Subject.objects.filter(courses=course)

    if request.user.role == 'student':
        subjects = subjects.filter(courses=course)

    elif request.user.role == 'teacher':
        subjects = subjects.filter(teacher=request.user)

    deadlines = Assignment.objects.filter(course=course)

    return render(request, 'course_detail.html', {

        'course': course,

        'tab': tab,

        'schedule': schedule,

        'subjects': subjects,

        'deadlines': deadlines
    })


@login_required
def register_student(request, pk):

    if not request.user.is_teacher():
        return redirect('course_list')

    course = get_object_or_404(Course, id=pk)
    error = None

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            error = "Заповніть всі поля"

        elif User.objects.filter(username=username).exists():
            error = "Користувач вже існує"

        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                role='student'
            )

            Enrollment.objects.create(
                student=user,
                course=course
            )

            return redirect('course_detail', pk=pk)

    return render(request, 'register_student.html', {
        'error': error,
        'course': course
    })

@login_required
def subject_detail(request, pk):

    subject = get_object_or_404(Subject, id=pk)

    if request.user.role == 'teacher':
        if subject.teacher != request.user:
            return redirect('course_list')

    if request.user.role == 'student':
        if not Enrollment.objects.filter(
            student=request.user,
            course__in=subject.courses.all()
        ).exists():
            return redirect('course_list')

    tasks = Assignment.objects.filter(subject=subject)

    return render(request, 'subject.html', {

        'subject': subject,
        'tasks': tasks

    })

@login_required
def create_subject(request):

    if not request.user.is_teacher():
        return redirect('course_list')

    form = SubjectForm(request.POST or None)

    if form.is_valid():
        subject = form.save(commit=False)
        subject.teacher = request.user
        subject.save()
        form.save_m2m()
        return redirect('course_list')

    return render(request, 'create_subject.html', {'form': form})

@login_required
def add_schedule(request, pk):

    if not request.user.is_teacher():
        return redirect('course_list')

    course = get_object_or_404(Course, id=pk)

    form = ScheduleForm(request.POST or None)

    if form.is_valid():

        schedule = form.save(commit=False)
        schedule.course = course
        schedule.save()

        return redirect('course_detail', pk=pk)

    return render(request, 'add_schedule.html', {
        'form': form,
        'course': course
    })

@login_required
def create_assignment(request):

    if not request.user.is_teacher():
        return redirect('course_list')

    form = AssignmentForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        subject = form.cleaned_data['subject']

        for course in subject.courses.all():
            Assignment.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data.get('image'),
                deadline=form.cleaned_data['deadline'],
                subject=subject,
                course=course
            )

        return redirect('course_list')

    return render(request, 'create_assignment.html', {'form': form})


@login_required
def schedule_page(request):

    if request.user.is_student():
        schedules = Schedule.objects.filter(
            course__enrollments__student=request.user
        )
        course = schedules.first().course if schedules.exists() else None

    else:
        schedules = Schedule.objects.all()
        course = schedules.first().course if schedules.exists() else None

    return render(request, 'schedule.html', {
        'schedules': schedules,
        'course': course
    })

@login_required
def deadlines_page(request):

    assignments = Assignment.objects.filter(
        course__enrollments__student=request.user
    )

    pending = assignments.exclude(
        submission__student=request.user,
        submission__submitted=True
    )

    return render(request, 'deadlines.html', {
        'assignments': pending
    })

@login_required
def submit_assignment(request, id):

    assignment = get_object_or_404(Assignment, id=id)

    submission, created = Submission.objects.get_or_create(
        assignment=assignment,
        student=request.user
    )

    submission.submitted = True
    submission.save()

    return redirect('deadlines_page')

@login_required
def add_assignment(request, pk):

    if not request.user.is_teacher():
        return redirect('course_list')

    subject = get_object_or_404(Subject, id=pk)

    if request.user.role == 'teacher' and subject.teacher != request.user:
        return redirect('course_list')

    form = AssignmentForm(request.POST or None, request.FILES or None)

    if form.is_valid():

        for course in subject.courses.all():
            Assignment.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data.get('image'),
                deadline=form.cleaned_data['deadline'],
                subject=subject,
                course=course
            )

        return redirect('subject_detail', pk=pk)

    return render(request, 'add_assignment.html', {
        'form': form,
        'subject': subject
    })