from django.shortcuts import render

from .models import Literature

# Create your views here.


def literature_list(request):
    context = {
        "qs": Literature.objects.all(),
    }
    return render(request, "literature/literature_list.html", context=context)
