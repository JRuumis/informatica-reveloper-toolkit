from informatica import configuration
from informatica import access_validation
from informatica import pmrep


config = configuration.FromJSON()

validation_result = access_validation.check()
if not validation_result: exit (1)




infa_connection = pmrep.Pmrep(config.content["connections"]["EBS_UAT"])

infa_connection.connect()
ress = infa_connection.get_objects_list(object_type="folder")
print len(ress)

foo = infa_connection.get_repository_folders
print len(foo)

wfl = infa_connection.get_workflows("SILOS")
print len(wfl)

mpg = infa_connection.get_mappings("SILOS")
print len(mpg)


resss = infa_connection.create_repository_folder("JANIS_from_PMREP_test2")
#if not resss:
#    print "Error creating folder!!!"


ffff = infa_connection.export_repository_folder("Janis_BIDW_CUSTOM_SILOS","")


gggg = infa_connection.import_repository_folder("Folder___BIDW_UAT_EBS_961___Janis_BIDW_CUSTOM_SILOS.xml")

#



