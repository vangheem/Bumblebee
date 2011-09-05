
class CSS(object):
    """
    Selector for css
    """
    
    def __init__(self, selector):
        self.selector = selector
    
        
    def __call__(self, node):
        return node.cssselect(self.selector)
        
        
class XPath(object):
    """
    
    """
    
    def __init__(self, xpath):
        self.xpath = xpath
    
    
    def __call__(self, node):
        return node.xpath(self.xpath)
        
        