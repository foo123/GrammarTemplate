var GrammarTemplate = require("../src/js/GrammarTemplate.js"), echo = console.log;

echo('GrammarTemplate.VERSION = ' + GrammarTemplate.VERSION);
echo( );

var tpl = "\\\\[var]\n\\[[var2]\\][[ \\[[var2]*\\]]][[# comment #]]\n[foo]\\?[foo] ?";

var grm = new GrammarTemplate( tpl, ['[',']','[[',']]'], true );
echo("input template:");
echo(tpl);

echo( );

echo("output:");
echo(grm.render({
    "foo"   : "foo",
    "var"   : "var",
    "var2"  : [
        "var1",
        "var2",
        "var3"
    ]
}));
