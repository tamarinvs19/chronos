from django.db.models import Count, Q
from django.forms import forms
from django.http import HttpResponse, HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from tasks.forms import TaskForm

import json

from .models import Task


def index(request: HttpRequest) -> HttpResponse:
    tasks = Task.objects.annotate(
        incompleted_dep_count=Count(
            'dependencies',
            filter=~Q(dependencies__status__in=[Task.TaskStatus.DONE, Task.TaskStatus.CANCELLED])
        )
    ).filter(incompleted_dep_count=0).prefetch_related('continuations')
    return render(request, "tasks/index.html", {"tasks": tasks})


def detail(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "tasks/detail.html", {"task": task})


def create_task(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        new_task = Task.objects.create(title=request.POST["title"])
        parent = Task.objects.get(id=request.POST["parent"])
        new_task.dependencies.add(parent)
        new_task.save()
        return redirect(reverse("tasks:index"))
    else:
        return render(request, "tasks/createTask.html", {"tasks": Task.objects.all()})


def create_task2(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TaskForm(request.POST) 
        if form.is_valid():
            form.save()
    else:
        form = TaskForm()
    return render(request, "tasks/create.html", {"form": form})


def update_status(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        request_body = json.loads(request.body)
        task_id = request_body.get('task_id')
        task = Task.objects.get(id=task_id)
        status_name = json.loads(request.body).get('status', '')
        match status_name:
            case 'TODO':
                task.status = Task.TaskStatus.TODO
            case 'IN_PROGRESS':
                task.status = Task.TaskStatus.INPROGRESS
            case 'DONE':
                task.status = Task.TaskStatus.DONE
            case 'CANCELLED':
                task.status = Task.TaskStatus.CANCELLED
        task.save()
        return JsonResponse({'status': 'ok', 'newStatus': task.status})
    else:
        return JsonResponse({'status': 'fail'})
