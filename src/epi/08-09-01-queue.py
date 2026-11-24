class EmptyQueueError(Exception):
	pass


class Queue:
	def __init__(self):
		self._values = []

	def enqueue(self, value):
		self._values.append(value)

	def dequeue(self):
		if not self._values:
			raise EmptyQueueError("Queue is empty!")

		value = self._values[0]
		self._values = self._values[1:]  # self._values.pop(0)
		return value

	def __len__(self):
		return len(self._values)

if __name__ == "__main__":
	q = Queue()
	q.enqueue(5)
	q.enqueue(8)
	q.enqueue(10)
	assert len(q) == 3
	assert q.dequeue() == 5
	assert q.dequeue() == 8
	assert q.dequeue() == 10

	try:
		q.dequeue()
	except EmptyQueueError as e:
		print(e)
	else:
	    raise AssertionError("Should have raised!!")

