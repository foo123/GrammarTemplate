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

# foreach expression as term: foreach term as factor: ..
tpl = "<:expression_tpl>:=[<term>:=[(<factor>:=[<lhs>[ <?op> <rhs|NULL>]][ AND <*factor>])][ OR <*term>]]<expression:expression_tpl>\n<expression2:expression_tpl>"

expr = GrammarTemplate(tpl)

echo("input template:")
echo(tpl)

echo( )

echo("output:")
echo(expr.render({
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
        ]
    ]
}))
