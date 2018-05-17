from informatica import system

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



    # pmrep connect
    # pmrep createFolder
    # pmrep objectexport
    # pmrep objectimport
    # pmrep listobjects  <- can list folders
    # pmrep updateseqgenvals <-- updates sequence values!
    # pmrep VALIDATION
    # pmrep backup and restore
