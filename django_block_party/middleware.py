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

def new_template_init(self, template_string, origin=None, name='<Unknown Template>'):
    old_template_init(self, template_string, origin, name)
    self.origin = origin
Template.__init__ = new_template_init

from django.http import HttpResponse

class VimMiddleware(object):


    vimrequest = False


    def __init__(self):
        try:
            import vim
            self.processors = []
            self.processors.append(TemplateProcessor())
            self.vimrequest = True

        except ImportError:
            #todo in temp for ipython
            self.processors = []
            self.processors.append(TemplateProcessor())
            return None

    def process_request(self,request):
        pass

    def process_response(self, request, response):
        if self.vimrequest:
            result = [p.content() for p in self.processors]
            return response
        else:
            return response


from django.template.loader_tags import BlockNode,IncludeNode


class Processor(object):

    def process_request(self, request):
        pass

    def process_response(self,request,response):
        pass

class TemplateProcessor(Processor):

    def __init__(self):
        self.templates = []
        template_rendered.connect(self._storeTemplateInfo)

    def _storeTemplateInfo(self, sender, **kwargs):
        self.templates.append(kwargs)

    def content(self):
        #return "\n".join(t['template'].name for t in self.templates if 'template' in t)
        c = ""
        rendered_blocks = []

        for t in self.templates:
            c += (u"\nTemplate %s {{{bp1" % t['template'].name)
            #if 'context' in t:
            #   for k in t['context']:
            #       c += ("\n    v: %s" % k)
                    #c += ("        %s" % t['context'][k] )

            c += u"\n    Blocks:"
            for n in t['template'].nodelist.get_nodes_by_type((BlockNode,IncludeNode)):
                c+= (u"\n        block: %s" % str(n.name))
                try:
                    c+= (u"\n        template_name: %s" % str(n.template_name))
                except:
                    pass
                try:
                    ren = n.render(t['context'])
                    if not unicode( ren ) == u"" and not n.name in rendered_blocks:
                        rendered_blocks.append(n.name)
                        c+= u"\n             render: {{{bp"
                        c+= (u"\n            %s" % ren.replace(u"\n",u"\n            "))
                        c+= u"\n             bp}}}"
                except:
                    c+= (u"\n            (Context Render Failed)")

            for n in t['template'].nodelist.get_nodes_by_type(IncludeNode):
                c+= (u"\n    include: %s" % (str(n.name) ))

        import vim
        vim.command("tabnew")
        vim.command('vert aboveleft 60 split ')
        vim.command('enew')
        vim.command("set nowrap")
        #vim.command("set fileencoding=utf-8")
        vim.current.buffer.append(str(c).split('\n'))
        vim.command('setlocal  ft=html')
        vim.command("setlocal  foldmethod=marker")
        vim.command("setlocal foldmarker={{{bp,bp}}}")
        vim.command("setlocal foldlevel=0")
        vim.command('syn match Ignore /{{{bp\d*/')
        vim.command('syn match Ignore /bp}}}/')
        vim.command('syn match Special /block:/')
        try:
            vim.command('silent %s/\s\+$//')
            vim.command('silent g/^$/d')
        except:
            pass
        vim.command('norm gg')
        vim.command('set buftype=nofile')
        vim.command("setlocal nomodifiable")
        vim.command('nnoremap <buffer> <cr> :call DBP_find_block()<cr>')
        vim.command('nnoremap <buffer> <mouse> :call DBP_find_block()<cr>')

        return ""
        #return "\n".join(str(t) for t in self.templates if 'template' in t)
