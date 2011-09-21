Introduction
============

Bumblebee is a deliverance-like html transformation framwork
implementation that only works on the output an html document.

It doesn't use xslt so it isn't as fast as what Diazo is; however,
it accomplishes the very simple use-case of moving elements around
on html output.


Why
---

Because I almost never needed the full-fledge deliverance approach
for what I wanted to do. In fact, it was usually an annoyance when
all I wanted to do was move an element around on a page.


How-to Use
==========

Configurating your transformations is done with a very xml syntax.

Example:

HTML::

    <html>
        <head></head>
        <body>
            <div id="#header"></div>
            <div id="content"></div>
            <div id="footer"></div>
        </body>
    </html>


Rules XML::
    
    <xml>
        <block if-content="#content">
            <after src="#header" dst="#footer" />
        </block>
    </xml>


Running it through::
    
    from bumblebee import transform
    from repoze.xmliter.utils import getHTMLSerializer
    from bumblebee.xml import convertRules

    html = getHTMLSerializer(output)
    rules = convertRules(rules_xml)
    result = transform(html, rules)


Selectors
---------

For xml configuration that selects elements, you can use CSS selectors(default)
or XPath.

To use XPath, just append '-path' onto the node name::

    <after src-xpath="/html/body/div[0]" src-xpath="/html/body/div[2]" />


arbitrary html
~~~~~~~~~~~~~~

Use this to inject html into a page::

    <after src-html="" dst="#foo">
        <div id="foobar">
            <h1>hello, world</h1>
        </div>
    </after>


Rules
-----

Before
~~~~~~

Move an element before another element::

    <before src="#foo" dst="#bar" />

Moves "#foo" before "#bar"

After
~~~~~

Move an element after another::

    <after src="#foo" "#bar" />

Moves "#foo" after "#bar"

Drop
~~~~

Remove an element from the dom::

    <drop src="#foo" />

Replace
~~~~~~~

Replace an element with another::

    <replace src="#foo" dst="#bar" />

Replaces "#dst" with "#src"


Class
~~~~~

Add or remove classes from an element::

    <class src="#foo" add="three four" remove="one two" />

Remove the classes "one" and "two" from "#foo" and add
the classes "three" and "four".


Tag
~~~

Change a tag::

    <tag src="#foo" tag="p" />


Attributes
~~~~~~~~~~

Add, remove and replace attributes.

To copy from another node::

    <attributes src="#foo" dst="#bar" add="class style" remove="width" replace="id" />

Adds the class and style attributes from src to dst, removes the
width attribute from dst and replaces the dst id with the src id.


Add them inline::

    <attributes src="#foo" add="class=foo bar" replace="id=bar" />

Add attribute class(if not present) and add "foo bar" to src and replace
the id of src with "bar"


Group
~~~~~

Group rules together with a conditions::

    <group if-content="#foo">
        <drop src="#bar" />
    </group>

Performs some rules if "#foo" is in the document.


Conditions
----------

if-content
~~~~~~~~~~

Performs actions if the selector is found in the document::

    <after src="#foo" dst="#bar" if-content="#foo" />


not conditiion
~~~~~~~~~~~~~~

Any condition can be negated for the opposite affect::

    <drop src="#foo" if-not-content="#bar" />


Extending
---------

Creating a Rule::
    
    from bumblebee.rules import BaseDouble
    class Append(BaseDouble):
        def __call__(self, root):
            src, dst, skip = self.process_nodes(root)
            if skip:
                return None
            dst = dst[0]
            for el in dst:
                dst.append(el)
            return src
    
    from bumblebee.xml import addTag
    addTag('append', Append)

To use the rule, you would::

    <append src="#foo" dst="#bar" />


Creating a Condition::

    from bumblebee.conditions import BaseIf
    class IfPath(BaseIf):
        def __init__(self, path, extras={}):
            super(IfPath, self).__init__(extras)
            self.path = path
        def __call__(self, root):
            req = self.extras['request']
            path = req['PATH_INFO']
            if self.path.startswith('/'):
                return path.startswith(self.path)
            else:
                return self.path in path
    from bumblebee.xml import addCondition
    addCondition('path', IfPath)

To use this condition, you would::

    <drop src="#foo" if-path="/foo/bar" />

or::

    <drop src="#foo" if-not-path="/foo/bar" />

