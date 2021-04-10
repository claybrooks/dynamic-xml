import dynamicxml

root = dynamicxml.parse('data/ConfigFile.xml')

print (root.tag)

runtimeNode = root.Runtime[0]

print (runtimeNode.attr_timeout)
print (runtimeNode.attr_runtimeDataPath)

runtimeNode.attr_timeout = str(int(runtimeNode.attr_timeout) + 1)

dynamicxml.write('data/ConfigFile_Updated.xml', root)
