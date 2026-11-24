from typing import NamedTuple

class EmptyStackError (Exception):
    pass 

class Stack:
    def __init__( self ):
        self._values = []

    def push( self, value ):
        self._values.append(value)

    def pop( self ):
        if not self._values:
            raise EmptyStackError("Pop from Empty Stack")
        return self._values.pop()

    def len( self ):
        return len( self._values)

class Entry(NamedTuple):
    value: int 
    min_so_far: int 

class MinStack:
    def __init__( self ):
        self._values = []

    def push( self, value ):
        if not self._values:
            min_value = value
        else: 
            _, current_min = self._values[- 1]
            min_value = min( value, current_min )
        self._values.append( Entry( value, min_value ) )

    def pop( self ):
        if not self._values:
            raise EmptyStackError("Pop from Empty Stack")
        return self._values.pop().value

    def min( self ):
        if not self._values:
            raise EmptyStackError("Nothing there on the stack")
        return self._values[-1].min_so_far

    def __len__( self ):
        return len( self._values)

if __name__ == "__main__":
    stack = MinStack()
    stack.push( 20 )
    stack.push( 30 )
    stack.push( 10 )

    assert len(stack) == 3
    assert stack.min() == 10
    assert stack.pop() == 10
    assert stack.min() == 20
    assert stack.pop() == 30 
    assert stack.pop() == 20 

    try:
        stack.min()
    except EmptyStackError as e:
        print( e )
    else:
        raise AssertionError("Pop on empty stack should raise")

