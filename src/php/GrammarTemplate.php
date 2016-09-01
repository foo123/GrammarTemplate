<?php
/**
*   GrammarTemplate, 
*   versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript
* 
*   @version: 1.1.0
*   https://github.com/foo123/GrammarTemplate
*
**/
if ( !class_exists('GrammarTemplate') )
{
class GrammarTemplate
{    
    const VERSION = '1.1.0';
    
    private static function walk( $obj, $keys )
    {
        $o = $obj; $l = count($keys); $i = 0;
        while( $i < $l )
        {
            $k = $keys[$i++];
            if ( isset($o) )
            {
                if ( is_array($o) && isset($o[$k]) )
                    $o = $o[$k];
                elseif ( is_object($o) && isset($o->{$k}) )
                    $o = $o->{$k};
                else return null;
            }
            else return null;
        }
        return $o;
    }
    
    public static function multisplit( $tpl, $delims )
    {
        $IDL = $delims[0]; $IDR = $delims[1]; $OBL = $delims[2]; $OBR = $delims[3];
        $lenIDL = strlen($IDL); $lenIDR = strlen($IDR); $lenOBL = strlen($OBL); $lenOBR = strlen($OBR);
        $ESC = '\\'; $OPT = '?'; $OPTR = '*'; $NEG = '!'; $DEF = '|'; $REPL = '{'; $REPR = '}';
        $default_value = null; $negative = 0; $optional = 0; $start_i = 0; $end_i = 0;
        $l = strlen($tpl);
        $i = 0; $a = array(array(), null, null, 0, 0, 0, 0, null); $stack = array(); $s = ''; $escaped = false;
        while( $i < $l )
        {
            $ch = $tpl[$i];
            if ( $ESC === $ch )
            {
                $escaped = !$escaped;
                $i += 1;
            }
            
            if ( $IDL === substr($tpl,$i,$lenIDL) )
            {
                if ( $escaped )
                {
                    $s .= $IDL;
                    $i += $lenIDL;
                    $escaped = false;
                    continue;
                }
                
                $i += $lenIDL;
                if ( strlen($s) ) $a[0][] = array(0, $s);
                $s = '';
            }
            elseif ( $IDR === substr($tpl,$i,$lenIDR) )
            {
                if ( $escaped )
                {
                    $s .= $IDR;
                    $i += $lenIDR;
                    $escaped = false;
                    continue;
                }
                
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
                $c = $argument[0];
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
                    $argument = substr($argument,1);
                    if ( $NEG === $argument[0] )
                    {
                        $negative = 1;
                        $argument = substr($argument,1);
                    }
                    else
                    {
                        $negative = 0;
                    }
                }
                elseif ( $REPL === $c )
                {
                    $s = ''; $j = 1; $jl = strlen($argument);
                    while ( $j < $jl && $REPR !== $argument[$j] ) $s .= $argument[$j++];
                    $argument = substr($argument, $j+1);
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
                
                $nested = false !== strpos($argument, '.') ? explode('.', $argument) : null;
                
                if ( $optional && !$a[2] )
                {
                    $a[1] = $argument;
                    $a[2] = $nested;
                    $a[3] = $optional;
                    $a[4] = $negative;
                    $a[5] = $start_i;
                    $a[6] = $end_i;
                    // handle multiple optional arguments for same optional block
                    $a[7] = array(array($argument,$negative,$start_i,$end_i,$nested));
                }
                elseif( $optional )
                {
                    // handle multiple optional arguments for same optional block
                    $a[7][] = array($argument,$negative,$start_i,$end_i,$nested);
                }
                elseif ( !$optional && (null === $a[1]) )
                {
                    $a[1] = $argument;
                    $a[2] = $nested;
                    $a[3] = 0;
                    $a[4] = $negative;
                    $a[5] = $start_i;
                    $a[6] = $end_i;
                    $a[7] = array(array($argument,$negative,$start_i,$end_i,$nested));
                }
                $a[0][] = array(1, $argument, $nested, $default_value, $optional, $negative, $start_i, $end_i);
            }
            elseif ( $OBL === substr($tpl,$i,$lenOBL) )
            {
                if ( $escaped )
                {
                    $s .= $OBL;
                    $i += $lenOBL;
                    $escaped = false;
                    continue;
                }
                
                $i += $lenOBL;
                // optional block
                if ( strlen($s) ) $a[0][] = array(0, $s);
                $s = '';
                $stack[] = $a;
                $a = array(array(), null, null, 0, 0, 0, 0, null);
            }
            elseif ( $OBR === substr($tpl,$i,$lenOBR) )
            {
                if ( $escaped )
                {
                    $s .= $OBR;
                    $i += $lenOBR;
                    $escaped = false;
                    continue;
                }
                
                $i += $lenOBR;
                $b = $a; $a = array_pop($stack);
                if ( strlen($s) ) $b[0][] = array(0, $s);
                $s = '';
                $a[0][] = array(-1, $b[1], $b[2], $b[3], $b[4], $b[5], $b[6], $b[7], $b[0]);
            }
            else
            {
                if ( $ESC === $ch ) $s .= $ch;
                else $s .= $tpl[$i++];
            }
        }
        if ( strlen($s) ) $a[0][] = array(0, $s);
        return $a[0];
    }
    
    public static $defaultDelims = array('<','>','[',']'/*,'?','*','!','|','{','}'*/);
    
    public $id = null;
    public $tpl = null;
    protected $_args = null;
    protected $_parsed = false;
    
    public function __construct($tpl='', $delims=null)
    {
        $this->id = null;
        $this->tpl = null;
        if ( empty($delims) ) $delims = self::$defaultDelims;
        // lazy init
        $this->_args = array($tpl, $delims);
        $this->_parsed = false;
    }

    public function __destruct()
    {
        $this->dispose();
    }
    
    public function dispose()
    {
        $this->id = null;
        $this->tpl = null;
        $this->_args = null;
        $this->_parsed = null;
        return $this;
    }
    
    public function parse( )
    {
        if ( false === $this->_parsed )
        {
            // lazy init
            $this->_parsed = true;
            $this->tpl = self::multisplit( $this->_args[0], $this->_args[1] );
            $this->_args = null;
        }
        return $this;
    }
    
    public function render($args=null)
    {
        if ( false === $this->_parsed )
        {
            // lazy init
            $this->parse( );
        }
        
        if ( null === $args ) $args = array();
        
        $tpl = $this->tpl; $l = count($tpl); $stack = array();
        $rarg = null; $ri = 0; $out = '';
        $i = 0;
        while ( $i < $l || !empty($stack) )
        {
            if ( $i >= $l )
            {
                $p = array_pop($stack);
                $tpl = $p[0]; $i = $p[1]; $l = $p[2];
                $rarg = $p[3]; $ri = $p[4];
                continue;
            }
            
            $t = $tpl[ $i ]; $tt = $t[ 0 ]; $s = $t[ 1 ];
            if ( -1 === $tt )
            {
                // optional block
                $opts_vars = $t[ 7 ];
                if ( !empty($opts_vars) )
                {
                    $render = true;
                    foreach($opts_vars as $opt_v)
                    {
                        $opt_arg = $opt_v[4] ? self::walk( $args, $opt_v[4] ) : (isset($args[$opt_v[0]]) ? $args[$opt_v[0]] : null);
                        if ( (0 === $opt_v[1] && !isset($opt_arg)) ||
                            (1 === $opt_v[1] && isset($opt_arg))
                        )
                        {
                            $render = false;
                            break;
                        }
                    }
                    if ( $render )
                    {
                        if ( 1 === $t[ 4 ] )
                        {
                            $stack[] = array($tpl, $i+1, $l, $rarg, $ri);
                            $tpl = $t[ 8 ]; $i = 0; $l = count($tpl);
                            $rarg = null; $ri = 0;
                            continue;
                        }
                        else
                        {
                            $opt_arg = $t[2] ? self::walk( $args, $t[2] )/*nested key*/ : $args[$s]/*plain key*/;
                            $arr = is_array( $opt_arg ); $arr_len = $arr ? count($opt_arg) : 1;
                            if ( $arr && ($t[5] !== $t[6]) && ($arr_len > $t[ 5 ]) )
                            {
                                $rs = $t[ 5 ];
                                $re = -1 === $t[ 6 ] ? $arr_len-1 : min($t[ 6 ], $arr_len-1);
                                if ( $re >= $rs )
                                {
                                    $stack[] = array($tpl, $i+1, $l, $rarg, $ri);
                                    $tpl = $t[ 8 ]; $i = 0; $l = count($tpl);
                                    $rarg = $s;
                                    for($ri=$re; $ri>$rs; $ri--) $stack[] = array($tpl, 0, $l, $rarg, $ri);
                                    $ri = $rs;
                                    continue;
                                }
                            }
                            else if ( !$arr && ($t[5] === $t[6]) )
                            {
                                $stack[] = array($tpl, $i+1, $l, $rarg, $ri);
                                $tpl = $t[ 8 ]; $i = 0; $l = count($tpl);
                                $rarg = $s; $ri = 0;
                                continue;
                            }
                        }
                    }
                }
            }
            else if ( 1 === $tt )
            {
                // default value if missing
                $opt_arg = $t[2] ? self::walk( $args, $t[2] )/*nested key*/ : (isset($args[$s]) ? $args[$s] : null)/*plain key*/;
                $out .= !isset($opt_arg) && (null !== $t[ 3 ])
                    ? $t[ 3 ]
                    : (is_array($opt_arg)
                    ? ($s === $rarg
                    ? $opt_arg[$t[6]===$t[7]?$t[6]:$ri]
                    : $opt_arg[$t[6]])
                    : $opt_arg)
                ;
            }
            else /*if ( 0 === $tt )*/
            {
                $out .= $s;
            }
            $i++;
        }
        return $out;
    }
}    
}