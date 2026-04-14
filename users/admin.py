from django.contrib.auth.decorators import user_passes_test

def is_teacher(user):
    return user.role == 'teacher'

@user_passes_test(is_teacher)
def teacher_view(request):
    ...
