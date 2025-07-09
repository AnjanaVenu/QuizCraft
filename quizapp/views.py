from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from .models import QuizProfile, Question, AttemptedQuestion
from .forms import UserLoginForm, RegistrationForm


def home(request):
    context = {}
    return render(request, 'quizzz/home.html', context=context)


@login_required()
def user_home(request):
    context = {}
    return render(request, 'quizzz/user_home.html', context=context)


def leaderboard(request):

    top_quiz_profiles = QuizProfile.objects.order_by('-total_score')[:500]
    total_count = top_quiz_profiles.count()
    context = {
        'top_quiz_profiles': top_quiz_profiles,
        'total_count': total_count,
    }
    return render(request, 'quizzz/leaderboard.html', context=context)


@login_required()
def play(request):
    quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        question_pk = request.POST.get('question_pk')

        attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=question_pk)

        choice_pk = request.POST.get('choice_pk')

        try:
            selected_choice = attempted_question.question.choices.get(pk=choice_pk)
        except ObjectDoesNotExist:
            raise Http404

        quiz_profile.evaluate_attempt(attempted_question, selected_choice)

        return redirect(attempted_question)

    else:
        question = quiz_profile.get_new_question()
        if question is not None:
            quiz_profile.create_attempt(question)

        context = {
            'question': question,
        }

        return render(request, 'quizzz/play.html', context=context)


@login_required()
def submission_result(request, attempted_question_pk):
    attempted_question = get_object_or_404(AttemptedQuestion, pk=attempted_question_pk)
    context = {
        'attempted_question': attempted_question,
    }

    return render(request, 'quizzz/submission_result.html', context=context)


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/user-home')
    return render(request, 'quizzz/login.html', {"form": form, "title": title})


def register(request):
    title = "Create account"
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        # If form is NOT valid, execution continues here.
        # 'form' now contains the errors, and we want to display it again.
        # We don't need an 'else' here for the inner 'if'.
    else: # This 'else' is for GET requests (initial display of empty form)
        form = RegistrationForm()

    # This 'context' and 'return render' are now OUTSIDE the
    # 'if request.method == 'POST':' / 'else:' structure.
    # It will be executed in two cases:
    # 1. For GET requests (after 'form = RegistrationForm()' runs in the 'else' block).
    # 2. For POST requests where the form was NOT valid (after 'form = RegistrationForm(request.POST)' runs
    #    and the inner 'if form.is_valid():' is skipped).
    context = {'form': form, 'title': title}
    return render(request, 'quizzz/registration.html', context=context) # <--- IMPORTANT: Changed 'quizzz' to 'quiz' here too!


def logout_view(request):
    logout(request)
    return redirect('/')

@login_required()
def rules_view(request):
    return render(request, 'quizzz/rules.html')
