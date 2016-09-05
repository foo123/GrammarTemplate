<?php
include "../src/php/GrammarTemplate.php";
function echo_($s='')
{
    echo $s . PHP_EOL;
}

echo_('GrammarTemplate.VERSION = ' . GrammarTemplate::VERSION);
echo_();

// foreach expression as term: foreach term as factor: ..
$tpl = "<:expression_tpl>:=[<term>:=[(<factor>:=[<lhs>[ <?op> <rhs|NULL>]][ AND <*factor>])][ OR <*term>]]<expression:expression_tpl>\n<expression2:expression_tpl>";

$expr = new GrammarTemplate($tpl);

echo_("input template:");
echo_($tpl);

echo_( );

echo_("output:");
echo_($expr->render(array(
    'expression'  => array(
        // term
        array(
            // factor
            array('lhs'=> 1, 'op'=> '=', 'rhs'=> 1),
            // factor
            array('lhs'=> 1, 'op'=> '=', 'rhs'=> 2),
            // factor
            array('lhs'=> 1, 'op'=> '=', 'rhs'=> 3)
        ),
        // term
        array(
            // factor
            array('lhs'=> 1, 'op'=> '<', 'rhs'=> 1),
            // factor
            array('lhs'=> 1, 'op'=> '<', 'rhs'=> 2),
            // factor
            array('lhs'=> 1, 'op'=> '<', 'rhs'=> 3)
        ),
        // term
        array(
            // factor
            array('lhs'=> 1, 'op'=> '>', 'rhs'=> 1),
            // factor
            array('lhs'=> 1, 'op'=> '>', 'rhs'=> 2),
            // factor
            array('lhs'=> 1, 'op'=> '>', 'rhs'=> 3)
        )
    ),
    'expression2'  => array(
        // term
        array(
            // factor
            array('lhs'=> 2, 'op'=> '=', 'rhs'=> 1),
            // factor
            array('lhs'=> 2, 'op'=> '=', 'rhs'=> 2),
            // factor
            array('lhs'=> 2, 'op'=> '=', 'rhs'=> 3)
        ),
        // term
        array(
            // factor
            array('lhs'=> 2, 'op'=> '<', 'rhs'=> 1),
            // factor
            array('lhs'=> 2, 'op'=> '<', 'rhs'=> 2),
            // factor
            array('lhs'=> 2, 'op'=> '<', 'rhs'=> 3)
        ),
        // term
        array(
            // factor
            array('lhs'=> 2, 'op'=> '>', 'rhs'=> 1),
            // factor
            array('lhs'=> 2, 'op'=> '>', 'rhs'=> 2),
            // factor
            array('lhs'=> 2, 'op'=> '>', 'rhs'=> 3)
        ),
        // term
        array(
            // factor
            array('lhs'=> 3),
            // factor
            array('lhs'=> 3, 'op'=> '!=')
        )
    )
)));