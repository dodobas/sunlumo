# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import json

from django.views.generic import TemplateView

from sunlumo_mapserver.project import SunlumoProject


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        project = SunlumoProject('/data/simple.qgs')

        context['SL_Details'] = json.dumps(project.getDetails())

        return context
