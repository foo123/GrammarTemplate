<?php
include "../src/php/GrammarTemplate.php";
function echo_($s='')
{
    echo $s . PHP_EOL;
}

echo_('GrammarTemplate.VERSION = ' . GrammarTemplate::VERSION);
echo_();

/*
    i.e: 
    foreach "expression:terms" as "term":
        foreach "term:factors" as "factor":
            ..
    
    here an :EXPR template is defined which itself uses (anonymous) sub-templates
    it is equivalent to (expand sub-templates to distinct):

<:FACTOR>:=[<lhs>[ <?op> <rhs|NULL>]]

<:TERM>:=[(<factor:FACTOR>[ AND <*factor:FACTOR>])]

<:EXPR>:=[<term:TERM>[ OR <*term:TERM>]]

<expression:EXPR>
<expression2:EXPR>

*/
$tpl = "<:EXPR>:=[<term>:=[(<factor>:=[[<?globalNegation|>NOT ]<lhs>[ <?op> <rhs|NULL>]][ AND <*factor>])][ OR <*term>]]<expression:EXPR>\n<expression2:EXPR>";

$expr = new GrammarTemplate($tpl);

echo_("input template:");
echo_($tpl);

echo_( );

echo_("output:");
echo_($expr->render((object)array(
    'globalNegation'  => true,
    'expression'  => array(
        // term
        array(
            // factor
            (object)array('lhs'=> 1, 'op'=> '=', 'rhs'=> 1),
            // factor
            (object)array('lhs'=> 1, 'op'=> '=', 'rhs'=> 2),
            // factor
            (object)array('lhs'=> 1, 'op'=> '=', 'rhs'=> 3)
        ),
        // term
        array(
            // factor
            (object)array('lhs'=> 1, 'op'=> '<', 'rhs'=> 1),
            // factor
            (object)array('lhs'=> 1, 'op'=> '<', 'rhs'=> 2),
            // factor
            (object)array('lhs'=> 1, 'op'=> '<', 'rhs'=> 3)
        ),
        // term
        array(
            // factor
            (object)array('lhs'=> 1, 'op'=> '>', 'rhs'=> 1),
            // factor
            (object)array('lhs'=> 1, 'op'=> '>', 'rhs'=> 2),
            // factor
            (object)array('lhs'=> 1, 'op'=> '>', 'rhs'=> 3)
        )
    ),
    'expression2'  => array(
        // term
        array(
            // factor
            (object)array('lhs'=> 2, 'op'=> '=', 'rhs'=> 1),
            // factor
            (object)array('lhs'=> 2, 'op'=> '=', 'rhs'=> 2),
            // factor
            (object)array('lhs'=> 2, 'op'=> '=', 'rhs'=> 3)
        ),
        // term
        array(
            // factor
            (object)array('lhs'=> 2, 'op'=> '<', 'rhs'=> 1),
            // factor
            (object)array('lhs'=> 2, 'op'=> '<', 'rhs'=> 2),
            // factor
            (object)array('lhs'=> 2, 'op'=> '<', 'rhs'=> 3)
        ),
        // term
        array(
            // factor
            (object)array('lhs'=> 2, 'op'=> '>', 'rhs'=> 1),
            // factor
            (object)array('lhs'=> 2, 'op'=> '>', 'rhs'=> 2),
            // factor
            (object)array('lhs'=> 2, 'op'=> '>', 'rhs'=> 3)
        ),
        // term
        array(
            // factor
            (object)array('lhs'=> 3),
            // factor
            (object)array('lhs'=> 3, 'op'=> '!=')
        )
    )
)));