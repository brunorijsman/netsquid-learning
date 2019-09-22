# Discrete Events

NetSquid is first and foremost a discrete event simulator. In this lesson we will learn how to do
discrete event simulations in NetSquid.

A brief introduction to discrete event simulation in NetSquid is provided at
https://docs.netsquid.org/latest-release/overview.pydynaa.html (login required).

# Example: a supermarket

## Description

The system that we will simulate using disrete event simulation is a supermarket. 

There is some number of cash registers NR_CASH_REGISTERS.

The customer interarrival time is modeled using an exponential distribution with average
AVG_CUSTOMER_INTERARRIVAL_TIME seconds.

When the customer arrives, he always chooses cash register with the shortest queue, and then never
changes queue after that.

The service time at the cash registers is also modeled using an exponential distribution, with
average AVG_CASH_REGISTER_SERVICE_TIME seconds.

If a customer has to wait longer than MAX_CUSTOMER_WAITING_TIME seconds, he gives up and leave the
queue.

## Input parameters

 * Number of cash registers NR_CASH_REGISTERS
 * Average customer interarrival time AVG_CUSTOMER_INTERARRIVAL_TIME
 * Average customer service time AVG_CASH_REGISTER_SERVICE_TIME
 * Maximum waiting time before giving up MAX_CUSTOMER_WAITING_TIME

## Output parameters

 * Average waiting time (including service at cash register, including customers that give up)
 * Average queueing time (excluding service at cash register, including customers that give up)
 * Average queue length when a customer arrives (not including the itself)
 * Customers that gave up as a percentage of the customers that arrived