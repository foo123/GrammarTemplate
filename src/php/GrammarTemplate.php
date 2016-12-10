<?php
/**
*   GrammarTemplate, 
*   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
* 
*   @version: 3.0.0
*   https://github.com/foo123/GrammarTemplate
*
**/
if ( !class_exists('GrammarTemplate') )
{
class GrammarTemplate__StackEntry
{
    public $value = null;
    public $prev = null;
    
    public function __construct($stack=null, $value=null)
    {
        $this->prev = $stack;
        $this->value = $value;
    }
}
class GrammarTemplate__TplEntry
{
    public $node = null;
    public $prev = null;
    public $next = null;
    
    public function __construct($node=null, $tpl=null)
    {
        if ( $tpl ) $tpl->next = $this;
        $this->node = $node;
        $this->prev = $tpl;
        $this->next = null;
    }
}

class GrammarTemplate
{    
    const VERSION = '3.0.0';
    
    public static function pad( $s, $n, $z='0', $pad_right=false )
    {
        $ps = (string)$s;
        if ( $pad_right ) while ( strlen($ps) < $n ) $ps .= $z;
        else while ( strlen($ps) < $n ) $ps = $z . $ps;
        return $ps;
    }
    
    public static function guid( )
    {
        static $GUID = 0;
        $GUID += 1;
        return self::pad(dechex(time()),12).'--'.self::pad(dechex($GUID),4);
    }
    
    private static function is_array( $a )
    {
        if ( (null != $a) && is_array( $a ) )
        {
            $array_keys = array_keys( $a );
            return !empty($array_keys) && (array_keys($array_keys) === $array_keys);
        }
        return false;
    }
    
    private static function compute_alignment( $s, $i, $l )
    {
        $alignment = '';
        while ( $i < $l )
        {
            $c = $s[$i];
            if ( (" " === $c) || ("\r" === $c) || ("\t" === $c) || ("\v" === $c) || ("\0" === $c) )
            {
                $alignment .= $c;
                $i += 1;
            }
            else
            {
                break;
            }
        }
        return $alignment;
    }
    
    public static function align( $s, $alignment )
    {
        $l = strlen($s);
        if ( $l && strlen($alignment) )
        {
            $aligned = '';
            for($i=0; $i<$l; $i++)
            {
                $c = $s[$i];
                $aligned .= $c;
                if ( "\n" === $c ) $aligned .= $alignment;
            }
        }
        else
        {
            $aligned = $s;
        }
        return $aligned;
    }
    
    private static function walk( $obj, $keys, $keys_alt=null, $obj_alt=null )
    {
        $found = 0;
        if ( $keys )
        {
            $o = $obj;
            $l = count($keys);
            $i = 0;
            $found = 1;
            while( $i < $l )
            {
                $k = $keys[$i++];
                if ( isset($o) )
                {
                    if ( is_array($o) && isset($o[$k]) )
                    {
                        $o = $o[$k];
                    }
                    elseif ( is_object($o) && isset($o->{$k}) )
                    {
                        $o = $o->{$k};
                    }
                    else
                    {
                        $found = 0;
                        break;
                    }
                }
                else
                {
                    $found = 0;
                    break;
                }
            }
        }
        if ( !$found && $keys_alt )
        {
            $o = $obj;
            $l = count($keys_alt);
            $i = 0;
            $found = 1;
            while( $i < $l )
            {
                $k = $keys_alt[$i++];
                if ( isset($o) )
                {
                    if ( is_array($o) && isset($o[$k]) )
                    {
                        $o = $o[$k];
                    }
                    elseif ( is_object($o) && isset($o->{$k}) )
                    {
                        $o = $o->{$k};
                    }
                    else
                    {
                        $found = 0;
                        break;
                    }
                }
                else
                {
                    $found = 0;
                    break;
                }
            }
        }
        if ( !$found && (null !== $obj_alt) && ($obj_alt !== $obj) )
        {
            if ( $keys )
            {
                $o = $obj_alt;
                $l = count($keys);
                $i = 0;
                $found = 1;
                while( $i < $l )
                {
                    $k = $keys[$i++];
                    if ( isset($o) )
                    {
                        if ( is_array($o) && isset($o[$k]) )
                        {
                            $o = $o[$k];
                        }
                        elseif ( is_object($o) && isset($o->{$k}) )
                        {
                            $o = $o->{$k};
                        }
                        else
                        {
                            $found = 0;
                            break;
                        }
                    }
                    else
                    {
                        $found = 0;
                        break;
                    }
                }
            }
            if ( !$found && $keys_alt )
            {
                $o = $obj_alt;
                $l = count($keys_alt);
                $i = 0;
                $found = 1;
                while( $i < $l )
                {
                    $k = $keys_alt[$i++];
                    if ( isset($o) )
                    {
                        if ( is_array($o) && isset($o[$k]) )
                        {
                            $o = $o[$k];
                        }
                        elseif ( is_object($o) && isset($o->{$k}) )
                        {
                            $o = $o->{$k};
                        }
                        else
                        {
                            $found = 0;
                            break;
                        }
                    }
                    else
                    {
                        $found = 0;
                        break;
                    }
                }
            }
        }
        return $found ? $o : null;
    }
    
    public static function multisplit( $tpl, $delims, $postop=false )
    {
        $IDL = $delims[0]; $IDR = $delims[1];
        $OBL = $delims[2]; $OBR = $delims[3];
        $lenIDL = strlen($IDL); $lenIDR = strlen($IDR);
        $lenOBL = strlen($OBL); $lenOBR = strlen($OBR);
        $ESC = '\\'; $OPT = '?'; $OPTR = '*'; $NEG = '!'; $DEF = '|'; $COMMENT = '#';
        $TPL = ':='; $REPL = '{'; $REPR = '}'; $DOT = '.'; $REF = ':'; $ALGN = '@'; //$NOTALGN = '&';
        $COMMENT_CLOSE = $COMMENT.$OBR;
        $default_value = null; $negative = 0; $optional = 0;
        $aligned = 0; $localised = 0;
        $l = strlen($tpl);
        
        $delim1 = array($IDL, $lenIDL, $IDR, $lenIDR);
        $delim2 = array($OBL, $lenOBL, $OBR, $lenOBR);
        $delim_order = array(null,0,null,0,null,0,null,0);
        
        $postop = true === $postop;
        $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> '', 'algn'=> ''));
        $cur_arg = (object)array(
            'type'    => 1,
            'name'    => null,
            'key'     => null,
            'stpl'    => null,
            'dval'    => null,
            'opt'     => 0,
            'neg'     => 0,
            'algn'    => 0,
            'loc'     => 0,
            'start'   => 0,
            'end'     => 0
        );
        $roottpl = $a; $block = null;
        $opt_args = null; $subtpl = array(); $cur_tpl = null; $arg_tpl = array(); $start_tpl = null;
        
        // hard-coded merge-sort for arbitrary delims parsing based on str len
        if ( $delim1[1] < $delim1[3] )
        {
            $s = $delim1[0]; $delim1[2] = $delim1[0]; $delim1[0] = $s;
            $i = $delim1[1]; $delim1[3] = $delim1[1]; $delim1[1] = $i;
        }
        if ( $delim2[1] < $delim2[3] )
        {
            $s = $delim2[0]; $delim2[2] = $delim2[0]; $delim2[0] = $s;
            $i = $delim2[1]; $delim2[3] = $delim2[1]; $delim2[1] = $i;
        }
        $start_i = 0; $end_i = 0; $i = 0;
        while ( (4 > $start_i) && (4 > $end_i) )
        {
            if ( $delim1[$start_i+1] < $delim2[$end_i+1] )
            {
                $delim_order[$i] = $delim2[$end_i];
                $delim_order[$i+1] = $delim2[$end_i+1];
                $end_i += 2;
            }
            else
            {
                $delim_order[$i] = $delim1[$start_i];
                $delim_order[$i+1] = $delim1[$start_i+1];
                $start_i += 2;
            }
            $i += 2;
        }
        while ( 4 > $start_i )
        {
            $delim_order[$i] = $delim1[$start_i];
            $delim_order[$i+1] = $delim1[$start_i+1];
            $start_i += 2; $i += 2;
        }
        while ( 4 > $end_i )
        {
            $delim_order[$i] = $delim2[$end_i];
            $delim_order[$i+1] = $delim2[$end_i+1];
            $end_i += 2; $i += 2;
        }
            
        $stack = null; $s = '';
        
        $i = 0;
        while( $i < $l )
        {
            $c = $tpl[$i];
            if ( $ESC === $c )
            {
                $s .= $i+1 < $l ? $tpl[$i+1] : '';
                $i += 2;
                continue;
            }
            
            $delim = null;
            if ( $delim_order[0] === substr($tpl,$i,$delim_order[1]) )
                $delim = $delim_order[0];
            elseif ( $delim_order[2] === substr($tpl,$i,$delim_order[3]) )
                $delim = $delim_order[2];
            elseif ( $delim_order[4] === substr($tpl,$i,$delim_order[5]) )
                $delim = $delim_order[4];
            elseif ( $delim_order[6] === substr($tpl,$i,$delim_order[7]) )
                $delim = $delim_order[6];
            
            if ( $IDL === $delim )
            {
                $i += $lenIDL;
                
                if ( strlen($s) )
                {
                    if ( 0 === $a->node->type ) $a->node->val .= $s;
                    else $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> $s, 'algn'=> ''), $a);
                }
                
                $s = '';
            }
            else if ( $IDR === $delim )
            {
                $i += $lenIDR;
                
                // argument
                $argument = $s; $s = '';
                $p = strpos($argument, $DEF);
                if ( false !== $p )
                {
                    $default_value = substr($argument, $p+1);
                    $argument = substr($argument, 0, $p);
                }
                else
                {
                    $default_value = null;
                }
                if ( $postop )
                {
                    $c = $i < $l ? $tpl[$i] : '';
                }
                else
                {
                    $c = $argument[0];
                }
                if ( $OPT === $c || $OPTR === $c )
                {
                    $optional = 1;
                    if ( $OPTR === $c )
                    {
                        $start_i = 1;
                        $end_i = -1;
                    }
                    else
                    {
                        $start_i = 0;
                        $end_i = 0;
                    }
                    if ( $postop )
                    {
                        $i += 1;
                        if ( ($i < $l) && ($NEG === $tpl[$i]) )
                        {
                            $negative = 1;
                            $i += 1;
                        }
                        else
                        {
                            $negative = 0;
                        }
                    }
                    else
                    {
                        if ( $NEG === $argument[1] )
                        {
                            $negative = 1;
                            $argument = substr($argument,2);
                        }
                        else
                        {
                            $negative = 0;
                            $argument = substr($argument,1);
                        }
                    }
                }
                elseif ( $REPL === $c )
                {
                    if ( $postop )
                    {
                        $s = ''; $j = $i+1; $jl = $l;
                        while ( ($j < $jl) && ($REPR !== $tpl[j]) ) $s .= $tpl[$j++];
                        $i = $j+1;
                    }
                    else
                    {
                        $s = ''; $j = 1; $jl = strlen($argument);
                        while ( ($j < $jl) && ($REPR !== $argument[$j]) ) $s .= $argument[$j++];
                        $argument = substr($argument, $j+1);
                    }
                    $s = explode(',', $s);
                    if ( count($s) > 1 )
                    {
                        $start_i = trim($s[0]);
                        $start_i = strlen($start_i) ? intval($start_i,10) : 0;
                        if ( is_nan($start_i) ) $start_i = 0;
                        $end_i = trim($s[1]);
                        $end_i = strlen($end_i) ? intval($end_i,10) : -1;
                        if ( is_nan($end_i) ) $end_i = 0;
                        $optional = 1;
                    }
                    else
                    {
                        $start_i = trim($s[0]);
                        $start_i = strlen($start_i) ? intval($start_i,10) : 0;
                        if ( is_nan($start_i) ) $start_i = 0;
                        $end_i = $start_i;
                        $optional = 0;
                    }
                    $s = '';
                    $negative = 0;
                }
                else
                {
                    $optional = 0;
                    $negative = 0;
                    $start_i = 0;
                    $end_i = 0;
                }
                if ( $negative && (null === $default_value) ) $default_value = '';
                
                $c = $argument[0];
                if ( $ALGN === $c )
                {
                    $aligned = 1;
                    $argument = substr($argument,1);
                }
                else
                {
                    $aligned = 0;
                }
                
                $c = $argument[0];
                if ( $DOT === $c )
                {
                    $localised = 1;
                    $argument = substr($argument,1);
                }
                else
                {
                    $localised = 0;
                }
                
                $template = false !== strpos($argument, $REF) ? explode($REF, $argument) : array($argument,null);
                $argument = $template[0]; $template = $template[1];
                $nested = false !== strpos($argument, $DOT) ? explode($DOT, $argument) : null;
                
                if ( $cur_tpl && !isset($arg_tpl[$cur_tpl]) ) $arg_tpl[$cur_tpl] = array();
                
                if ( $TPL.$OBL === substr($tpl,$i,2+$lenOBL) )
                {
                    // template definition
                    $i += 2;
                    $template = $template&&strlen($template) ? $template : 'grtpl--'.self::guid( );
                    $start_tpl = $template;
                    if ( $cur_tpl && strlen($argument))
                        $arg_tpl[$cur_tpl][$argument] = $template;
                }
                
                if ( !strlen($argument) ) continue; // template definition only
                
                if ( (null==$template) && $cur_tpl && isset($arg_tpl[$cur_tpl]) && isset($arg_tpl[$cur_tpl][$argument]) )
                    $template = $arg_tpl[$cur_tpl][$argument];
                
                if ( $optional && !$cur_arg->opt )
                {
                    $cur_arg->name = $argument;
                    $cur_arg->key = $nested;
                    $cur_arg->stpl = $template;
                    $cur_arg->dval = $default_value;
                    $cur_arg->opt = $optional;
                    $cur_arg->neg = $negative;
                    $cur_arg->algn = $aligned;
                    $cur_arg->loc = $localised;
                    $cur_arg->start = $start_i;
                    $cur_arg->end = $end_i;
                    // handle multiple optional arguments for same optional block
                    $opt_args = new GrammarTemplate__StackEntry(null, array($argument,$nested,$negative,$start_i,$end_i,$optional,$localised));
                }
                else if ( $optional )
                {
                    // handle multiple optional arguments for same optional block
                    if ( ($start_i !== $end_i) && ($cur_arg->start === $cur_arg->end) )
                    {
                        // set as main arg a loop arg, if exists
                        $cur_arg->name = $argument;
                        $cur_arg->key = $nested;
                        $cur_arg->stpl = $template;
                        $cur_arg->dval = $default_value;
                        $cur_arg->opt = $optional;
                        $cur_arg->neg = $negative;
                        $cur_arg->algn = $aligned;
                        $cur_arg->loc = $localised;
                        $cur_arg->start = $start_i;
                        $cur_arg->end = $end_i;
                    }
                    $opt_args = new GrammarTemplate__StackEntry($opt_args, array($argument,$nested,$negative,$start_i,$end_i,$optional,$localised));
                }
                else if ( !$optional && (null === $cur_arg->name) )
                {
                    $cur_arg->name = $argument;
                    $cur_arg->key = $nested;
                    $cur_arg->stpl = $template;
                    $cur_arg->dval = $default_value;
                    $cur_arg->opt = 0;
                    $cur_arg->neg = $negative;
                    $cur_arg->algn = $aligned;
                    $cur_arg->loc = $localised;
                    $cur_arg->start = $start_i;
                    $cur_arg->end = $end_i;
                    // handle multiple optional arguments for same optional block
                    $opt_args = new GrammarTemplate__StackEntry(null, array($argument,$nested,$negative,$start_i,$end_i,0,$localised));
                }
                if ( 0 === $a->node->type ) $a->node->algn = self::compute_alignment($a->node->val, 0, strlen($a->node->val));
                $a = new GrammarTemplate__TplEntry((object)array(
                    'type'    => 1,
                    'name'    => $argument,
                    'key'     => $nested,
                    'stpl'    => $template,
                    'dval'    => $default_value,
                    'opt'     => $optional,
                    'algn'    => $aligned,
                    'loc'     => $localised,
                    'start'   => $start_i,
                    'end'     => $end_i
                ), $a);
            }
            else if ( $OBL === $delim )
            {
                $i += $lenOBL;
                
                if ( strlen($s) )
                {
                    if ( 0 === $a->node->type ) $a->node->val .= $s;
                    else $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> $s, 'algn'=> ''), $a);
                }
                $s = '';
                
                // comment
                if ( $COMMENT === $tpl[$i] )
                {
                    $j = $i+1; $jl = $l;
                    while ( ($j < $jl) && ($COMMENT_CLOSE !== substr($tpl,$j,$lenOBR+1)) ) $s .= $tpl[$j++];
                    $i = $j+$lenOBR+1;
                    if ( 0 === $a->node->type ) $a->node->algn = self::compute_alignment($a->node->val, 0, strlen($a->node->val));
                    $a = new GrammarTemplate__TplEntry((object)array('type'=> -100, 'val'=> $s), $a);
                    $s = '';
                    continue;
                }
                
                // optional block
                $stack = new GrammarTemplate__StackEntry($stack, array($a, $block, $cur_arg, $opt_args, $cur_tpl, $start_tpl));
                if ( $start_tpl ) $cur_tpl = $start_tpl;
                $start_tpl = null;
                $cur_arg = (object)array(
                    'type'    => 1,
                    'name'    => null,
                    'key'     => null,
                    'stpl'    => null,
                    'dval'    => null,
                    'opt'     => 0,
                    'neg'     => 0,
                    'algn'    => 0,
                    'loc'     => 0,
                    'start'   => 0,
                    'end'     => 0
                );
                $opt_args = null;
                $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> '', 'algn'=> ''));
                $block = $a;
            }
            else if ( $OBR === $delim )
            {
                $i += $lenOBR;
                
                $b = $a;
                $cur_block = $block;
                $prev_arg = $cur_arg;
                $prev_opt_args = $opt_args;
                if ( $stack )
                {
                    $a = $stack->value[0];
                    $block = $stack->value[1];
                    $cur_arg = $stack->value[2];
                    $opt_args = $stack->value[3];
                    $cur_tpl = $stack->value[4];
                    $start_tpl = $stack->value[5];
                    $stack = $stack->prev;
                }
                else
                {
                    $a = null;
                }
                if ( strlen($s) )
                {
                    if ( 0 === $b->node->type ) $b->node->val .= $s;
                    else $b = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> $s, 'algn'=> ''), $b);
                }
                
                $s = '';
                if ( $start_tpl )
                {
                    $subtpl[$start_tpl] = new GrammarTemplate__TplEntry((object)array(
                        'type'    => 2,
                        'name'    => $prev_arg->name,
                        'key'     => $prev_arg->key,
                        'loc'     => $prev_arg->loc,
                        'algn'    => $prev_arg->algn,
                        'start'   => $prev_arg->start,
                        'end'     => $prev_arg->end,
                        'opt_args'=> null,
                        'tpl'     => $cur_block
                    ));
                    $start_tpl = null;
                }
                else
                {
                    if ( 0 === $a->node->type ) $a->node->algn = self::compute_alignment($a->node->val, 0, strlen($a->node->val));
                    $a = new GrammarTemplate__TplEntry((object)array(
                        'type'    => -1,
                        'name'    => $prev_arg->name,
                        'key'     => $prev_arg->key,
                        'loc'     => $prev_arg->loc,
                        'algn'    => $prev_arg->algn,
                        'start'   => $prev_arg->start,
                        'end'     => $prev_arg->end,
                        'opt_args'=> $prev_opt_args,
                        'tpl'     => $cur_block
                    ), $a);
                }
            }
            else
            {
                $c = $tpl[$i++];
                if ( "\n" === $c )
                {
                    // note line changes to handle alignments
                    if ( strlen($s) )
                    {
                        if ( 0 === $a->node->type ) $a->node->val .= $s;
                        else $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> $s, 'algn'=> ''), $a);
                    }
                    $s = '';
                    if ( 0 === $a->node->type ) $a->node->algn = self::compute_alignment($a->node->val, 0, strlen($a->node->val));
                    $a = new GrammarTemplate__TplEntry((object)array('type'=> 100, 'val'=> "\n"), $a);
                }
                else
                {
                    $s .= $c;
                }
            }
        }
        if ( strlen($s) )
        {
            if ( 0 === $a->node->type ) $a->node->val .= $s;
            else $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> $s, 'algn'=> ''), $a);
        }
        if ( 0 === $a->node->type ) $a->node->algn = self::compute_alignment($a->node->val, 0, strlen($a->node->val));
        return array($roottpl, &$subtpl);
    }

    public static function optional_block( $args, $block, &$SUB, &$FN, $index=null, $alignment='', $orig_args=null )
    {
        $out = '';
        $block_arg = null;
        
        if ( -1 === $block->type )
        {
            // optional block, check if optional variables can be rendered
            $opt_vars = $block->opt_args;
            // if no optional arguments, render block by default
            if ( $opt_vars && $opt_vars->value[5] )
            {
                while( $opt_vars )
                {
                    $opt_v = $opt_vars->value;
                    $opt_arg = self::walk( $args, $opt_v[1], array((string)$opt_v[0]), $opt_v[6] ? null : $orig_args );
                    if ( (null === $block_arg) && ($block->name === $opt_v[0]) ) $block_arg = $opt_arg;
                    
                    if ( (0 === $opt_v[2] && null === $opt_arg) || (1 === $opt_v[2] && null !== $opt_arg) )  return '';
                    $opt_vars = $opt_vars->prev;
                }
            }
        }
        else
        {
            $block_arg = self::walk( $args, $block->key, array((string)$block->name), $block->loc ? null : $orig_args );
        }
        
        $arr = self::is_array( $block_arg ); $len = $arr ? count($block_arg) : -1;
        //if ( !$block->algn ) $alignment = '';
        if ( $arr && ($len > $block->start) )
        {
            for($rs=$block->start,$re=(-1===$block->end?$len-1:min($block->end,$len-1)),$ri=$rs; $ri<=$re; $ri++)
                $out .= self::main( $args, $block->tpl, $SUB, $FN, $ri, $alignment, $orig_args );
        }
        else if ( !$arr && ($block->start === $block->end) )
        {
            $out = self::main( $args, $block->tpl, $SUB, $FN, null, $alignment, $orig_args );
        }
        return $out;
    }
    public static function non_terminal( $args, $symbol, &$SUB, &$FN, $index=null, $alignment='', $orig_args=null )
    {
        $out = '';
        if ( $symbol->stpl && (
            (!empty($SUB) && isset($SUB[$symbol->stpl])) ||
            (isset(self::$subGlobal[$symbol->stpl])) ||
            (!empty($FN) && (isset($FN[$symbol->stpl]) || isset($FN['*']))) ||
            (isset(self::$fnGlobal[$symbol->stpl]) || isset(self::$fnGlobal['*']))
        ) )
        {
            // using custom function or sub-template
            $opt_arg = self::walk( $args, $symbol->key, array((string)$symbol->name), $symbol->loc ? null : $orig_args );
        
            if ( (!empty($SUB) && isset($SUB[$symbol->stpl])) || isset(self::$subGlobal[$symbol->stpl]) )
            {
                // sub-template
                if ( (null !== $index) && ((0 !== $index) || ($symbol->start !== $symbol->end) || !$symbol->opt) && self::is_array($opt_arg) )
                {
                    $opt_arg = $index < count($opt_arg) ? $opt_arg[ $index ] : null;
                }
                if ( (null === $opt_arg) && (null !== $symbol->dval) )
                {
                    // default value if missing
                    $out = $symbol->dval;
                }
                else
                {
                    // try to associate sub-template parameters to actual input arguments
                    $tpl = !empty($SUB) && isset($SUB[$symbol->stpl]) ? $SUB[$symbol->stpl]->node : self::$subGlobal[$symbol->stpl]->node;
                    $tpl_args = array();
                    if ( null !== $opt_arg )
                    {
                        if ( self::is_array($opt_arg) ) $tpl_args[$tpl->name] = $opt_arg;
                        else $tpl_args = $opt_arg;
                    }
                    $out = self::optional_block( $tpl_args, $tpl, $SUB, $FN, null, $symbol->algn ? $alignment : '', null === $orig_args ? $args : $orig_args );
                    //if ( $symbol->algn ) $out = self::align($out, $alignment);
                }
            }
            else//if ( $fn )
            {
                // custom function
                $fn = null;
                if     ( !empty($FN) && isset($FN[$symbol->stpl]) ) $fn = $FN[$symbol->stpl];
                elseif ( !empty($FN) && isset($FN['*']) )           $fn = $FN['*'];
                elseif ( isset(self::$fnGlobal[$symbol->stpl]) )    $fn = self::$fnGlobal[$symbol->stpl];
                elseif ( isset(self::$fnGlobal['*']) )              $fn = self::$fnGlobal['*'];
                
                if ( self::is_array($opt_arg) )
                {
                    $index = null !== $index ? $index : $symbol->start;
                    $opt_arg = $index < count($opt_arg) ? $opt_arg[ $index ] : null;
                }
                
                if ( is_callable($fn) )
                {
                    $fn_arg = (object)array(
                        //'value'               => $opt_arg,
                        'symbol'              => $symbol,
                        'index'               => $index,
                        'currentArguments'    => &$args,
                        'originalArguments'   => &$orig_args,
                        'alignment'           => $alignment
                    );
                    $opt_arg = call_user_func($fn, $opt_arg, $fn_arg);
                }
                else
                {
                    $opt_arg = strval($fn);
                }
                
                $out = (null === $opt_arg) && (null !== $symbol->dval) ? $symbol->dval : strval($opt_arg);
                if ( $symbol->algn ) $out = self::align($out, $alignment);
            }
        }
        elseif ( $symbol->opt && (null !== $symbol->dval) )
        {
            // boolean optional argument
            $out = $symbol->dval;
        }
        else
        {
            // plain symbol argument
            $opt_arg = self::walk( $args, $symbol->key, array((string)$symbol->name), $symbol->loc ? null : $orig_args );
            
            // default value if missing
            if ( self::is_array($opt_arg) )
            {
                $index = null !== $index ? $index : $symbol->start;
                $opt_arg = $index < count($opt_arg) ? $opt_arg[ $index ] : null;
            }
            $out = (null === $opt_arg) && (null !== $symbol->dval) ? $symbol->dval : strval($opt_arg);
            if ( $symbol->algn ) $out = self::align($out, $alignment);
        }
        return $out;
    }
    public static function main( $args, $tpl, &$SUB=null, &$FN=null, $index=null, $alignment='', $orig_args=null )
    {
        $out = '';
        $current_alignment = $alignment;
        while ( $tpl )
        {
            $tt = $tpl->node->type;
            if ( -1 === $tt ) /* optional code-block */
            {
                $out .= self::optional_block( $args, $tpl->node, $SUB, $FN, $index, $tpl->node->algn ? $current_alignment : $alignment, $orig_args );
            }
            elseif ( 1 === $tt ) /* non-terminal */
            {
                $out .= self::non_terminal( $args, $tpl->node, $SUB, $FN, $index, $tpl->node->algn ? $current_alignment : $alignment, $orig_args );
            }
            elseif ( 0 === $tt ) /* terminal */
            {
                $current_alignment .= $tpl->node->algn;
                $out .= $tpl->node->val;
            }
            elseif ( 100 === $tt ) /* new line */
            {
                $current_alignment = $alignment;
                $out .= "\n" . $alignment;
            }
            /*elseif ( -100 === $tt ) /* comment * /
            {
                /* pass * /
            }*/
            $tpl = $tpl->next;
        }
        return $out;
    }
    
    public static $defaultDelimiters = array('<','>','[',']');
    public static $fnGlobal = array();
    public static $subGlobal = array();
    
    public $id = null;
    public $tpl = null;
    public $fn = null;
    protected $_args = null;
    
    public function __construct($tpl='', $delims=null, $postop=false)
    {
        $this->id = null;
        $this->tpl = null;
        $this->fn = array();
        if ( empty($delims) ) $delims = self::$defaultDelimiters;
        // lazy init
        $this->_args = array($tpl, $delims, $postop);
    }

    public function __destruct()
    {
        $this->dispose();
    }
    
    public function dispose()
    {
        $this->id = null;
        $this->tpl = null;
        $this->fn = null;
        $this->_args = null;
        return $this;
    }
    
    public function parse( )
    {
        if ( (null === $this->tpl) && (null !== $this->_args) )
        {
            // lazy init
            $this->tpl = self::multisplit( $this->_args[0], $this->_args[1], $this->_args[2] );
            $this->_args = null;
        }
        return $this;
    }
    
    public function render($args=null)
    {
        // lazy init
        if ( null === $this->tpl ) $this->parse( );
        return self::main( null === $args ? array() : $args, $this->tpl[0], $this->tpl[1], $this->fn );
    }
}    
}