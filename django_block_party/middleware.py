from os.path import normpath
import os
from pprint import pformat

import django
from django.conf import settings
from django.core.signals import request_started
from django.dispatch import Signal
from django.template.loader import render_to_string
from django.test.signals import template_rendered
from debug_toolbar.panels import DebugPanel

from django.http import HttpResponse

try:
    DBP_PATH = settings.BLOCK_PARTY_ROOT
except:
    DBP_PATH = '/tmp/.dbp'

import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

class VimMiddleware(object):

    internal_request = True

    def __init__(self):
        self.processor = TemplateProcessor()
        self.vimrequest = True

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        if (request.META['REMOTE_ADDR'] in settings.INTERNAL_IPS
                and settings.DEBUG and not request.is_ajax()):

            mkdir_p(DBP_PATH)
            fp = open('%s/%s.dbparty' % (
                DBP_PATH, request.path.replace('/','-')), 'w')
            fp.write("Request.path: %s \n\n" % request.path)
            result = self.processor.content(fp)
            fp.close()
            return response
        else:
            return response


from django.template.loader_tags import BlockNode, IncludeNode


class Processor(object):

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass


class TemplateProcessor(Processor):

    def __init__(self):
        self.templates = []
        template_rendered.connect(self._storeTemplateInfo)

    def _storeTemplateInfo(self, sender, **kwargs):
        self.templates.append(kwargs)

    def content(self,fp):
        #return "\n".join(t['template'].name for t in
        #self.templates if 'template' in t)
        rendered_blocks = []

        temps = []

        for t in self.templates:

            if not t['template'].name in temps:
                temps.append(t['template'].name)

                fp.write(u"\nTemplate %s {{{bp1" % t['template'].origin)
                fp.write(u"\n    Path  %s {{{bp1" % t['template'].name)
                #if 'context' in t:
                #   for k in t['context']:
                #       c += ("\n    v: %s" % k)
                        #c += ("        %s" % t['context'][k] )

                fp.write(u"\n    Blocks:")
                #for n in t['template'].nodelist.get_nodes_by_type(
                # (BlockNode,IncludeNode)):
                for n in t['template'].nodelist.get_nodes_by_type((BlockNode)):
                    if isinstance(n, IncludeNode):
                        pass
                    else:
                        fp.write(u"\n        block: %s" % str(n.name))
                        try:
                            fp.write(u"\n        template_name: %s" %
                                    str(n.template_name))
                        except:
                            pass
                        try:
                            ren = n.render(t['context'])
                            if not unicode(ren) == u"" \
                                    and not n.name in rendered_blocks:
                                rendered_blocks.append(n.name)
                                fp.write(u"\n             render: {{{bp")
                                fp.write(u"\n            %s" % \
                                        ren.replace(u"\n", u"\n            "))
                                fp.write(u"\n             bp}}}")
                        except:
                            fp.write(u"\n            (Context Render Failed)")

