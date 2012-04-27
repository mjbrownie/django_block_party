from os.path import normpath
from pprint import pformat

from django.conf import settings
from django.core.signals import request_started
from django.dispatch import Signal
from django.template.context import get_standard_processors
from django.template.loader import render_to_string
from django.test.signals import template_rendered
from debug_toolbar.panels import DebugPanel

# Monkeypatch instrumented test renderer from django.test.utils - we could use
# django.test.utils.setup_test_environment for this but that would also set up
# e-mail interception, which we don't want
from django.test.utils import instrumented_test_render
from django.template import Template
if Template.render != instrumented_test_render:
    Template.original_render = Template.render
    Template.render = instrumented_test_render
# MONSTER monkey-patch
old_template_init = Template.__init__


def new_template_init(self, template_string, origin=None,
        name='<Unknown Template>'):
    old_template_init(self, template_string, origin, name)
    self.origin = origin
Template.__init__ = new_template_init

from django.http import HttpResponse

try:
    DBP_PATH = settings.BLOCK_PARTY_ROOT
except:
    DBP_PATH = settings.MEDIA_ROOT


class VimMiddleware(object):

    internal_request = True

    def __init__(self):
        self.processors = []
        self.processors.append(TemplateProcessor())
        self.vimrequest = True

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        if (request.META['REMOTE_ADDR'] in settings.INTERNAL_IPS
                and settings.DEBUG and not request.is_ajax()):
            result = [p.content() for p in self.processors]
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

    def content(self):
        #return "\n".join(t['template'].name for t in
        #self.templates if 'template' in t)
        fp = open('%s/.dbp.template_view' % DBP_PATH, 'w')
        rendered_blocks = []

        temps = []

        for t in self.templates:

            if not t['template'].name in temps:
                temps.append(t['template'].name)

                fp.write(u"\nTemplate %s {{{bp1" % t['template'].name)
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

        fp.close()
