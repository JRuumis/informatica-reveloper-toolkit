import json

def test123(): print 'uril...'

class FromJSON:

    def __init__(self, config_json = 'config.json'):

        print "Reading configuration JSON..."
        try:
            json_config = open(config_json,'rb')
            self.content = json.load(json_config)
        except Exception, err:
            print "Error getting configuration from JSON: %s" % err
            print "Make sure the file 'condif.json' exists in the current folder or provide full path to the JSON file."
            exit(1)

        # TODO: validate the JSON content

        print 'JSON successfully read!'

