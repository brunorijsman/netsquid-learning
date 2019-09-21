import netsquid
import numpy

VERBOSE = True

NR_CASH_REGISTERS = 5
AVG_CUSTOMER_INTERARRIVAL_TIME = 5.0 
MAX_CUSTOMER_WAITING_TIME = 60.0
AVG_CASH_REGISTER_SERVICE_TIME = 3.0

SIMULATION_DURATION = 1000.0

def report(message):
    if VERBOSE:
        now = netsquid.sim_time()
        print(f"{now:8.2f}: {message}")

customer_arrival_event = netsquid.EventType("CustomerArrivalEvent", "Customer Arrives")

service_complete_event = netsquid.EventType("ServiceCompleteEvent", "Service Complete")

class Customer:

    next_id = 1

    def __init__(self):
        self.id = Customer.next_id
        Customer.next_id += 1
        self.arrival_time = netsquid.sim_time()

    def time_since_arrival(self):
        return netsquid.sim_time() - self.arrival_time

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
        customer = Customer()
        report(f"Customer {customer.id} arrived and queued at cash register {self.id}")
        self.queue.append(customer)
        if self.queue_length() == 1:
            self.schedule_next_service_complete()

    def schedule_next_service_complete(self):
        service_time = numpy.random.exponential(AVG_CASH_REGISTER_SERVICE_TIME)
        customer = self.queue[0]
        report(f"Cash register {self.id} starts servicing customer {customer.id} for {service_time:.2f}")
        self._schedule_after(service_time, service_complete_event)

    def handle_service_complete(self):
        customer = self.queue[0]
        report(f"Cash register {self.id} completed servicing customer {customer.id}")
        self.queue = self.queue[1:]
        if self.queue != []:
            self.schedule_next_service_complete()

def run_simulation():
    netsquid.sim_reset()
    report("Start of simulation")
    payment_section = PaymentSection()
    netsquid.sim_run(duration=SIMULATION_DURATION)

if __name__ == "__main__":
    run_simulation()
