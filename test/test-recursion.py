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
#<:FACTOR>:=[<lhs>[ <?op> <rhs|NULL>]]
#
#<:TERM>:=[(<factor:FACTOR>[ AND <*factor:FACTOR>])]
#
#<:EXPR>:=[<term:TERM>[ OR <*term:TERM>]]
#
#<expression:EXPR>
#<expression2:EXPR>
#
#
tpl = "<:EXPR>:=[<term>:=[(<factor>:=[[<?globalNegation|>NOT ]<lhs>[ <?op> <rhs|NULL>]][ AND <*factor>])][ OR <*term>]]<expression:EXPR>\n<expression2:EXPR>"

expr = GrammarTemplate(tpl)

echo("input template:")
echo(tpl)

echo( )

echo("output:")
echo(expr.render({
    'globalNegation': True,
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
