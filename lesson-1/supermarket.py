import math
import netsquid
import numpy

VERBOSE = False

NR_CASH_REGISTERS = 3
AVG_CUSTOMER_INTERARRIVAL_TIME = 5.0 / NR_CASH_REGISTERS
MAX_CUSTOMER_WAITING_TIME = 60.0
AVG_CASH_REGISTER_SERVICE_TIME = 4.5

SIMULATION_DURATION = 100000.0

def report(message):
    if VERBOSE:
        now = netsquid.sim_time()
        print(f"{now:8.2f}: {message}")

customer_arrival_event = netsquid.EventType("CustomerArrivalEvent", "Customer Arrives")

service_complete_event = netsquid.EventType("ServiceCompleteEvent", "Service Complete")

class Observation:

    def __init__(self):
        self._sum = 0.0
        self._count = 0

    def observe(self, value):
        self._sum += value
        self._count += 1

    def average(self):
        if self._count == 0:
            return math.nan
        else:
            return self._sum / self._count

OBSERVED_QUEUE_LENGTHS = Observation()

WAITING_TIMES = Observation()

class PaymentSection(netsquid.Entity):

    def __init__(self):
        report("Create payment section")
        self.cash_registers = []
        for _ in range(NR_CASH_REGISTERS):
            self.cash_registers.append(CashRegister())
        customer_arrival_handler = netsquid.EventHandler(lambda _event: self.handle_customer_arrival())
        self._wait(customer_arrival_handler, event_type=customer_arrival_event)
        self.schedule_next_customer_arrival()

    def schedule_next_customer_arrival(self):
        interarrival_time = numpy.random.exponential(AVG_CUSTOMER_INTERARRIVAL_TIME)
        self._schedule_after(interarrival_time, customer_arrival_event)

    def handle_customer_arrival(self):
        cash_register = min(self.cash_registers, key=lambda cr: cr.queue_length())
        cash_register.handle_customer_arrival()
        self.schedule_next_customer_arrival()

class CashRegister(netsquid.Entity):

    next_id = 1

    def __init__(self):
        self.id = CashRegister.next_id
        CashRegister.next_id += 1
        self.queue = []
        service_complete_handler = netsquid.EventHandler(lambda _event: self.handle_service_complete())
        self._wait(service_complete_handler, entity=self, event_type=service_complete_event)

    def queue_length(self):
        return len(self.queue)

    def handle_customer_arrival(self):
        global OBSERVED_QUEUE_LENGTHS
        customer = Customer()
        report(f"Customer {customer.id} arrived and queued at cash register {self.id}")
        OBSERVED_QUEUE_LENGTHS.observe(self.queue_length())
        self.queue.append(customer)
        if self.queue_length() == 1:
            self.schedule_next_service_complete()

    def schedule_next_service_complete(self):
        service_time = numpy.random.exponential(AVG_CASH_REGISTER_SERVICE_TIME)
        customer = self.queue[0]
        report(f"Cash register {self.id} starts servicing customer {customer.id} for {service_time:.2f}")
        self._schedule_after(service_time, service_complete_event)

    def handle_service_complete(self):
        global WAITING_TIMES
        customer = self.queue[0]
        report(f"Cash register {self.id} completed servicing customer {customer.id}")
        WAITING_TIMES.observe(customer.time_since_arrival())
        self.queue = self.queue[1:]
        if self.queue != []:
            self.schedule_next_service_complete()

class Customer(netsquid.Entity):

    next_id = 1

    def __init__(self):
        self.id = Customer.next_id
        Customer.next_id += 1
        self.arrival_time = netsquid.sim_time()

    def time_since_arrival(self):
        return netsquid.sim_time() - self.arrival_time

def run_simulation():
    netsquid.sim_reset()
    report("Start of simulation")
    payment_section = PaymentSection()
    netsquid.sim_run(duration=SIMULATION_DURATION)
    print(f"Average observed queue length: {OBSERVED_QUEUE_LENGTHS.average():.2f}")
    print(f"Average waiting time (including service): {WAITING_TIMES.average():.2f}")

def average_str(count, summed):
    if count == 0:
        return "-"
    average = summed / count
    return f"{average:.2f}"

if __name__ == "__main__":
    run_simulation()
