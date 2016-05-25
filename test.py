import asyncio



@asyncio.coroutine
def do_work(task_name, work_queue):
    while not work_queue.empty():
        queue_item = yield from work_queue.get()
        print('{0} grabbed item: {1}'.format(task_name, queue_item))
        q.put_nowait(queue_item+10)
        q.put_nowait(queue_item+10)
        yield from asyncio.sleep(0.5)
        print('processed - ',task_name)


q = asyncio.Queue()

for x in range(20):
    q.put_nowait(x)

print(q)

loop = asyncio.get_event_loop()

tasks = [ asyncio.async(do_work('task' + str(x), q)) for x in range(q.qsize()) ]
    # asyncio.async(do_work('task2', q)),
    # asyncio.async(do_work('task3', q))]

loop.run_until_complete(asyncio.wait(tasks))
loop.close()
