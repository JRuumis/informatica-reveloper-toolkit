from informatica import configuration
from informatica import access_validation
from informatica import pmrep
from version_control import git


config = configuration.get_from_json()

validation_result = access_validation.check()  # todo: nesmuki. sho vajadzeetu infa konstruktoraa
if not validation_result: exit (1) # exit vajadzeetu validatoraa


infa_connection = pmrep.Pmrep(config.content) # todo: vienkaarshi config, content resolution jaavuut funkcijaas
infa_connection.connect()

# todo: import output to log - DONE
# todo: export to log - DONE
# todo: folder to migrate - auto - DONE
# todo: infa test exports folder - also in config - DONE

# todo: git
# todo: rm git !!!!!!!!!!!!!
# todo: infa validation - to informatica class
# todo: git validation - to git class
# todo: calling from command line
    # todo: export (git)
    # todo: import, (git)
    # todo: duplicate folder with different name
    # todo: create folder
    # todo: delete folder
# todo: REFACTOR (4 - 12h)


ggg = git.Git()

asdf = ggg.validate_environment()





#export_outcome = infa_connection.export_control()
#import_outcome = infa_connection.import_control()



