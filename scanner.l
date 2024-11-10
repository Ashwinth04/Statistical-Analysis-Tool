%{
#include <stdio.h>
#include <stdlib.h>
#include "parser.tab.h"
%}

%%

[0-9]+              { yylval.num = atoi(yytext); return NUMBER; }
\"[^\"]*\"          { yylval.str = strdup(yytext); return STRING_LITERAL; }
"import"            { return IMPORT; }
"preprocess"        { return PREPROCESS; }
"visualize"         { return VISUALIZE; }
"model"             { return MODEL; }
"export"            { return EXPORT; }
"setfile"           { return SETFILE; }
"split"             { return SPLIT; }
"summarize"         { return SUMMARIZE; }
"auto_model"        { return AUTO_MODEL; }
"kernel"            { return KERNEL; }
"x"                 { return X; }
"y"                 { return Y; }
"C"                 { return C; }
"gamma"             { return GAMMA; }
"train_size"        { return TRAIN_SIZE; }
"method"            { return METHOD; }
"target"            { return TARGET; }
"save_model"        { return SAVE_MODEL; }
"eval"              { return EVAL; }
"="                 { return '='; }

[ \t\n]+            /* Ignore whitespace */
.                   { return yytext[0]; }

%%

int yywrap(void) {
    return 1;
}
