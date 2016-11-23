var GrammarTemplate = require("../src/js/GrammarTemplate.js"), echo = console.log;

echo('GrammarTemplate.VERSION = ' + GrammarTemplate.VERSION);
echo('GrammarTemplate POST-OP Mode');
echo( );

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
var tpl = "<:EXPR>:=[<term>:=[(<factor>:=[<globalNegation:NEG><lhs>[ <op:OP>? <rhs|NULL>]][ AND <factor>*])][ OR <term>*]]<expression:EXPR>\n<expression2:EXPR>\n<foo:FOO>?<foo:FOO>\\?<foo:FOO> ?";

var expr = new GrammarTemplate( tpl, null, true/* post-op mode */ );
GrammarTemplate.fnGlobal['NEG'] = function( val ) {
    return val ? 'NOT ' : '';
};
GrammarTemplate.fnGlobal['FOO'] = function( val ) {
    return 'foo';
};
expr.fn['OP'] = function( val ) {
    return '!=' === val ? '<>' : val;
};
echo("input template:");
echo(tpl);

echo( );

echo("output:");
echo(expr.render({
    globalNegation: false,
    expression  : [
        // term
        [
            // factor
            {lhs: 1, op: '=', rhs: 1},
            // factor
            {lhs: 1, op: '=', rhs: 2},
            // factor
            {lhs: 1, op: '=', rhs: 3}
        ],
        // term
        [
            // factor
            {lhs: 1, op: '<', rhs: 1},
            // factor
            {lhs: 1, op: '<', rhs: 2},
            // factor
            {lhs: 1, op: '<', rhs: 3}
        ],
        // term
        [
            // factor
            {lhs: 1, op: '>', rhs: 1},
            // factor
            {lhs: 1, op: '>', rhs: 2},
            // factor
            {lhs: 1, op: '>', rhs: 3}
        ]
    ],
    expression2  : [
        // term
        [
            // factor
            {lhs: 2, op: '=', rhs: 1},
            // factor
            {lhs: 2, op: '=', rhs: 2},
            // factor
            {lhs: 2, op: '=', rhs: 3}
        ],
        // term
        [
            // factor
            {lhs: 2, op: '<', rhs: 1},
            // factor
            {lhs: 2, op: '<', rhs: 2},
            // factor
            {lhs: 2, op: '<', rhs: 3}
        ],
        // term
        [
            // factor
            {lhs: 2, op: '>', rhs: 1},
            // factor
            {lhs: 2, op: '>', rhs: 2},
            // factor
            {lhs: 2, op: '>', rhs: 3}
        ],
        // term
        [
            // factor
            {lhs: 3},
            // factor
            {lhs: 3, op: '!='}
        ]
    ]
}));
