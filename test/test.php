<?php
include "../src/php/GrammarTemplate.php";
function echo_($s='')
{
    echo $s . PHP_EOL;
}

echo_('GrammarTemplate.VERSION = ' . GrammarTemplate::VERSION);
echo_();

$tpl = "SELECT <column.select>[, <*column.select>]\nFROM <table.from>[, <*table.from>][\nWHERE (<?required.where>) AND (<?condition.where>)][\nWHERE <?required.where><?!condition.where>][\nWHERE <?!required.where><?condition.where>][\nGROUP BY <?group>[, <*group>]][\nHAVING (<?required.having>) AND (<?condition.having>)][\nHAVING <?required_.having><?!condition.having>][\nHAVING <?!required.having><?condition.having>][\nORDER BY <?order>[, <*order>]][\nLIMIT <offset|0>, <?count>]";

$sql = new GrammarTemplate($tpl);

echo_("input template:");
echo_($tpl);

echo_( );

echo_("output:");
echo_($sql->render(array(
    'column'      => array( 'select' => array( 'field1', 'field2', 'field3', 'field4' ) ),
    'table'       => array( 'from' => array( 'tbl1', 'tbl2' ) ),
    'condition'   => array( 'where' => 'field1=1 AND field2=2', 'having' => 'field3=1 OR field4=2' ),
    'count'       => 5
)));