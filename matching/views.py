# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from base.queries import get_this_season
from base.decorators import korean_required

from matching.models import Matching, MatchingLanguage, MatchingConnection
from matching.forms import MatchingKoreanForm, MatchingForeignerForm


@login_required
def list(request):
    matching_list = Matching.objects.filter(
        user__groups__name='Korean',
        season=get_this_season())
    return render(request, 'matching/list.html', {
        'matching_list': matching_list
    })


@login_required
@korean_required
def register(request):
    form = MatchingKoreanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        matching = form.save(commit=False)
        matching.user = request.user
        matching.season = get_this_season()
        matching.save()
        return redirect(register_finish)

    return render(request, 'matching/register.html', {
        'form': form
    })


@login_required
@korean_required
def register_finish(request):
    return render(request, 'matching/register_finish.html', {})


@login_required
def view(request, matching_id):
    matching = Matching.objects.get(id=matching_id)
    return render(request, 'matching/view.html', {
        'matching': matching
    })


@login_required
def register_foreigner(request, matching_id):
    korean_matching = Matching.objects.get(id=matching_id)

    matching_count = MatchingConnection.objects.filter(
        korean_matching=korean_matching).count()
    matching_valid = (korean_matching.max_buddy_number > matching_count)
    if not matching_valid:
        return redirect(register_full)

    form = MatchingForeignerForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        matching = form.save(commit=False)
        matching.user = request.user
        matching.season = get_this_season()
        matching.save()
        matching_connection = MatchingConnection.objects.create(
            korean_matching=korean_matching,
            foreign_matching=matching)
        return redirect(register_foreigner_finish)
        
    return render(request, 'matching/register_foreigner.html', {
        'matching': korean_matching,
        'form': form
    })


@login_required
def register_foreigner_finish(request):
    return render(request, 'matching/register_foreigner_finish.html', {})

@login_required
def register_full(request):
    return render(request, 'matching/register_full.html', {})


@login_required
def delete(request, matching_id):
    matching = Matching.objects.get(id=matching_id)
    if request.user == matching.user:
        return render(request, 'matching/delete.html', {
            'matching': matching
        })

    return redirect(list)


@login_required
def delete_bye(request, matching_id):
    matching = Matching.objects.get(id=matching_id)
    if request.user == matching.user:
        MatchingLanguage.objects.filter(matching=matching).delete()
        matching_connections = MatchingConnection.objects.filter(
            korean_matching=matching)
        for item in matching_connections:
            item.foreign_matching.delete()
            item.delete()
        MatchingConnection.objects.filter(foreign_matching=matching).delete()
        matching.delete()

    return redirect(list)
