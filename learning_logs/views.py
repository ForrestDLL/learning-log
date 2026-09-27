from django.shortcuts import render, redirect

from .models import Topic
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """首页"""
    return render(request, "learning_logs/index.html")


def topics(request):
    """展示所有主题"""
    topics = Topic.objects.all()
    context = {"topics": topics}
    return render(request, "learning_logs/topics.html", context)


def topic(request, topic_id):
    """访问主题下的条目"""
    topic = Topic.objects.get(pk=topic_id)
    entries = topic.entries.order_by("-date")
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


def new_topic(request):
    """新增主题"""
    if request.method != "POST":
        # 未提交数据，创建一个空表单
        form = TopicForm()
    else:
        # POST提交的数据：处理数据
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topics")  # 保存后调回主题列表

    # 显示空表单，或指出表单数据无效
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


def edit_topic(request, topic_id):
    """编辑现有主题"""
    topic = Topic.objects.get(pk=topic_id)
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


def new_entry(request, topic_id):
    # 增加当前主题的新条目
    topic = Topic.objects.get(pk=topic_id)
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
