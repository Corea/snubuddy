# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden

from base.models import UserSeason, UserProfile
from base.queries import get_this_season
from base.decorators import guest_required, admin_required

from .models import ApplicationForeigner
from .forms import ApplicationForeignerForm

from matching.models import Matching

import StringIO
import xlsxwriter


@login_required
def index(request):
    user_season = UserSeason.objects.filter(
        user=request.user, season=get_this_season())
    if not user_season.exists():
        return redirect(register)
    return redirect(list)


@login_required
@admin_required
def list(request):
    season = get_this_season()

    application_infos = []
    application_list = ApplicationForeigner.objects.filter(
        season=season,
        is_removed=False).order_by('id')
    for application in application_list:
        matching = Matching.objects.filter(
            user=application.user,
            season=season)
        if matching.exists():
            matching = matching[0]
        application_infos.append([application, matching])

    return render(request, 'application/list.html', {
        'application_infos': application_infos
    })


@login_required
@admin_required
def download(request):
    season = get_this_season()
    applications = ApplicationForeigner.objects.filter(
        season=season, is_removed=False).order_by('id')
    xlsx = StringIO.StringIO()
    book = xlsxwriter.Workbook(xlsx)
    sheet = book.add_worksheet('Applications')

    header = [
        'First Name',
        'Last Name',
        'Full Name',
        'Gender',
        'Date of Birth', 
        'Country',
        'Korean Name',
        'SNU Member No.',
        'Facebook Name',
        'Facebook E-Mail',
        'Returning Buddy?',
        'Matching Done?'
    ]
    bold = book.add_format({'bold': True})
    col = 0
    for item in header:
        sheet.write(0, col, item, bold)
        col += 1
        
    row = 1
    for item in applications:
        user = item.user
        matching = Matching.objects.filter(user=user, season=season).exists()
        birth = ''
        try:
            birth = user.profile.birth.strftime('%Y/%m/%d')
        except:
            pass

        data = [
            user.first_name,
            user.last_name,
            user.first_name + ' ' + user.last_name,
            dict(UserProfile.GENDER_CHOICES)[user.profile.gender],
            birth,
            user.profile.country.name,
            user.profile.korean_name,
            item.snu_id,
            item.fb_name,
            item.fb_email,
            # item.created_on,
            'O' if item.returning else '',
            'O' if matching else '']
        col = 0
        for item in data:
            sheet.write(row, col, item)
            col += 1
        row += 1
    book.close()

    xlsx.seek(0)
    EXCEL_MIMETYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(xlsx.read(), content_type=EXCEL_MIMETYPE)
    response['Content-Disposition'] = "attachment; filename=applications.xlsx"

    return response


@login_required
@admin_required
def accept(request, application_id):
    application = ApplicationForeigner.objects.get(id=application_id)
    UserSeason.objects.create(
        user=application.user,
        season=application.season,
        user_type=UserSeason.FOREIGNER).save()
    return redirect(list)


@login_required
@guest_required
def register(request):
    form = ApplicationForeignerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        applications = ApplicationForeigner.objects.filter(
            user=request.user,
            season=get_this_season(),
            is_removed=False)
        for application in applications:
            application.is_removed = True
            application.save()
        application = form.save(commit=False)
        application.user = request.user
        application.season = get_this_season()
        application.save()
        return redirect(register_finish)

    application_exist = ApplicationForeigner.objects.filter(
        user=request.user,
        season=get_this_season(),
        is_removed=False).count() > 0

    return render(request, 'application/register.html', {
        'form': form,
        'exists': application_exist
    })


@login_required
@guest_required
def register_finish(request):
    return render(request, 'application/register_finish.html', {})
