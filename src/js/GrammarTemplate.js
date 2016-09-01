/**
*   GrammarTemplate, 
*   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
* 
*   @version: 1.1.0
*   https://github.com/foo123/GrammarTemplate
*
**/
!function( root, name, factory ){
"use strict";
if ( ('undefined'!==typeof Components)&&('object'===typeof Components.classes)&&('object'===typeof Components.classesByID)&&Components.utils&&('function'===typeof Components.utils['import']) ) /* XPCOM */
    (root.$deps = root.$deps||{}) && (root.EXPORTED_SYMBOLS = [name]) && (root[name] = root.$deps[name] = factory.call(root));
else if ( ('object'===typeof module)&&module.exports ) /* CommonJS */
    (module.$deps = module.$deps||{}) && (module.exports = module.$deps[name] = factory.call(root));
else if ( ('undefined'!==typeof System)&&('function'===typeof System.register)&&('function'===typeof System['import']) ) /* ES6 module */
    System.register(name,[],function($__export){$__export(name, factory.call(root));});
else if ( ('function'===typeof define)&&define.amd&&('function'===typeof require)&&('function'===typeof require.specified)&&require.specified(name) /*&& !require.defined(name)*/ ) /* AMD */
    define(name,['module'],function(module){factory.moduleUri = module.uri; return factory.call(root);});
else if ( !(name in root) ) /* Browser/WebWorker/.. */
    (root[name] = factory.call(root)||1)&&('function'===typeof(define))&&define.amd&&define(function(){return root[name];} );
}(  /* current root */          this, 
    /* module name */           "GrammarTemplate",
    /* module factory */        function ModuleFactory__GrammarTemplate( undef ){
"use strict";

var PROTO = 'prototype', HAS = 'hasOwnProperty', toString = Object[PROTO].toString,
    CHAR = 'charAt', CHARCODE = 'charCodeAt',
    trim_re = /^\s+|\s+$/g,
    trim = String[PROTO].trim
        ? function( s ){ return s.trim(); }
        : function( s ){ return s.replace(trim_re, ''); }
;

function is_array( o )
{
    return o instanceof Array || '[object Array]' === toString.call(o);
}
function walk( obj, keys )
{
    var o = obj, l = keys.length, i = 0, k;
    while( i < l )
    {
        k = keys[i++];
        if ( o && (null != o[k]) ) o = o[k];
        else return null;
    }
    return o;
}

function GrammarTemplate( tpl, delims )
{
    var self = this;
    if ( !(self instanceof GrammarTemplate) ) return new GrammarTemplate(tpl, delims);
    self.id = null;
    self.tpl = null;
    // lazy init
    self._args = [tpl||'', delims||GrammarTemplate.defaultDelims];
    self._parsed = false;
};
GrammarTemplate.VERSION = '1.1.0';
GrammarTemplate.defaultDelims = ['<','>','[',']'/*,'?','*','!','|','{','}'*/];
GrammarTemplate.multisplit = function multisplit( tpl, delims ) {
    var IDL = delims[0], IDR = delims[1], OBL = delims[2], OBR = delims[3],
        lenIDL = IDL.length, lenIDR = IDR.length, lenOBL = OBL.length, lenOBR = OBR.length,
        ESC = '\\', OPT = '?', OPTR = '*', NEG = '!', DEF = '|', REPL = '{', REPR = '}',
        default_value = null, negative = 0, optional = 0, nested, start_i, end_i,
        argument, p, stack, c, a, b, s, l = tpl.length, i, j, jl, escaped, ch;
    
    i = 0; a = [[], null, null, 0, 0, 0, 0, null]; stack = []; s = ''; escaped = false;
    while( i < l )
    {
        ch = tpl[CHAR](i);
        if ( ESC === ch )
        {
            escaped = !escaped;
            i += 1;
        }
        
        if ( IDL === tpl.substr(i,lenIDL) )
        {
            if ( escaped )
            {
                s += IDL;
                i += lenIDL;
                escaped = false;
                continue;
            }
            
            i += lenIDL;
            if ( s.length ) a[0].push([0, s]);
            s = '';
        }
        else if ( IDR === tpl.substr(i,lenIDR) )
        {
            if ( escaped )
            {
                s += IDR;
                i += lenIDR;
                escaped = false;
                continue;
            }
            
            i += lenIDR;
            // argument
            argument = s; s = '';
            if ( -1 < (p=argument.indexOf(DEF)) )
            {
                default_value = argument.slice( p+1 );
                argument = argument.slice( 0, p );
            }
            else
            {
                default_value = null;
            }
            c = argument[CHAR](0);
            if ( OPT === c || OPTR === c )
            {
                optional = 1;
                if ( OPTR === c )
                {
                    start_i = 1;
                    end_i = -1;
                }
                else
                {
                    start_i = 0;
                    end_i = 0;
                }
                argument = argument.slice(1);
                if ( NEG === argument[CHAR](0) )
                {
                    negative = 1;
                    argument = argument.slice(1);
                }
                else
                {
                    negative = 0;
                }
            }
            else if ( REPL === c )
            {
                s = ''; j = 1; jl = argument.length;
                while ( j < jl && REPR !== argument[CHAR](j) ) s += argument[CHAR](j++);
                argument = argument.slice( j+1 );
                s = s.split(',');
                if ( s.length > 1 )
                {
                    start_i = trim(s[0]);
                    start_i = start_i.length ? parseInt(start_i,10)||0 : 0;
                    end_i = trim(s[1]);
                    end_i = end_i.length ? parseInt(end_i,10)||0 : -1;
                    optional = 1;
                }
                else
                {
                    start_i = trim(s[0]);
                    start_i = start_i.length ? parseInt(start_i,10)||0 : 0;
                    end_i = start_i;
                    optional = 0;
                }
                s = '';
                negative = 0;
            }
            else
            {
                optional = 0;
                negative = 0;
                start_i = 0;
                end_i = 0;
            }
            if ( negative && (null === default_value) ) default_value = '';
            
            nested = -1 < argument.indexOf('.') ? argument.split('.') : null;
            
            if ( optional && !a[3] )
            {
                a[1] = argument;
                a[2] = nested;
                a[3] = optional;
                a[4] = negative;
                a[5] = start_i;
                a[6] = end_i;
                // handle multiple optional arguments for same optional block
                a[7] = [[argument,negative,start_i,end_i,nested]];
            }
            else if( optional )
            {
                // handle multiple optional arguments for same optional block
                a[7].push([argument,negative,start_i,end_i,nested]);
            }
            else if ( !optional && (null === a[1]) )
            {
                a[1] = argument;
                a[2] = nested;
                a[3] = 0;
                a[4] = negative;
                a[5] = start_i;
                a[6] = end_i;
                a[7] = [[argument,negative,start_i,end_i,nested]];
            }
            a[0].push([1, argument, nested, default_value, optional, negative, start_i, end_i]);
        }
        else if ( OBL === tpl.substr(i,lenOBL) )
        {
            if ( escaped )
            {
                s += OBL;
                i += lenOBL;
                escaped = false;
                continue;
            }
            
            i += lenOBL;
            // optional block
            if ( s.length ) a[0].push([0, s]);
            s = '';
            stack.push(a);
            a = [[], null, null, 0, 0, 0, 0, null];
        }
        else if ( OBR === tpl.substr(i,lenOBR) )
        {
            if ( escaped )
            {
                s += OBR;
                i += lenOBR;
                escaped = false;
                continue;
            }
            
            i += lenOBR;
            b = a; a = stack.pop( );
            if ( s.length ) b[0].push([0, s]);
            s = '';
            a[0].push([-1, b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[0]]);
        }
        else
        {
            if ( ESC === ch ) s += ch;
            else s += tpl[CHAR](i++);
        }
    }
    if ( s.length ) a[0].push([0, s]);
    return a[0];
};
GrammarTemplate[PROTO] = {
    constructor: GrammarTemplate
    
    ,id: null
    ,tpl: null
    ,_parsed: false
    ,_args: null
    
    ,dispose: function( ) {
        var self = this;
        self.id = null;
        self.tpl = null;
        self._args = null;
        self._parsed = null;
        return self;
    }
    ,parse: function( ) {
        var self = this;
        if ( false === self._parsed )
        {
            // lazy init
            self._parsed = true;
            self.tpl = GrammarTemplate.multisplit( self._args[0], self._args[1] );
            self._args = null;
        }
        return self;
    }
    ,render: function( args ) {
        var self = this;
        if ( false === self._parsed )
        {
            // lazy init
            self.parse( );
        }
        
        args = args || { };
        var tpl = self.tpl, l = tpl.length,
            p, arr, MIN = Math.min,
            i, t, tt, s, rarg = null,
            ri = 0, rs, re, out = '',
            opts_vars, render, oi, ol, opt_v, opt_arg,
            // pre-allocate stack for efficiency
            stack = new Array(200), slen = 0
        ;
        i = 0;
        while ( i < l || slen )
        {
            if ( i >= l )
            {
                p = stack[--slen];
                tpl = p[0]; i = p[1]; l = p[2];
                rarg = p[3]||null; ri = p[4]||0;
                continue;
            }
            
            t = tpl[ i ]; tt = t[ 0 ]; s = t[ 1 ];
            if ( -1 === tt )
            {
                // optional block
                opts_vars = t[ 7 ];
                if ( opts_vars && opts_vars.length )
                {
                    render = true;
                    for(oi=0,ol=opts_vars.length; oi<ol; oi++)
                    {
                        opt_v = opts_vars[oi];
                        opt_arg = opt_v[4] ? walk( args, opt_v[4] ) : args[opt_v[0]];
                        if ( (0 === opt_v[1] && null == opt_arg/*!args[HAS](opt_v[0])*/) ||
                            (1 === opt_v[1] && null != opt_arg/*args[HAS](opt_v[0])*/)
                        )
                        {
                            render = false;
                            break;
                        }
                    }
                    if ( render )
                    {
                        if ( 1 === t[ 4 ] )
                        {
                            stack[slen++] = [tpl, i+1, l, rarg, ri];
                            tpl = t[ 8 ]; i = 0; l = tpl.length;
                            rarg = null; ri = 0;
                            continue;
                        }
                        else
                        {
                            opt_arg = t[2] ? walk( args, t[2] )/*nested key*/ : args[s]/*plain key*/;
                            arr = is_array( opt_arg );
                            if ( arr && (t[5] !== t[6]) && opt_arg.length > t[ 5 ] )
                            {
                                rs = t[ 5 ];
                                re = -1 === t[ 6 ] ? opt_arg.length-1 : MIN(t[ 6 ], opt_arg.length-1);
                                if ( re >= rs )
                                {
                                    stack[slen++] = [tpl, i+1, l, rarg, ri];
                                    tpl = t[ 8 ]; i = 0; l = tpl.length;
                                    rarg = s;
                                    for(ri=re; ri>rs; ri--) stack[slen++] = [tpl, 0, l, rarg, ri];
                                    ri = rs;
                                    continue;
                                }
                            }
                            else if ( !arr && (t[5] === t[6]) )
                            {
                                stack[slen++] = [tpl, i+1, l, rarg, ri];
                                tpl = t[ 8 ]; i = 0; l = tpl.length;
                                rarg = s; ri = 0;
                                continue;
                            }
                        }
                    }
                }
            }
            else if ( 1 === tt )
            {
                // default value if missing
                opt_arg = t[2] ? walk( args, t[2] )/*nested key*/ : args[s]/*plain key*/;
                out += (null == opt_arg/*!args[HAS](s)*/) && (null !== t[ 3 ])
                    ? t[ 3 ]
                    : (is_array(opt_arg)
                    ? (s === rarg
                    ? opt_arg[t[6]===t[7]?t[6]:ri]
                    : opt_arg[t[6]])
                    : opt_arg)
                ;
            }
            else /*if ( 0 === tt )*/
            {
                out += s;
            }
            i++;
        }
        return out;
    }
};

// export it
return GrammarTemplate;
});
