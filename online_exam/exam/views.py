from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Exam, Question, Result


# 🏠 HOME PAGE
def home(request):
    exams = Exam.objects.all()
    return render(request, 'home.html', {'exams': exams})


# 📝 REGISTER VIEW
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("home")

    return render(request, "register.html")


# 🧠 TAKE EXAM (LOGIN REQUIRED)
@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)

    if request.method == "POST":

        score = 0
        violations = int(request.POST.get("violations", 0))
        canceled = request.POST.get("canceled", "false") == "true"

        # Calculate score
        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected == question.correct_answer:
                score += 1

        # Save result in database
        Result.objects.create(
            user=request.user,
            exam=exam,
            score=score,
            violations=violations,
            is_canceled=canceled
        )

        # If exam canceled
        if canceled:
            return render(request, "canceled.html")

        return render(request, "result.html", {"score": score})

    return render(request, "exam.html", {"exam": exam, "questions": questions})
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    results = Result.objects.filter(user=request.user).order_by('-id')
    return render(request, "dashboard.html", {"results": results})