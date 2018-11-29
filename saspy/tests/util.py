import saspy

class Utilities:
    def __init__(self, session = None):
        if session is None:
            self.sas = saspy.SASsession(cfgname=saspy.SASsession().sascfg.SAScfg.SAS_config_names[0])
        else:
            self.sas = session

    def procExists(self, plist: list) -> bool:
        """
        Checks to see if the given list of procs exist on the instance.
        :param plist: A list of procs.
        :return:      True if all procs are found, False otherwise
        """
        assert isinstance(plist, list)
        for proc in plist:
            res = self.sas.submit("proc %s; run;" % proc)
            log = res['LOG'].splitlines()
            for line in log:
                if line == 'ERROR: Procedure %s not found.' % proc.upper():
                    return False
        return True

    def procLicensed(self, plist):
        """
        Checks to see if the given list of procs are licensed on the instance.
        :param plist: A list of procs.
        :return:      True if all procs are licensed, false otherwise.
        """
        assert isinstance(plist, list)
        for proc in plist:
            res = self.sas.submit("proc %s; run;" % proc)
            log = res['LOG'].splitlines()
            for line in log:
                if line == 'ERROR: Bad product ID for procedure %s.' % proc.upper():
                    return False
        return True

    def procFound(self, plist):
        """
        Determines if the procs listed are usable on the available sas instance.
        """
        return self.procExists(plist) and self.procLicensed(plist)