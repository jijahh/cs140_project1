'''
Dela Vega, Audrey Kirsten R.
2019-09567
Galang, Elijah Israel A.
2020-08288
'''

class Process:
    def __init__(self, name, burst_times, io_times, arrival_time):
        self.name = name
        self.burst_times = burst_times
        self.io_times = io_times
        self.state = True
        self.arrival_time = arrival_time
        self.finish_time = -1
        self.wait_time = 0
        self.is_done = False
        self.queue = "queue_1"
        self.has_arrived = False
        self.is_waiting = True


class Queue:
    def __init__(self, name):
        self.name = name
        ready_queue = []
        running_process = None

class Queue_1(Queue):
    def __init__(self, time_allotment):
        super().__init__('queue_1')
        self.time_quantum = 4
        self.time_allotment = time_allotment

class Queue_2(Queue):
    def __init__(self, time_allotment):
        super().__init__('queue_2')
        self.time_allotment = time_allotment

class Queue_3(Queue):
    def __init__(self):
        super().__init__('queue_3')

class MLFQ:
    def __init__(self, num_processes, queue1_time_allotment, queue2_time_allotment, context_switch_time, processes):
        self.time = 0
        self.queue_list = [Queue_1(queue1_time_allotment), Queue_2(queue2_time_allotment), Queue_3()]
        self.active_queue = queue_list[0]
        self.not_arrived = processes
        self.context_switch_time = context_switch_time
    def run(self):
        while self.not_arrived:
            for process in self.not_arrived:
                if process.arrival_time == self.time:
                    process.has_arrived = True
                    self.queue_list[0].ready_queue.append(process)
                    process.has_arrived = True
                    self.not_arrived.remove(process)
            if self.context_switch_time > 0:
                self.context_switch_time -= 1
                continue
            self.active_queue.run()
            self.time += 1


print("# Enter Scheduler Details #")
num_processes = int(input())
queue1_time_allotment = int(input())
queue2_time_allotment = int(input())
context_switch_time = int(input())
print(f"# Enter {num_processes} Process Details #")
processes = []

for i in range(num_processes):
    process_deets = input().split(";")
    process_name = process_deets[0]
    arrival_time = int(process_deets[1])
    burst_times = []
    io_times = []
    for i in range(2, len(process_deets)):
        if i % 2 == 0:
            burst_times.append(int(process_deets[i]))
        else:
            io_times.append(int(process_deets[i]))
    processes.append(Process(process_name, burst_times, io_times, arrival_time))

mlfq = MLFQ(num_processes, queue1_time_allotment, queue2_time_allotment, context_switch_time, processes)
mlfq.run()
