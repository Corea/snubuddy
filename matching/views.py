# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from base.queries import get_this_season
from base.decorators import (
    group_required, reverse_group_required, new_buddy_required)
from base.models import Language

from matching.models import Matching, MatchingLanguage, MatchingConnection
from matching.forms import MatchingKoreanForm, MatchingForeignerForm


def get_count_matched_buddies(matching):
    return MatchingConnection.objects.filter(korean_matching=matching).count()


@login_required
@reverse_group_required('Guest')
def list(request):
    matching_list = Matching.objects.filter(
        user__groups__name='Korean',
        season=get_this_season()).order_by('id')

    matching_list = sorted(matching_list,
            key=lambda x: (get_count_matched_buddies(x) / x.max_buddy_number))

    return render(request, 'matching/list.html', {
        'matching_list': matching_list
    })


def remove_prior_matching(request):
    matching_list = Matching.objects.filter(
        user=request.user,
        season=get_this_season())
    for matching in matching_list:
        MatchingLanguage.objects.filter(matching=matching).delete()
        matching_connections = MatchingConnection.objects.filter(
            korean_matching=matching)
        for item in matching_connections:
            item.foreign_matching.delete()
            item.delete()
        MatchingConnection.objects.filter(foreign_matching=matching).delete()
        matching.delete()
    

@login_required
@group_required('Korean')
def register(request):
    form = MatchingKoreanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        remove_prior_matching(request)

        matching = form.save(commit=False)
        matching.user = request.user
        matching.season = get_this_season()
        matching.save()

        languages = form.data.getlist('language[]')
        language_levels = form.data.getlist('language_level[]')
        for i in xrange(len(languages)):
            language = Language.objects.get(id=int(languages[i]))
            matching_language = MatchingLanguage.objects.create(
                matching=matching,
                language=language,
                level=int(language_levels[i])
            )

        return redirect(view, matching_id=matching.id)

    matching_exist = Matching.objects.filter(
        user=request.user,
        season=get_this_season()).count() > 0

    return render(request, 'matching/register.html', {
        'form': form,
        'exists': matching_exist
    })


@login_required
@reverse_group_required('Guest')
def view(request, matching_id):
    try:
        matching = Matching.objects.get(id=matching_id)
    except:
        return redirect(list)
    languages = MatchingLanguage.objects.filter(matching=matching)

    foreigners = []
    for item in MatchingConnection.objects.filter(korean_matching=matching):
        foreigners.append([
            item.foreign_matching,
            MatchingLanguage.objects.filter(matching=item.foreign_matching)
        ])

    return render(request, 'matching/view.html', {
        'matching': matching,
        'languages': languages,
        'foreigners': foreigners
    })


@login_required
@new_buddy_required
@group_required('Foreigner')
def register_foreigner(request, matching_id):
    try:
        korean_matching = Matching.objects.get(id=matching_id)
    except:
        return redirect(list)

    matching_count = MatchingConnection.objects.filter(
        korean_matching=korean_matching).count()
    matching_valid = (korean_matching.max_buddy_number > matching_count)
    if not matching_valid:
        return redirect(register_full)

    form = MatchingForeignerForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        remove_prior_matching(request)

        matching = form.save(commit=False)
        matching.user = request.user
        matching.season = get_this_season()
        matching.save()

        matching_connection = MatchingConnection.objects.create(
            korean_matching=korean_matching,
            foreign_matching=matching)

        languages = form.data.getlist('language[]')
        language_levels = form.data.getlist('language_level[]')
        for i in xrange(len(languages)):
            language = Language.objects.get(id=int(languages[i]))
            matching_language = MatchingLanguage.objects.create(
                matching=matching,
                language=language,
                level=int(language_levels[i])
            )

        return redirect(view, matching_id=matching_id)
        
    matching_exist = Matching.objects.filter(
        user=request.user,
        season=get_this_season()).count() > 0

    return render(request, 'matching/register_foreigner.html', {
        'matching': korean_matching,
        'form': form,
        'exists': matching_exist
    })


@login_required
@new_buddy_required
@group_required('Foreigner')
def register_full(request):
    return render(request, 'matching/register_full.html', {})


@login_required
def delete(request, matching_id):
    try:
        matching = Matching.objects.get(id=matching_id)
    except:
        return redirect(list)

    if request.user == matching.user:
        return render(request, 'matching/delete.html', {
            'matching': matching
        })

    return redirect(list)


@login_required
def delete_bye(request, matching_id):
    try:
        matching = Matching.objects.get(id=matching_id)
    except:
        return redirect(list)

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
