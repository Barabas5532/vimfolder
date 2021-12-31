set nocompatible              " required for Vundle
filetype off                  " required for Vundle

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" Keep Plugin commands between vundle#begin/end.
Plugin 'tpope/vim-fugitive'
Plugin 'lifepillar/vim-solarized8'
Plugin 'ycm-core/YouCompleteMe'
Plugin 'vhdirk/vim-cmake'
Plugin 'gmoe/vim-faust'
Plugin 'vimwiki/vimwiki'
Plugin 'vimsence/vimsence'
Plugin 'dart-lang/dart-vim-plugin'

" All of your Plugins must be added before the following line
call vundle#end()            " required for Vundle
filetype plugin indent on    " required for Vundle

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

" hide ycm live compilation warnings
" let g:ycm_show_diagnostics_ui = 0
" don't do automatic #include header 
let g:ycm_clangd_args = [ '--header-insertion=never' ]
let g:ycm_global_ycm_extra_conf = '~/.vim/.ycm_extra_conf.py'
"jump to definition
nnoremap <leader>d :YcmCompleter GoToDefinition<CR>

"autoformat with clang-format 
"https://clang.llvm.org/docs/ClangFormat.html
noremap <leader>f :py3file /usr/share/clang/clang-format.py<cr>

"format the whole file at once
:function FormatFile()
:  let l:lines="all"
:  py3f /usr/share/clang/clang-format.py
:endfunction

noremap <leader>r :call FormatFile()<cr>

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
