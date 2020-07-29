# coding=utf-8

'''
Created on 22 apr 2017

@author: Andrea Montanari

This is an Interface that permits to create q-message and r-message
'''

from messages.MessageR import MessageR
from messages.MessageQ import MessageQ


class MessageFactory:
    
    def getMessageQ(self, sender, receiver, content):
        '''
            sender: NodeVariable sender
            receiver: NodeFunction receiver
            content: MessageContent
            Creates new q-message
        '''
        return MessageQ(sender, receiver, content)
    
    def getMessageR(self, sender, receiver, content):
        '''
            sender: NodeFunction sender
            receiver: NodeVariable receiver
            content: MessageContent
            Creates new r-message
        '''
        return MessageR(sender, receiver, content)
