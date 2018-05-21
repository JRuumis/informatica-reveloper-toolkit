from informatica import configuration
from informatica import validation
from informatica import pmrep


config = configuration.FromJSON()

validation_result = validation.system_validation()
if not validation_result: exit (1)


infa_connection = pmrep.Pmrep(config.content["connections"]["EBS_UAT"])
infa_connection.connect()

#ress = infa_connection.get_objects_list(object_type="folder")
#print len(ress)

#foo = infa_connection.get_repository_folders()
#print len(foo)

#wfl = infa_connection.get_folder_workflows("SILOS")
#print len(wfl)

#mpg = infa_connection.get_folder_mappings("SILOS")
#print len(mpg)


#resss = infa_connection.create_repository_folder("JANIS_from_PMREP_test2")

#if not resss:
#    print "Error creating folder!!!"


export_outcome = infa_connection.export_repository_folders(config.content['folders_to_migrate'], '~/InfaTest/exports')
import_outcome = infa_connection.import_all_xmls_from_folder('~/InfaTest/exports', True)

#export_outcome = infa_connection.export_repository_folder("Janis_BIDW_CUSTOM_SILOS", "")
#import_outcome = infa_connection.import_repository_folder("Folder___BIDW_UAT_EBS_961___Janis_BIDW_CUSTOM_SILOS.xml")





