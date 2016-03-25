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

sql = GrammarTemplate("SELECT <select_columns>[,<*select_columns>]\nFROM <from_tables>[,<*from_tables>][\n<?join_clauses>[\n<*join_clauses>]][\nWHERE (<?where_conditions_required>) AND (<?where_conditions>)][\nWHERE <?where_conditions_required><?!where_conditions>][\nWHERE <?!where_conditions_required><?where_conditions>][\nGROUP BY <?group_conditions>[,<*group_conditions>]][\nHAVING (<?having_conditions_required>) AND (<?having_conditions>)][\nHAVING <?having_conditions_required><?!having_conditions>][\nHAVING <?!having_conditions_required><?having_conditions>][\nORDER BY <?order_conditions>[,<*order_conditions>]][\nLIMIT <offset|0>,<?count>]");

echo(sql.render({
    'select_columns':['field1','field2','field3'],
    'from_tables':['tbl1','tbl2'],
    'where_conditions': 'field1=1 AND field2=2',
    'count': 5
}))
