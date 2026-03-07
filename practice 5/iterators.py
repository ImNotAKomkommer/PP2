#
def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

ctr = fun(5)
for n in ctr:
    print(n)
#Creating Generators
def fun():
    yield 1            
    yield 2            
    yield 3            
 
# Driver code to check above generator function
for val in fun(): 
    print(val)
#Yield vs Return
#Yield: is used in generator functions to provide a sequence of values over time.
#When yield is executed, it pauses the function, returns the current value and retains the state of the function.
#This allows the function to continue from same point when called again, making it ideal for generating large or complex sequences efficiently.
#Return: is used to exit a function and return a final value. 
#Once return is executed, function is terminated immediately and no state is retained. 
#This is suitable for cases where a single result is needed from a function.
def fun():
    return 1 + 2 + 3

res = fun()
print(res)
#Generator Expression
sq = (x*x for x in range(1, 6))
for i in sq:
    print(i)