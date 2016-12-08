<?php
include "../src/php/GrammarTemplate.php";
function echo_($s='')
{
    echo $s . PHP_EOL;
}

echo_('GrammarTemplate.VERSION = ' . GrammarTemplate::VERSION);
echo_();

$tpl = "<:BLOCK>:=[BLOCK <.name>\n{\n[    <@.blocks:BLOCKS>?\n]}]<:BLOCKS>:=[<@block:BLOCK>[\n<@block:BLOCK>*]]<@blocks:BLOCKS>";

$aligned = new GrammarTemplate($tpl, null, true);

echo_("input template:");
echo_($tpl);

echo_( );

echo_("output:");
echo_($aligned->render((object)array(
    'blocks'      => array(
    array(
        'name'        => "block1",
        'blocks'      => null
    ),
    array(
        'name'        => "block2",
        'blocks'      => array(
            array(
                'name'   => "block21",
                'blocks' => array(
                    array(
                        'name'   => "block211",
                        'blocks' => array(
                            array(
                                'name'   => "block2111",
                                'blocks' => null
                            ),
                            array(
                                'name'   => "block2112"
                            )
                        )
                    ),
                    array(
                        'name'   => "block212"
                    )
                )
            ),
            array(
                'name'   => "block22",
                'blocks' => array(
                    array(
                        'name'   => "block221"
                    ),
                    array(
                        'name'   => "block222"
                    )
                )
            )
        )
    ),
    array(
        'name'        => "block3"
    )
)
)));