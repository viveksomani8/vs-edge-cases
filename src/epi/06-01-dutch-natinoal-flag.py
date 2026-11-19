#Problem 6.1: Write a function that takes an array A and an index i into A, and
#rearranges the elements such that all elements less than A[i] appear first, followed
#by elements equal to A[i], followed by elements greater than A[i]. Your algorithm
#should have 0(1) space complexity and OOAI)time complexity.

"""
len, append, extend, while, no ++ --, 
smaller, equal, larger = 0, 0, len(A)
A = lower + equal + larger  # wrong new biding 
A[:] = lower + equal + larger # correct, in-place update
"""
# test1 
A = [ 9, 6, 1, 2,4, 6, 5, 8, 1 ]
# test2 A = []
# test3 A = [ 1,2,3,4,5 ] i = 0, i = 4 i=2
# test4 A = [ 5,4,3,2,1] i = 0, i = 4 i = 2

def rearrange_bf(A, i):
    lower = []
    higher = []
    equal = []
    pivot = A[i]

    for val in A:
        if val < pivot:
            lower.append( val )
        elif val > pivot:
            higher.append( val )
        else:
            equal.append( val )

    A[:] = lower + equal + higher 

def rearrange_bf2(A, i):
    pivot = A[i] 
    lower = [ x for x in A if x < pivot ]
    equal = [ x for x in A if x == pivot ]
    higher = [ x for x in A if x > pivot ]
    A[:] = lower + equal + higher 

def rearrange(A, i):
    pivot = A[i]
    low  = 0
    high = len( A ) - 1

    i = 0 

    while i <= high:
        while low < high and  A[low] < pivot:
            low += 1

        while high > low and A[high] > pivot:
            high -= 1 

        if A[i] > pivot:
            A[ high ], A[i] = A[i], A[ high ]
            high -= 1
        elif A[i] < pivot:
            A[ low ], A[i] = A[ i ], A[ low ]
            low += 1 
        i += 1

    print( A )

# smaller : Everything before it is less than pivot
# larger  : Anything after that is greater than pivot
# equal   : Anything between smaller and equal are equal to pivot 
def rearrange_2(A, i):
    pivot = A[i]
    smaller = 0 ;
    equal = 0
    larger = len( A )

    while equal < larger: 
        if A[equal] < pivot: 
            swap( A, equal, smaller )
            smaller += 1 
            equal += 1
        elif A[equal] > pivot:
            swap( A, equal, larger )
            larger -= 1
        else:
            equal += 1



def swap( A, i, j ):
    A[i], A[j] = A[j], A[i]

rearrange( A, 4 )

# ---------------------------------------------------------------------------
# Book version (EPI, single pass, O(n) time, O(1) space).
#
# Invariants maintained throughout the loop:
#   A[:smaller]        -> elements less than pivot
#   A[smaller:equal]   -> elements equal to pivot
#   A[equal:larger]    -> unclassified elements
#   A[larger:]         -> elements greater than pivot
# ---------------------------------------------------------------------------
def dutch_flag_partition(pivot_index, A):
    pivot = A[pivot_index]
    smaller, equal, larger = 0, 0, len(A)

    # Keep going as long as there is an unclassified element.
    while equal < larger:
        # A[equal] is the incoming unclassified element.
        if A[equal] < pivot:
            A[smaller], A[equal] = A[equal], A[smaller]
            smaller, equal = smaller + 1, equal + 1
        elif A[equal] == pivot:
            equal += 1
        else:  # A[equal] > pivot
            larger -= 1
            A[equal], A[larger] = A[larger], A[equal]
            # equal is NOT advanced: the element swapped in is still unclassified.


B = [9, 6, 1, 2, 4, 6, 5, 8, 1]
dutch_flag_partition(4, B)
print(B)
