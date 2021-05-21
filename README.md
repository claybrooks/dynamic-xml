# dynamicxml

A simple extension of Etree that gives users the ability to directly access attributes and nodes without having to
implement boilerplate python code.

Rationale for this library: [Dynamic XML Library with Python](https://claybrooks.github.io/python/2021/04/09/python-dynamic-xml.html)

Pip Installer: [pip](https://pypi.org/project/dynamicxml/)

python -m pip install dynamicxml

`DynamicElement` is a drop-in replacement for any Etree code that you already have

```xml
<!-- ConfigFile.xml -->
<ConfigurationData>
    <Runtime timeout="1000" runtimeDataPath="/path/to/runtime/data" />
</ConfigurationData>
```

```python
# main.py
import dynamicxml

# parse the data and get back an instance of DynamicElement
root = dynamicxml.parse('data/ConfigFile.xml')

# Print the tag of the root element, just like you would a typical etree
# element
print (root.tag)

# get access to the runtime data node, which is a child of
# <ConfigurationData />.  The library returns a list of child
# nodes, regardless of how many elements there are.  An "AttributeError"
# is raised if the node does not exist.
runtimeNode = root.Runtime[0]

# Access the attributes of the node directly using the "attr_" prefix.
print (runtimeNode.attr_timeout)
print (runtimeNode.attr_runtimeDataPath)

# set the data directly
runtimeNode.attr_timeout = str(int(runtimeNode.attr_timeout) + 1)

# easy writing of the data
dynamicxml.write('data/ConfigFile_Updated.xml', root)

```