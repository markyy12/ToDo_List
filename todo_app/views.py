from django.shortcuts import render, redirect, get_object_or_404
from todo.models import Task


def dashboard(request):

    if request.method == "POST":

        action = request.POST.get("action")

        # Add task
        if not action:
            title = request.POST.get("title")

            if title:
                Task.objects.create(title=title)

        # Complete task
        elif action == "complete":
            task_id = request.POST.get("task_id")
            task = get_object_or_404(Task, id=task_id)
            task.completed = True
            task.save()

        # Delete task
        elif action == "delete":
            task_id = request.POST.get("task_id")
            task = get_object_or_404(Task, id=task_id)
            task.delete()

        return redirect("dashboard")

    # Get all tasks
    tasks = Task.objects.all().order_by("-created_at")

    # Separate tasks
    pending_list = tasks.filter(completed=False)
    completed_list = tasks.filter(completed=True)

    # Statistics
    total_tasks = tasks.count()
    pending_tasks = pending_list.count()
    completed_tasks = completed_list.count()

    context = {
        "tasks": tasks,
        "pending_list": pending_list,
        "completed_list": completed_list,
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
    }

    return render(request, "dashboard.html", context)
