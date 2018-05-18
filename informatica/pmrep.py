from informatica import system
import re
import os


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
            print "Message returned:\n=========================%s\n=========================\n" % connect_result
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
            print "Message returned:\n=========================%s\n=========================\n" % listing_result
        else:
            results_search = "Invoked at (?:.*?$)(.*).listobjects completed successfully."
            res = re.search(results_search, listing_result, re.MULTILINE|re.DOTALL)
            if res:
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
            print "Message returned:\n=========================%s\n=========================\n" % create_result
            return False
        else:
            print "Folder successfully created!"


    def export_repository_folder(self, informatica_folder_name, extract_xml_folder_path):
        xml_export_file_name = "Folder___%s___%s.xml" % (self.connection["repository"], informatica_folder_name)
        print "Exporting the Informatica folder %s to XML format in folder %s..." % (informatica_folder_name, extract_xml_folder_path)
        print "Export file name: %s" % xml_export_file_name
        print "Export file name format: Folder___<source repository name>___<informatica source folder name).xml"

        extract_xml_path = os.path.join(extract_xml_folder_path, xml_export_file_name)

        export_folder_command = "pmrep objectexport -f %s -u %s" % (informatica_folder_name, extract_xml_path)

        export_result = system.execute_command_line(export_folder_command)

        results_search = "Exported (\d*) object\(s\) - (\d*) Error\(s\), - (\d*) Warning\(s\)"
        res = re.search(results_search, export_result)

        if not "objectexport completed successfully." in export_result:
            print "ERROR: Folder export to XML command was unsuccessful!"
            print "Export command used: [%s]" % export_folder_command
            print "Message returned:\n=========================%s\n=========================\n" % export_result
            return False
        else:
            print "Export successful!"
            if res:
                print "Export summary:\n %s" % res.group(0)
                return True
            else:
                print "ERROR: cannot read export summary!"
                return False


    def import_repository_folder(self, import_xml_file_path):

        print "\n\nImporting an informatica folder from an XML file..."
        print "INFO: XML file naming is important - the source repository and folder names are used by the import procedure and are derived from the import XML file name."
        print "INFO: XML file names are case-sensitive. Neither the repository nor the folder name should not have two consecutive underlines in it."
        print "INFO: Export file name format: Folder___<source repository name>___<informatica source folder name).xml"


        # validations and preparations
        if not os.path.isfile(import_xml_file_path):
            print "ERROR: Cannot find the XML import file [%s]" % import_xml_file_path
            return False

        folder_name_parse = "Folder___(.+)___(.+)\."
        res = re.search(folder_name_parse, import_xml_file_path)
        if res:
            source_repository_name = res.group(1)
            source_folder_name = res.group(2)
            print "XML file name successfully parsed:\n\tsource repository name: %s\n\tsource folder name: %s" % (source_repository_name, source_folder_name)
        else:
            print "ERROR: XML file name parsing failed!\nPlease note the file name is case-sensitive.\n" \
                  "The required XML import file name should follow this format: Folder___<source repository name>___<informatica source folder name).xml\nExample: Folder___UAT_REPO___SIL_Order_Lines.xml"
            return False

        imp_control_definition_path = os.path.join(system.get_environment_variable("INFA_HOME"), "server", "bin", "impcntl.dtd")
        if not os.path.isfile(imp_control_definition_path):
            print "ERROR: Cannot find the control definition file 'impcntl.dtd' in path $INFA_HOME/server/bin/imcntl.dtd (%s)" % imp_control_definition_path
            return False

        if not os.path.isfile("import_control_template.ctl"):
            print "ERROR: Cannot find file import_control_template.ctl in the current folder. Make sure you run the import from the Informatica Developer Toolkit home folder and that the template file is there."
            return False

        target_repository_name = self.connection["repository"]
        target_folder_name = source_folder_name


        # write control file
        print "Writing control file..."
        cmd_file_content = system.read_file("import_control_template.ctl")

        control_replacements = {
            "{{IMPCNTL_DTD}}" : imp_control_definition_path,
            "{{SOURCE_FOLDER}}" : source_folder_name,
            "{{SOURCE_REPOSITORY}}" : source_repository_name,
            "{{TARGET_FOLDER}}" : target_folder_name,
            "{{TARGET_REPOSITORY}}" : target_repository_name
        }

        for key in control_replacements.keys():
            print "key: %s, replacement: %s" % (key, control_replacements[key])
            cmd_file_content = cmd_file_content.replace(key, control_replacements[key])

        system.write_file("import_control_current.ctl", cmd_file_content)

        print "Control file written."


        # execute import
        print "Starting import..."

        import_folder_command = "pmrep objectimport -i %s -c %s" % (import_xml_file_path, "import_control_current.ctl")

        import_result = system.execute_command_line(import_folder_command)

        results_search = "(\d*) Processed, (\d*) Errors, (\d*) Warnings"
        res = re.search(results_search, import_result)

        if not "objectimport completed successfully." in import_result:
            print "ERROR: Folder import command was unsuccessful!"
            print "Import command used: [%s]" % import_folder_command
            print "Message returned:\n=========================%s\n=========================\n" % import_result
            return False
        else:
            print "Import successful!"
            if res:
                print "Import summary:\n %s" % res.group(0)
                return True
            else:
                print "ERROR: cannot read export summary!"
                return False

        return True










"""
    < !DOCTYPE
    IMPORTPARAMS
    SYSTEM
    "{{IMPCNTL_DTD}}" >

    < IMPORTPARAMS
    CHECKIN_AFTER_IMPORT = "YES"
    CHECKIN_COMMENTS = "Rittman Mead Informatica Repository auto-import"
    RETAIN_GENERATED_VALUE = "YES"
    APPLY_DEFAULT_CONNECTION = "NO" >

    < FOLDERMAP
    SOURCEFOLDERNAME = "{{SOURCE_FOLDER}}"
    SOURCEREPOSITORYNAME = "{{SOURCE_REPOSITORY}}"
    TARGETFOLDERNAME = "{{TARGET_FOLDER}}"
    TARGETREPOSITORYNAME = "{{TARGET_REPOSITORY}}" / >
"""






# pmrep objectexport
# pmrep objectimport

# pmrep updateseqgenvals <-- updates sequence values!
# pmrep VALIDATION
# pmrep backup and restore




