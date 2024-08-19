Reliable Data Transmission (RDT) Layer Simulation
Overview
This repository contains the completed implementation of a Reliable Data Transmission (RDT) Layer simulation. The project simulates reliable data transfer over an unreliable network, overcoming challenges like packet loss, delays, out-of-order delivery, and checksum errors.

Project Structure
RDTLayer Class: The completed RDTLayer class ensures reliable data transmission over an unreliable channel. It includes mechanisms such as pipelining, flow control, cumulative ACK, and retransmissions, allowing for efficient and accurate data transfer.

UnreliableChannel Class: This class simulates an unreliable network channel that introduces various issues like packet drops, delays, and errors. The RDTLayer implementation successfully handles these challenges to deliver data reliably.

Segment Class: Represents the data and acknowledgment (ACK) packets used in the transmission process. The class includes checksum verification and timestamping via iteration counts to ensure data integrity.

rdt_main.py: The main script that runs the simulation. It uses the RDTLayer class to manage both client and server roles, demonstrating the effectiveness of the RDT implementation.

Key Features
Reliable Transmission: The RDTLayer class ensures all data is transmitted correctly, even under conditions of extreme unreliability.

Pipelining and Flow Control: Implements pipelined transmission and flow control mechanisms, allowing multiple segments to be sent per iteration, maximizing efficiency.

Error Handling: Features robust error detection and correction methods, including checksum validation, segment timeouts, and retransmission strategies like Go-Back-N or Selective Retransmit.

Efficiency: The implementation is optimized to minimize the number of iterations required to transfer all data, even with all unreliable features enabled.

How to Run
Set Up: Ensure all necessary classes (RDTLayer, UnreliableChannel, Segment) are in the same directory.

Run the Simulation: Execute rdt_main.py to simulate data transmission between the client and server using the RDTLayer.

Adjust Unreliability: Modify the flags in UnreliableChannel to simulate different network conditions and observe how the RDTLayer handles them.

Conclusion
The project successfully implements a reliable data transmission protocol over an unreliable network. The RDTLayer class handles various network challenges, delivering data accurately and efficiently, meeting all project requirements.
