
from informatica import configuration
#from informatica import system
from informatica import access_validation



config = configuration.get_from_json()

#print config.content
#print config.content['connections']['EBS_UAT']['domain']
#print "\n\n\n"


res = access_validation.check()
print res