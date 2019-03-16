/**
*   GrammarTemplate, 
*   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
* 
*   @version: 3.0.0
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
}(  /* current root */          'undefined' !== typeof self ? self : this, 
    /* module name */           "GrammarTemplate",
    /* module factory */        function ModuleFactory__GrammarTemplate( undef ){
"use strict";

var PROTO = 'prototype',
    CHAR = 'charAt', CHARCODE = 'charCodeAt',
    hasOwnProperty = Object[PROTO].hasOwnProperty,
    toString = Object[PROTO].toString,
    trim_re = /^\s+|\s+$/g,
    trim = String[PROTO].trim
        ? function( s ){ return s.trim(); }
        : function( s ){ return s.replace(trim_re, ''); }
;

function HAS( o, x )
{
    return o && hasOwnProperty.call(o, x) ? 1 : 0;
}
function pad( s, n, z, pad_right )
{
    var ps = String(s);
    z = z || '0';
    if ( pad_right ) while ( ps.length < n ) ps += z;
    else while ( ps.length < n ) ps = z + ps;
    return ps;
}
function guid( )
{
    guid.GUID += 1;
    return pad(new Date().getTime().toString(16),12)+'--'+pad(guid.GUID.toString(16),4);
}
guid.GUID = 0;
function is_array( x )
{
    return (x instanceof Array) || ('[object Array]' === toString.call(x));
}
/*function is_string( x )
{
    return (x instanceof String) || ('[object String]' === toString.call(x));
}*/
function compute_alignment( s, i, l )
{
    var alignment = '', c;
    while ( i < l )
    {
        c = s[CHAR](i);
        if ( (" " === c) || ("\r" === c) || ("\t" === c) || ("\v" === c) || ("\0" === c) )
        {
            alignment += c;
            i += 1;
        }
        else
        {
            break;
        }
    }
    return alignment;
}
function align( s, alignment )
{
    var aligned, c, i, l = s.length;
    if ( l && alignment.length )
    {
        aligned = '';
        for(i=0; i<l; i++)
        {
            c = s[CHAR](i);
            aligned += c;
            if ( "\n" === c ) aligned += alignment;
        }
    }
    else
    {
        aligned = s;
    }
    return aligned;
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

function multisplit( tpl, delims, postop )
{
    var IDL = delims[0], IDR = delims[1],
        OBL = delims[2], OBR = delims[3],
        lenIDL = IDL.length, lenIDR = IDR.length,
        lenOBL = OBL.length, lenOBR = OBR.length,
        ESC = '\\', OPT = '?', OPTR = '*', NEG = '!', DEF = '|', COMMENT = '#',
        TPL = ':=', REPL = '{', REPR = '}', DOT = '.', REF = ':', ALGN = '@', //NOTALGN = '&',
        COMMENT_CLOSE = COMMENT+OBR,
        default_value = null, negative = 0, optional = 0,
        nested, aligned = 0, localised = 0, start_i, end_i, template,
        argument, p, stack, c, a, b, s, l = tpl.length, i, j, jl,
        subtpl, arg_tpl, cur_tpl, start_tpl, cur_arg, opt_args,
        roottpl, block, cur_block, prev_arg, prev_opt_args,
        delim1 = [IDL, lenIDL, IDR, lenIDR], delim2 = [OBL, lenOBL, OBR, lenOBR],
        delim_order = [null,0,null,0,null,0,null,0], delim;
    
    postop = true === postop;
    a = new TplEntry({type: 0, val: '', algn: ''});
    cur_arg = {
        type    : 1,
        name    : null,
        key     : null,
        stpl    : null,
        dval    : null,
        opt     : 0,
        neg     : 0,
        algn    : 0,
        loc     : 0,
        start   : 0,
        end     : 0
    };
    roottpl = a; block = null;
    opt_args = null; subtpl = {}; cur_tpl = null; arg_tpl = {}; start_tpl = null;
    
    // hard-coded merge-sort for arbitrary delims parsing based on str len
    if ( delim1[1] < delim1[3] )
    {
        s = delim1[0]; delim1[2] = delim1[0]; delim1[0] = s;
        i = delim1[1]; delim1[3] = delim1[1]; delim1[1] = i;
    }
    if ( delim2[1] < delim2[3] )
    {
        s = delim2[0]; delim2[2] = delim2[0]; delim2[0] = s;
        i = delim2[1]; delim2[3] = delim2[1]; delim2[1] = i;
    }
    start_i = 0; end_i = 0; i = 0;
    while ( (4 > start_i) && (4 > end_i) )
    {
        if ( delim1[start_i+1] < delim2[end_i+1] )
        {
            delim_order[i] = delim2[end_i];
            delim_order[i+1] = delim2[end_i+1];
            end_i += 2;
        }
        else
        {
            delim_order[i] = delim1[start_i];
            delim_order[i+1] = delim1[start_i+1];
            start_i += 2;
        }
        i += 2;
    }
    while ( 4 > start_i )
    {
        delim_order[i] = delim1[start_i];
        delim_order[i+1] = delim1[start_i+1];
        start_i += 2; i += 2;
    }
    while ( 4 > end_i )
    {
        delim_order[i] = delim2[end_i];
        delim_order[i+1] = delim2[end_i+1];
        end_i += 2; i += 2;
    }
    
    stack = null; s = '';
    
    i = 0;
    while( i < l )
    {
        c = tpl[CHAR](i);
        if ( ESC === c )
        {
            s += i+1 < l ? tpl[CHAR](i+1) : '';
            i += 2;
            continue;
        }
        
        delim = null;
        if ( delim_order[0] === tpl.substr(i,delim_order[1]) )
            delim = delim_order[0];
        else if ( delim_order[2] === tpl.substr(i,delim_order[3]) )
            delim = delim_order[2];
        else if ( delim_order[4] === tpl.substr(i,delim_order[5]) )
            delim = delim_order[4];
        else if ( delim_order[6] === tpl.substr(i,delim_order[7]) )
            delim = delim_order[6];
        
        if ( IDL === delim )
        {
            i += lenIDL;
            
            if ( s.length )
            {
                if ( 0 === a.node.type ) a.node.val += s;
                else a = new TplEntry({type: 0, val: s, algn: ''}, a);
            }
            s = '';
        }
        else if ( IDR === delim )
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
            if ( postop )
            {
                c = i < l ? tpl[CHAR](i) : '';
            }
            else
            {
                c = argument[CHAR](0);
            }
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
                if ( postop )
                {
                    i += 1;
                    if ( (i < l) && (NEG === tpl[CHAR](i)) )
                    {
                        negative = 1;
                        i += 1;
                    }
                    else
                    {
                        negative = 0;
                    }
                }
                else
                {
                    if ( NEG === argument[CHAR](1) )
                    {
                        negative = 1;
                        argument = argument.slice(2);
                    }
                    else
                    {
                        negative = 0;
                        argument = argument.slice(1);
                    }
                }
            }
            else if ( REPL === c )
            {
                if ( postop )
                {
                    s = ''; j = i+1; jl = l;
                    while ( (j < jl) && (REPR !== tpl[CHAR](j)) ) s += tpl[CHAR](j++);
                    i = j+1;
                }
                else
                {
                    s = ''; j = 1; jl = argument.length;
                    while ( (j < jl) && (REPR !== argument[CHAR](j)) ) s += argument[CHAR](j++);
                    argument = argument.slice( j+1 );
                }
                s = s.split(',');
                if ( s.length > 1 )
                {
                    start_i = trim(s[0]);
                    start_i = start_i.length ? (+start_i)|0 /*parseInt(start_i,10)||0*/ : 0;
                    end_i = trim(s[1]);
                    end_i = end_i.length ? (+end_i)|0 /*parseInt(end_i,10)||0*/ : -1;
                    optional = 1;
                }
                else
                {
                    start_i = trim(s[0]);
                    start_i = start_i.length ? (+start_i)|0 /*parseInt(start_i,10)||0*/ : 0;
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
            
            c = argument[CHAR](0);
            if ( ALGN === c )
            {
                aligned = 1;
                argument = argument.slice(1);
            }
            else
            {
                aligned = 0;
            }
            
            c = argument[CHAR](0);
            if ( DOT === c )
            {
                localised = 1;
                argument = argument.slice(1);
            }
            else
            {
                localised = 0;
            }
            
            template = -1 < argument.indexOf(REF) ? argument.split(REF) : [argument,null];
            argument = template[0]; template = template[1];
            nested = -1 < argument.indexOf(DOT) ? argument.split(DOT) : null;
            
            if ( cur_tpl && !HAS(arg_tpl,cur_tpl) ) arg_tpl[cur_tpl] = {};
            
            if ( TPL+OBL === tpl.substr(i,2+lenOBL) )
            {
                // template definition
                i += 2;
                template = template&&template.length ? template : 'grtpl--'+guid( );
                start_tpl = template;
                if ( cur_tpl && argument.length)
                    arg_tpl[cur_tpl][argument] = template;
            }
            
            if ( !argument.length ) continue; // template definition only
            
            if ( (null==template) && cur_tpl && HAS(arg_tpl,cur_tpl) && HAS(arg_tpl[cur_tpl],argument) )
                template = arg_tpl[cur_tpl][argument];
            
            if ( optional && !cur_arg.opt )
            {
                cur_arg.name = argument;
                cur_arg.key = nested;
                cur_arg.stpl = template;
                cur_arg.dval = default_value;
                cur_arg.opt = optional;
                cur_arg.neg = negative;
                cur_arg.algn = aligned;
                cur_arg.loc = localised;
                cur_arg.start = start_i;
                cur_arg.end = end_i;
                // handle multiple optional arguments for same optional block
                opt_args = new StackEntry(null, [argument,nested,negative,start_i,end_i,optional,localised]);
            }
            else if ( optional )
            {
                // handle multiple optional arguments for same optional block
                if ( (start_i !== end_i) && (cur_arg.start === cur_arg.end) )
                {
                    // set as main arg a loop arg, if exists
                    cur_arg.name = argument;
                    cur_arg.key = nested;
                    cur_arg.stpl = template;
                    cur_arg.dval = default_value;
                    cur_arg.opt = optional;
                    cur_arg.neg = negative;
                    cur_arg.algn = aligned;
                    cur_arg.loc = localised;
                    cur_arg.start = start_i;
                    cur_arg.end = end_i;
                }
                opt_args = new StackEntry(opt_args, [argument,nested,negative,start_i,end_i,optional,localised]);
            }
            else if ( !optional && (null === cur_arg.name) )
            {
                cur_arg.name = argument;
                cur_arg.key = nested;
                cur_arg.stpl = template;
                cur_arg.dval = default_value;
                cur_arg.opt = 0;
                cur_arg.neg = negative;
                cur_arg.algn = aligned;
                cur_arg.loc = localised;
                cur_arg.start = start_i;
                cur_arg.end = end_i;
                // handle multiple optional arguments for same optional block
                opt_args = new StackEntry(null, [argument,nested,negative,start_i,end_i,0,localised]);
            }
            if ( 0 === a.node.type ) a.node.algn = compute_alignment(a.node.val, 0, a.node.val.length);
            a = new TplEntry({
                type    : 1,
                name    : argument,
                key     : nested,
                stpl    : template,
                dval    : default_value,
                opt     : optional,
                algn    : aligned,
                loc     : localised,
                start   : start_i,
                end     : end_i
            }, a);
        }
        else if ( OBL === delim )
        {
            i += lenOBL;
            
            if ( s.length )
            {
                if ( 0 === a.node.type ) a.node.val += s;
                else a = new TplEntry({type: 0, val: s, algn: ''}, a);
            }
            s = '';
            
            // comment
            if ( COMMENT === tpl[CHAR](i) )
            {
                j = i+1; jl = l;
                while ( (j < jl) && (COMMENT_CLOSE !== tpl.substr(j,lenOBR+1)) ) s += tpl[CHAR](j++);
                i = j+lenOBR+1;
                if ( 0 === a.node.type ) a.node.algn = compute_alignment(a.node.val, 0, a.node.val.length);
                a = new TplEntry({type: -100, val: s}, a);
                s = '';
                continue;
            }
            
            // optional block
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
                algn    : 0,
                loc     : 0,
                start   : 0,
                end     : 0
            };
            opt_args = null;
            a = new TplEntry({type: 0, val: '', algn: ''});
            block = a;
        }
        else if ( OBR === delim )
        {
            i += lenOBR;
            
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
                else b = new TplEntry({type: 0, val: s, algn: ''}, b);
            }
            s = '';
            if ( start_tpl )
            {
                subtpl[start_tpl] = new TplEntry({
                    type    : 2,
                    name    : prev_arg.name,
                    key     : prev_arg.key,
                    loc     : prev_arg.loc,
                    algn    : prev_arg.algn,
                    start   : prev_arg.start,
                    end     : prev_arg.end,
                    opt_args: null/*opt_args*/,
                    tpl     : cur_block
                });
                start_tpl = null;
            }
            else
            {
                if ( 0 === a.node.type ) a.node.algn = compute_alignment(a.node.val, 0, a.node.val.length);
                a = new TplEntry({
                    type    : -1,
                    name    : prev_arg.name,
                    key     : prev_arg.key,
                    loc     : prev_arg.loc,
                    algn    : prev_arg.algn,
                    start   : prev_arg.start,
                    end     : prev_arg.end,
                    opt_args: prev_opt_args,
                    tpl     : cur_block
                }, a);
            }
        }
        else
        {
            c = tpl[CHAR](i++);
            if ( "\n" === c )
            {
                // note line changes to handle alignments
                if ( s.length )
                {
                    if ( 0 === a.node.type ) a.node.val += s;
                    else a = new TplEntry({type: 0, val: s, algn: ''}, a);
                }
                s = '';
                if ( 0 === a.node.type ) a.node.algn = compute_alignment(a.node.val, 0, a.node.val.length);
                a = new TplEntry({type: 100, val: "\n"}, a);
            }
            else
            {
                s += c;
            }
        }
    }
    if ( s.length )
    {
        if ( 0 === a.node.type ) a.node.val += s;
        else a = new TplEntry({type: 0, val: s, algn: ''}, a);
    }
    if ( 0 === a.node.type ) a.node.algn = compute_alignment(a.node.val, 0, a.node.val.length);
    return [roottpl, subtpl];
}

function optional_block( args, block, SUB, FN, index, alignment, orig_args )
{
    var opt_vars, opt_v, opt_arg, arr, rs, re, ri, len, block_arg = null, out = '';
    
    if ( -1 === block.type )
    {
        // optional block, check if optional variables can be rendered
        opt_vars = block.opt_args;
        // if no optional arguments, render block by default
        if ( opt_vars && opt_vars.value[5] )
        {
            while( opt_vars )
            {
                opt_v = opt_vars.value;
                opt_arg = walk( args, opt_v[1], [String(opt_v[0])], opt_v[6] ? null : orig_args );
                if ( (null === block_arg) && (block.name === opt_v[0]) ) block_arg = opt_arg;
                
                if ( (0 === opt_v[2] && null == opt_arg) ||
                    (1 === opt_v[2] && null != opt_arg)
                )
                    return '';
                opt_vars = opt_vars.prev;
            }
        }
    }
    else
    {
        block_arg = walk( args, block.key, [String(block.name)], block.loc ? null : orig_args );
    }
    
    arr = is_array( block_arg ); len = arr ? block_arg.length : -1;
    //if ( !block.algn ) alignment = '';
    if ( arr && (len > block.start) )
    {
        for(rs=block.start,re=(-1===block.end?len-1:Math.min(block.end,len-1)),ri=rs; ri<=re; ri++)
            out += main( args, block.tpl, SUB, FN, ri, alignment, orig_args );
    }
    else if ( !arr && (block.start === block.end) )
    {
        out = main( args, block.tpl, SUB, FN, null, alignment, orig_args );
    }
    return out;
}
function non_terminal( args, symbol, SUB, FN, index, alignment, orig_args )
{
    var opt_arg, tpl_args, tpl, out = '', fn;
    if ( symbol.stpl && (
        HAS(SUB,symbol.stpl) ||
        HAS(GrammarTemplate.subGlobal,symbol.stpl) ||
        HAS(FN,symbol.stpl) || HAS(FN,'*') ||
        HAS(GrammarTemplate.fnGlobal,symbol.stpl) ||
        HAS(GrammarTemplate.fnGlobal,'*')
    ) )
    {
        // using custom function or sub-template
        opt_arg = walk( args, symbol.key, [String(symbol.name)], symbol.loc ? null : orig_args );
        
        if ( HAS(SUB,symbol.stpl) || HAS(GrammarTemplate.subGlobal,symbol.stpl) )
        {
            // sub-template
            if ( (null != index) && ((0 !== index) || (symbol.start !== symbol.end) || !symbol.opt) && is_array(opt_arg) )
            {
                opt_arg = index < opt_arg.length ? opt_arg[ index ] : null;
            }
            
            if ( (null == opt_arg) && (null !== symbol.dval) )
            {
                // default value if missing
                out = symbol.dval;
            }
            else
            {
                // try to associate sub-template parameters to actual input arguments
                tpl = HAS(SUB,symbol.stpl) ? SUB[symbol.stpl].node : GrammarTemplate.subGlobal[symbol.stpl].node;
                tpl_args = {};
                if ( null != opt_arg )
                {
                    /*if ( HAS(opt_arg,tpl.name) && !HAS(opt_arg,symbol.name) ) tpl_args = opt_arg;
                    else tpl_args[tpl.name] = opt_arg;*/
                    if ( is_array(opt_arg) ) tpl_args[tpl.name] = opt_arg;
                    else tpl_args = opt_arg;
                }
                out = optional_block( tpl_args, tpl, SUB, FN, null, symbol.algn ? alignment : '', null == orig_args ? args : orig_args );
                //if ( symbol.algn ) out = align(out, alignment);
            }
        }
        else //if ( fn )
        {
            // custom function
            fn = null;
            if      ( HAS(FN,symbol.stpl) )                         fn = FN[symbol.stpl];
            else if ( HAS(FN,'*') )                                 fn = FN['*'];
            else if ( HAS(GrammarTemplate.fnGlobal,symbol.stpl) )   fn = GrammarTemplate.fnGlobal[symbol.stpl];
            else if ( GrammarTemplate.fnGlobal['*'] )               fn = GrammarTemplate.fnGlobal['*'];
            
            if ( is_array(opt_arg) )
            {
                index = null != index ? index : symbol.start;
                opt_arg = index < opt_arg.length ? opt_arg[ index ] : null;
            }
            
            if ( "function" === typeof fn )
            {
                var fn_arg = {
                    //value               : opt_arg,
                    symbol              : symbol,
                    index               : index,
                    currentArguments    : args,
                    originalArguments   : orig_args,
                    alignment           : alignment
                };
                opt_arg = fn( opt_arg, fn_arg );
            }
            else
            {
                opt_arg = String(fn);
            }
            
            out = (null == opt_arg) && (null !== symbol.dval) ? symbol.dval : String(opt_arg);
            if ( symbol.algn ) out = align(out, alignment);
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
        opt_arg = walk( args, symbol.key, [String(symbol.name)], symbol.loc ? null : orig_args );
        
        // default value if missing
        if ( is_array(opt_arg) )
        {
            index = null != index ? index : symbol.start;
            opt_arg = index < opt_arg.length ? opt_arg[ index ] : null;
        }
        out = (null == opt_arg) && (null !== symbol.dval) ? symbol.dval : String(opt_arg);
        if ( symbol.algn ) out = align(out, alignment);
    }
    return out;
}
function main( args, tpl, SUB, FN, index, alignment, orig_args )
{
    alignment = alignment || '';
    var tt, current_alignment = alignment, out = '';
    while ( tpl )
    {
        tt = tpl.node.type;
        if ( -1 === tt ) /* optional code-block */
        {
            out += optional_block( args, tpl.node, SUB, FN, index, tpl.node.algn ? current_alignment : alignment, orig_args );
        }
        else if ( 1 === tt ) /* non-terminal */
        {
            out += non_terminal( args, tpl.node, SUB, FN, index, tpl.node.algn ? current_alignment : alignment, orig_args );
        }
        else if ( 0 === tt ) /* terminal */
        {
            current_alignment += tpl.node.algn;
            out += tpl.node.val;
        }
        else if ( 100 === tt ) /* new line */
        {
            current_alignment = alignment;
            out += "\n" + alignment;
        }
        /*else if ( -100 === tt ) /* comment * /
        {
            /* pass * /
        }*/
        tpl = tpl.next;
    }
    return out;
}


function GrammarTemplate( tpl, delims, postop )
{
    var self = this;
    if ( !(self instanceof GrammarTemplate) ) return new GrammarTemplate(tpl, delims, postop);
    self.id = null;
    self.tpl = null;
    self.fn = {};
    // lazy init
    self._args = [tpl||'', delims||GrammarTemplate.defaultDelimiters, postop||false];
};
GrammarTemplate.VERSION = '3.0.0';
GrammarTemplate.defaultDelimiters = ['<','>','[',']'];
GrammarTemplate.fnGlobal = {};
GrammarTemplate.subGlobal = {};
GrammarTemplate.guid = guid;
GrammarTemplate.multisplit = multisplit;
GrammarTemplate.align = align;
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
            self.tpl = GrammarTemplate.multisplit( self._args[0], self._args[1], self._args[2] );
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
