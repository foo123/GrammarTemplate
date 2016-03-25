##
#   GrammarTemplate, 
#   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
# 
#   @version: 1.0.0
#   https://github.com/foo123/GrammarTemplate
#
##


def is_array( v ):
    return isinstance(v, (list,tuple))
    

class GrammarTemplate:
    """
    GrammarTemplate for Python,
    https://github.com/foo123/GrammarTemplate
    """
    
    VERSION = '1.0.0'
    
    def multisplit( tpl, delims ):
        IDL = delims[0]
        IDR = delims[1]
        OBL = delims[2]
        OBR = delims[3]
        lenIDL = len(IDL)
        lenIDR = len(IDR)
        lenOBL = len(OBL)
        lenOBR = len(OBR)
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
        a = [[], None, 0, 0, 0, 0, None]
        stack = []
        s = ''
        while i < l:
            
            if IDL == tpl[i:i+lenIDL]:
                i += lenIDL
                if len(s): a[0].append([0, s])
                s = ''
            
            elif IDR == tpl[i:i+lenIDR]:
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
                
                if optional and not a[2]:
                    a[1] = argument
                    a[2] = optional
                    a[3] = negative
                    a[4] = start_i
                    a[5] = end_i
                    # handle multiple optional arguments for same optional block
                    a[6] = [[argument,negative,start_i,end_i]]
                elif optional:
                    # handle multiple optional arguments for same optional block
                    a[6].append([argument,negative,start_i,end_i])
                elif (not optional) and (a[1] is None):
                    a[1] = argument
                    a[2] = 0
                    a[3] = negative
                    a[4] = start_i
                    a[5] = end_i
                    a[6] = [[argument,negative,start_i,end_i]]
                a[0].append([1, argument, default_value, optional, negative, start_i, end_i])
            
            elif OBL == tpl[i:i+lenOBL]:
                i += lenOBL
                # optional block
                if len(s): a[0].append([0, s])
                s = ''
                stack.append(a)
                a = [[], None, 0, 0, 0, 0, None]
            
            elif OBR == tpl[i:i+lenOBR]:
                i += lenOBR
                b = a
                a = stack.pop(-1)
                if len(s): b[0].append([0, s])
                s = ''
                a[0].append([-1, b[1], b[2], b[3], b[4], b[5], b[6], b[0]])
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
    
    def render(self, args=None):
        if self._parsed is False:
            # lazy init
            self.tpl = GrammarTemplate.multisplit( self._args[0], self._args[1] )
            self._args = None
            self._parsed = True
        
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
                opts_vars = t[ 6 ]
                if opts_vars and len(opts_vars):
                    
                    render = True
                    for opt_v in opts_vars:
                        if (0 == opt_v[1] and (opt_v[0] not in args)) or (1 == opt_v[1] and (opt_v[0] in args)):
                            render = False
                            break
                    
                    if render:
                        
                        if 1 == t[ 3 ]:
                            stack.append([tpl, i+1, l, rarg, ri])
                            tpl = t[ 7 ]
                            i = 0
                            l = len(tpl)
                            rarg = None
                            ri = 0
                            continue
                        
                        else:
                            arr = is_array( args[s] )
                            if arr and (t[4] != t[5]) and len(args[s]) > t[ 4 ]:
                                rs = t[ 4 ]
                                re = len(args[s])-1 if -1 == t[ 5 ] else min(t[ 5 ], len(args[s])-1)
                                if re >= rs:
                                    stack.append([tpl, i+1, l, rarg, ri])
                                    tpl = t[ 7 ]
                                    i = 0
                                    l = len(tpl)
                                    rarg = s
                                    for ri in range(re,rs,-1): stack.append([tpl, 0, l, rarg, ri])
                                    ri = rs
                                    continue
                                    
                            elif (not arr) and (t[4] == t[5]):
                                stack.append([tpl, i+1, l, rarg, ri])
                                tpl = t[ 7 ]
                                i = 0
                                l = len(tpl)
                                rarg = s
                                ri = 0
                                continue
            
            elif 1 == tt:
                #TODO: handle nested/structured/deep arguments
                # default value if missing
                out += str(t[2]) if (s not in args) and t[ 2 ] is not None else (str(args[s][(t[5] if t[5]==t[6] else ri)] if s == rarg else args[s][t[5]]) if is_array(args[ s ]) else str(args[s]))
            
            else: #if 0 == tt
                out += s
            
            i += 1
            #if i >= l and len(stack):
            #    p = stack.pop(-1)
            #    tpl = p[0]
            #    i = p[1]
            #    l = p[2]
            #    rarg = p[3]
            #    ri = p[4]
        
        return out



__all__ = ['GrammarTemplate']

