from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ThreadForm, ReplyForm
from .models import Thread


def index(request):
    form = ThreadForm()
    threads = Thread.objects.all()
    context = {'form': form, 'threads': threads}
    return render(request, 'forum/index.html', context)


def thread(request, thread_id):
    thread = Thread.objects.get(pk=thread_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        reply = form.save(commit=False)
        reply.thread = thread
        reply.user = request.user
        reply.save()
        return redirect('forum:thread', thread_id=thread.id)

    context = {'thread': thread, 'form': ReplyForm()}
    return render(request, 'forum/thread.html', context)


@login_required
def new_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        thread = form.save()
        return redirect('forum:thread', thread_id=thread.id)

    return render(request, 'forum/new_thread.html', {'form': ThreadForm()})
