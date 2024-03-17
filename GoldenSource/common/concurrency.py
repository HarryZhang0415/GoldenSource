
class Trigger(object):
    """
    Defines an object which trigger(domain) method is meant to be invoked by the MonirotService when a series of jobs completes
    """

    def trigger(self, domain):
        """
        Method to be invoked by the MonitorService when a series of jobs completes
        :param domain: The domain
        """
        raise NotImplementedError("{}.trigger".format(self.__class__.__name__))
    
    def __str__(self):
        return "{}".format(self.__class__.__name__)