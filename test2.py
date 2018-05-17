
from informatica import configuration
#from informatica import system
from informatica import validation



config = configuration.FromJSON()

#print config.content
#print config.content['connections']['EBS_UAT']['domain']
#print "\n\n\n"


res = validation.system_validation()
print res