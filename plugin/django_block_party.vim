"Block view test Client {{{1
python << EOP
#import warnings
#
#def fxn():
#warnings.warn("deprecated", DeprecationWarning)
#
#with warnings.catch_warnings():
#warnings.simplefilter("ignore")
#fxn()

import warnings
warnings.filterwarnings('ignore')
from django.core.management import setup_environ
import settings
setup_environ(settings)

import vim

try:
    vim.command ('let g:django_block_party_directory = "%s"' % settings.BLOCK_PARTY_ROOT )
except:
    vim.command ('let g:django_block_party_directory = "%s"' % settings.MEDIA_ROOT )


EOP
fun! DBP_find_block()

    set iskeyword=@,48-57,_,192-255,-

    if getline(".") =~ '^Template \(.*\) {{{bp1'
        exec 'norm! 0W'
        let file = expand('<cfile>')
        exec "wincmd l|find " . file
    else
        call  search('^\s\+block: \([0-9A-Za-z_-]\+\)$',"bpc")
        exec "norm! WW"
        let block = expand('<cword>')
        call search('^Template \(.*\) {{{bp1','bp')
        exec 'norm! 0W'
        let file = expand('<cfile>')
        exec "wincmd l|find " . file
        call search ('block \<' . block . '\>')
    endif
endfun

"com! -nargs=1 DBlock  python django_block_view(<f-args>)

fun DBP_template_view()
    tabnew
    vert aboveleft 60 split
    exec "edit " . g:django_block_party_directory .  "/.dbp.template_view"
    set nowrap
    set fileencoding=utf-8
    setlocal  ft=html
    setlocal  foldmethod=marker
    setlocal foldmarker={{{bp,bp}}}
    setlocal foldlevel=0
    syn match Ignore /{{{bp\d*/
    syn match Ignore /bp}}}/
    syn match Special /block:/
    try
        silent %s/\s\+$//
        silent g/^$/d
    finally
    endtry
    norm gg
    set buftype=nofile
    setlocal nomodifiable
    nnoremap <buffer> <cr> :call DBP_find_block()<cr>
    nnoremap <buffer> <mouse> :call DBP_find_block()<cr>
endfun

command DBPOpen call DBP_template_view()
