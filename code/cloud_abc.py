

class CloudABC(object):
    
    def __init__(self, **kwargs):
        """
        key arguments: kwargs, used for initial params for cloud (customer used).
        """
        raise NotImplementedError("this method should me implemented for customer designed Cloud Object")
    
    def connect(self):
        """connect to Coud"""
        raise NotImplementedError("customer should implement this method to connect cloud")
    
    def listen(self):
        """listen message from cloud.
        
        usually we use this method to start a thread for receiving message from the cloud and put message input a Queue, and then use `self.recv` method to get it on app side.
        """
        raise NotImplementedError("customer should implement this method to listen cloud message")
    
    def recv(self):
        """receive a message"""
        raise NotImplementedError("customer should implement this method to recv a message")
    
    def send(self, *args):
        """send message
        
        position arguments: args, customer designed method used for send message 
        """
        raise NotImplementedError("customer should implement this method to send a message")
