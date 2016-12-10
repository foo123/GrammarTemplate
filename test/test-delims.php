<?php
include "../src/php/GrammarTemplate.php";
function echo_($s='')
{
    echo $s . PHP_EOL;
}

echo_('GrammarTemplate.VERSION = ' . GrammarTemplate::VERSION);
echo_();

$tpl = "\\\\[var]\n\\[[var2]\\][[ \\[[var2]*\\]]][[# comment #]]\n[foo]\\?[foo] ?";

$grm = new GrammarTemplate($tpl, array('[',']','[[',']]'), true);

echo_("input template:");
echo_($tpl);

echo_( );

echo_("output:");
echo_($grm->render((object)array(
    "foo"   => "foo",
    "var"   => "var",
    "var2"  => array(
        "var1",
        "var2",
        "var3"
    )
)));