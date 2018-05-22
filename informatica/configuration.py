import json

def test123(): print 'uril...'

class get_from_json:

    def __init__(self, config_json = 'config.json'):

        print "Reading configuration JSON..."
        try:
            json_config = open(config_json,'rb')
            self.content = json.load(json_config)
        except Exception, err:
            print "Error getting configuration from JSON: %s" % err
            print "Make sure the file 'condif.json' exists in the current folder or provide full path to the JSON file."
            exit(1)

        print 'JSON successfully read.'
        print 'JSON file structure is valid but the content has not yet been validated.\n'

