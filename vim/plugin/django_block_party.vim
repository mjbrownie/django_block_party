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

def django_block_view(url, post=None, strip_tags=False):
    

    from django.core.management import setup_environ
    import settings
    setup_environ(settings)

    import vim
    from django.test.client import Client

    if not 'django_block_party.middleware.VimMiddleware' in settings.MIDDLEWARE_CLASSES:
        print "Django Block Party needs django_block_party.middleware.VimMiddleware to work"
        return ''

    c = Client()

    if not post:
        r = c.get(url)
    else:
        r = c.post(url, data=post)

    return ''
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

com! -nargs=1 DBlock  python django_block_view(<f-args>)


