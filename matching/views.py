# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from base.queries import get_this_season
from base.decorators import (
    korean_required, authorize_required,
    new_buddy_required, foreigner_required)
from base.models import Language

from matching.models import Matching, MatchingLanguage, MatchingConnection
from matching.forms import MatchingKoreanForm, MatchingForeignerForm

from base import queries as base_queries
from matching import queries as matching_queries


@login_required
@authorize_required
def list(request):
    sort_ftn = lambda x: (matching_queries.count_matched_buddies(x) /
                          x.max_buddy_number)
    matching_list = matching_queries.get_korean_matching_list()
    matching_list = sorted(matching_list, key=sort_ftn)

    return render(request, 'matching/list.html', {
        'matching_list': matching_list
    })


@login_required
@korean_required
def register(request):
    return redirect(list)
    form = MatchingKoreanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        matching_queries.delete_matching_by_user(request.user)

        matching = form.save(commit=False)
        matching.user = request.user
        matching.season = get_this_season()
        matching.save()

        languages = map(int, form.data.getlist('language[]'))
        language_levels = map(int, form.data.getlist('language_level[]'))
        for i in xrange(len(languages)):
            language = base_queries.get_language(languages[i])
            matching_language = MatchingLanguage.objects.create(
                matching=matching,
                language=language,
                level=language_levels[i])

        return redirect(view, id=matching.id)

    matching_exist = matching_queries.has_matching(request.user)

    return render(request, 'matching/register.html', {
        'form': form,
        'exists': matching_exist
    })


@login_required
@authorize_required
def view(request, id):
    matching = get_object_or_404(Matching, id=id)

    languages = MatchingLanguage.objects.filter(matching=matching)
    foreigners = [[x, MatchingLanguage.objects.filter(matching=x)]
                  for x in matching_queries.get_personal_buddies(matching)]

    return render(request, 'matching/view.html', {
        'matching': matching,
        'languages': languages,
        'foreigners': foreigners
    })


@korean_required
@login_required
@new_buddy_required
@foreigner_required
def register_foreigner(request, id):
    korean_matching = get_object_or_404(Matching, id=id)

    matching_count = MatchingConnection.objects.filter(
        korean_matching=korean_matching).count()
    matching_valid = (korean_matching.max_buddy_number > matching_count)
    if not matching_valid:
        return redirect(register_full)

    form = MatchingForeignerForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        matching_queries.delete_matching_by_user(request.user)

        matching = form.save(commit=False)
        matching.user = request.user
        matching.season = get_this_season()
        matching.save()

        matching_connection = MatchingConnection.objects.create(
            korean_matching=korean_matching,
            foreign_matching=matching)

        languages = map(int, form.data.getlist('language[]'))
        language_levels = map(int, form.data.getlist('language_level[]'))
        for i in xrange(len(languages)):
            language = base_queries.get_language(languages[i])
            matching_language = MatchingLanguage.objects.create(
                matching=matching,
                language=language,
                level=language_levels[i])

        return redirect(view, id=id)

    matching_exist = matching_queries.has_matching(request.user)

    return render(request, 'matching/register_foreigner.html', {
        'matching': korean_matching,
        'form': form,
        'exists': matching_exist
    })


@korean_required
@login_required
@new_buddy_required
@foreigner_required
def register_full(request):
    return render(request, 'matching/register_full.html', {})


@korean_required
@foreigner_required
@login_required
def delete(request, id):
    matching = get_object_or_404(Matching, id=id)
    if request.user == matching.user:
        return render(request, 'matching/delete.html', {
            'matching': matching
        })

    return redirect(list)


@korean_required
@foreigner_required
@login_required
def delete_bye(request, id):
    matching = get_object_or_404(Matching, id=id)
    if request.user == matching.user:
        matching_queries.delete_matching(matching)

    return redirect(list)
