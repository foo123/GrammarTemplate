# GrammarTemplate

`GrammarTemplate` versatile and intuitive grammar-based templating for PHP, Python, Node/XPCOM/JS, ActionScript (see for example [here](https://github.com/foo123/Dialect) and [here](https://github.com/foo123/RhoLambda) and [eventualy there](https://github.com/foo123/Xpresion))


![GrammarTemplate](/grammartemplate.jpg)


[Etymology of *"grammar"*](http://www.etymonline.com/index.php?term=grammar)
[Etymology of *"template"*](http://www.etymonline.com/index.php?term=template)


**light-weight (~5.5kB minified, ~2.4kB zipped)**

* `GrammarTemplate` is also a `XPCOM JavaScript Component` (Firefox) (e.g to be used in firefox browser addons/plugins)


**version 2.1.1** [GrammarTemplate.js](https://raw.githubusercontent.com/foo123/GrammarTemplate/master/src/js/GrammarTemplate.js), [GrammarTemplate.min.js](https://raw.githubusercontent.com/foo123/GrammarTemplate/master/src/js/GrammarTemplate.min.js)

[Live Playground Example](https://foo123.github.io/examples/grammar-template)


**see also:**  

* [Contemplate](https://github.com/foo123/Contemplate) a light-weight template engine for Node/XPCOM/JS, PHP, Python, ActionScript
* [HtmlWidget](https://github.com/foo123/HtmlWidget) html widgets used as (template) plugins and/or standalone for PHP, Node/XPCOM/JS, Python both client and server-side
* [Tao](https://github.com/foo123/Tao.js) A simple, tiny, isomorphic, precise and fast template engine for handling both string and live dom based templates
* [ModelView](https://github.com/foo123/modelview.js) a light-weight and flexible MVVM framework for JavaScript/HTML5
* [ModelView MVC jQueryUI Widgets](https://github.com/foo123/modelview-widgets) plug-n-play, state-full, full-MVC widgets for jQueryUI using modelview.js (e.g calendars, datepickers, colorpickers, tables/grids, etc..) (in progress)
* [Dromeo](https://github.com/foo123/Dromeo) a flexible, agnostic router for Node/XPCOM/JS, PHP, Python, ActionScript
* [Regex Analyzer/Composer](https://github.com/foo123/RegexAnalyzer) Regular Expression Analyzer and Composer for Node/XPCOM/JS, PHP, Python, ActionScript
* [GrammarPattern](https://github.com/foo123/GrammarPattern) versatile grammar-based pattern-matching for Node/XPCOM/JS (IN PROGRESS)
* [Xpresion](https://github.com/foo123/Xpresion) a simple and flexible eXpression parser engine (with custom functions and variables support) for PHP, Python, Node/XPCOM/JS, ActionScript
* [Dialect](https://github.com/foo123/Dialect) a simple cross-platform SQL construction for PHP, Python, Node/XPCOM/JS, ActionScript
* [PublishSubscribe](https://github.com/foo123/PublishSubscribe) a simple and flexible publish-subscribe pattern implementation for Node/XPCOM/JS, PHP, Python, ActionScript
* [RT](https://github.com/foo123/RT) client-side real-time communication for Node/XPCOM/JS with support for Poll/BOSH/WebSockets
* [Asynchronous](https://github.com/foo123/asynchronous.js) a simple manager for async, linearised, parallelised, interleaved and sequential tasks for JavaScript


###API

**Grammar Template**

A block inside `[..]` represents an optional block of `code` (depending on passed parameters) and `<..>` describe placeholders for `query` parameters / variables (i.e `non-terminals`).
The optional block of code depends on whether **all** optional parameters defined inside (with `<?..>`, `<?!..>` or `<*..>` and `<{n,m}..>` for rest parameters) exist. Then, that block (and any nested blocks it might contain) is output, else bypassed.

A block defined with `:=[..]` represents a (recursive) sub-template, which can be used to render any deep/structured argument a needed (see below).


```javascript
var GrammarTemplate = require("../src/js/GrammarTemplate.js"), echo = console.log;

echo('GrammarTemplate.VERSION = ' + GrammarTemplate.VERSION);
echo( );

var tpl = "SELECT <column.select>[, <*column.select>]\nFROM <table.from>[, <*table.from>][\nWHERE (<?required.where>) AND (<?condition.where>)][\nWHERE <?required.where><?!condition.where>][\nWHERE <?!required.where><?condition.where>][\nGROUP BY <?group>[, <*group>]][\nHAVING (<?required.having>) AND (<?condition.having>)][\nHAVING <?required.having><?!condition.having>][\nHAVING <?!required.having><?condition.having>][\nORDER BY <?order>[, <*order>]][\nLIMIT <offset|0>, <?count>]";

var sql = new GrammarTemplate( tpl );

echo("input template:");
echo(tpl);

echo( );

echo("output:");
echo(sql.render({
    column      : { select : [ 'field1', 'field2', 'field3', 'field4' ] },
    table       : { from : [ 'tbl1', 'tbl2' ] },
    condition   : { where : 'field1=1 AND field2=2', having : 'field3=1 OR field4=2' },
    count       : 5
}));
```

**output**
```text
GrammarTemplate.VERSION = 2.0.0

input template:
SELECT <column.select>[, <*column.select>]
FROM <table.from>[, <*table.from>]
[WHERE (<?required.where>) AND (<?condition.where>)]
[WHERE <?required.where><?!condition.where>]
[WHERE <?!required.where><?condition.where>]
[GROUP BY <?group>[, <*group>]]
[HAVING (<?required.having>) AND (<?condition.having>)]
[HAVING <?required.having><?!condition.having>]
[HAVING <?!required.having><?condition.having>]
[ORDER BY <?order>[, <*order>]]
[LIMIT <offset|0>, <?count>]

output:
SELECT field1, field2, field3, field4
FROM tbl1, tbl2
WHERE field1=1 AND field2=2
HAVING field3=1 OR field4=2
LIMIT 0, 5

```

```javascript
var GrammarTemplate = require("../src/js/GrammarTemplate.js"), echo = console.log;

echo('GrammarTemplate.VERSION = ' + GrammarTemplate.VERSION);
echo( );

/*
    i.e: 
    foreach "expression:terms" as "term":
        foreach "term:factors" as "factor":
            ..
    
    here an :EXPR template is defined which itself uses (anonymous) sub-templates
    it is equivalent to (expand sub-templates to distinct):

<:FACTOR>:=[<lhs>[ <?op> <rhs|NULL>]]

<:TERM>:=[(<factor:FACTOR>[ AND <*factor:FACTOR>])]

<:EXPR>:=[<term:TERM>[ OR <*term:TERM>]]

<expression:EXPR>
<expression2:EXPR>

*/

var tpl = "<:EXPR>:=[<term>:=[(<factor>:=[<lhs>[ <?op> <rhs|NULL>]][ AND <*factor>])][ OR <*term>]]<expression:EXPR>\n<expression2:EXPR>";

var expr = new GrammarTemplate( tpl );

echo("input template:");
echo(tpl);

echo( );

echo("output:");
echo(expr.render({
    expression  : [
        // term
        [
            // factor
            {lhs: 1, op: '=', rhs: 1},
            // factor
            {lhs: 1, op: '=', rhs: 2},
            // factor
            {lhs: 1, op: '=', rhs: 3}
        ],
        // term
        [
            // factor
            {lhs: 1, op: '<', rhs: 1},
            // factor
            {lhs: 1, op: '<', rhs: 2},
            // factor
            {lhs: 1, op: '<', rhs: 3}
        ],
        // term
        [
            // factor
            {lhs: 1, op: '>', rhs: 1},
            // factor
            {lhs: 1, op: '>', rhs: 2},
            // factor
            {lhs: 1, op: '>', rhs: 3}
        ]
    ],
    expression2  : [
        // term
        [
            // factor
            {lhs: 2, op: '=', rhs: 1},
            // factor
            {lhs: 2, op: '=', rhs: 2},
            // factor
            {lhs: 2, op: '=', rhs: 3}
        ],
        // term
        [
            // factor
            {lhs: 2, op: '<', rhs: 1},
            // factor
            {lhs: 2, op: '<', rhs: 2},
            // factor
            {lhs: 2, op: '<', rhs: 3}
        ],
        // term
        [
            // factor
            {lhs: 2, op: '>', rhs: 1},
            // factor
            {lhs: 2, op: '>', rhs: 2},
            // factor
            {lhs: 2, op: '>', rhs: 3}
        ],
        // term
        [
            // factor
            {lhs: 3},
            // factor
            {lhs: 3, op: '!='}
        ]
    ]
}));
```
**output**
```text
GrammarTemplate.VERSION = 2.0.0

input template:
<:EXPR>:=[<term>:=[(<factor>:=[<lhs>[ <?op> <rhs|NULL>]][ AND <*factor>])][ OR <*term>]]
<expression:EXPR>
<expression2:EXPR>

output:
(1 = 1 AND 1 = 2 AND 1 = 3) OR (1 < 1 AND 1 < 2 AND 1 < 3) OR (1 > 1 AND 1 > 2 AND 1 > 3)
(2 = 1 AND 2 = 2 AND 2 = 3) OR (2 < 1 AND 2 < 2 AND 2 < 3) OR (2 > 1 AND 2 > 2 AND 2 > 3) OR (3 AND 3 != NULL)
```

###TODO

* handle literal symbols (so for example grammar-specific delimiters can also be used literaly, right now delimiters can be adjusted as parameters) [DONE, through escaping]
* handle nested/deep arguments [DONE, through nested object-dot notation]
* handle recursion/loop deep structured arguments and sub-templates [DONE, through defining recursive sub-templates for rendering any deep argument]
* handle boolean-like optional arguments [DONE, through setting (empty) default value for optional argumement, is handled as pure boolean on/off flag argument]
* optimise parsing and rendering [DONE]
* support some basic and/or user-defined functions [DONE, similar custom function definition as custom sub-template, calls function if custom function with same name has been defined]
* support both `pre-` and `post-` (repeat) grammar operators, i.e both `<?symbol>`,`<*symbol>`,`<{n,m}symbol>` and `<symbol>?`,`<symbol>*`,`<symbol>{n,m}` for more familiar grammar syntax [DONE, via extra parameter in template instantiation]
