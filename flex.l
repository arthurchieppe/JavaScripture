%{
#include <string>
#include <stdio.h>
#include "node.h"
#include "parser.hpp"
#define SAVE_TOKEN yylval.string = new std::string(yytext, yyleng)
#define TOKEN(t) (yylval.token = t)
extern "C" int yywrap() { }
%}

%option noyywrap // do not wrap input to multiple calls of input()

%{
// declare global variables and functions here
%}

// Regular expressions for tokens
%{
[ \t]+          /* skip whitespace */
"=="            { return EQ_OP; }
">"             { return GT_OP; }
"<"             { return LT_OP; }
">="            { return GE_OP; }
"<="            { return LE_OP; }
"||"            { return OR_OP; }
"&&"            { return AND_OP; }
"!"             { return NOT_OP; }
"+"             { return ADD_OP; }
"-"             { return SUB_OP; }
"*"             { return MUL_OP; }
"/"             { return DIV_OP; }
"%"             { return MOD_OP; }
"("             { return LEFT_PAREN; }
")"             { return RIGHT_PAREN; }
"{"             { return LEFT_BRACE; }
"}"             { return RIGHT_BRACE; }
";"             { return SEMICOLON; }
","             { return COMMA; }
"."             { return DOT; }
":"             { return COLON; }
"?"             { return QUESTION_MARK; }
"="             { return ASSIGN_OP; }
"proclaim"      { return PRINT; }
"baptize"       { return DECLARE; }
"giveth"        { return ASSIGN; }
"prayAsLongAs"  { return WHILE_LOOP; }
"blessFor"      { return FOR_LOOP; }
"testify"       { return IF; }
"otherwise"     { return ELSE; }
"preach"        { return FUNCTION; }
"as"            { return AS; }
"number"        { return NUMBER; }
"string"        { return STRING; }
"boolean"       { return BOOLEAN; }
"true"          { yylval.booleanValue = 1; return BOOLEAN_VALUE; }
"false"         { yylval.booleanValue = 0; return BOOLEAN_VALUE; }
[0-9]+          { yylval.intValue = atoi(yytext); return INTEGER_VALUE; }
[a-zA-Z][a-zA-Z0-9_]* { yylval.identifier = strdup(yytext); return IDENTIFIER; }
"\""([^"])*"\"" { yylval.stringValue = strdup(yytext+1); yylval.stringValue[strlen(yytext)-2] = '\0'; return STRING_VALUE; }
.               { fprintf(stderr, "Error: Invalid character %c\n", *yytext); }

%}

%%

// Rules for handling tokens
%%
// handle special cases first
{INTEGER_VALUE} { yylval.intValue = atoi(yytext); return INTEGER_VALUE; }
{IDENTIFIER}    { yylval.identifier = strdup(yytext); return IDENTIFIER; }
{STRING_VALUE}  { yylval.stringValue = strdup(yytext+1); yylval.stringValue[strlen(yytext)-2] = '\0'; return STRING_VALUE; }
.               { fprintf(stderr, "Error: Invalid character %c\n", *yytext); }

// handle the remaining tokens
{EQ_OP}         { return EQ_OP; }
{GT_OP}         { return GT_OP; }
{LT_OP}         { return LT_OP; }
{GE_OP}         { return GE_OP; }
{LE_OP}         { return LE_OP; }
{OR_OP}         { return OR_OP; }
{AND_OP}        { return AND_OP; }
{NOT_OP}        { return NOT_OP
