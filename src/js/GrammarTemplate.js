/**
*   GrammarTemplate, 
*   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
* 
*   @version: 1.0.0
*   https://github.com/foo123/grammar-template
*
**/
!function( root, name, factory ) {
"use strict";
var m;
if ( ('undefined'!==typeof Components)&&('object'===typeof Components.classes)&&('object'===typeof Components.classesByID)&&Components.utils&&('function'===typeof Components.utils['import']) ) /* XPCOM */
    (root.EXPORTED_SYMBOLS = [ name ]) && (root[ name ] = factory.call( root ));
else if ( ('object'===typeof module)&&module.exports ) /* CommonJS */
    module.exports = factory.call( root );
else if ( ('function'===typeof(define))&&define.amd&&('function'===typeof(require))&&('function'===typeof(require.specified))&&require.specified(name) ) /* AMD */
    define(name,['require','exports','module'],function( ){return factory.call( root );});
else if ( !(name in root) ) /* Browser/WebWorker/.. */
    (root[ name ] = (m=factory.call( root )))&&('function'===typeof(define))&&define.amd&&define(function( ){return m;} );
}(  /* current root */          this, 
    /* module name */           "GrammarTemplate",
    /* module factory */        function( exports, undef ) {
"use strict";

var PROTO = 'prototype', HAS = 'hasOwnProperty', 
    toString = Object[PROTO].toString,
    CHAR = 'charAt', CHARCODE = 'charCodeAt',
    trim_re = /^\s+|\s+$/g,
    trim = String[PROTO].trim
        ? function( s ){ return s.trim(); }
        : function( s ){ return s.replace(trim_re, ''); },
    GrammarTemplate
;
function is_array( o )
{
    return o instanceof Array || '[object Array]' === toString.call(o);
}

GrammarTemplate = function GrammarTemplate( tpl, delims ) {
    var self = this;
    if ( !(self instanceof GrammarTemplate) ) return new GrammarTemplate(tpl, delims);
    self.id = null;
    self.tpl = null;
    // lazy init
    self._args = [tpl||'', delims||GrammarTemplate.defaultDelims];
    self._parsed = false;
};
GrammarTemplate.VERSION = '1.0.0';
GrammarTemplate.defaultDelims = ['<','>','[',']'/*,'?','*','!','|','{','}'*/];
GrammarTemplate.multisplit = function multisplit( tpl, delims ) {
    var IDL = delims[0], IDR = delims[1], OBL = delims[2], OBR = delims[3],
        lenIDL = IDL.length, lenIDR = IDR.length, lenOBL = OBL.length, lenOBR = OBR.length,
        OPT = '?', OPTR = '*', NEG = '!', DEF = '|', REPL = '{', REPR = '}',
        default_value = null, negative = 0, optional = 0, start_i, end_i,
        argument, p, stack, c, a, b, s, l = tpl.length, i, j, jl;
    i = 0; a = [[], null, 0, 0, 0, 0, null]; stack = []; s = '';
    while( i < l )
    {
        if ( IDL === tpl.substr(i,lenIDL) )
        {
            i += lenIDL;
            if ( s.length ) a[0].push([0, s]);
            s = '';
        }
        else if ( IDR === tpl.substr(i,lenIDR) )
        {
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
            if ( negative && null === default_value ) default_value = '';
            
            if ( optional && !a[2] )
            {
                a[1] = argument;
                a[2] = optional;
                a[3] = negative;
                a[4] = start_i;
                a[5] = end_i;
                // handle multiple optional arguments for same optional block
                a[6] = [[argument,negative,start_i,end_i]];
            }
            else if( optional )
            {
                // handle multiple optional arguments for same optional block
                a[6].push([argument,negative,start_i,end_i]);
            }
            else if ( !optional && (null === a[1]) )
            {
                a[1] = argument;
                a[2] = 0;
                a[3] = negative;
                a[4] = start_i;
                a[5] = end_i;
                a[6] = [[argument,negative,start_i,end_i]];
            }
            a[0].push([1, argument, default_value, optional, negative, start_i, end_i]);
        }
        else if ( OBL === tpl.substr(i,lenOBL) )
        {
            i += lenOBL;
            // optional block
            if ( s.length ) a[0].push([0, s]);
            s = '';
            stack.push(a);
            a = [[], null, 0, 0, 0, 0, null];
        }
        else if ( OBR === tpl.substr(i,lenOBR) )
        {
            i += lenOBR;
            b = a; a = stack.pop( );
            if ( s.length ) b[0].push([0, s]);
            s = '';
            a[0].push([-1, b[1], b[2], b[3], b[4], b[5], b[6], b[0]]);
        }
        else
        {
            s += tpl[CHAR](i++);
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
    ,render: function( args ) {
        var self = this;
        if ( false === self._parsed )
        {
            // lazy init
            self.tpl = GrammarTemplate.multisplit( self._args[0], self._args[1] );
            self._args = null;
            self._parsed = true;
        }
        
        args = args || { };
        var tpl = self.tpl, l = tpl.length,
            stack = [], p, arr, MIN = Math.min,
            i, t, tt, s, rarg = null,
            ri = 0, rs, re, out = '',
            opts_vars, render, oi, ol, opt_v
        ;
        i = 0;
        while ( i < l || stack.length )
        {
            if ( i >= l )
            {
                p = stack.pop( );
                tpl = p[0]; i = p[1]; l = p[2];
                rarg = p[3]||null; ri = p[4]||0;
                continue;
            }
            
            t = tpl[ i ]; tt = t[ 0 ]; s = t[ 1 ];
            if ( -1 === tt )
            {
                // optional block
                opts_vars = t[ 6 ];
                if ( !!opts_vars && opts_vars.length )
                {
                    render = true;
                    for(oi=0,ol=opts_vars.length; oi<ol; oi++)
                    {
                        opt_v = opts_vars[oi];
                        if ( (0 === opt_v[1] && !args[HAS](opt_v[0])) ||
                            (1 === opt_v[1] && args[HAS](opt_v[0]))
                        )
                        {
                            render = false;
                            break;
                        }
                    }
                    if ( render )
                    {
                        if ( 1 === t[ 3 ] )
                        {
                            stack.push([tpl, i+1, l, rarg, ri]);
                            tpl = t[ 7 ]; i = 0; l = tpl.length;
                            rarg = null; ri = 0;
                            continue;
                        }
                        else
                        {
                            arr = is_array( args[s] );
                            if ( arr && (t[4] !== t[5]) && args[s].length > t[ 4 ] )
                            {
                                rs = t[ 4 ];
                                re = -1 === t[ 5 ] ? args[s].length-1 : MIN(t[ 5 ], args[s].length-1);
                                if ( re >= rs )
                                {
                                    stack.push([tpl, i+1, l, rarg, ri]);
                                    tpl = t[ 7 ]; i = 0; l = tpl.length;
                                    rarg = s;
                                    for(ri=re; ri>rs; ri--) stack.push([tpl, 0, l, rarg, ri]);
                                    ri = rs;
                                    continue;
                                }
                            }
                            else if ( !arr && (t[4] === t[5]) )
                            {
                                stack.push([tpl, i+1, l, rarg, ri]);
                                tpl = t[ 7 ]; i = 0; l = tpl.length;
                                rarg = s; ri = 0;
                                continue;
                            }
                        }
                    }
                }
            }
            else if ( 1 === tt )
            {
                //TODO: handle nested/structured/deep arguments
                // default value if missing
                out += !args[HAS](s) && null !== t[ 2 ]
                    ? t[ 2 ]
                    : (is_array(args[ s ])
                    ? (s === rarg
                    ? args[s][t[5]===t[6]?t[5]:ri]
                    : args[s][t[5]])
                    : args[s])
                ;
            }
            else /*if ( 0 === tt )*/
            {
                out += s;
            }
            i++;
            /*if ( i >= l && stack.length )
            {
                p = stack.pop( );
                tpl = p[0]; i = p[1]; l = p[2];
                rarg = p[3]||null; ri = p[4]||0;
            }*/
        }
        return out;
    }
};

// export it
return GrammarTemplate;
});
