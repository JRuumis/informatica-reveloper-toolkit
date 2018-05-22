from common import config
from version_control import git_control


config = config.get_from_json()


#validation_result = access_validation.check()  # todo: nesmuki. sho vajadzeetu infa konstruktoraa
#if not validation_result: exit (1) # exit vajadzeetu validatoraa

#infa_connection = pmrep.Pmrep(config.content) # todo: vienkaarshi config, content resolution jaavuut funkcijaas
#infa_connection.connect()



# todo: DONE - import output to log - DONE
# todo: DONE - export to log - DONE
# todo: DONE - folder to migrate - auto - DONE
# todo: DONE - infa test exports folder - also in config - DONE

# todo: git
# todo: code ---> to rm git !!!!!!!!!!!!!
# todo: infa validation - to informatica class
# todo: DONE - git validation - to git class
# todo: calling from command line
    # todo: export (git)
    # todo: import, (git)
    # todo: duplicate folder with different name
    # todo: create folder
    # todo: delete folder
# todo: REFACTOR (4 - 12h)


git_access = git_control.Git(config)


current_branch = git_access.get_current_branch()
print 'currently in branch: %s' % current_branch






#export_outcome = infa_connection.export_control()
#import_outcome = infa_connection.import_control()



