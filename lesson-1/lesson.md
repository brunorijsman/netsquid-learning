# Discrete Events

NetSquid is first and foremost a discrete event simulator. In this lesson we will learn how to do discrete event simulations in NetSquid.

# The supermarket

The system that we will simulate using disrete event simulation is a supermarket. There is some number of cash registers. The customer interarrival time is modeled using an exponential distribution. The customer always chooses the shortest queue. The service time at the cash registers is also modeled using an exponential distribution. If a customer has to wait longer than some maximum amount of time they give up and leave the queue.

# Input parameters

 * Number of cash registers
 * Average customer interarrival time
 * Average customer service time
 * Maximum waiting time before giving up

# Output parameters

 * Average waiting time (including service at cash register, including customers that give up)
 * Average queue length when a customer arrives (not including the itself)
 * Percentage of customers that give up