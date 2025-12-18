from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from .models import Task, Category, Notification
from .forms import TaskForm, CategoryForm
from django.contrib.auth.models import User



# ---------------- Auth ----------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if username and email and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return redirect("signup")

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created! Please login.")
            return redirect("login")

    return render(request, "registration/signup.html")



@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

# ---------------- Tasks ----------------
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    total = tasks.count()
    completed = tasks.filter(status='completed').count()
    overdue = sum(1 for t in tasks if t.is_overdue())
    categories = Category.objects.filter(user=request.user).order_by('name')
    return render(request, "task/task_list.html", {"tasks": tasks, "total": total, "completed": completed, "overdue": overdue, "categories": categories})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, "task/task_detail.html", {"task": task})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task created.")
            return redirect("task-list")
    else:
        form = TaskForm()
    return render(request, "task/task_form.html", {"form": form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated.")
            return redirect("task-list")
    else:
        form = TaskForm(instance=task)
    return render(request, "task/task_form.html", {"form": form, "task": task})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task deleted.")
        return redirect("task-list")
    return render(request, "task/task_confirm_delete.html", {"task": task})

# ---------------- Categories ----------------
@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user).order_by('name')
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            messages.success(request, "Category added.")
            return redirect("category-list")
    else:
        form = CategoryForm()
    return render(request, "category/categories.html", {"categories": categories, "form": form})

@login_required
def category_tasks(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    tasks = Task.objects.filter(user=request.user, category=category).order_by("due_date")
    return render(request, "category/category_tasks.html", {"category": category, "tasks": tasks})

# ---------------- Notifications ----------------
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "notifications/notification_list.html", {"notifications": notifications})

# ---------------- Dashboard ----------------
@login_required

def dashboard(request):
    user_tasks = Task.objects.filter(user=request.user)
    total = user_tasks.count()
    completed = user_tasks.filter(status='completed').count()
    overdue = sum(1 for t in user_tasks if t.is_overdue())
    categories = Category.objects.filter(user=request.user).order_by('name')
    upcoming = user_tasks.order_by('due_date')[:5]

    context = {
        "tasks": user_tasks,
        "upcoming": upcoming,
        "total": total,
        "completed": completed,
        "overdue": overdue,
        "categories": categories
    }
    return render(request, "dashboard.html", context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "registration/login.html")

