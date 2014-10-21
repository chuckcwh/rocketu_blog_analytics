from collections import Counter
import json
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from analytics.models import Page, View


def main(request):
    return render(request, 'main.html', {
        'pages': Page.objects.all(),
    })


def page_map(request, pk):
    return render(request, 'page_map.html', {
        'page': Page.objects.get(pk=pk),
        'views': View.objects.filter(page=pk),
    })

def page_analytics(request, pk):
    page = Page.objects.filter(pk=pk)
    url = page[0].url
    view_obj = View.objects.filter(page=pk)
    count = View.objects.filter(page=pk).count()
    view_obj2 = View.objects.filter(page=pk).values("longitude", "latitude").annotate(Count("id")).order_by()
    return render(request, 'page_analytics.html', {
        'count': count,
        'view_list': view_obj,
        'sorted_views':view_obj2,
        'url':url
    })

@csrf_exempt
def page_map_ajax(request):
    url_path = json.loads(request.body)
    views = View.objects.filter(page__url=url_path)
    view_list = []
    for view in views:
        coordinate = [view.latitude, view.longitude]
        view_list.append(coordinate)
    return HttpResponse(
        json.dumps(view_list),
        content_type='application.json'
    )