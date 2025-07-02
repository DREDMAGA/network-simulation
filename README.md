# Network Simulation

A Python-based simulation of data transfer between virtual servers via a central router.

This project demonstrates core networking concepts such as routing, message TTL (time to live), priority-based processing, and logging — all implemented using object-oriented Python.

---

## Features

- Virtual servers with unique IP addresses
- Data packets with:
  - Priority
  - TTL (Time to Live)
  - Timestamp
  - Source and destination IP
- Router with:
  - Message queue (buffer)
  - One-by-one message processing with delay simulation
  - Logging of all sent and dropped messages
- Random traffic generator for testing network behavior
