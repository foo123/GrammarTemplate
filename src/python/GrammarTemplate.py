##
#   GrammarTemplate, 
#   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
# 
#   @version: 3.0.0
#   https://github.com/foo123/GrammarTemplate
#
##

import time

def pad( s, n, z='0', pad_right=False ):
    ps = str(s)
    if pad_right:
        while len(ps) < n: ps += z
    else:
        while len(ps) < n: ps = z + ps
    return ps

GUID = 0
def guid( ):
    global GUID
    GUID += 1
    return pad(hex(int(time.time()))[2:],12)+'--'+pad(hex(GUID)[2:],4)

def is_array( v ):
    return isinstance(v, (list,tuple))
    

def compute_alignment( s, i, l ):
    alignment = ''
    while i < l:
        c = s[i]
        if (" " == c) or ("\r" == c) or ("\t" == c) or ("\v" == c) or ("\0" == c):
            alignment += str(c)
            i += 1
        else:
            break
    return alignment

def align( s, alignment ):
    l = len(s)
    if l and len(alignment):
        aligned = '';
        for c in s:
            aligned += str(c)
            if "\n" == c: aligned += alignment
    else:
        aligned = s
    return aligned

def walk( obj, keys, keys_alt=None, obj_alt=None ):
    found = 0
    if keys:
        o = obj
        l = len(keys)
        i = 0
        found = 1
        while i < l:
            k = keys[i]
            i += 1
            if o is not None:
                if isinstance(o,(list,tuple)) and int(k)<len(o):
                    o = o[k]
                elif isinstance(o,dict) and (k in o):
                    o = o[k]
                else:
                    try:
                        o = getattr(o, k)
                    except AttributeError:
                        found = 0
                        break
            else:
                found = 0
                break
    if (not found) and keys_alt:
        o = obj
        l = len(keys_alt)
        i = 0
        found = 1
        while i < l:
            k = keys_alt[i]
            i += 1
            if o is not None:
                if isinstance(o,(list,tuple)) and int(k)<len(o):
                    o = o[k]
                elif isinstance(o,dict) and (k in o):
                    o = o[k]
                else:
                    try:
                        o = getattr(o, k)
                    except AttributeError:
                        found = 0
                        break
            else:
                found = 0
                break
    if (not found) and (obj_alt is not None) and (obj_alt is not obj):
        if keys:
            o = obj_alt
            l = len(keys)
            i = 0
            found = 1
            while i < l:
                k = keys[i]
                i += 1
                if o is not None:
                    if isinstance(o,(list,tuple)) and int(k)<len(o):
                        o = o[k]
                    elif isinstance(o,dict) and (k in o):
                        o = o[k]
                    else:
                        try:
                            o = getattr(o, k)
                        except AttributeError:
                            found = 0
                            break
                else:
                    found = 0
                    break
        if (not found) and keys_alt:
            o = obj_alt
            l = len(keys_alt)
            i = 0
            found = 1
            while i < l:
                k = keys_alt[i]
                i += 1
                if o is not None:
                    if isinstance(o,(list,tuple)) and int(k)<len(o):
                        o = o[k]
                    elif isinstance(o,dict) and (k in o):
                        o = o[k]
                    else:
                        try:
                            o = getattr(o, k)
                        except AttributeError:
                            found = 0
                            break
                else:
                    found = 0
                    break
    return o if found else None
    

class StackEntry:
    def __init__(self, stack=None, value=None):
        self.prev = stack
        self.value = value

class TplEntry:
    def __init__(self, node=None, tpl=None ):
        if tpl: tpl.next = self
        self.node = node
        self.prev = tpl
        self.next = None

def multisplit( tpl, delims, postop=False ):
    IDL = delims[0]
    IDR = delims[1]
    OBL = delims[2]
    OBR = delims[3]
    TPL = delims[4]
    lenIDL = len(IDL)
    lenIDR = len(IDR)
    lenOBL = len(OBL)
    lenOBR = len(OBR)
    lenTPL = len(TPL)
    ESC = '\\'
    OPT = '?'
    OPTR = '*'
    NEG = '!'
    DEF = '|'
    COMMENT = '#'
    REPL = '{'
    REPR = '}'
    DOT = '.'
    REF = ':'
    ALGN = '@'
    #NOTALGN = '&'
    default_value = None
    negative = 0
    optional = 0
    aligned = 0
    localised = 0
    l = len(tpl)
    
    postop = postop is True
    a = TplEntry({'type': 0, 'val': '', 'algn': ''})
    cur_arg = {
        'type'    : 1,
        'name'    : None,
        'key'     : None,
        'stpl'    : None,
        'dval'    : None,
        'opt'     : 0,
        'neg'     : 0,
        'algn'    : 0,
        'loc'     : 0,
        'start'   : 0,
        'end'     : 0
    }
    roottpl = a
    block = None
    opt_args = None
    subtpl = {}
    cur_tpl = None
    arg_tpl = {}
    start_tpl = None
    stack = None
    s = ''
    escaped = False
    
    i = 0
    while i < l:
        
        escaped = False
        ch = tpl[i]
        if ESC == ch:
            escaped = True
            i += 1
        
        if IDL == tpl[i:i+lenIDL]:
            i += lenIDL
            
            if escaped:
                s += IDL
                continue
            
            if len(s):
                if 0 == a.node['type']: a.node['val'] += s
                else: a = TplEntry({'type': 0, 'val': s, 'algn': ''}, a)
            s = ''
        
        elif IDR == tpl[i:i+lenIDR]:
            i += lenIDR
            
            if escaped:
                s += IDR
                continue
            
            # argument
            argument = s
            s = ''
            p = argument.find(DEF)
            if -1 < p:
                default_value = argument[p+1:]
                argument = argument[0:p]
            else:
                default_value = None
            if postop:
                c = tpl[i] if i < l else ''
            else:
                c = argument[0]
            if OPT == c or OPTR == c:
                optional = 1
                if OPTR == c:
                    start_i = 1
                    end_i = -1
                else:
                    start_i = 0
                    end_i = 0
                if postop:
                    i += 1
                    if (i < l) and (NEG == tpl[i]):
                        negative = 1
                        i += 1
                    else:
                        negative = 0
                else:
                    if NEG == argument[1]:
                        negative = 1
                        argument = argument[2:]
                    else:
                        negative = 0
                        argument = argument[1:]
            elif REPL == c:
                if postop:
                    s = ''
                    j = i+1
                    jl = l
                    while (j < jl) and (REPR != tpl[j]):
                        s += tpl[j]
                        j += 1
                    i = j+1
                else:
                    s = ''
                    j = 1
                    jl = len(argument)
                    while (j < jl) and (REPR != argument[j]):
                        s += argument[j]
                        j += 1
                    argument = argument[j+1:]
                s = s.split(',')
                if len(s) > 1:
                    start_i = s[0].strip()
                    start_i = int(start_i,10) if len(start_i) else 0
                    end_i = s[1].strip()
                    end_i = int(end_i,10) if len(end_i) else -1
                    optional = 1
                else:
                    start_i = s[0].strip()
                    start_i = int(start_i,10) if len(start_i) else 0
                    end_i = start_i
                    optional = 0
                s = ''
                negative = 0
            else:
                optional = 0
                negative = 0
                start_i = 0
                end_i = 0
            if negative and default_value is None: default_value = ''
            
            c = argument[0]
            if ALGN == c:
                aligned = 1
                argument = argument[1:]
            else:
                aligned = 0
            
            c = argument[0]
            if DOT == c:
                localised = 1
                argument = argument[1:]
            else:
                localised = 0
            
            p = argument.find(REF)
            template = argument.split(REF) if -1 < p else [argument,None]
            argument = template[0]
            template = template[1]
            p = argument.find(DOT)
            nested = argument.split(DOT) if -1 < p else None
            
            if cur_tpl and (cur_tpl not in arg_tpl): arg_tpl[cur_tpl] = {}
            
            if TPL+OBL == tpl[i:i+lenTPL+lenOBL]:
                # template definition
                i += lenTPL
                template = template if template and len(template) else 'grtpl--'+guid()
                start_tpl = template
                if cur_tpl and len(argument):
                    arg_tpl[cur_tpl][argument] = template
            
            if not len(argument): continue # template definition only
            
            if (template is None) and cur_tpl and (cur_tpl in arg_tpl) and (argument in arg_tpl[cur_tpl]):
                template = arg_tpl[cur_tpl][argument]
            
            if optional and not cur_arg['opt']:
                cur_arg['name'] = argument
                cur_arg['key'] = nested
                cur_arg['stpl'] = template
                cur_arg['dval'] = default_value
                cur_arg['opt'] = optional
                cur_arg['neg'] = negative
                cur_arg['algn'] = aligned
                cur_arg['loc'] = localised
                cur_arg['start'] = start_i
                cur_arg['end'] = end_i
                # handle multiple optional arguments for same optional block
                opt_args = StackEntry(None, [argument,nested,negative,start_i,end_i,optional,localised])
                
            elif optional:
                # handle multiple optional arguments for same optional block
                if (start_i != end_i) and (cur_arg['start'] == cur_arg['end']):
                    # set as main arg a loop arg, if exists
                    cur_arg['name'] = argument
                    cur_arg['key'] = nested
                    cur_arg['stpl'] = template
                    cur_arg['dval'] = default_value
                    cur_arg['opt'] = optional
                    cur_arg['neg'] = negative
                    cur_arg['algn'] = aligned
                    cur_arg['loc'] = localised
                    cur_arg['start'] = start_i
                    cur_arg['end'] = end_i
                opt_args = StackEntry(opt_args, [argument,nested,negative,start_i,end_i,optional,localised])
            
            elif (not optional) and (cur_arg['name'] is None):
                cur_arg['name'] = argument
                cur_arg['key'] = nested
                cur_arg['stpl'] = template
                cur_arg['dval'] = default_value
                cur_arg['opt'] = 0
                cur_arg['neg'] = negative
                cur_arg['algn'] = aligned
                cur_arg['loc'] = localised
                cur_arg['start'] = start_i
                cur_arg['end'] = end_i
                # handle multiple optional arguments for same optional block
                opt_args = StackEntry(None, [argument,nested,negative,start_i,end_i,0,localised])
            
            if 0 == a.node['type']: a.node['algn'] = compute_alignment(a.node['val'], 0, len(a.node['val']))
            a = TplEntry({
                'type'    : 1,
                'name'    : argument,
                'key'     : nested,
                'stpl'    : template,
                'dval'    : default_value,
                'opt'     : optional,
                'algn'    : aligned,
                'loc'     : localised,
                'start'   : start_i,
                'end'     : end_i
            }, a)
        
        elif OBL == tpl[i:i+lenOBL]:
            i += lenOBL
            
            if escaped:
                s += OBL
                continue
            
            if len(s):
                if 0 == a.node['type']: a.node['val'] += s
                else: a = TplEntry({'type': 0, 'val': s, 'algn': ''}, a)
            s = ''
            
            # comment
            if COMMENT == tpl[i]:
                j = i+1
                jl = l
                while (j < jl) and (COMMENT+OBR != tpl[j:lenOBR+1]):
                    s += tpl[j]
                    j += 1
                i = j+lenOBR+1
                if 0 == a.node['type']: a.node['algn'] = compute_alignment(a.node['val'], 0, len(a.node['val']))
                a = TplEntry({'type': -100, 'val': s}, a)
                s = ''
                continue
            
            # optional block
            stack = StackEntry(stack, [a, block, cur_arg, opt_args, cur_tpl, start_tpl])
            if start_tpl: cur_tpl = start_tpl
            start_tpl = None
            cur_arg = {
                'type'    : 1,
                'name'    : None,
                'key'     : None,
                'stpl'    : None,
                'dval'    : None,
                'opt'     : 0,
                'neg'     : 0,
                'algn'    : 0,
                'loc'     : 0,
                'start'   : 0,
                'end'     : 0
            }
            opt_args = None
            a = TplEntry({'type': 0, 'val': '', 'algn': ''})
            block = a
        
        elif OBR == tpl[i:i+lenOBR]:
            i += lenOBR
            
            if escaped:
                s += OBR
                continue
            
            b = a
            cur_block = block
            prev_arg = cur_arg
            prev_opt_args = opt_args
            if stack:
                a = stack.value[0]
                block = stack.value[1]
                cur_arg = stack.value[2]
                opt_args = stack.value[3]
                cur_tpl = stack.value[4]
                start_tpl = stack.value[5]
                stack = stack.prev
            else:
                a = None
            
            if len(s):
                if 0 == b.node['type']: b.node['val'] += s
                else: b = TplEntry({'type': 0, 'val': s, 'algn': ''}, b)
            s = ''
            
            if start_tpl:
                subtpl[start_tpl] = TplEntry({
                    'type'    : 2,
                    'name'    : prev_arg['name'],
                    'key'     : prev_arg['key'],
                    'loc'     : prev_arg['loc'],
                    'algn'    : prev_arg['algn'],
                    'start'   : prev_arg['start'],
                    'end'     : prev_arg['end'],
                    'opt_args': None,#opt_args
                    'tpl'     : cur_block
                })
                start_tpl = None
            else:
                if 0 == a.node['type']: a.node['algn'] = compute_alignment(a.node['val'], 0, len(a.node['val']))
                a = TplEntry({
                    'type'    : -1,
                    'name'    : prev_arg['name'],
                    'key'     : prev_arg['key'],
                    'loc'     : prev_arg['loc'],
                    'algn'    : prev_arg['algn'],
                    'start'   : prev_arg['start'],
                    'end'     : prev_arg['end'],
                    'opt_args': prev_opt_args,
                    'tpl'     : cur_block
                }, a)
        
        else:
            ch = tpl[i]
            i += 1
            if "\n" == ch:
                # note line changes to handle alignments
                if len(s):
                    if 0 == a.node['type']: a.node['val'] += s
                    else: a = TplEntry({'type': 0, 'val': s, 'algn': ''}, a)
                s = ''
                if 0 == a.node['type']: a.node['algn'] = compute_alignment(a.node['val'], 0, len(a.node['val']))
                a = TplEntry({'type': 100, 'val': "\n"}, a)
            else:
                s += ch
    
    if len(s):
        if 0 == a.node['type']: a.node['val'] += s
        else: a = TplEntry({'type': 0, 'val': s, 'algn': ''}, a)
    if 0 == a.node['type']: a.node['algn'] = compute_alignment(a.node['val'], 0, len(a.node['val']))
    return [roottpl, subtpl]

def optional_block( args, block, SUB=None, FN=None, index=None, alignment='', orig_args=None ):
    out = ''
    block_arg = None
    
    if -1 == block['type']:
        # optional block, check if optional variables can be rendered
        opt_vars = block['opt_args']
        # if no optional arguments, render block by default
        if opt_vars and opt_vars.value[5]:
            while opt_vars:
                opt_v = opt_vars.value
                opt_arg = walk( args, opt_v[1], [str(opt_v[0])], None if opt_v[6] else orig_args )
                if (block_arg is None) and (block['name'] == opt_v[0]): block_arg = opt_arg
                
                if ((0 == opt_v[2]) and (opt_arg is None)) or ((1 == opt_v[2]) and (opt_arg is not None)): return ''
                opt_vars = opt_vars.prev
    else:
        block_arg = walk( args, block['key'], [str(block['name'])], None if block['loc'] else orig_args )
    
    arr = is_array( block_arg )
    lenn = len(block_arg) if arr else -1
    #if not block['algn']: alignment = ''
    if arr and (lenn > block['start']):
        rs = block['start']
        re = lenn-1 if -1==block['end'] else min(block['end'],lenn-1)
        ri = rs
        while ri <= re:
            out += main( args, block['tpl'], SUB, FN, ri, alignment, orig_args )
            ri += 1
    elif (not arr) and (block['start'] == block['end']):
        out = main( args, block['tpl'], SUB, FN, None, alignment, orig_args )
    
    return out

def non_terminal( args, symbol, SUB=None, FN=None, index=None, alignment='', orig_args=None ):
    out = ''
    if symbol['stpl'] and ((SUB and (symbol['stpl'] in SUB)) or (symbol['stpl'] in GrammarTemplate.subGlobal) or (FN and ((symbol['stpl'] in FN) or ('*' in FN))) or ((symbol['stpl'] in GrammarTemplate.fnGlobal) or ('*' in GrammarTemplate.fnGlobal))):
        # using custom function or sub-template
        opt_arg = walk( args, symbol['key'], [str(symbol['name'])], None if symbol['loc'] else orig_args )
        
        if (SUB and (symbol['stpl'] in SUB)) or (symbol['stpl'] in GrammarTemplate.subGlobal):
            # sub-template
            if (index is not None) and ((0 != index) or (symbol['start'] != symbol['end']) or (not symbol['opt'])) and is_array(opt_arg):
                opt_arg = opt_arg[ index ] if index < len(opt_arg) else None
            
            if (opt_arg is None) and (symbol['dval'] is not None):
                # default value if missing
                out = symbol['dval']
            else:
                # try to associate sub-template parameters to actual input arguments
                tpl = SUB[symbol['stpl']].node if SUB and (symbol['stpl'] in SUB) else GrammarTemplate.subGlobal[symbol['stpl']].node
                tpl_args = {}
                if opt_arg is not None:
                    if is_array(opt_arg): tpl_args[tpl['name']] = opt_arg
                    else: tpl_args = opt_arg
                out = optional_block( tpl_args, tpl, SUB, FN, None, alignment if symbol['algn'] else '', args if orig_args is None else orig_args )
                #if symbol['algn']: out = align(out, alignment)
        else:#elif fn:
            # custom function
            fn = None
            if   FN and (symbol['stpl'] in FN):              fn = FN[symbol['stpl']]
            elif FN and ('*' in FN):                         fn = FN['*']
            elif symbol['stpl'] in GrammarTemplate.fnGlobal: fn = GrammarTemplate.fnGlobal[symbol['stpl']]
            elif '*' in GrammarTemplate.fnGlobal:            fn = GrammarTemplate.fnGlobal['*']
            
            if is_array(opt_arg):
                index = index if index is not None else symbol['start']
                opt_arg = opt_arg[ index ] if index < len(opt_arg) else None
            
            if callable(fn):
                fn_arg = {
                    #'value'               : opt_arg,
                    'symbol'              : symbol,
                    'index'               : index,
                    'currentArguments'    : args,
                    'originalArguments'   : orig_args,
                    'alignment'           : alignment
                }
                opt_arg = fn( opt_arg, fn_arg )
            else:
                opt_arg = str(fn)
            
            out = symbol['dval'] if (opt_arg is None) and (symbol['dval'] is not None) else str(opt_arg)
            if symbol['algn']: out = align(out, alignment)
    
    elif symbol['opt'] and (symbol['dval'] is not None):
        # boolean optional argument
        out = symbol['dval']
    
    else:
        # plain symbol argument
        opt_arg = walk( args, symbol['key'], [str(symbol['name'])], None if symbol['loc'] else orig_args )
        
        # default value if missing
        if is_array(opt_arg):
            index = index if index is not None else symbol['start']
            opt_arg = opt_arg[ index ] if index < len(opt_arg) else None
        out = symbol['dval'] if (opt_arg is None) and (symbol['dval'] is not None) else str(opt_arg)
        if symbol['algn']: out = align(out, alignment)
    
    return out

def main( args, tpl, SUB=None, FN=None, index=None, alignment='', orig_args=None ):
    out = ''
    current_alignment = alignment
    while tpl:
        tt = tpl.node['type']
        if -1 == tt: # optional code-block
            out += optional_block( args, tpl.node, SUB, FN, index, current_alignment, orig_args )
        elif 1 == tt: # non-terminal
            out += non_terminal( args, tpl.node, SUB, FN, index, current_alignment, orig_args )
        elif 0 == tt: # terminal
            current_alignment += tpl.node['algn']
            out += tpl.node['val']
        elif 100 == tt: # new line
            current_alignment = alignment
            out += "\n" + alignment
        #elif -100 == tt: # comment
        #    # pass
        tpl = tpl.next
    return out


class GrammarTemplate:
    """
    GrammarTemplate for Python,
    https://github.com/foo123/GrammarTemplate
    """
    
    VERSION = '3.0.0'
    

    #defaultDelims = ['<','>','[',']',':=','?','*','!','|','{','}']
    defaultDelims = ['<','>','[',']',':=']
    fnGlobal = {}
    subGlobal = {}
    guid = guid
    multisplit = multisplit
    align = align
    main = main
    
    def __init__(self, tpl='', delims=None, postop=False):
        self.id = None
        self.tpl = None
        self.fn = {}
        # lazy init
        self._args = [ tpl, delims if delims else GrammarTemplate.defaultDelims, postop ]

    def __del__(self):
        self.dispose()
        
    def dispose(self):
        self.id = None
        self.tpl = None
        self.fn = None
        self._args = None
        return self
    
    def parse(self):
        if (self.tpl is None) and (self._args is not None):
            # lazy init
            self.tpl = GrammarTemplate.multisplit( self._args[0], self._args[1], self._args[2] )
            self._args = None
        return self
    
    def render(self, args=None):
        # lazy init
        if self.tpl is None: self.parse( )
        return GrammarTemplate.main( {} if None == args else args, self.tpl[0], self.tpl[1], self.fn )



__all__ = ['GrammarTemplate']

