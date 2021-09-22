from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.utils import timezone as datetime
from .models import Mpoint, Msections, Mvalue
import pandas as pd


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()


class MpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):
        form = CsvImportForm()
        data = {"form": form}
        if request.method != "POST":
            return render(request, "admin/csv_upload.html", data)

        csv_file = request.FILES["csv_upload"]
        if not csv_file.name.endswith('.csv'):
            messages.warning(request, 'Wrong file type, please upload csv files')
            return HttpResponseRedirect(request.path_info)
        point = csv_file.name[:-4]
        tmp = point.split('-')
        if len(tmp) != 2:
            messages.warning(request, 'Invalid filename, please use name like "DC4-6.csv"')
            return HttpResponseRedirect(request.path_info)
        section = tmp[0]
        sec_object, sec_created = Msections.objects.get_or_create(
            name=section
        )
        result_message = ''
        if sec_created:
            result_message += f'section {section} created;'
        else:
            result_message += f'section {section} existed;'

        point_obj = Mpoint.objects.filter(name=point).first()
        if point_obj:
            result_message += f'delete old point {point};'
            point_obj.delete()
        else:
            result_message += f'point {point} created;'
        point_obj = Mpoint.objects.create(name=point, section=sec_object)

        raw_content = pd.read_csv(csv_file, header=None)
        content = raw_content.dropna(axis=0, how='any')
        date = pd.to_datetime(content[0], errors='coerce')
        value = content[1].astype('float')
        handled_content = {
            'date': date,
            'value': value
        }
        df = pd.DataFrame(handled_content)
        count = 0
        v_objects = []
        for _, row in df.iterrows():
            date = datetime.make_aware(row['date'])
            value = row['value']
            v_objects.append(Mvalue(value=value, m_time=date, m_point=point_obj))
            count += 1
        Mvalue.objects.bulk_create(v_objects)
        result_message += f'{count} lines of values added to {point};'
        data['message'] = result_message
        return render(request, "admin/csv_upload.html", data)


class MsectionsAdmin(admin.ModelAdmin):
    list_display = ('name', )


class MvalueAdmin(admin.ModelAdmin):
    list_display = ('get_point', 'm_time', 'value', )
    ordering = ('m_point', 'm_time',)
    list_filter = ('m_point__name',)

    def get_point(self, obj):
        return obj.m_point.name
    get_point.short_description = 'm_point'
    get_point.admin_order_field = 'm_point__name'


admin.site.register(Mpoint, MpointAdmin)
admin.site.register(Msections, MsectionsAdmin)
admin.site.register(Mvalue, MvalueAdmin)
