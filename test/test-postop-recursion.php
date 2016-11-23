<?php
include "../src/php/GrammarTemplate.php";
function echo_($s='')
{
    echo $s . PHP_EOL;
}

echo_('GrammarTemplate.VERSION = ' . GrammarTemplate::VERSION);
echo_('GrammarTemplate POST-OP Mode');
echo_();

/*
    i.e: 
    foreach "expression:terms" as "term":
        foreach "term:factors" as "factor":
            ..
    
    here an :EXPR template is defined which itself uses (anonymous) sub-templates
    it is equivalent to (expand sub-templates to distinct):

<:FACTOR>:=[<lhs>[ <op>? <rhs|NULL>]]

<:TERM>:=[(<factor:FACTOR>[ AND <factor:FACTOR>*])]

<:EXPR>:=[<term:TERM>[ OR <term:TERM>*]]

<expression:EXPR>
<expression2:EXPR>

*/
$tpl = "<:EXPR>:=[<term>:=[(<factor>:=[<globalNegation:NEG><lhs>[ <op:OP>? <rhs|NULL>]][ AND <factor>*])][ OR <term>*]]<expression:EXPR>\n<expression2:EXPR>\n<foo:FOO>?<foo:FOO>\\?<foo:FOO> ?";

function op_func( $val )
{
    return '!=' === $val ? '<>' : $val;
}
function neg_func( $val )
{
    return $val ? 'NOT ' : '';
}
function foo_func( $val )
{
    return 'foo';
}
$expr = new GrammarTemplate($tpl, null, true/* post-op mode */);
GrammarTemplate::$fnGlobal['NEG'] = 'neg_func';
GrammarTemplate::$fnGlobal['FOO'] = 'foo_func';
$expr->fn['OP'] = 'op_func';

echo_("input template:");
echo_($tpl);

echo_( );

echo_("output:");
echo_($expr->render((object)array(
    'globalNegation'  => false,
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