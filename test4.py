from common import config
from informatica import OBSOLETE___access_validation
from informatica import pmrep


config = config.get_from_json()

validation_result = OBSOLETE___access_validation.check()
if not validation_result: exit (1)


infa_connection = pmrep.Pmrep(config.content)
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

#export_outcome = infa_connection.export_repository_folder("Janis_BIDW_CUSTOM_SILOS", "")
#import_outcome = infa_connection.import_repository_folder("Folder___BIDW_UAT_EBS_961___Janis_BIDW_CUSTOM_SILOS.xml")


# todo: import output to log - DONE
# todo: export to log - DONE
# todo: folder to migrate - auto - DONE
# todo: infa test exports folder - also in config - DONE
# todo: git
# todo: infa validation - to informatica class
# todo: git validation - to git class
# todo: calling from command line
    # todo: export (git)
    # todo: import, (git)
    # todo: duplicate folder with different name
    # todo: create folder
    # todo: delete folder
# todo: REFACTOR (4 - 12h)

#infa_connection.duplicate_rename_informatica_folder('BIDW_CUSTOM_GDD', 'Janis_BIDW_CUSTOM_GDD')
#infa_connection.duplicate_rename_informatica_folder('BIDW_CUSTOM_PLP', 'Janis_BIDW_CUSTOM_PLP')
#infa_connection.duplicate_rename_informatica_folder('BIDW_CUSTOM_SDE_ORA12', 'Janis_BIDW_CUSTOM_SDE_ORA12')

#export_outcome = infa_connection.export_repository_folders(config.content['folders_to_migrate'], '/home/c51102a/InfaTest/exports')
#import_outcome = infa_connection.import_all_xmls_from_folder('/home/c51102a/InfaTest/exports', True)


export_outcome = infa_connection.do_export()
import_outcome = infa_connection.do_import()




