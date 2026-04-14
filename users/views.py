from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


@login_required
def profile_view(request):

    form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user
    )

    if form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, 'profile.html', {
        'form': form
    })