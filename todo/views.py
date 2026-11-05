from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Task


def dashboard(request):

    # Add a new task
    if request.method == "POST" and request.POST.get("action") == "add":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title:
            Task.objects.create(title=title, description=description)

        return redirect("dashboard")

    # Search tasks
    search = request.GET.get("search", "").strip()

    tasks = Task.objects.all()

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    # Separate tasks
    pending_tasks = tasks.filter(completed=False)
    completed_tasks = tasks.filter(completed=True)

    # Statistics (based on all tasks, not just search results)
    all_tasks = Task.objects.all()

    context = {
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "total_count": all_tasks.count(),
        "pending_count": all_tasks.filter(completed=False).count(),
        "completed_count": all_tasks.filter(completed=True).count(),
        "search": search,
    }

    return render(request, "dashboard.html", context)


def complete_task(request, task_id):

    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.completed = not task.completed
        task.save()

    return redirect("dashboard")


def delete_task(request, task_id):

    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id)
        task.delete()

    return redirect("dashboard")


def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":

        title = request.POST.get("title", "").strip()

        if title:
            task.title = title
            task.description = request.POST.get("description", "").strip()
            task.save()

            return redirect("dashboard")

    return render(request, "edit.html", {"task": task})
