from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django import forms
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages import admin as flatpages_admin
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_protect

from tinymce.widgets import TinyMCE
from flatpages_tinymce import settings


class FlatPageAdmin(flatpages_admin.FlatPageAdmin):
    # @csrf_protect
    def __init__(self, *args, **kwargs):
        super(FlatPageAdmin, self).__init__(*args, **kwargs)
        self.ajax_save = csrf_protect(
            permission_required('flatpages.change_flatpage')(self._ajax_save)
        )

    @transaction.atomic
    def _ajax_save(self, request):
        try:
            page_id = int(request.REQUEST.get("id", 0))
        except ValueError:
            page_id = 0

        page = get_object_or_404(FlatPage, id=page_id)
        page_content = request.REQUEST.get("content", "").strip()
        if not page_content:
            raise Http404()
        page.content = page_content
        page.save()
        return HttpResponse(page.content)

    def get_urls(self):
        return patterns(
            '',
            url(r'^ajax-save/$', self.admin_site.admin_view(self.ajax_save),
                name='flatpages_ajax_save'),
        ) + super(FlatPageAdmin, self).get_urls()

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            if settings.USE_ADMIN_AREA_TINYMCE:
                return db_field.formfield(widget=TinyMCE(
                    attrs={'cols': 80, 'rows': 30},
                    mce_attrs={'external_link_list_url': reverse(
                        'tinymce.views.flatpages_link_list')},
                ))
        elif db_field.name == "template_name" and settings.USE_TEMPLATE_DROPDOWN:
            prev_field = super(FlatPageAdmin, self).formfield_for_dbfield(
                db_field, **kwargs
            )
            return forms.FilePathField(
                label=prev_field.label,
                path=settings.TEMPLATE_DIR,
                required=False,
                recursive=False,
                match=settings.TEMPLATE_FILES_REGEXP,
            )
        return super(FlatPageAdmin, self).formfield_for_dbfield(db_field,
                                                                **kwargs)

    # redefining
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'),
         {'classes': ('collapse',), 'fields': ('enable_comments',
                                               'registration_required',
                                               'template_name')}),
    )


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
