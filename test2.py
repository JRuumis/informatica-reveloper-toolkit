from common import config
#from informatica import system
from informatica import OBSOLETE___access_validation



config = config.get_from_json()

#print config.content
#print config.content['connections']['EBS_UAT']['domain']
#print "\n\n\n"


res = OBSOLETE___access_validation.check()
print res