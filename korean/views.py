from django.shortcuts import render

from django.contrib.auth.models import User, Group
from base.models import UserProfile
from base.queries import get_this_season
from matching.models import Matching


def index(request):
    return render(request, 'korean/index.html', {})


def korean_list(request):
    group = Group.objects.get(name='Korean')
    infos = []
    users = group.user_set.all()
    for user in users:
        exist = Matching.objects.filter(
            user=user,
            season=get_this_season()).exists()
        infos.append([user, exist])
    
    return render(request, 'korean/korean_list.html', {
        'infos': infos
    })
