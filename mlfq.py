"""
Dela Vega, Audrey Kirsten R.
2019-09567
Galang, Elijah Israel A.
2020-08288
"""


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
        self.queue = 0
        self.has_arrived = False
        self.is_waiting = True
        self.time_allotment = 0

    def check_done(self):
        return self.check_burst() and self.check_io()

    def check_burst(self):
        return self.burst_times == []

    def check_io(self):
        return self.io_times == []


class Queue:
    def __init__(self, name):
        self.name = name
        self.ready_queue = []
        self.running_process = None


class Queue_1(Queue):
    def __init__(self, time_allotment):
        super().__init__("queue_1")
        self.time_quantum = 4
        self.curr_time_quantum = 4
        self.time_allotment = time_allotment

    def run(self, mlfq):
        if not self.ready_queue:
            return
        if self.running_process is None:
            self.running_process = self.ready_queue[0]
        self.curr_time_quantum -= 1
        mlfq.is_context_switching = False
        self.running_process.is_waiting = False
        self.running_process.burst_times[0] -= 1
        self.running_process.time_allotment -= 1
        # print(self.running_process.time_allotment)
        # print(self.curr_time_quantum)
        # print(self.running_process.burst_times[0])
        if self.running_process.burst_times[0] == 0:
            mlfq.is_context_switching = True
            del self.running_process.burst_times[0]
            if not self.running_process.check_io():
                mlfq.in_io.append(self.running_process)
            else:
                self.running_process.is_done = True
                self.running_process.finish_time = mlfq.time
                mlfq.to_print[1].append(self.running_process.name)
                mlfq.done_processes.append(self.running_process)
            self.ready_queue.remove(self.running_process)
            self.running_process = None
            self.curr_time_quantum = self.time_quantum
        elif (
            self.running_process is not None
            and self.running_process.time_allotment == 0
        ):
            mlfq.is_context_switching = True
            self.running_process.is_waiting = True
            mlfq.to_print[5].append(self.running_process.name)
            self.running_process.queue += 1
            mlfq.queue_list[self.running_process.queue].enqueue(self.running_process)
            self.ready_queue.remove(self.running_process)
            self.running_process = None
            self.curr_time_quantum = self.time_quantum
        elif self.curr_time_quantum == 0:
            mlfq.is_context_switching = True
            self.running_process.is_waiting = True
            self.ready_queue.append(self.running_process)
            del self.ready_queue[0]
            self.curr_time_quantum = self.time_quantum
            self.running_process = None

    def enqueue(self, process):
        process.time_allotment = self.time_allotment
        self.ready_queue.append(process)


class Queue_2(Queue):
    def __init__(self, time_allotment):
        super().__init__("queue_2")
        self.time_allotment = time_allotment

    def run(self, mlfq):
        if not self.ready_queue:
            return
        if self.running_process is None:
            self.running_process = self.ready_queue[0]
        mlfq.is_context_switching = False
        self.running_process.is_waiting = False
        self.running_process.burst_times[0] -= 1
        self.running_process.time_allotment -= 1
        if self.running_process.burst_times[0] == 0:
            mlfq.is_context_switching = True
            if not self.running_process.check_io():
                mlfq.in_io.append(self.running_process)
            else:
                self.running_process.is_done = True
                self.running_process.finish_time = mlfq.time
                mlfq.to_print[1].append(process.name)
                mlfq.done_processes.append(running_process)
            del self.running_process.burst_times[0]
            self.ready_queue.remove(self.running_process)
            self.running_process = None
        if self.running_process.time_allotment == 0:
            mlfq.is_context_switching = True
            self.running_process.queue += 1
            self.running_process.is_waiting = True
            mlfq.queue_list[self.running_process.queue].enqueue(self.running_process)
            mlfq.to_print[5].append(self.running_process.name)
            self.ready_queue.remove(self.running_process)
            self.running_process = None

    def enqueue(self, process):
        process.time_allotment = self.time_allotment
        self.ready_queue.append(process)


class Queue_3(Queue):
    def __init__(self):
        super().__init__("queue_3")
        self.enqueue_list = []

    def run(self, mlfq):
        # print(self.ready_queue)

        if self.running_process is None:
            self.running_process = self.ready_queue[0]

        mlfq.is_context_switching = False
        self.running_process.is_waiting = False
        self.running_process.burst_times[0] -= 1
        if self.running_process.burst_times[0] == 0:
            mlfq.is_context_switching = True
            del self.running_process.burst_times[0]
            if not self.running_process.check_io():
                mlfq.in_io.append(self.running_process)
            else:
                self.running_process.is_done = True
                self.running_process.finish_time = mlfq.time
                mlfq.to_print[1].append(self.running_process.name)
                mlfq.done_processes.append(self.running_process)
            self.ready_queue.remove(self.running_process)
            self.running_process = None

    def enqueue(self, process):
        self.enqueue_list.append(process)

    def enqueue_everything(self):
        self.enqueue_list = sorted(
            self.enqueue_list, key=lambda x: sum(x.burst_times) + sum(x.io_times)
        )
        if self.enqueue_list != []:
            self.ready_queue = self.ready_queue + self.enqueue_list
        self.enqueue_list = []


class MLFQ:
    def __init__(
        self,
        num_processes,
        queue1_time_allotment,
        queue2_time_allotment,
        context_switch_time,
        processes,
    ):
        self.time = 1
        self.queue_list = [
            Queue_1(queue1_time_allotment),
            Queue_2(queue2_time_allotment),
            Queue_3(),
        ]
        self.active_queue = self.queue_list[0]
        self.not_arrived = processes
        self.done_processes = []
        self.context_switch_time = context_switch_time
        self.to_be_queued = []
        self.in_io = []
        self.is_done = False
        self.is_context_switching = False
        self.to_print = [[], [], [[], [], []], [], [], []]

    def run(self):
        while True:
            self.not_arrived = list(
                filter(lambda x: x.has_arrived == False, self.not_arrived)
            )
            for process in self.not_arrived:
                if process.arrival_time == self.time or (process.arrival_time == 0 and self.time == 1):
                    self.to_print[0].append(process.name)
                    process.has_arrived = True
                    self.queue_list[0].enqueue(process)
                    # print(self.queue_list[0].ready_queue)
            for i in self.queue_list:
                if i.ready_queue:
                    self.active_queue = i
                    break
            self.active_queue.run(self)
            for i in self.queue_list:
                if i.ready_queue: 
                    for j in i.ready_queue:
                        if j.is_waiting and self.time != 1:
                            j.wait_time += 1
                            # print("----------------")
                            # print(f"waiting process: {j.name}, total: {j.wait_time}")
                if self.is_context_switching:
                    self.time += self.context_switch_time
                    self.is_context_switching = False
                    # print("Context Switching")
            for i in self.queue_list:
                if i.ready_queue:
                    self.active_queue = i
                    break
            io_done = []
            for process in self.in_io:
                # print(process.name, process.io_times[0])
                if process.io_times[0] == 0:
                    del process.io_times[0]
                    if process.check_done():
                        self.done_processes.append(process)
                        process.is_done = True
                        process.finish_time = self.time
                        self.to_print[1].append(process.name)
                    else:
                        self.queue_list[process.queue].enqueue(process)
                    process.is_waiting = True
                    io_done.append(process)
                else:
                    process.io_times[0] -= 1
            for i in io_done:
                self.in_io.remove(i)
            io_done = []
            self.queue_list[2].enqueue_everything()
            for i in range(len(self.queue_list)):
                if self.queue_list[i].ready_queue:
                    for j in self.queue_list[i].ready_queue:
                        self.to_print[2][i].append(j.name)
            if self.active_queue.ready_queue:
                self.to_print[3].append(self.active_queue.ready_queue[0].name)
            for process in self.in_io:
                self.to_print[4].append(process.name)
            self.print_everything()
            if self.check_done():
                self.done()
                break
            self.time += 1

    def check_done(self):
        for queue in self.queue_list:
            if queue.ready_queue:
                return False
        if self.in_io:
            return False
        return True

    def enqueue(self):
        for process in self.to_be_queued:
            self.queue_list[process.queue].ready_queue.append(process)

    def print_everything(self):
        print(f"At time {self.time - 1}")
        if self.to_print[0]:
            print("Arriving :", end=" ")
            print(self.to_print[0])
        for i in self.to_print[1]:
            print(f"{i} DONE")
        print("Queues :", end=" ")
        print(
            # [   self.to_print[2][0],
            #     self.to_print[2][1],
            #     self.to_print[2][2],
            [
                self.to_print[2][x][1:] if x == self.queue_list.index(self.active_queue) else self.to_print[2][x]
                for x in range(len(self.to_print[2]))
            ]
            # ]
        )
        print(f"CPU: {self.to_print[3]}")
        print(f"I/O: {self.to_print[4]}")
        for i in self.to_print[5]:
            print(f"{i} DEMOTED")
        self.to_print = [[], [], [[], [], []], [], [], []]
        print("\n")

    def done(self):
        print("SIMULATION DONE")
        turnaround_times = []

        for i in self.done_processes:
            turnaround_time = i.finish_time - i.arrival_time
            turnaround_times.append(turnaround_time)
            print(
                f"Turnaround time for Process {i.name}: {i.finish_time} - {i.arrival_time} = {turnaround_time} ms"
            )
        print(
            f"Average Turnaround Time = {sum(turnaround_times)/len(turnaround_times)} ms"
        )
        for i in self.done_processes:
            print(f"Waiting time for Process {i.name}: {i.wait_time} ms")


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
    # print(process_name, burst_times, io_times, arrival_time)
    processes.append(Process(process_name, burst_times, io_times, arrival_time))

mlfq = MLFQ(
    num_processes,
    queue1_time_allotment,
    queue2_time_allotment,
    context_switch_time,
    processes,
)
mlfq.run()

