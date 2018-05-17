from informatica import system
import re


class Pmrep:
    def __init__(self, connection):
        self.connection = connection

    def connect(self):

        print "Connecting to Informatica pmrep..."

        connect_command = "pmrep connect -r %s -d %s -n %s -x %s" % \
                          (self.connection["repository"], self.connection["domain"], self.connection["login_name"], self.connection["password"])

        connect_result = system.execute_command_line(connect_command)

        if "connect completed successfully" in connect_result:
            print "Connect to pmrep successful!"
            return True
        else:
            print "ERROR: Connect to pmrep failed!"
            print "Connect returned message: %s" % connect_result
            return False

    def get_objects_list(self, object_type, folder=None):

        listing_command_head = "pmrep listobjects -o %s" % object_type
        if folder:
            additional_folder = " -f %s" % folder
        else:
            additional_folder = ""

        listing_command = listing_command_head + additional_folder

        listing_result = system.execute_command_line(listing_command)

        if not ".listobjects completed successfully." in listing_result:
            print "ERROR: Listing command %s was unsuccessful!"
            print "Message returned:\n%s" & listing_result
        else:

            results_search = "Invoked at (?:.*?$)(.*).listobjects completed successfully."

            res = re.search(results_search, listing_result, re.MULTILINE|re.DOTALL)
            if res:
                #print "regsearch 1: %s" % res.group(1)
                objects_list = res.group(1).splitlines()
                objects_list_cleaned = [o.strip() for o in objects_list if len(o) > 0]

                return objects_list_cleaned  # TODO: add column split
            else:
                print "listobjects parse result appears to be empty: %s" % str(res)
                return List()





    # pmrep createFolder
    # pmrep objectexport
    # pmrep objectimport
    # pmrep listobjects  <- can list folders
    # pmrep updateseqgenvals <-- updates sequence values!
    # pmrep VALIDATION
    # pmrep backup and restore
