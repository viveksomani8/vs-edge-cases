# Problem 7.1: Write a function that takes L and F, and returns the merge of L and F. 
# Your code should use 0(1) additional storage-it should reuse the nodes from
# the lists provided as input. Your function should use 0(1) additional storage, as
# illustrated in Figure 7.3.The only field you can change in a node is next

class Node:
	def __init__( self, data, next ):
		self.data = data
		self.next = next

# 
#  2,5,8,10
#  1,7,9,13, 14, 15   
#  start -> 1 -> 2->5->7

def merge_sorted_lists( L, F ):

	if L == None:
		return F
	if F == None:
		return L 

	l = L 
	f = F 
    
    
	if l.data < f.data:
		head = l
		l = l.next
	else:
		head = f
		f = f.next 

	cur = head 

	while l.next != None and f.next != None :
		if l.data <= f.data:
			cur.next = l 
			l = l.next  
		else:
			cur.next = f;
			f = f.next 

	while f.next != None: 
		cur.next = f
		f = f.next

	while l.next != None:
		cur.next = l
		l = l.next
	
	return head

def build_from_array( A ):
	L = None
	prev_node = None
	for val in A:
		node = Node( val, None )

		if prev_node != None:
			prev_node.next = node 
		
		if L == None:
			L = node 
		prev_node = node 
		
	return L

L = build_from_array( [ 2,5,8,10 ] )
F = build_from_array( [ 1,7,9,13,14,15 ] )

merged = merge_sorted_lists( L, F )
print_ll( merged )

def print_ll( ll ):
    while ll.next != None:
        print( ll.data ) 
        
    print( ll.data )
	
