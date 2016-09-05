##
#   GrammarTemplate, 
#   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
# 
#   @version: 2.0.0
#   https://github.com/foo123/GrammarTemplate
#
##

import time
TPL_ID = 0
def guid( ):
    global TPL_ID
    TPL_ID += 1
    return 'grtpl--'+str(int(time.time()))+'--'+str(TPL_ID)

def is_array( v ):
    return isinstance(v, (list,tuple))
    

def walk( obj, keys ):
    o = obj
    l = len(keys)
    i = 0
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
                    return None
        else: return None
    return o
    

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

def multisplit( tpl, delims ):
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
        
        ch = tpl[i]
        
        if ESC == ch:
            escaped = not escaped
            i += 1
        
        if IDL == tpl[i:i+lenIDL]:
            i += lenIDL
            
            if escaped:
                s += IDL
                escaped = False
                continue
            
            if len(s):
                if 0 == a.node['type']: a.node['val'] += s
                else: a = TplEntry({'type': 0, 'val': s}, a)
            
            s = ''
        
        elif IDR == tpl[i:i+lenIDR]:
            i += lenIDR
            
            if escaped:
                s += IDR
                escaped = False
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
            
            c = argument[0]
            if OPT == c or OPTR == c:
                optional = 1
                if OPTR == c:
                    start_i = 1
                    end_i = -1
                else:
                    start_i = 0
                    end_i = 0
                argument = argument[1:]
                if NEG == argument[0]:
                    negative = 1
                    argument = argument[1:]
                else:
                    negative = 0
            elif REPL == c:
                s = ''
                j = 1
                jl = len(argument)
                while j < jl and REPR != argument[j]:
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
                template = template if template and len(template) else guid()
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
                opt_args = StackEntry(None, [argument,nested,negative,start_i,end_i])
                
            elif optional:
                # handle multiple optional arguments for same optional block
                opt_args = StackEntry(opt_args, [argument,nested,negative,start_i,end_i])
            
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
                opt_args = StackEntry(None, [argument,nested,negative,start_i,end_i])
            
            a = TplEntry({
                'type'    : 1,
                'name'    : argument,
                'key'     : nested,
                'stpl'    : template,
                'dval'    : default_value,
                'start'   : start_i,
                'end'     : end_i
            }, a)
        
        elif OBL == tpl[i:i+lenOBL]:
            i += lenOBL
            
            if escaped:
                s += OBL
                escaped = False
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
                escaped = False
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
            if ESC == ch:
                s += ch
            else:
                s += tpl[i]
                i += 1
    
    if len(s):
        if 0 == a.node['type']: a.node['val'] += s
        else: a = TplEntry({'type': 0, 'val': s}, a)
    
    return [roottpl, subtpl]

def optional_block( SUB, args, block, index=None ):
    out = ''
    
    if -1 == block['type']:
        # optional block, check if optional variables can be rendered
        opt_vars = block['opt_args']
        if not opt_vars: return ''
        while opt_vars:
            opt_v = opt_vars.value
            opt_arg = walk( args, opt_v[1] if opt_v[1] else [opt_v[0]] )
            if ((0 == opt_v[2]) and (opt_arg is None)) or ((1 == opt_v[2]) and (opt_arg is not None)): return ''
            opt_vars = opt_vars.prev
    
    if block['key']:
        opt_arg = walk( args, block['key'] )#nested key
        if (opt_arg is None) and (block['name'] in args): opt_arg = args[block['name']]
    else:
        opt_arg = walk( args, [block['name']] )#plain key
    
    arr = is_array( opt_arg )
    if arr and (len(opt_arg) > block['start']):
        rs = block['start']
        re = len(opt_arg)-1 if -1==block['end'] else min(block['end'], len(opt_arg)-1)
        ri = rs
        while ri <= re:
            out += main( SUB, args, block['tpl'], ri )
            ri += 1
    elif (not arr) and (block['start'] == block['end']):
        out = main( SUB, args, block['tpl'], None )
    
    return out

def non_terminal( SUB, args, symbol, index=None ):
    out = ''
    if SUB and symbol['stpl'] and (symbol['stpl'] in SUB):
        # using sub-template
        if symbol['key']:
            opt_arg = walk( args, symbol['key'] )
            if (opt_arg is None) and (symbol['name'] in args): opt_arg = args[symbol['name']]
        else:
            opt_arg = walk( args, [symbol['name']] )
        
        if (index is not None) and is_array(opt_arg):
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
            out = optional_block( SUB, tpl_args, tpl, None )
    else:
        # plain symbol argument
        if symbol['key']:
            opt_arg = walk( args, symbol['key'] )
            if (opt_arg is None) and (symbol['name'] in args): opt_arg = args[symbol['name']]
        else:
            opt_arg = walk( args, [symbol['name']] )
        # default value if missing
        if is_array(opt_arg):
            opt_arg = opt_arg[index] if index is not None else opt_arg[symbol['start']]
        out = symbol['dval'] if (opt_arg is None) and (symbol['dval'] is not None) else str(opt_arg)
    
    return out

def main( SUB, args, tpl, index=None ):
    out = ''
    while tpl:
        tt = tpl.node['type']
        out += (optional_block( SUB, args, tpl.node, index ) if -1 == tt else (non_terminal( SUB, args, tpl.node, index ) if 1 == tt else tpl.node['val']))
        tpl = tpl.next
    return out


class GrammarTemplate:
    """
    GrammarTemplate for Python,
    https://github.com/foo123/GrammarTemplate
    """
    
    VERSION = '2.0.0'
    

    #defaultDelims = ['<','>','[',']',':=','?','*','!','|','{','}']
    defaultDelims = ['<','>','[',']',':=']
    multisplit = multisplit
    main = main
    
    def __init__(self, tpl='', delims=None):
        self.id = None
        self.tpl = None
        # lazy init
        self._args = [ tpl, delims if delims else GrammarTemplate.defaultDelims ]
        self._parsed = False

    def __del__(self):
        self.dispose()
        
    def dispose(self):
        self.id = None
        self.tpl = None
        self._args = None
        self._parsed = None
        return self
    
    def parse(self):
        if self._parsed is False:
            # lazy init
            self._parsed = True
            self.tpl = GrammarTemplate.multisplit( self._args[0], self._args[1] )
            self._args = None
        return self
    
    def render(self, args=None):
        # lazy init
        if self._parsed is False: self.parse( )
        return GrammarTemplate.main( self.tpl[1], {} if None == args else args, self.tpl[0] )



__all__ = ['GrammarTemplate']

