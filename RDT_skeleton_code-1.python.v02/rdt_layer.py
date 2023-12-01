from segment import Segment


# #################################################################################################################### #
# RDTLayer                                                                                                             #
#                                                                                                                      #
# Description:                                                                                                         #
# The reliable data transfer (RDT) layer is used as a communication layer to resolve issues over an unreliable         #
# channel.                                                                                                             #
#                                                                                                                      #
#                                                                                                                      #
# Notes:                                                                                                               #
# This file is meant to be changed.                                                                                    #
#                                                                                                                      #
#                                                                                                                      #
# #################################################################################################################### #


class RDTLayer(object):
    # ################################################################################################################ #
    # Class Scope Variables                                                                                            #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    DATA_LENGTH = 4 # in characters                     # The length of the string data that will be sent per packet...
    FLOW_CONTROL_WIN_SIZE = 15 # in characters          # Receive window size for flow-control
    sendChannel = None
    receiveChannel = None
    dataToSend = ''
    currentIteration = 0                                # Use this for segment 'timeouts'
    # Add items as needed

    # ################################################################################################################ #
    # __init__()                                                                                                       #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None
        self.dataToSend = ''
        self.currentIteration = 0
        self.dataDict = {}
        self.leftWindowEdge = 0
        self.rightWindowEdge = self.FLOW_CONTROL_WIN_SIZE//self.DATA_LENGTH
        self.isClient = False
        self.parsedData = []
        # Add items as needed
    # ################################################################################################################ #
    # setSendChannel()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable sending lower-layer channel                                                 #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # ################################################################################################################ #
    # setReceiveChannel()                                                                                              #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the unreliable receiving lower-layer channel                                               #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # ################################################################################################################ #
    # setDataToSend()                                                                                                  #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to set the string data to send                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def setDataToSend(self,data):
        self.dataToSend = data

    # ################################################################################################################ #
    # getDataReceived()                                                                                                #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Called by main to get the currently received and buffered string data, in order                                  #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def getDataReceived(self):
        # ############################################################################################################ #
        # Identify the data that has been received...

        receivedData = ""

        # The following code for sorting a dictionary by keys was adapted from
        # https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
        # on August 16, 2023
        # Sort dictionary maintained for received data
        seqNumList = list(self.dataDict.keys())
        seqNumList.sort()
        self.dataDict = {i: self.dataDict[i] for i in seqNumList}

        # print('getDataReceived(): Complete this...')
        for data in self.dataDict:
            receivedData = receivedData + self.dataDict[data]
           # print(receivedData)
        # ############################################################################################################ #
        return receivedData

    # ################################################################################################################ #
    # processData()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # "timeslice". Called by main once per iteration                                                                   #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processData(self):
        self.currentIteration += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    # ################################################################################################################ #
    # processSend()                                                                                                    #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment sending tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processSend(self):


        # ############################################################################################################ #
        # print('processSend(): Complete this...')

        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)



        if self.dataToSend != '' and not self.isClient:
            # Use list comprehension to parse dataToSend into segments of length DATA_LENGTH
            self.parsedData = [self.dataToSend[i:i+self.DATA_LENGTH] for i in range(0, len(self.dataToSend), self.DATA_LENGTH)]
            self.isClient = True

            # ############################################################################################################ #
            # Display sending segment
        if self.isClient:
            # retrieve portion of data within alotted data size
            # and create segment to be sent to server
            for i in range(self.leftWindowEdge, self.rightWindowEdge):
                if i < len(self.parsedData):
                    data = self.parsedData[i]
                    seqnum = i * self.DATA_LENGTH + 1
                    segmentSend = Segment()
                    segmentSend.setData(int(seqnum),data)
                    print("Sending segment: ", segmentSend.to_string())
                    # Use the unreliable sendChannel to send the segment
                    self.sendChannel.send(segmentSend)

            # Slide window to send next set of segments
            # Windows will slide back once ack is received based on the ack
            self.leftWindowEdge = self.rightWindowEdge
            self.rightWindowEdge = self.FLOW_CONTROL_WIN_SIZE//self.DATA_LENGTH + self.leftWindowEdge

    # ################################################################################################################ #
    # processReceive()                                                                                                 #
    #                                                                                                                  #
    # Description:                                                                                                     #
    # Manages Segment receive tasks                                                                                    #
    #                                                                                                                  #
    #                                                                                                                  #
    # ################################################################################################################ #
    def processReceiveAndSendRespond(self):

        # This call returns a list of incoming segments (see Segment class)...
        listIncomingSegments = self.receiveChannel.receive()

        # Check if the incoming list is empty
        if listIncomingSegments:

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented

            for segment in listIncomingSegments:
                # Process as incoming data from client
                if segment.acknum == -1 and segment.checkChecksum():
                    # Store the data in a dictionary if seq number not already stored as key
                    if segment.seqnum not in self.dataDict:
                        self.dataDict[segment.seqnum] = segment.payload

                # Else: segment is Ack from server
                else:
                    # Set new window frame
                    self.leftWindowEdge = int((segment.acknum - 1)/self.DATA_LENGTH)
                    self.rightWindowEdge = self.FLOW_CONTROL_WIN_SIZE//self.DATA_LENGTH + self.leftWindowEdge
                    return

        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segments?
        #     print('processReceive(): Complete this...')

            # Somewhere in here you will be setting the contents of the ack segments to send.
            # The goal is to employ cumulative ack, just like TCP does...
            segmentAck = Segment()  # Segment acknowledging packet(s) received
            acknum = 1
            while acknum in self.dataDict:
                acknum += self.DATA_LENGTH

            # ############################################################################################################ #
                # Display response segment
            segmentAck.setAck(acknum)
            print("Sending ack: ", segmentAck.to_string())

            # Use the unreliable sendChannel to send the ack packet
            self.sendChannel.send(segmentAck)
        else:
            return