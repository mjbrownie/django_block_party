"Block view test Client {{{1
python << EOP
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

#   except:
#       vim.command("echo 'Failed to GET Response'")
#       return

    try:
        #vim.command(vim.eval('g:split_command'))
        vim.command('vert aboveleft 60 split ')
        vim.command('enew')
        vim.current.buffer.append(r.content.split('\n'))
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

    except:
        vim.command("echo 'Failed to append vim'")
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


