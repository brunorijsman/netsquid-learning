import math
import netsquid
import numpy

VERBOSE = False

NR_CASH_REGISTERS = 3
AVG_CUSTOMER_INTERARRIVAL_TIME = 20.0 / NR_CASH_REGISTERS
MAX_CUSTOMER_WAITING_TIME = 180.0
AVG_CASH_REGISTER_SERVICE_TIME = 18.0

SIMULATION_DURATION = 100000.0

def report(message):
    if VERBOSE:
        now = netsquid.sim_time()
        print(f"{now:8.2f}: {message}")

arrival_event_type = netsquid.EventType("Arrival", "Customer arrives")
serviced_event_type = netsquid.EventType("Serviced", "Customer service complete")
give_up_event_type =  netsquid.EventType("GiveUp", "Customer gives up")

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

QUEUE_LENGTH = Observation()
QUEUEING_TIME = Observation()
WAITING_TIME = Observation()

ARRIVE_COUNT = 0
GIVE_UP_COUNT = 0

class PaymentSection(netsquid.Entity):

    def __init__(self):
        report("Create payment section")
        self.cash_registers = []
        for _ in range(NR_CASH_REGISTERS):
            self.cash_registers.append(CashRegister())
        arrival_handler = netsquid.EventHandler(lambda _event: self.customer_arrives())
        self._wait(arrival_handler, event_type=arrival_event_type)
        self.schedule_next_arrival()

    def schedule_next_arrival(self):
        interarrival_delay = numpy.random.exponential(AVG_CUSTOMER_INTERARRIVAL_TIME)
        self._schedule_after(interarrival_delay, arrival_event_type)

    def customer_arrives(self):
        cash_register = min(self.cash_registers, key=lambda cr: cr.queue_length())
        cash_register.customer_arrives()
        self.schedule_next_arrival()

class CashRegister(netsquid.Entity):

    next_id = 1

    def __init__(self):
        self.id = CashRegister.next_id
        CashRegister.next_id += 1
        self.queue = []
        serviced_handler = netsquid.EventHandler(lambda _event: self.handle_serviced())
        self._wait(serviced_handler, entity=self, event_type=serviced_event_type)

    def queue_length(self):
        return len(self.queue)

    def customer_arrives(self):
        global QUEUE_LENGTH
        customer = Customer(self)
        QUEUE_LENGTH.observe(self.queue_length())
        self.queue.append(customer)
        if self.queue_length() == 1:
            self.schedule_next_serviced()

    def schedule_next_serviced(self):
        customer = self.queue[0]
        customer.start_service()
        serviced_delay = numpy.random.exponential(AVG_CASH_REGISTER_SERVICE_TIME)
        self._schedule_after(serviced_delay, serviced_event_type)

    def handle_serviced(self):
        customer = self.queue[0]
        customer.finish_service()
        self.queue = self.queue[1:]
        if self.queue != []:
            self.schedule_next_serviced()

    def remove_customer(self, customer):
        self.queue.remove(customer)

class Customer(netsquid.Entity):

    next_id = 1

    def __init__(self, cash_register):
        global ARRIVE_COUNT
        ARRIVE_COUNT += 1
        self.id = Customer.next_id
        Customer.next_id += 1
        self._cash_register = cash_register
        self._arrival_time = netsquid.sim_time()
        self._give_up_event = self._schedule_after(MAX_CUSTOMER_WAITING_TIME, give_up_event_type)
        give_up_handler = netsquid.EventHandler(lambda _event: self.give_up())
        self._wait(give_up_handler, entity=self, event_type=give_up_event_type)
        report(f"Customer {self.id} arrives and queues at cash register {cash_register.id}")

    def start_service(self):
        global QUEUEING_TIME
        time_since_arrival = netsquid.sim_time() - self._arrival_time
        QUEUEING_TIME.observe(time_since_arrival)
        self._give_up_event.unschedule()
        report(f"Customer {self.id} starts being serviced at register {self._cash_register.id}")

    def finish_service(self):
        global WAITING_TIME
        report(f"Customer {self.id} finishes being serviced at register {self._cash_register.id}")
        time_since_arrival = netsquid.sim_time() - self._arrival_time
        WAITING_TIME.observe(time_since_arrival)

    def give_up(self):
        global GIVE_UP_COUNT, QUEUEING_TIME, WAITING_TIME
        report(f"Customer {self.id} gives up waiting and leaves queue for register {self._cash_register.id}")
        GIVE_UP_COUNT += 1
        time_since_arrival = netsquid.sim_time() - self._arrival_time
        QUEUEING_TIME.observe(time_since_arrival)
        WAITING_TIME.observe(time_since_arrival)
        self._cash_register.remove_customer(self)

def run_simulation():
    netsquid.sim_reset()
    report("Start of simulation")
    payment_section = PaymentSection()
    netsquid.sim_run(duration=SIMULATION_DURATION)
    print(f"Average observed queue length: {QUEUE_LENGTH.average():.2f} customers")
    print(f"Average waiting time (including service): {WAITING_TIME.average():.2f} seconds")
    print(f"Average queueing time (excluding service): {QUEUEING_TIME.average():.2f} seconds")
    give_up_percentage = GIVE_UP_COUNT / ARRIVE_COUNT * 100.0
    print(f"Percentage of customers that gave up: {give_up_percentage:.2f}%")

def average_str(count, summed):
    if count == 0:
        return "-"
    average = summed / count
    return f"{average:.2f}"

if __name__ == "__main__":
    run_simulation()
