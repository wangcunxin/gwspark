__author__ = 'wangcx'

class Properties(object):
    def __init__(self):
        pass

    def getProperties(self, fileName):
        try:
            pro_file = open(fileName, 'r')
            try:
                properties = {}
                for line in pro_file:
                    if line.find('=') > 0:
                        strs = line.replace('\n', '').split('=')
                        properties[strs[0]] = strs[1]
            except Exception, e1:
                print e1
            finally:
                pro_file.close()
        except Exception, e:
            print e

        return properties
