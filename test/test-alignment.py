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

tpl = "<:BLOCK>:=[BLOCK <.name>\n{\n[    <@.blocks:BLOCKS>?\n]}]<:BLOCKS>:=[<@block:BLOCK>[\n<@block:BLOCK>*]]<@blocks:BLOCKS>"

    
aligned = GrammarTemplate(tpl, None, True)

echo("input template:")
echo(tpl)

echo( )

echo("output:")
echo(aligned.render({
    'blocks'      : [
    {
        'name'        : "block1",
        'blocks'      : None
    },
    {
        'name'        : "block2",
        'blocks'      : [
            {
                'name'   : "block21",
                'blocks' : [
                    {
                        'name'   : "block211",
                        'blocks' : [
                            {
                                'name'   : "block2111",
                                'blocks' : None
                            },
                            {
                                'name'   : "block2112"
                            }
                        ]
                    },
                    {
                        'name'   : "block212"
                    }
                ]
            },
            {
                'name'   : "block22",
                'blocks' : [
                    {
                        'name'   : "block221"
                    },
                    {
                        'name'   : "block222"
                    }
                ]
            }
        ]
    },
    {
        'name'        : "block3"
    }
]
}))
