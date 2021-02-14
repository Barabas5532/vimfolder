if exists("c_no_cformat")
  syn region    cString     start=+L\="+ skip=+\\\\\|\\"+ end=+"+ contains=cSpecial
else
  syn region    cString     start=+L\="+ skip=+\\\\\|\\"+ end=+"+ contains=cSpecial,cFormat
endif

if !exists("c_no_c11") " ISO C11
  if exists("c_no_cformat")
    syn region  cString     start=+\%(U\|u8\=\)"+ skip=+\\\\\|\\"+ end=+"+ contains=cSpecial
  else
    syn region  cString     start=+\%(U\|u8\=\)"+ skip=+\\\\\|\\"+ end=+"+ contains=cSpecial,cFormat
  endif
endif
