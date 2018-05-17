from informatica import configuration
from informatica import validation
from informatica import pmrep


config = configuration.FromJSON()

validation_result = validation.system_validation()
if not validation_result: exit (1)




infa_connection = pmrep.Pmrep(config.content["connections"]["EBS_UAT"])

infa_connection.connect()
infa_connection.get_objects_list(object_type="folder")



