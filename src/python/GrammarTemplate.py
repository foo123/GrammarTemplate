##
#   GrammarTemplate, 
#   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
# 
#   @version: 1.1.0
#   https://github.com/foo123/GrammarTemplate
#
##


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
    

class GrammarTemplate:
    """
    GrammarTemplate for Python,
    https://github.com/foo123/GrammarTemplate
    """
    
    VERSION = '1.1.0'
    
    def multisplit( tpl, delims ):
        IDL = delims[0]
        IDR = delims[1]
        OBL = delims[2]
        OBR = delims[3]
        lenIDL = len(IDL)
        lenIDR = len(IDR)
        lenOBL = len(OBL)
        lenOBR = len(OBR)
        ESC = '\\'
        OPT = '?'
        OPTR = '*'
        NEG = '!'
        DEF = '|'
        REPL = '{'
        REPR = '}'
        default_value = None
        negative = 0
        optional = 0
        rest = 0
        l = len(tpl)
        i = 0
        a = [[], None, None, 0, 0, 0, 0, None]
        stack = []
        s = ''
        escaped = False
        while i < l:
            
            ch = tpl[i]
            if ESC == ch:
                escaped = not escaped
                i += 1
                
            if IDL == tpl[i:i+lenIDL]:
                if escaped:
                    s += IDL
                    i += lenIDL
                    escaped = False
                    continue
            
                i += lenIDL
                if len(s): a[0].append([0, s])
                s = ''
            
            elif IDR == tpl[i:i+lenIDR]:
                if escaped:
                    s += IDR
                    i += lenIDR
                    escaped = False
                    continue
            
                i += lenIDR
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
                
                p = argument.find('.')
                if -1 < p:
                    nested = argument.split('.')
                else:
                    nested = None
            
                if optional and not a[3]:
                    a[1] = argument
                    a[2] = nested
                    a[3] = optional
                    a[4] = negative
                    a[5] = start_i
                    a[6] = end_i
                    # handle multiple optional arguments for same optional block
                    a[7] = [[argument,negative,start_i,end_i,nested]]
                elif optional:
                    # handle multiple optional arguments for same optional block
                    a[7].append([argument,negative,start_i,end_i,nested])
                elif (not optional) and (a[1] is None):
                    a[1] = argument
                    a[2] = nested
                    a[3] = 0
                    a[4] = negative
                    a[5] = start_i
                    a[6] = end_i
                    a[7] = [[argument,negative,start_i,end_i,nested]]
                a[0].append([1, argument, nested, default_value, optional, negative, start_i, end_i])
            
            elif OBL == tpl[i:i+lenOBL]:
                if escaped:
                    s += OBL
                    i += lenOBL
                    escaped = False
                    continue
            
                i += lenOBL
                # optional block
                if len(s): a[0].append([0, s])
                s = ''
                stack.append(a)
                a = [[], None, None, 0, 0, 0, 0, None]
            
            elif OBR == tpl[i:i+lenOBR]:
                if escaped:
                    s += OBR
                    i += lenOBR
                    escaped = False
                    continue
            
                i += lenOBR
                b = a
                a = stack.pop(-1)
                if len(s): b[0].append([0, s])
                s = ''
                a[0].append([-1, b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[0]])
            else:
                if ESC == ch:
                    s += ch
                else:
                    s += tpl[i]
                    i += 1
        
        if len(s): a[0].append([0, s])
        return a[0]

    #defaultDelims = ['<','>','[',']','?','*','!','|','{','}']
    defaultDelims = ['<','>','[',']']
    
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
        if self._parsed is False:
            # lazy init
            self.parse( )
        
        if None == args: args = { }
        tpl = self.tpl
        l = len(tpl)
        stack = []
        rarg = None
        ri = 0
        out = ''
        i = 0
        while i < l or len(stack):
            if i >= l:
                p = stack.pop(-1)
                tpl = p[0]
                i = p[1]
                l = p[2]
                rarg = p[3]
                ri = p[4]
                continue
            
            t = tpl[ i ]
            tt = t[ 0 ]
            s = t[ 1 ]
            
            if -1 == tt:
                
                # optional block
                opts_vars = t[ 7 ]
                if opts_vars and len(opts_vars):
                    
                    render = True
                    for opt_v in opts_vars:
                        opt_arg = walk( args, opt_v[4] ) if opt_v[4] else (args[opt_v[0]] if opt_v[0] in args else None)
                        if ((0 == opt_v[1]) and (opt_arg is None)) or ((1 == opt_v[1]) and (opt_arg is not None)):
                            render = False
                            break
                    
                    if render:
                        
                        if 1 == t[ 4 ]:
                            stack.append([tpl, i+1, l, rarg, ri])
                            tpl = t[ 8 ]
                            i = 0
                            l = len(tpl)
                            rarg = None
                            ri = 0
                            continue
                        
                        else:
                            opt_arg = walk( args, t[2] ) if t[2] else args[s]
                            arr = is_array( opt_arg )
                            if arr and (t[5] != t[6]) and len(opt_arg) > t[ 5 ]:
                                rs = t[ 5 ]
                                re = len(opt_arg)-1 if -1 == t[ 6 ] else min(t[ 6 ], len(opt_arg)-1)
                                if re >= rs:
                                    stack.append([tpl, i+1, l, rarg, ri])
                                    tpl = t[ 8 ]
                                    i = 0
                                    l = len(tpl)
                                    rarg = s
                                    for ri in range(re,rs,-1): stack.append([tpl, 0, l, rarg, ri])
                                    ri = rs
                                    continue
                                    
                            elif (not arr) and (t[5] == t[6]):
                                stack.append([tpl, i+1, l, rarg, ri])
                                tpl = t[ 8 ]
                                i = 0
                                l = len(tpl)
                                rarg = s
                                ri = 0
                                continue
            
            elif 1 == tt:
                # default value if missing
                opt_arg = walk( args, t[2] ) if t[2] else (args[s] if s in args else None)
                out += str(t[3]) if (opt_arg is None) and t[ 3 ] is not None else (str(opt_arg[(t[6] if t[6]==t[7] else ri)] if s == rarg else opt_arg[t[6]]) if is_array(opt_arg) else str(opt_arg))
            
            else: #if 0 == tt
                out += s
            
            i += 1
        
        return out



__all__ = ['GrammarTemplate']

