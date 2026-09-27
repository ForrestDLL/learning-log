from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """首页"""
    return render(request, "learning_logs/index.html")


@login_required
def topics(request):
    """展示所有主题"""
    topics = Topic.objects.filter(owner=request.user)
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    """访问主题下的条目"""
    topic = get_object_or_404(Topic, pk=topic_id, owner=request.user)
    entries = topic.entries.order_by("-date")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """新增主题"""
    if request.method != "POST":
        # 未提交数据，创建一个空表单
        form = TopicForm()
    else:
        # POST提交的数据：处理数据
        form = TopicForm(data=request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.owner = request.user
            topic.save()
            return redirect("learning_logs:topics")  # 保存后返回主题列表

    # 显示空表单，或指出表单数据无效
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def edit_topic(request, topic_id):
    """编辑现有主题"""
    topic = get_object_or_404(Topic, pk=topic_id, owner=request.user)
    if request.method != "POST":
        # 原数据填进表单
        form = TopicForm(instance=topic)
    else:
        # 把提交的数据绑定到已存在的对象上
        form = TopicForm(data=request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topics")

    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/edit_topic.html", context)


@login_required
def new_entry(request, topic_id):
    # 增加当前主题的新条目
    topic = get_object_or_404(Topic, pk=topic_id, owner=request.user)
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    context = {"form": form, "topic": topic}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """编辑条目内容"""
    entry = get_object_or_404(Entry, pk=entry_id, topic__owner=request.user)
    topic = entry.topic
    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(data=request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=entry.topic_id)
        
    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)
