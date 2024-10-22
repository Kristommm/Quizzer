from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .forms import UserProfileForm


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        form = CustomUserCreationForm()
        profile_form = UserProfileForm()
    else:
        # Process completed form.
        form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            new_user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            login(request, new_user)
            return redirect('quizzer_app:index')

    # Display a blank or invalid form.
    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'registration/register.html', context)