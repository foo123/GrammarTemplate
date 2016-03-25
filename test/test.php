<?php
include "../src/php/GrammarTemplate.php";
function echo_($s='')
{
    echo $s . PHP_EOL;
}

echo_('GrammarTemplate.VERSION = ' . GrammarTemplate::VERSION);
echo_();

$sql = new GrammarTemplate("SELECT <select_columns>[,<*select_columns>]\nFROM <from_tables>[,<*from_tables>][\n<?join_clauses>[\n<*join_clauses>]][\nWHERE (<?where_conditions_required>) AND (<?where_conditions>)][\nWHERE <?where_conditions_required><?!where_conditions>][\nWHERE <?!where_conditions_required><?where_conditions>][\nGROUP BY <?group_conditions>[,<*group_conditions>]][\nHAVING (<?having_conditions_required>) AND (<?having_conditions>)][\nHAVING <?having_conditions_required><?!having_conditions>][\nHAVING <?!having_conditions_required><?having_conditions>][\nORDER BY <?order_conditions>[,<*order_conditions>]][\nLIMIT <offset|0>,<?count>]");

echo_($sql->render(array(
    'select_columns'=>array('field1','field2','field3'),
    'from_tables'=>array('tbl1','tbl2'),
    'where_conditions'=> 'field1=1 AND field2=2',
    'count'=> 5
)));