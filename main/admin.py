from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from .models import Mpoint, Msections, Mvalue


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class MpointAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")

            for x in csv_data:
                fields = x.split(",")
                
            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_upload.html", data)

admin.site.register(Mpoint, MpointAdmin)
admin.site.register(Msections)
admin.site.register(Mvalue)
