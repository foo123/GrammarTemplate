/**
*   GrammarTemplate, 
*   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
* 
*   @version: 2.1.0
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
        : function( s ){ return s.replace(trim_re, ''); },
    GUID = 0;

function guid( )
{
    return ''+new Date().getTime()+'--'+(++GUID);
}
function is_array( o )
{
    return o instanceof Array || '[object Array]' === toString.call(o);
}
function walk( obj, keys, keys_alt, obj_alt )
{
    var o, l, i, k, found = 0;
    if ( keys )
    {
        o = obj;
        l = keys.length;
        i = 0;
        found = 1;
        while( i < l )
        {
            k = keys[i++];
            if ( (null != o) && (null != o[k]) )
            {
                o = o[k];
            }
            else
            {
                found = 0;
                break;
            }
        }
    }
    if ( !found && keys_alt )
    {
        o = obj;
        l = keys_alt.length;
        i = 0;
        found = 1;
        while( i < l )
        {
            k = keys_alt[i++];
            if ( (null != o) && (null != o[k]) )
            {
                o = o[k];
            }
            else
            {
                found = 0;
                break;
            }
        }
    }
    if ( !found && (null != obj_alt) && (obj_alt !== obj) )
    {
        if ( keys )
        {
            o = obj_alt;
            l = keys.length;
            i = 0;
            found = 1;
            while( i < l )
            {
                k = keys[i++];
                if ( (null != o) && (null != o[k]) )
                {
                    o = o[k];
                }
                else
                {
                    found = 0;
                    break;
                }
            }
        }
        if ( !found && keys_alt )
        {
            o = obj_alt;
            l = keys_alt.length;
            i = 0;
            found = 1;
            while( i < l )
            {
                k = keys_alt[i++];
                if ( (null != o) && (null != o[k]) )
                {
                    o = o[k];
                }
                else
                {
                    found = 0;
                    break;
                }
            }
        }
    }
    return found ? o : null;
}
function StackEntry( stack, value )
{
    this.prev = stack || null;
    this.value = value || null;
}
function TplEntry( node, tpl )
{
    if ( tpl ) tpl.next = this;
    this.node = node || null;
    this.prev = tpl || null;
    this.next = null;
}

function multisplit( tpl, delims )
{
    var IDL = delims[0], IDR = delims[1],
        OBL = delims[2], OBR = delims[3], TPL = delims[4],
        lenIDL = IDL.length, lenIDR = IDR.length,
        lenOBL = OBL.length, lenOBR = OBR.length, lenTPL = TPL.length,
        ESC = '\\', OPT = '?', OPTR = '*', NEG = '!', DEF = '|',
        REPL = '{', REPR = '}', DOT = '.', REF = ':',
        default_value = null, negative = 0, optional = 0, nested, start_i, end_i, template,
        argument, p, stack, c, a, b, s, l = tpl.length, i, j, jl, escaped, ch,
        subtpl, arg_tpl, cur_tpl, start_tpl, cur_arg, opt_args,
        roottpl, block, cur_block, prev_arg, prev_opt_args;
    
    a = new TplEntry({type: 0, val: ''});
    cur_arg = {
        type    : 1,
        name    : null,
        key     : null,
        stpl    : null,
        dval    : null,
        opt     : 0,
        neg     : 0,
        start   : 0,
        end     : 0
    };
    roottpl = a; block = null;
    opt_args = null; subtpl = {}; cur_tpl = null; arg_tpl = {}; start_tpl = null;
    stack = null; s = ''; escaped = false;
    
    i = 0;
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
            i += lenIDL;
            
            if ( escaped )
            {
                s += IDL;
                escaped = false;
                continue;
            }
            
            if ( s.length )
            {
                if ( 0 === a.node.type ) a.node.val += s;
                else a = new TplEntry({type: 0, val: s}, a);
            }
            s = '';
        }
        else if ( IDR === tpl.substr(i,lenIDR) )
        {
            i += lenIDR;
            
            if ( escaped )
            {
                s += IDR;
                escaped = false;
                continue;
            }
            
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
            
            template = -1 < argument.indexOf(REF) ? argument.split(REF) : [argument,null];
            argument = template[0]; template = template[1];
            nested = -1 < argument.indexOf(DOT) ? argument.split(DOT) : null;
            
            if ( cur_tpl && !arg_tpl[cur_tpl] ) arg_tpl[cur_tpl] = {};
            
            if ( TPL+OBL === tpl.substr(i,lenTPL+lenOBL) )
            {
                // template definition
                i += lenTPL;
                template = template&&template.length ? template : 'grtpl--'+guid( );
                start_tpl = template;
                if ( cur_tpl && argument.length)
                    arg_tpl[cur_tpl][argument] = template;
            }
            
            if ( !argument.length ) continue; // template definition only
            
            if ( (null==template) && cur_tpl && arg_tpl[cur_tpl] && arg_tpl[cur_tpl][argument] )
                template = arg_tpl[cur_tpl][argument];
            
            if ( optional && !cur_arg.opt )
            {
                cur_arg.name = argument;
                cur_arg.key = nested;
                cur_arg.stpl = template;
                cur_arg.dval = default_value;
                cur_arg.opt = optional;
                cur_arg.neg = negative;
                cur_arg.start = start_i;
                cur_arg.end = end_i;
                // handle multiple optional arguments for same optional block
                opt_args = new StackEntry(null, [argument,nested,negative,start_i,end_i]);
            }
            else if ( optional )
            {
                // handle multiple optional arguments for same optional block
                opt_args = new StackEntry(opt_args, [argument,nested,negative,start_i,end_i]);
            }
            else if ( !optional && (null === cur_arg.name) )
            {
                cur_arg.name = argument;
                cur_arg.key = nested;
                cur_arg.stpl = template;
                cur_arg.dval = default_value;
                cur_arg.opt = 0;
                cur_arg.neg = negative;
                cur_arg.start = start_i;
                cur_arg.end = end_i;
                // handle multiple optional arguments for same optional block
                opt_args = new StackEntry(null, [argument,nested,negative,start_i,end_i]);
            }
            a = new TplEntry({
                type    : 1,
                name    : argument,
                key     : nested,
                stpl    : template,
                dval    : default_value,
                opt     : optional,
                start   : start_i,
                end     : end_i
            }, a);
        }
        else if ( OBL === tpl.substr(i,lenOBL) )
        {
            i += lenOBL;
            
            if ( escaped )
            {
                s += OBL;
                escaped = false;
                continue;
            }
            
            // optional block
            if ( s.length )
            {
                if ( 0 === a.node.type ) a.node.val += s;
                else a = new TplEntry({type: 0, val: s}, a);
            }
            s = '';
            stack = new StackEntry(stack, [a, block, cur_arg, opt_args, cur_tpl, start_tpl]);
            if ( start_tpl ) cur_tpl = start_tpl;
            start_tpl = null;
            cur_arg = {
                type    : 1,
                name    : null,
                key     : null,
                stpl    : null,
                dval    : null,
                opt     : 0,
                neg     : 0,
                start   : 0,
                end     : 0
            };
            opt_args = null;
            a = new TplEntry({type: 0, val: ''});
            block = a;
        }
        else if ( OBR === tpl.substr(i,lenOBR) )
        {
            i += lenOBR;
            
            if ( escaped )
            {
                s += OBR;
                escaped = false;
                continue;
            }
            
            b = a;
            cur_block = block;
            prev_arg = cur_arg;
            prev_opt_args = opt_args;
            if ( stack )
            {
                a = stack.value[0];
                block = stack.value[1];
                cur_arg = stack.value[2];
                opt_args = stack.value[3];
                cur_tpl = stack.value[4];
                start_tpl = stack.value[5];
                stack = stack.prev;
            }
            else
            {
                a = null;
            }
            if ( s.length )
            {
                if ( 0 === b.node.type ) b.node.val += s;
                else b = new TplEntry({type: 0, val: s}, b);
            }
            s = '';
            if ( start_tpl )
            {
                subtpl[start_tpl] = new TplEntry({
                    type    : 2,
                    name    : prev_arg.name,
                    key     : prev_arg.key,
                    start   : 0/*cur_arg.start*/,
                    end     : 0/*cur_arg.end*/,
                    opt_args: null/*opt_args*/,
                    tpl     : cur_block
                });
                start_tpl = null;
            }
            else
            {
                a = new TplEntry({
                    type    : -1,
                    name    : prev_arg.name,
                    key     : prev_arg.key,
                    start   : prev_arg.start,
                    end     : prev_arg.end,
                    opt_args: prev_opt_args,
                    tpl     : cur_block
                }, a);
            }
        }
        else
        {
            if ( ESC === ch ) s += ch;
            else s += tpl[CHAR](i++);
        }
    }
    if ( s.length )
    {
        if ( 0 === a.node.type ) a.node.val += s;
        else a = new TplEntry({type: 0, val: s}, a);
    }
    return [roottpl, subtpl];
}

function optional_block( args, block, SUB, FN, index, orig_args )
{
    var opt_vars, opt_v, opt_arg, arr, rs, re, ri, len, block_arg = null, out = '';
    
    if ( -1 === block.type )
    {
        // optional block, check if optional variables can be rendered
        opt_vars = block.opt_args; if ( !opt_vars ) return '';
        while( opt_vars )
        {
            opt_v = opt_vars.value;
            opt_arg = walk( args, opt_v[1], [String(opt_v[0])], orig_args );
            if ( (null === block_arg) && (block.name === opt_v[0]) ) block_arg = opt_arg;
            
            if ( (0 === opt_v[2] && null == opt_arg) ||
                (1 === opt_v[2] && null != opt_arg)
            )
                return '';
            opt_vars = opt_vars.prev;
        }
    }
    else
    {
        block_arg = walk( args, block.key, [String(block.name)], orig_args );
    }
    
    arr = is_array( block_arg ); len = arr ? block_arg.length : -1;
    if ( arr && (len > block.start) )
    {
        for(rs=block.start,re=(-1===block.end?len-1:Math.min(block.end,len-1)),ri=rs; ri<=re; ri++)
            out += main( args, block.tpl, SUB, FN, ri, orig_args );
    }
    else if ( !arr && (block.start === block.end) )
    {
        out = main( args, block.tpl, SUB, FN, null, orig_args );
    }
    return out;
}
function non_terminal( args, symbol, SUB, FN, index, orig_args )
{
    var opt_arg, tpl_args, tpl, out = '', fn;
    if ( symbol.stpl && ((SUB && SUB[symbol.stpl]) || (FN && FN[symbol.stpl]) || (GrammarTemplate.fnGlobal[symbol.stpl])) )
    {
        // using custom function or sub-template
        opt_arg = walk( args, symbol.key, [String(symbol.name)], orig_args );
        
        if ( SUB && SUB[symbol.stpl] )
        {
            // sub-template
            if ( (null != index/* || null != symbol.start*/) && (0 !== index || !symbol.opt) && is_array(opt_arg) )
            {
                opt_arg = opt_arg[/*null != index ?*/ index /*: symbol.start*/];
            }
            if ( (null == opt_arg) && (null !== symbol.dval) )
            {
                // default value if missing
                out = symbol.dval;
            }
            else
            {
                // try to associate sub-template parameters to actual input arguments
                tpl = SUB[symbol.stpl].node; tpl_args = {};
                if ( null != opt_arg )
                {
                    /*if ( opt_arg[HAS](tpl.name) && !opt_arg[HAS](symbol.name) ) tpl_args = opt_arg;
                    else tpl_args[tpl.name] = opt_arg;*/
                    if ( is_array(opt_arg) ) tpl_args[tpl.name] = opt_arg;
                    else tpl_args = opt_arg;
                }
                out = optional_block( tpl_args, tpl, SUB, FN, null, null == orig_args ? args : orig_args );
            }
        }
        else //if ( fn )
        {
            // custom function
            fn = FN && FN[symbol.stpl] ? FN[symbol.stpl] : (GrammarTemplate.fnGlobal[symbol.stpl] ? GrammarTemplate.fnGlobal[symbol.stpl] : null);
            
            if ( is_array(opt_arg) )
            {
                index = null != index ? index : symbol.start;
                opt_arg = index < opt_arg.length ? opt_arg[index] : null;
            }
            
            opt_arg = "function" === typeof fn ? fn(opt_arg, index, args, orig_args, symbol) : String(fn);
            
            out = (null == opt_arg) && (null !== symbol.dval) ? symbol.dval : String(opt_arg);
        }
    }
    else if ( symbol.opt && (null !== symbol.dval) )
    {
        // boolean optional argument
        out = symbol.dval;
    }
    else
    {
        // plain symbol argument
        opt_arg = walk( args, symbol.key, [String(symbol.name)], orig_args );
        
        // default value if missing
        if ( is_array(opt_arg) )
        {
            index = null != index ? index : symbol.start;
            opt_arg = index < opt_arg.length ? opt_arg[index] : null;
        }
        out = (null == opt_arg) && (null !== symbol.dval) ? symbol.dval : String(opt_arg);
    }
    return out;
}
function main( args, tpl, SUB, FN, index, orig_args )
{
    var tt, out = '';
    while ( tpl )
    {
        tt = tpl.node.type;
        out += (-1 === tt
            ? optional_block( args, tpl.node, SUB, FN, index, orig_args ) /* optional code-block */
            : (1 === tt
            ? non_terminal( args, tpl.node, SUB, FN, /*0 === index ? (tpl.node.opt&&tpl.node.stpl?null:index) : */index, orig_args ) /* non-terminal */
            : tpl.node.val /* terminal */
        ));
        tpl = tpl.next;
    }
    return out;
}


function GrammarTemplate( tpl, delims )
{
    var self = this;
    if ( !(self instanceof GrammarTemplate) ) return new GrammarTemplate(tpl, delims);
    self.id = null;
    self.tpl = null;
    self.fn = {};
    // lazy init
    self._args = [tpl||'', delims||GrammarTemplate.defaultDelims];
};
GrammarTemplate.VERSION = '2.1.0';
GrammarTemplate.defaultDelims = ['<','>','[',']',':='/*,'?','*','!','|','{','}'*/];
GrammarTemplate.fnGlobal = {};
GrammarTemplate.guid = guid;
GrammarTemplate.multisplit = multisplit;
GrammarTemplate.main = main;
GrammarTemplate[PROTO] = {
    constructor: GrammarTemplate
    
    ,id: null
    ,tpl: null
    ,fn: null
    ,_args: null
    
    ,dispose: function( ) {
        var self = this;
        self.id = null;
        self.tpl = null;
        self.fn = null;
        self._args = null;
        return self;
    }
    ,parse: function( ) {
        var self = this;
        if ( (null === self.tpl) && (null !== self._args) )
        {
            // lazy init
            self.tpl = GrammarTemplate.multisplit( self._args[0], self._args[1] );
            self._args = null;
        }
        return self;
    }
    ,render: function( args ) {
        var self = this;
        // lazy init
        if ( null === self.tpl ) self.parse( );
        return GrammarTemplate.main( null==args ? {} : args, self.tpl[0], self.tpl[1], self.fn );
    }
};

// export it
return GrammarTemplate;
});
