set nocompatible
filetype plugin indent on

" Automatically load the doxygen syntax extensions
:let g:load_doxygen_syntax=1

set nu
" show line numbers relative to current line
set relativenumber

set cursorline
set wildmenu

" fix colour in tmux
let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"
let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"

" solarized stuff
syntax enable
set termguicolors
set background=light
colorscheme solarized8

" show existing tab with 4 spaces width
set tabstop=4
" when indenting with '>', use 4 spaces width
set shiftwidth=4
" On pressing tab, insert 4 spaces
set expandtab
" show vertical line at column 80
set colorcolumn=80
" search in all subfolders for files
set path+=**
" scroll before hitting bottom of window
set scrolloff=5

let mapleader=","

" word count on selection
xnoremap <leader>w <esc>:'<,'>:w !wc -w<CR>

let g:dart_trailing_comma_indent = v:true

set foldmethod=syntax
" only fold extremely deep folds automatically
set foldlevelstart=10

" Enable spell checking for syntax files which check the spelling in comments,
" and other plain text files
set spelllang=en_gb
autocmd FileType c setlocal spell
autocmd FileType markdown setlocal spell
autocmd FileType vimwiki setlocal spell

set listchars=tab:>·,trail:·,extends:>,precedes:<
set list

" Show the status line always
set laststatus=2

" Persistent undo
set undodir=~/.vim/undo-dir
set undofile

" Turn off vimwiki for files outside of the wiki directory
let g:vimwiki_global_ext = 0 

" Do not automatically insert newline at end of file
:set nofixendofline

if executable("rg")
    set grepprg=rg\ --vimgrep\ --no-heading
    set grepformat=%f:%l:%c:%m,%f:%l:%m
endif

packadd! matchit
# match_words for verilog
let b:match_words = '\<begin\>:\<end\>,\<module\>:\<endmodule\>,\<case\>:\<endcase\>'
