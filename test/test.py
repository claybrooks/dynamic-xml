import dynamicxml

data = {
    "beams": {
       "BEAM_ID_1": {
            "getAngle": 50,
            "getRate": 10,
            "getRotationalVelocity": 5,
        },
    },
    "antennas": {
        "ANTENNA_ID_1": {
            "getBeams": [
                "BEAM_ID_1"
            ],
            "getType": "ANTENNA_TYPE_1",
        }
    }
}

class Environment:
    def __init__(self):

        #with open(file_path, 'r') as f:
        self.data = dict(data)#json.load(f)
        self.inject()

    def inject(self):
        for object_class_key, object_class_value in self.data.items():
            for key in object_class_value:
                setattr(self, key, self.data[object_class_key][key])

env = Environment()
print (env.BEAM_ID_1)
print (env.ANTENNA_ID_1)

root = dynamicxml.parse('data/ConfigFile.xml')

print (root.tag)

runtimeNode = root.Runtime[0]

print (runtimeNode.attr_timeout)
print (runtimeNode.attr_runtimeDataPath)

runtimeNode.attr_timeout = str(int(runtimeNode.attr_timeout) + 1)

dynamicxml.write('data/ConfigFile_Updated.xml', root)
