from blog.models import Post, Tag, Ads


def latest_post(request):
    return {
        'latest_post': Post.objects.latest('created')
    }

def sidebar(request):
    tags = []
    tags_all = Tag.objects.all()
    for i in tags_all:
        if not i in tags:
            tags.append(i)

    month_list = Post.objects.dates('created', 'month')
    return {
        'tags': tags,
        'months': month_list
    }

def random_ad(request):
    if Ads.objects.filter(state=request.location['region']):
        return {
            'ad': Ads.objects.filter(state=request.location['region']).order_by('?')[0]
        }
    else:
        return {}

