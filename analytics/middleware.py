from ipware.ip import get_real_ip
import requests
from analytics.models import Page, Location, View
from rocketu_blog_analytics import settings


class LocationMiddleware(object):
    def process_request(self, request):
        ip = get_real_ip(request)
        if ip is None and settings.DEBUG:
            ip = requests.get('http://icanhazip.com/').text

        if ip is not None:
            response = requests.get('http://ipinfo.io/{}/json'.format(ip))
            if response.status_code == 200:
                request.location = response.json()
                request.location['latitude'], request.location['longitude'] = request.location['loc'].split(',')

        request.ip = ip


class PageViewMiddleware(object):
    def process_request(self, request):
        obj_page, created = Page.objects.get_or_create(url=request.META['PATH_INFO'])
        obj_loc, created = Location.objects.get_or_create(
            city=request.location['city'],
            country=request.location['country'],
            region=request.location['region'],
        )
        View.objects.create(
            page=obj_page,
            location=obj_loc,
            latitude=request.location['latitude'],
            longitude=request.location['longitude'],
            ip_address=request.location['ip']
        )
