##
#   GrammarTemplate, 
#   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
# 
#   @version: 2.1.1
#   https://github.com/foo123/GrammarTemplate
#
##

import time

GUID = 0
def guid( ):
    global GUID
    GUID += 1
    return str(int(time.time()))+'--'+str(GUID)

def is_array( v ):
    return isinstance(v, (list,tuple))
    

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
    REPL = '{'
    REPR = '}'
    DOT = '.'
    REF = ':'
    default_value = None
    negative = 0
    optional = 0
    l = len(tpl)
    
    postop = postop is True
    a = TplEntry({'type': 0, 'val': ''})
    cur_arg = {
        'type'    : 1,
        'name'    : None,
        'key'     : None,
        'stpl'    : None,
        'dval'    : None,
        'opt'     : 0,
        'neg'     : 0,
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
                else: a = TplEntry({'type': 0, 'val': s}, a)
            
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
                cur_arg['start'] = start_i
                cur_arg['end'] = end_i
                # handle multiple optional arguments for same optional block
                opt_args = StackEntry(None, [argument,nested,negative,start_i,end_i,optional])
                
            elif optional:
                # handle multiple optional arguments for same optional block
                opt_args = StackEntry(opt_args, [argument,nested,negative,start_i,end_i,optional])
            
            elif (not optional) and (cur_arg['name'] is None):
                cur_arg['name'] = argument
                cur_arg['key'] = nested
                cur_arg['stpl'] = template
                cur_arg['dval'] = default_value
                cur_arg['opt'] = 0
                cur_arg['neg'] = negative
                cur_arg['start'] = start_i
                cur_arg['end'] = end_i
                # handle multiple optional arguments for same optional block
                opt_args = StackEntry(None, [argument,nested,negative,start_i,end_i,0])
            
            a = TplEntry({
                'type'    : 1,
                'name'    : argument,
                'key'     : nested,
                'stpl'    : template,
                'dval'    : default_value,
                'opt'     : optional,
                'start'   : start_i,
                'end'     : end_i
            }, a)
        
        elif OBL == tpl[i:i+lenOBL]:
            i += lenOBL
            
            if escaped:
                s += OBL
                continue
            
            # optional block
            if len(s):
                if 0 == a.node['type']: a.node['val'] += s
                else: a = TplEntry({'type': 0, 'val': s}, a)
            
            s = ''
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
                'start'   : 0,
                'end'     : 0
            }
            opt_args = None
            a = TplEntry({'type': 0, 'val': ''})
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
                else: b = TplEntry({'type': 0, 'val': s}, b)
            
            s = ''
            if start_tpl:
                subtpl[start_tpl] = TplEntry({
                    'type'    : 2,
                    'name'    : prev_arg['name'],
                    'key'     : prev_arg['key'],
                    'start'   : 0,#cur_arg.start
                    'end'     : 0,#cur_arg.end
                    'opt_args': None,#opt_args
                    'tpl'     : cur_block
                })
                start_tpl = None
            else:
                a = TplEntry({
                    'type'    : -1,
                    'name'    : prev_arg['name'],
                    'key'     : prev_arg['key'],
                    'start'   : prev_arg['start'],
                    'end'     : prev_arg['end'],
                    'opt_args': prev_opt_args,
                    'tpl'     : cur_block
                }, a)
        
        else:
            s += tpl[i]
            i += 1
    
    if len(s):
        if 0 == a.node['type']: a.node['val'] += s
        else: a = TplEntry({'type': 0, 'val': s}, a)
    
    return [roottpl, subtpl]

def optional_block( args, block, SUB=None, FN=None, index=None, orig_args=None ):
    out = ''
    block_arg = None
    
    if -1 == block['type']:
        # optional block, check if optional variables can be rendered
        opt_vars = block['opt_args']
        # if no optional arguments, render block by default
        if opt_vars and opt_vars.value[5]:
            while opt_vars:
                opt_v = opt_vars.value
                opt_arg = walk( args, opt_v[1], [str(opt_v[0])], orig_args )
                if (block_arg is None) and (block['name'] == opt_v[0]): block_arg = opt_arg
                
                if ((0 == opt_v[2]) and (opt_arg is None)) or ((1 == opt_v[2]) and (opt_arg is not None)): return ''
                opt_vars = opt_vars.prev
    else:
        block_arg = walk( args, block['key'], [str(block['name'])], orig_args )
    
    arr = is_array( block_arg )
    lenn = len(block_arg) if arr else -1
    if arr and (lenn > block['start']):
        rs = block['start']
        re = lenn-1 if -1==block['end'] else min(block['end'],lenn-1)
        ri = rs
        while ri <= re:
            out += main( args, block['tpl'], SUB, FN, ri, orig_args )
            ri += 1
    elif (not arr) and (block['start'] == block['end']):
        out = main( args, block['tpl'], SUB, FN, None, orig_args )
    
    return out

def non_terminal( args, symbol, SUB=None, FN=None, index=None, orig_args=None ):
    out = ''
    if symbol['stpl'] and ((SUB and (symbol['stpl'] in SUB)) or (FN and (symbol['stpl'] in FN)) or ((symbol['stpl'] in GrammarTemplate.fnGlobal))):
        # using custom function or sub-template
        opt_arg = walk( args, symbol['key'], [str(symbol['name'])], orig_args )
        
        if SUB and (symbol['stpl'] in SUB):
            # sub-template
            #if ((index is not None) or (symbol['start'] is not None)) and is_array(opt_arg):
            #    opt_arg = opt_arg[index] if index is not None else opt_arg[symbol['start']]
            if (index is not None) and ((index is not 0) or (not symbol['opt'])) and is_array(opt_arg):
                opt_arg = opt_arg[index]
            
            if (opt_arg is None) and (symbol['dval'] is not None):
                # default value if missing
                out = symbol['dval']
            else:
                # try to associate sub-template parameters to actual input arguments
                tpl = SUB[symbol['stpl']].node
                tpl_args = {}
                if opt_arg is not None:
                    #if (tpl['name'] in opt_arg) and (symbol['name'] not in opt_arg): tpl_args = opt_arg
                    #else: tpl_args[tpl['name']] = opt_arg
                    if is_array(opt_arg): tpl_args[tpl['name']] = opt_arg
                    else: tpl_args = opt_arg
                out = optional_block( tpl_args, tpl, SUB, FN, None, args if orig_args is None else orig_args )
        else:#elif fn:
            # custom function
            fn = FN[symbol['stpl']] if FN and (symbol['stpl'] in FN) else (GrammarTemplate.fnGlobal[symbol['stpl']] if symbol['stpl'] in GrammarTemplate.fnGlobal else None)
            
            if is_array(opt_arg):
                index = index if index is not None else symbol['start']
                opt_arg = opt_arg[index] if index < len(opt_arg) else None
            
            opt_arg = fn(opt_arg, index, args, orig_args, symbol) if callable(fn) else str(fn)
            
            out = symbol['dval'] if (opt_arg is None) and (symbol['dval'] is not None) else str(opt_arg)
    elif symbol['opt'] and (symbol['dval'] is not None):
        # boolean optional argument
        out = symbol['dval']
    else:
        # plain symbol argument
        opt_arg = walk( args, symbol['key'], [str(symbol['name'])], orig_args )
        
        # default value if missing
        if is_array(opt_arg):
            index = index if index is not None else symbol['start']
            opt_arg = opt_arg[index] if index < len(opt_arg) else None
        out = symbol['dval'] if (opt_arg is None) and (symbol['dval'] is not None) else str(opt_arg)
    
    return out

def main( args, tpl, SUB=None, FN=None, index=None, orig_args=None ):
    out = ''
    while tpl:
        tt = tpl.node['type']
        out += (optional_block( args, tpl.node, SUB, FN, index, orig_args ) if -1 == tt else (non_terminal( args, tpl.node, SUB, FN, index, orig_args ) if 1 == tt else tpl.node['val']))
        tpl = tpl.next
    return out


class GrammarTemplate:
    """
    GrammarTemplate for Python,
    https://github.com/foo123/GrammarTemplate
    """
    
    VERSION = '2.1.1'
    

    #defaultDelims = ['<','>','[',']',':=','?','*','!','|','{','}']
    defaultDelims = ['<','>','[',']',':=']
    fnGlobal = {}
    guid = guid
    multisplit = multisplit
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

