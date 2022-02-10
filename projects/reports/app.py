# Global
import os
import argparse

# Externals
import numpy as np
import pyarrow as pa

# Application
if __name__  == '_main_':

    # Create Sample of Daily Data 
    arr = pa.array(np.arange(100))



    print(f"{arr[0]} .. {arr[-1]}")



    print(1 + 1)





    

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))



    with open('temp/123123.xlsx') as f:
        write.parquet(123123)


    # Se