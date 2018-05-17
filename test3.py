from informatica import configuration
from informatica import validation
from informatica import pmrep


config = configuration.FromJSON()

validation_result = validation.system_validation()
if not validation_result: exit (1)




infa_connection = pmrep.Pmrep(config.content["connections"]["EBS_UAT"])

infa_connection.connect()
ress = infa_connection.get_objects_list(object_type="folder")
print ress

foo = infa_connection.get_repository_folders()
print foo

wfl = infa_connection.get_folder_workflows("SILOS")
print wfl

mpg = infa_connection.get_folder_mappings("SILOS")
print mpg




