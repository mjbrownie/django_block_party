setlocal modifiable
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
