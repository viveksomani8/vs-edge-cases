# Problem 7.1: Write a function that takes L and F, and returns the merge of L and F. 
# Your code should use 0(1) additional storage-it should reuse the nodes from
# the lists provided as input. Your function should use 0(1) additional storage, as
# illustrated in Figure 7.3.The only field you can change in a node is next

from dataclasses import dataclass

@dataclass
class Node:
	data: int 
	next: Node | None = None 

# 
#  2,5,8,10
#  1,7,9,13, 14, 15   
#  start -> 1 -> 2->5->7

def merge_sorted_lists( a: Node | None, b: Node | None ) -> Node | None:
    """
        Merge two sorted linked lists by relinking their nodes. 
        Stable: on a tie the node from 'a' comes first. O( n + m ) time, O( 1 ) space. 
    """
    dummy = tail =  Node( 0 )  # The list is sorted from dummy to tail 
    
    while a and b:
        if a.data <= b.data:
            tail.next, a = a , a.next 
        else:
            tail.next, b = b, b.next 
        tail = tail.next 
        
    tail.next = a or b 
    return dummy.next 
    

def from_values(values):
    dummy = tail = Node(0) 
    for value in values:
        tail.next = Node( value ) 
        tail = tail.next 
    return dummy.next 
    
def to_values( node ):
    values = []
    while node:
        values.append( node.data ) 
        node = node.next 
    return values 

l = from_values( [ 2,5,8,10 ] )
f = from_values( [ 1,7,9,13,14,15 ] )

merged = merge_sorted_lists( l, f )
print( to_values( merged ) )

