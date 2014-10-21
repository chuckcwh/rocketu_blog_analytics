from blog.models import Post, Tag


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

    posts = []
    month_list = Post.objects.dates('created', 'month')
    # for month in month_list:
    #     post = Post.objects.filter()
    return {
        'tags': tags,
        'months': month_list
    }