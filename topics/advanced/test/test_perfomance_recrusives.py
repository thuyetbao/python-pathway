from timeit import Timer

################################################################
# Performance Test
# Between `fib`, `fibi`, and `fibm`
# with n in range(1, 30)
################################################################

for numb in range(1, 31):
    
    # Fib
    t1 = Timer("fib(" + str(numb) + ")", "from topics.advanced.recrusives import fib")
    time1 = t1.timeit(3)

    # Fibi
    t2 = Timer("fibi(" + str(numb) + ")", "from topics.advanced.recrusives import fibi")
    time2 = t2.timeit(3)

    # Fibm
    t3 = Timer("fibm(" + str(numb) + ")", "from topics.advanced.recrusives import fibm")
    time3 = t3.timeit(3)

    # Log
    print(f"n={numb:2d}, fib: {time1:8.6f}, fibi: {time2:7.6f}, fibm: {time3:7.6f}, time1/time2: {time1/time2:10.2f}, time2/time3: {time2/time3:10.2f}")
