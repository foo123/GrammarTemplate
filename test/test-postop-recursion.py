#!/usr/bin/env python

import os, sys
import pprint

def import_module(name, path):
    import imp
    try:
        mod_fp, mod_path, mod_desc  = imp.find_module(name, [path])
        mod = getattr( imp.load_module(name, mod_fp, mod_path, mod_desc), name )
    except ImportError as exc:
        mod = None
        sys.stderr.write("Error: failed to import module ({})".format(exc))
    finally:
        if mod_fp: mod_fp.close()
    return mod

# import the GrammarTemplate.py engine (as a) module, probably you will want to place this in another dir/package
GrammarTemplate = import_module('GrammarTemplate', os.path.join(os.path.dirname(__file__), '../src/python/'))
if not GrammarTemplate:
    print ('Could not load the GrammarTemplate Module')
    sys.exit(1)
else:    
    pass


def echo( s='' ):
    print (s)

echo('GrammarTemplate.VERSION = ' + GrammarTemplate.VERSION)
echo('GrammarTemplate POST-OP Mode')
echo( )

#
#    i.e: 
#    foreach "expression:terms" as "term":
#        foreach "term:factors" as "factor":
#            ..
#    
#    here an :EXPR template is defined which itself uses (anonymous) sub-templates
#    it is equivalent to (expand sub-templates to distinct):
#
#<:FACTOR>:=[<lhs>[ <op>? <rhs|NULL>]]
#
#<:TERM>:=[(<factor:FACTOR>[ AND <factor:FACTOR>*])]
#
#<:EXPR>:=[<term:TERM>[ OR <term:TERM>*]]
#
#<expression:EXPR>
#<expression2:EXPR>
#
#
tpl = "<:EXPR>:=[<term>:=[(<factor>:=[<globalNegation:NEG><lhs>[ <op:OP>? <rhs|NULL>]][ AND <factor>*])][ OR <term>*]]<expression:EXPR>\n<expression2:EXPR>"

def op_func( val, *rest ):
    return '<>' if '!=' == val else val

def neg_func( val, *rest ):
    return 'NOT ' if val else ''
    
expr = GrammarTemplate(tpl, None, True) # post-op mode
GrammarTemplate.fnGlobal['NEG'] = neg_func
expr.fn['OP'] = op_func

echo("input template:")
echo(tpl)

echo( )

echo("output:")
echo(expr.render({
    'globalNegation': False,
    'expression'  : [
        # term
        [
            # factor
            {'lhs': 1, 'op': '=', 'rhs': 1},
            # factor
            {'lhs': 1, 'op': '=', 'rhs': 2},
            # factor
            {'lhs': 1, 'op': '=', 'rhs': 3}
        ],
        # term
        [
            # factor
            {'lhs': 1, 'op': '<', 'rhs': 1},
            # factor
            {'lhs': 1, 'op': '<', 'rhs': 2},
            # factor
            {'lhs': 1, 'op': '<', 'rhs': 3}
        ],
        # term
        [
            # factor
            {'lhs': 1, 'op': '>', 'rhs': 1},
            # factor
            {'lhs': 1, 'op': '>', 'rhs': 2},
            # factor
            {'lhs': 1, 'op': '>', 'rhs': 3}
        ]
    ],
    'expression2'  : [
        # term
        [
            # factor
            {'lhs': 2, 'op': '=', 'rhs': 1},
            # factor
            {'lhs': 2, 'op': '=', 'rhs': 2},
            # factor
            {'lhs': 2, 'op': '=', 'rhs': 3}
        ],
        # term
        [
            # factor
            {'lhs': 2, 'op': '<', 'rhs': 1},
            # factor
            {'lhs': 2, 'op': '<', 'rhs': 2},
            # factor
            {'lhs': 2, 'op': '<', 'rhs': 3}
        ],
        # term
        [
            # factor
            {'lhs': 2, 'op': '>', 'rhs': 1},
            # factor
            {'lhs': 2, 'op': '>', 'rhs': 2},
            # factor
            {'lhs': 2, 'op': '>', 'rhs': 3}
        ],
        # term
        [
            # factor
            {'lhs': 3},
            # factor
            {'lhs': 3, 'op': '!='}
        ]
    ]
}))
