<?php
/**
*   GrammarTemplate, 
*   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
* 
*   @version: 2.1.1
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
    const VERSION = '2.1.1';
    private static $GUID = 0;
    
    private static function guid( )
    {
        return time().'--'.(++self::$GUID);
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
        $OBL = $delims[2]; $OBR = $delims[3]; $TPL = $delims[4];
        $lenIDL = strlen($IDL); $lenIDR = strlen($IDR);
        $lenOBL = strlen($OBL); $lenOBR = strlen($OBR); $lenTPL = strlen($TPL);
        $ESC = '\\'; $OPT = '?'; $OPTR = '*'; $NEG = '!'; $DEF = '|';
        $REPL = '{'; $REPR = '}'; $DOT = '.'; $REF = ':';
        $default_value = null; $negative = 0; $optional = 0;
        $l = strlen($tpl);
        
        $postop = true === $postop;
        $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> ''));
        $cur_arg = (object)array(
            'type'    => 1,
            'name'    => null,
            'key'     => null,
            'stpl'    => null,
            'dval'    => null,
            'opt'     => 0,
            'neg'     => 0,
            'start'   => 0,
            'end'     => 0
        );
        $roottpl = $a; $block = null;
        $opt_args = null; $subtpl = array(); $cur_tpl = null; $arg_tpl = array(); $start_tpl = null;
        $stack = null; $s = ''; $escaped = false;
        
        $i = 0;
        while( $i < $l )
        {
            $escaped = false;
            $ch = $tpl[$i];
            if ( $ESC === $ch )
            {
                $escaped = true;
                $i += 1;
            }
            
            if ( $IDL === substr($tpl,$i,$lenIDL) )
            {
                $i += $lenIDL;
                
                if ( $escaped )
                {
                    $s .= $IDL;
                    continue;
                }
                
                if ( strlen($s) )
                {
                    if ( 0 === $a->node->type ) $a->node->val .= $s;
                    else $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> $s), $a);
                }
                
                $s = '';
            }
            else if ( $IDR === substr($tpl,$i,$lenIDR) )
            {
                $i += $lenIDR;
                
                if ( $escaped )
                {
                    $s .= $IDR;
                    continue;
                }
                
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
                
                $template = false !== strpos($argument, $REF) ? explode($REF, $argument) : array($argument,null);
                $argument = $template[0]; $template = $template[1];
                $nested = false !== strpos($argument, $DOT) ? explode($DOT, $argument) : null;
                
                if ( $cur_tpl && !isset($arg_tpl[$cur_tpl]) ) $arg_tpl[$cur_tpl] = array();
                
                if ( $TPL.$OBL === substr($tpl,$i,$lenTPL+$lenOBL) )
                {
                    // template definition
                    $i += $lenTPL;
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
                    $cur_arg->start = $start_i;
                    $cur_arg->end = $end_i;
                    // handle multiple optional arguments for same optional block
                    $opt_args = new GrammarTemplate__StackEntry(null, array($argument,$nested,$negative,$start_i,$end_i,$optional));
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
                        $cur_arg->start = $start_i;
                        $cur_arg->end = $end_i;
                    }
                    $opt_args = new GrammarTemplate__StackEntry($opt_args, array($argument,$nested,$negative,$start_i,$end_i,$optional));
                }
                else if ( !$optional && (null === $cur_arg->name) )
                {
                    $cur_arg->name = $argument;
                    $cur_arg->key = $nested;
                    $cur_arg->stpl = $template;
                    $cur_arg->dval = $default_value;
                    $cur_arg->opt = 0;
                    $cur_arg->neg = $negative;
                    $cur_arg->start = $start_i;
                    $cur_arg->end = $end_i;
                    // handle multiple optional arguments for same optional block
                    $opt_args = new GrammarTemplate__StackEntry(null, array($argument,$nested,$negative,$start_i,$end_i,0));
                }
                $a = new GrammarTemplate__TplEntry((object)array(
                    'type'    => 1,
                    'name'    => $argument,
                    'key'     => $nested,
                    'stpl'    => $template,
                    'dval'    => $default_value,
                    'opt'     => $optional,
                    'start'   => $start_i,
                    'end'     => $end_i
                ), $a);
            }
            else if ( $OBL === substr($tpl,$i,$lenOBL) )
            {
                $i += $lenOBL;
                
                if ( $escaped )
                {
                    $s .= $OBL;
                    continue;
                }
                
                // optional block
                if ( strlen($s) )
                {
                    if ( 0 === $a->node->type ) $a->node->val .= $s;
                    else $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> $s), $a);
                }
                
                $s = '';
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
                    'start'   => 0,
                    'end'     => 0
                );
                $opt_args = null;
                $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> ''));
                $block = $a;
            }
            else if ( $OBR === substr($tpl,$i,$lenOBR) )
            {
                $i += $lenOBR;
                
                if ( $escaped )
                {
                    $s .= $OBR;
                    continue;
                }
                
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
                    else $b = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> $s), $b);
                }
                
                $s = '';
                if ( $start_tpl )
                {
                    $subtpl[$start_tpl] = new GrammarTemplate__TplEntry((object)array(
                        'type'    => 2,
                        'name'    => $prev_arg->name,
                        'key'     => $prev_arg->key,
                        'start'   => 0,
                        'end'     => 0,
                        'opt_args'=> null,
                        'tpl'     => $cur_block
                    ));
                    $start_tpl = null;
                }
                else
                {
                    $a = new GrammarTemplate__TplEntry((object)array(
                        'type'    => -1,
                        'name'    => $prev_arg->name,
                        'key'     => $prev_arg->key,
                        'start'   => $prev_arg->start,
                        'end'     => $prev_arg->end,
                        'opt_args'=> $prev_opt_args,
                        'tpl'     => $cur_block
                    ), $a);
                }
            }
            else
            {
                $s .= $tpl[$i++];
            }
        }
        if ( strlen($s) )
        {
            if ( 0 === $a->node->type ) $a->node->val .= $s;
            else $a = new GrammarTemplate__TplEntry((object)array('type'=> 0, 'val'=> $s), $a);
        }
        return array($roottpl, &$subtpl);
    }

    public static function optional_block( $args, $block, &$SUB, &$FN, $index=null, $orig_args=null )
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
                    $opt_arg = self::walk( $args, $opt_v[1], array((string)$opt_v[0]), $orig_args );
                    if ( (null === $block_arg) && ($block->name === $opt_v[0]) ) $block_arg = $opt_arg;
                    
                    if ( (0 === $opt_v[2] && null === $opt_arg) || (1 === $opt_v[2] && null !== $opt_arg) )  return '';
                    $opt_vars = $opt_vars->prev;
                }
            }
        }
        else
        {
            $block_arg = self::walk( $args, $block->key, array((string)$block->name), $orig_args );
        }
        
        $arr = self::is_array( $block_arg ); $len = $arr ? count($block_arg) : -1;
        if ( $arr && ($len > $block->start) )
        {
            for($rs=$block->start,$re=(-1===$block->end?$len-1:min($block->end,$len-1)),$ri=$rs; $ri<=$re; $ri++)
                $out .= self::main( $args, $block->tpl, $SUB, $FN, $ri, $orig_args );
        }
        else if ( !$arr && ($block->start === $block->end) )
        {
            $out = self::main( $args, $block->tpl, $SUB, $FN, null, $orig_args );
        }
        return $out;
    }
    public static function non_terminal( $args, $symbol, &$SUB, &$FN, $index=null, $orig_args=null )
    {
        $out = '';
        if ( $symbol->stpl && ((!empty($SUB) && isset($SUB[$symbol->stpl])) || (!empty($FN) && isset($FN[$symbol->stpl])) || (isset(self::$fnGlobal[$symbol->stpl]))) )
        {
            // using custom function or sub-template
            $opt_arg = self::walk( $args, $symbol->key, array((string)$symbol->name), $orig_args );
        
            if ( !empty($SUB) && isset($SUB[$symbol->stpl]) )
            {
                // sub-template
                if ( (null !== $index/* || null !== $symbol->start*/) && (0 !== $index || !$symbol->opt) && self::is_array($opt_arg) )
                {
                    $opt_arg = /*null !== $index ? (*/count($opt_arg) > $index ? $opt_arg[$index] : null/*) : (count($opt_arg) > $symbol->start ? $opt_arg[$symbol->start] : null)*/;
                }
                if ( (null === $opt_arg) && (null !== $symbol->dval) )
                {
                    // default value if missing
                    $out = $symbol->dval;
                }
                else
                {
                    // try to associate sub-template parameters to actual input arguments
                    $tpl = $SUB[$symbol->stpl]->node; $tpl_args = array();
                    if ( null !== $opt_arg )
                    {
                        /*if ( isset($opt_arg[$tpl->name]) && !isset($opt_arg[$symbol->name]) ) $tpl_args = $opt_arg;
                        else $tpl_args[$tpl->name] = $opt_arg;*/
                        if ( self::is_array($opt_arg) ) $tpl_args[$tpl->name] = $opt_arg;
                        else $tpl_args = $opt_arg;
                    }
                    $out = self::optional_block( $tpl_args, $tpl, $SUB, $FN, null, null === $orig_args ? $args : $orig_args );
                }
            }
            else//if ( $fn )
            {
                // custom function
                $fn = !empty($FN) && isset($FN[$symbol->stpl]) ? $FN[$symbol->stpl] : (isset(self::$fnGlobal[$symbol->stpl]) ? self::$fnGlobal[$symbol->stpl] : null);
                
                if ( self::is_array($opt_arg) )
                {
                    $index = null !== $index ? $index : $symbol->start;
                    $opt_arg = $index < count($opt_arg) ? $opt_arg[$index] : null;
                }
                
                $opt_arg = is_callable($fn) ? call_user_func($fn, $opt_arg, $index, $args, $orig_args, $symbol) : strval($fn);
                
                $out = (null === $opt_arg) && (null !== $symbol->dval) ? $symbol->dval : strval($opt_arg);
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
            $opt_arg = self::walk( $args, $symbol->key, array((string)$symbol->name), $orig_args );
            
            // default value if missing
            if ( self::is_array($opt_arg) )
            {
                $index = null !== $index ? $index : $symbol->start;
                $opt_arg = $index < count($opt_arg) ? $opt_arg[$index] : null;
            }
            $out = (null === $opt_arg) && (null !== $symbol->dval) ? $symbol->dval : strval($opt_arg);
        }
        return $out;
    }
    public static function main( $args, $tpl, &$SUB=null, &$FN=null, $index=null, $orig_args=null )
    {
        $out = '';
        while ( $tpl )
        {
            $tt = $tpl->node->type;
            $out .= (-1 === $tt
                ? self::optional_block( $args, $tpl->node, $SUB, $FN, $index, $orig_args ) /* optional code-block */
                : (1 === $tt
                ? self::non_terminal( $args, $tpl->node, $SUB, $FN, /*0 === $index ? ($tpl->node->opt&&$tpl->node->stpl?null:$index) : */$index, $orig_args ) /* non-terminal */
                : $tpl->node->val /* terminal */
            ));
            $tpl = $tpl->next;
        }
        return $out;
    }
    
    public static $defaultDelims = array('<','>','[',']',':='/*,'?','*','!','|','{','}'*/);
    public static $fnGlobal = array();
    
    public $id = null;
    public $tpl = null;
    public $fn = null;
    protected $_args = null;
    
    public function __construct($tpl='', $delims=null, $postop=false)
    {
        $this->id = null;
        $this->tpl = null;
        $this->fn = array();
        if ( empty($delims) ) $delims = self::$defaultDelims;
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