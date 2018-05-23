from common import system
import version_control

import re
import os



class Pmrep:
    def __init__(self, config, git_control, connection_name='default', validate=True, verbose=False, connect=True):

        self.verbose = verbose
        self.git_control = git_control

        try:
            self.connection = config.content["informatica_connections"][connection_name]

            self.connection_repository = self.connection["repository"]
            self.connection_domain = self.connection["domain"]
            self.connection_login_name = self.connection["login_name"]
            self.connection_password = self.connection["password"]

            self.xml_export_folder = config.content["xml_export_folder"]
            self.folders_to_migrate = config.content["folders_to_migrate"]

        except Exception as err:
            print 'ERROR: Failed to read all required parameters from config.json for informatica pmrep access.'
            print 'Check the json file format, e.g. are there any missing commas or closing quotes, brackets?'
            print 'Use the config.json.template file in this folder as your reference.\n'
            if verbose:
                print 'Exception:\n%s\n' % str(err)
            exit(1)

        if validate:
            result = self.validate_environment()
            if not result:
                exit(1)

        if connect:
            self.connect()


    def validate_environment(self):
        print "Validating system configuration for running pmrep..."

        required_system_variables = [
            'INFA_HOME',
            'INFA_DOMAINS_FILE',
            'LD_LIBRARY_PATH',
            'PATH'
        ]

        system_variables_exist_list = [system.get_environment_variable(v) for v in required_system_variables]
        system_variables_exist = reduce((lambda a, b: a and b), system_variables_exist_list)
        if not system_variables_exist: return False

        print "Validating the pmrep command..."
        if not system.check_command_exists("pmrep -version"):
            print "ERROR: Command pmrep not found. Please run manually 'pmrep -version' to troubleshoot.\n" \
                  "Make sure the required environment variables are set and with correct values.\n" \
                  "Make sure the PATH variable is updated with the INFA_HOME bin path.\n" \
                  "Please refer to the documentation for instructions on how to set up environment variables.\n"
            return False
        else:
            print "Command pmrep successfully validated.\n"

        return True


    def connect(self):
        print "Connecting to Informatica with pmrep ..."

        connect_command = "pmrep connect -r %s -d %s -n %s -x %s" % \
                          (
                              self.connection_repository,
                              self.connection_domain,
                              self.connection_login_name,
                              self.connection_password
                          )
        connect_result = system.execute_command_line(connect_command)

        if "connect completed successfully" in connect_result:
            print "Connection to Informatica established!\n"
            if self.verbose:
                print "Message returned:\n=========================\n%s\n=========================\n" % connect_result
            return True
        else:
            print "ERROR: Connect to Informatica failed!"
            print "Message returned:\n=========================\n%s\n=========================\n" % connect_result
            return False


    def get_objects_list(self, object_type, informatica_folder=None):
        listing_command_head = "pmrep listobjects -o %s" % object_type

        if informatica_folder:
            additional_folder = " -f %s" % informatica_folder
        else:
            additional_folder = ""

        listing_command = listing_command_head + additional_folder
        if self.verbose:
            print 'pmrep command: %s#n' % listing_command

        listing_result = system.execute_command_line(listing_command)
        if self.verbose:
            print 'pmrep command result\n%s\n\n' % listing_result

        if not "listobjects completed successfully." in listing_result:
            print "ERROR: Listing command was unsuccessful!"
            print "Message returned:\n=========================\n%s\n=========================\n" % listing_result
        else:
            results_search = "Invoked at (?:.*?$)(.*).listobjects completed successfully."
            parsed_result = re.search(results_search, listing_result, re.MULTILINE|re.DOTALL)

            if parsed_result:
                objects_list = parsed_result.group(1).splitlines()
                objects_list_cleaned = [o.strip() for o in objects_list if len(o) > 0]
                return objects_list_cleaned  # TODO: add column split
            else:
                print "listobjects parse result appears to be empty: %s" % str(parsed_result)
                return []

    def get_repository_folders(self):
        return self.get_objects_list("folder")

    def get_workflows(self, informatica_folder_name):
        return self.get_objects_list("workflow", informatica_folder=informatica_folder_name)

    def get_mappings(self, informatica_folder_name):
        return self.get_objects_list("mapping", informatica_folder=informatica_folder_name)

    def get_sessions(self, informatica_folder_name):
        return self.get_objects_list("session", informatica_folder=informatica_folder_name)

    def get_sources(self, informatica_folder_name):
        return self.get_objects_list("source", informatica_folder=informatica_folder_name)

    def get_targets(self, informatica_folder_name):
        return self.get_objects_list("target", informatica_folder=informatica_folder_name)

    def create_repository_folder(self, folder_name, shared=True):
        print "Creating a new folder %s..." % folder_name

        if shared:  shared_flag = "-s"
        else:       shared_flag = ""

        create_folder_command = "pmrep createfolder -n %s %s" % (folder_name, shared_flag)
        if self.verbose:
            print 'create folder command: %s\n' % create_folder_command

        create_result = system.execute_command_line(create_folder_command)
        if self.verbose:
            print 'create folder command result:\n%s\n\n' % create_result

        if not "createfolder completed successfully." in create_result:
            print "ERROR: Create folder command was unsuccessful!"

            # write log
            log_file_name = folder_name + '.create-folder.error.log'
            system.write_log(log_file_name, create_result)

            print 'Check log file for details: %s\n' % log_file_name
            return False
        else:
            print "Folder successfully created!\n"


    def export_repository_folder(self, informatica_folder_name, export_xml_folder_path):

        xml_export_file_name = "Folder___%s___%s.xml" % (self.connection["repository"], informatica_folder_name)

        print "----------------------------------------------------------------------------------"
        print "Exporting the Informatica folder %s in XML format to folder %s..." \
              % (informatica_folder_name, export_xml_folder_path)

        if not os.path.isdir(export_xml_folder_path):
            print "ERROR: The folder %s does not exist! (Create the folder and make sure Python can access it.)" \
                  % export_xml_folder_path
            return False

        print "Export file name: %s" % xml_export_file_name
        if self.verbose:
            print "Export file name format: Folder___<source repository name>___<informatica source folder name).xml"

        extract_xml_path = os.path.join(export_xml_folder_path, xml_export_file_name)
        export_folder_command = "pmrep objectexport -f %s -u %s" % (informatica_folder_name, extract_xml_path)
        if self.verbose:
            print 'export folder command: %s\n' % export_folder_command

        export_result = system.execute_command_line(export_folder_command)
        if self.verbose:
            print 'export folder command result:\n%s\n\n' % export_result

        # write log
        log_file_name = xml_export_file_name + '.export.log'
        system.write_log(log_file_name, export_result)
        if self.verbose:
            print 'log file written: %s' % log_file_name

        results_search = "Exported (\d*) object\(s\) - (\d*) Error\(s\), - (\d*) Warning\(s\)"
        parse_result = re.search(results_search, export_result)

        if not "objectexport completed successfully." in export_result:
            print "ERROR: Folder export to XML command was unsuccessful!"
            print "Export command used: [%s]" % export_folder_command
            print "Message returned:\n=========================\n%s\n=========================\n" % export_result
            return False
        else:
            print "Export successful!\n"
            if parse_result:
                print "Export summary:\n %s\n" % parse_result.group(0)
                return True
            else:
                print "ERROR: cannot read export summary!"
                return False


    def export_repository_folders(self, informatica_folder_name_list, export_xml_folder_path):
        print "----------------------------------------------------------------------------------"
        print "----------------------------------------------------------------------------------"
        print "Exporting %s informatica folders..." % len(informatica_folder_name_list)
        if self.verbose:
            print 'folders list: %s\n' % str(informatica_folder_name_list)

        for informatica_folder in informatica_folder_name_list:
            export_result = self.export_repository_folder(informatica_folder, export_xml_folder_path)
            if not export_result:
                return False

        print 'Folders list export done.\n'
        return True


    def import_repository_folder(self, import_xml_file_path, target_informatica_folder_name_override=None, create_target_folder_if_not_exist=True, delete_archive_after_successful_import=False):
        print "----------------------------------------------------------------------------------"
        print "Importing an informatica folder from XML file %s...\n" % import_xml_file_path

        # validations and preparations
        if not os.path.isfile(import_xml_file_path):
            print "ERROR: Cannot find the XML import file [%s]" % import_xml_file_path
            print "INFO: XML file naming is important - the source repository and folder names are used by the import procedure and are derived from the import XML file name."
            print "INFO: XML file names are case-sensitive. Neither the repository nor the folder name should not have two consecutive underlines in it."
            print "INFO: Export file name format: Folder___<source repository name>___<informatica source folder name).xml"
            return False

        folder_name_parse = "Folder___(.+)___(.+)\."
        folder_name_parse_result = re.search(folder_name_parse, import_xml_file_path)
        if folder_name_parse_result:
            source_repository_name = folder_name_parse_result.group(1)
            source_informatica_folder_name = folder_name_parse_result.group(2)
            print "XML file name successfully parsed:\n\tsource repository name: %s\n\tsource folder name: %s\n" % (source_repository_name, source_informatica_folder_name)
        else:
            print "ERROR: XML file name parsing failed!\nPlease note the file name is case-sensitive.\n" \
                  "The required XML import file name should follow this format: Folder___<source repository name>___<informatica source folder name).xml\nExample: Folder___UAT_REPO___SIL_Order_Lines.xml"
            print "INFO: XML file naming is important - the source repository and folder names are used by the import procedure and are derived from the import XML file name."
            print "INFO: XML file names are case-sensitive. Neither the repository nor the folder name should not have two consecutive underlines in it."
            print "INFO: Export file name format: Folder___<source repository name>___<informatica source folder name).xml"
            return False

        impcntl_dtd_path = os.path.join(system.get_environment_variable("INFA_HOME"), "server", "bin", "impcntl.dtd")
        if not os.path.isfile(impcntl_dtd_path):
            print "ERROR: Cannot find the control definition file 'impcntl.dtd' in path $INFA_HOME/server/bin/imcntl.dtd (%s)" % impcntl_dtd_path
            return False

        # TODO: add this to validation and create a class attribute!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if not os.path.isfile("import_control_template.ctl"):
            print "ERROR: Cannot find file import_control_template.ctl in the current folder. Make sure you run the import from the Informatica Developer Toolkit home folder and that the template file is there."
            return False

        target_repository_name = self.connection["repository"]
        if target_informatica_folder_name_override:
            target_informatica_folder_name = target_informatica_folder_name_override
            print "Target Informatica folder name overridde: %s" % target_informatica_folder_name
        else:
            target_informatica_folder_name = source_informatica_folder_name


        # create target folder if it does not exist already
        existing_folders = self.get_repository_folders()

        if target_informatica_folder_name in existing_folders:
            print "The target Informatica folder %s already exists in the repository. Current content will be overwritten.\n" % target_informatica_folder_name
        else:
            print "The target Informatica folder %s does not exist in the repository." % target_informatica_folder_name
            if not create_target_folder_if_not_exist:
                print "ERROR: create_target_folder_if_not_exist parameter is set to False. The folder will not be created. Exiting..."
                return False
            else:
                self.create_repository_folder(target_informatica_folder_name)


        # write control file
        template_ctl_file_name = "import_control_template.ctl"
        current_ctl_file_name = "import_control_current.ctl"

        print "Writing control file %s based on %s ..." % (current_ctl_file_name, template_ctl_file_name)
        if os.path.isfile(template_ctl_file_name):
            ctl_file_content = system.read_file(template_ctl_file_name)
        else:
            print "ERROR: Control template file %s not found in the current folder!"
            return False

        ctl_replacements = {
            "{{IMPCNTL_DTD}}": impcntl_dtd_path,
            "{{SOURCE_FOLDER}}": source_informatica_folder_name,
            "{{SOURCE_REPOSITORY}}": source_repository_name,
            "{{TARGET_FOLDER}}": target_informatica_folder_name,
            "{{TARGET_REPOSITORY}}": target_repository_name
        }

        for key in ctl_replacements.keys():
            ctl_file_content = ctl_file_content.replace(key, ctl_replacements[key])

        system.write_file(current_ctl_file_name, ctl_file_content)
        print "Control file written.\n"


        # execute import
        print "Starting import..."

        import_folder_command = "pmrep objectimport -i %s -c %s" % (import_xml_file_path, "import_control_current.ctl")

        import_result = system.execute_command_line(import_folder_command)

        # write log
        log_file_name = os.path.basename(import_xml_file_path) + '.import.log'
        system.write_log(log_file_name, import_result)

        results_search = "(\d*) Processed, (\d*) Errors, (\d*) Warnings"
        folder_name_parse_result = re.search(results_search, import_result)

        if not "objectimport completed successfully." in import_result:
            print "ERROR: Folder import command was unsuccessful!"
            print "Refer to the log file for details."
            print "Import command used: [%s]" % import_folder_command
            return False
        else:
            print "Import successful!"
            if folder_name_parse_result:
                print "Import summary:\n %s\n" % folder_name_parse_result.group(0)
            else:
                print "ERROR: cannot read import summary! Please analyse the detailed message below:"
                print "Refer to the log file for details."
                return False

        if delete_archive_after_successful_import:
            print "Deleting the archive file %s after a successful import..." % import_xml_file_path
            os.remove(import_xml_file_path)
            print "Delete successful.\n"

        return True


    def import_all_xmls_from_folder(self, archive_folder_name, delete_archive_after_successful_import=True):
        print "----------------------------------------------------------------------------------"
        print "----------------------------------------------------------------------------------"
        print "Importing all archive XML files from the folder %s" % archive_folder_name

        if not os.path.isdir(archive_folder_name):
            print "ERROR: Folder %s does not exist!" % archive_folder_name
            return False

        xml_archives_in_folder = [f for f in os.listdir(archive_folder_name) if os.path.isfile(os.path.join(archive_folder_name,f)) and f.upper().endswith('.XML')]
        print "%s archive files found" % len(xml_archives_in_folder)
        if self.verbose:
            print 'archive files:\n%s\n' % str(xml_archives_in_folder)

        if len(xml_archives_in_folder) == 0:
            print "ERROR: No xml archive files found in the folder %s." % archive_folder_name
            return False

        imports_successful = 0
        imports_failed = 0
        for xml_archive_file_name in xml_archives_in_folder:
            xml_archive_file_path = os.path.join(archive_folder_name, xml_archive_file_name)
            import_result = self.import_repository_folder(xml_archive_file_path, delete_archive_after_successful_import=delete_archive_after_successful_import)

            if import_result:   imports_successful += 1
            else:               imports_failed += 1

        print "----------------------------------------------------------------------------------"
        print "All imports from the folder %s done:\n\tsuccessful: %s\n\tfailed: %s" % (archive_folder_name, imports_successful, imports_failed)

        if imports_failed > 0:  return False
        else:                   return True


    def duplicate_rename_informatica_folder(self, informatica_source_folder_name, informatica_target_folder_name):

        print "----------------------------------------------------------------------------------"
        print "----------------------------------------------------------------------------------"
        print 'Duplicating Informatica repository folder:\n\tsource: %s\n\ttarget: %s\n' % (informatica_source_folder_name, informatica_target_folder_name)
        if informatica_source_folder_name == informatica_target_folder_name:
            print "ERROR: source and target folders are the same."
            return False

        # cleanup the temp folder
        print "Removing all xml archives from the temp folder..."
        temp_folder_path = os.path.join(".", 'temp')

        if not os.path.isdir(temp_folder_path):
            print "ERROR: temp folder does not exist. Please create one under the current folder."
            return False

        xml_archives_in_temp_folder = [f for f in os.listdir(temp_folder_path) if os.path.isfile(os.path.join(temp_folder_path, f)) and f.upper().endswith('.XML')]
        for archive in xml_archives_in_temp_folder:
            os.remove(os.path.join(temp_folder_path,archive))
        if len(xml_archives_in_temp_folder):
            print "Removed %s xml files from temp." % len(xml_archives_in_temp_folder)
        print "temp folder cleanup done.\n"


        export_result = self.export_repository_folder(informatica_source_folder_name, temp_folder_path)

        if export_result:

            xml_archives_in_temp_folder = [f for f in os.listdir(temp_folder_path) if os.path.isfile(os.path.join(temp_folder_path, f)) and f.upper().endswith('.XML')]
            if not xml_archives_in_temp_folder:
                print "ERROR: export XML file not found in %s folder." % temp_folder_path
                return False
            else:
                import_xml_file_path = os.path.join(temp_folder_path, xml_archives_in_temp_folder[0])
                import_result = self.import_repository_folder(import_xml_file_path, target_informatica_folder_name_override=informatica_target_folder_name, delete_archive_after_successful_import=True)

                if import_result:   return True
                else:               return False

        return False


    # bool attribute: use_git
    # take folder from either export or git.infa_root_folder
    def do_export(self, use_git=True):

        if use_git:
            self.git_control.checkout(self.git_control.git_default_branch)
            self.git_control.pull_branch(self.git_control.git_default_branch)

        export_result = self.export_repository_folders(self.folders_to_migrate, self.xml_export_folder)

        if use_git:
            self.git_control.commit_all('Rittman Mead informatica developer toolkit migration')
            self.git_control.push(self.git_control.git_default_branch)

        return export_result



    def do_import(self, use_git=True):

        if use_git:
            self.git_control.checkout(self.git_control.git_default_branch)
            self.git_control.pull_branch(self.git_control.git_default_branch)

        return self.import_all_xmls_from_folder(self.xml_export_folder, delete_archive_after_successful_import=True)


