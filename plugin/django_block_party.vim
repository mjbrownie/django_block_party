"Block view test Client {{{1
""TODO django settings module is hardcoded!
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
import os
warnings.filterwarnings('ignore')

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    from django.conf import settings
    from django.template.loader import get_template
    import vim

    try:
        vim.command ('let g:django_block_party_directory = "%s"' % settings.BLOCK_PARTY_ROOT )
    except:
        vim.command ('let g:django_block_party_directory = "%s"' % '/tmp/')

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
    exec "Explore " . g:django_block_party_directory .  "/.dbp/"
endfun

command DBPOpen call DBP_template_view()
