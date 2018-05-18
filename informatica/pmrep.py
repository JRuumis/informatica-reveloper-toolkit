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

        if not "listobjects completed successfully." in listing_result:
            print "ERROR: Listing command was unsuccessful!"
            print "Message returned:\n%s" % listing_result
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

    def get_repository_folders(self):
        return self.get_objects_list("folder")

    def get_folder_workflows(self, folder_name):
        return self.get_objects_list("workflow", folder=folder_name)

    def get_folder_mappings(self, folder_name):
        return self.get_objects_list("mapping", folder=folder_name)

    def get_folder_sessions(self, folder_name):
        return self.get_objects_list("session", folder=folder_name)

    def get_folder_sources(self, folder_name):
        return self.get_objects_list("source", folder=folder_name)

    def get_folder_targets(self, folder_name):
        return self.get_objects_list("target", folder=folder_name)

    def create_repository_folder(self, folder_name, shared=True):
        print "Creating a new folder %s..." % folder_name
        if shared: shared_flag = "-s"
        else: shared_flag = ""
        create_folder_command = "pmrep createfolder -n %s %s" % (folder_name, shared_flag)

        create_result = system.execute_command_line(create_folder_command)

        if not "createfolder completed successfully." in create_result:
            print "ERROR: Create folder command was unsuccessful!"
            print "Message returned:\n%s" % create_result
            return False
        else:
            print "Folder successfully created!"

    def export_repository_folder(self, folder_name, extract_xml_path):
        print "Exporting the folder %s to XML %s..." % (folder_name, extract_xml_path)
        export_folder_command = "pmrep objectexport -f %s -c %s" % (folder_name, extract_xml_path)

        export_result = system.execute_command_line(export_folder_command)

        results_search = "Exported (\d*) object\(s\) - (\d*) Error\(s\), - (\d*) Warning\(s\)"
        res = re.search(results_search, export_result)

        if not "objectexport completed successfully." in export_result:
            print "ERROR: Folder export to XML command was unsuccessful!"
            print "Message returned:\n%s" % export_result
            return False
        else:
            print "Export successful!"
            if res:
                print "Export summary:\n %s" ^ res.group(0)
                return True
            else:
                print "ERROR: cannot read export summary!"
                return False








    # pmrep objectexport
    # pmrep objectimport

    # pmrep updateseqgenvals <-- updates sequence values!
    # pmrep VALIDATION
    # pmrep backup and restore
