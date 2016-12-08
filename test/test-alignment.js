var GrammarTemplate = require("../src/js/GrammarTemplate.js"), echo = console.log;

echo('GrammarTemplate.VERSION = ' + GrammarTemplate.VERSION);
echo( );

var tpl = "<:BLOCK>:=[BLOCK <.name>\n{\n[    <@.blocks:BLOCKS>?\n]}]<:BLOCKS>:=[<@block:BLOCK>[\n<@block:BLOCK>*]]<@blocks:BLOCKS>";

var aligned = new GrammarTemplate( tpl, null, true );

echo("input template:");
echo(tpl);

echo( );

echo("output:");
echo(aligned.render({
    blocks      : [
    {
        name        : "block1",
        blocks      : null
    },
    {
        name        : "block2",
        blocks      : [
            {
                name   : "block21",
                blocks : [
                    {
                        name   : "block211",
                        blocks : [
                            {
                                name   : "block2111",
                                blocks : null
                            },
                            {
                                name   : "block2112"
                            }
                        ]
                    },
                    {
                        name   : "block212"
                    }
                ]
            },
            {
                name   : "block22",
                blocks : [
                    {
                        name   : "block221"
                    },
                    {
                        name   : "block222"
                    }
                ]
            }
        ]
    },
    {
        name        : "block3"
    }
]
}));
