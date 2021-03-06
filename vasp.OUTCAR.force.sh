#!/bin/bash

outcar=$3
tip_begin=$1
tip_end=$2

buffor=100

natoms=`grep -m 1 NIONS $outcar | awk '{print $12}'`

linetot=`wc $outcar|awk '{print $1}'`
line_from_the_end=`tac $outcar | grep -n POSITION  -m 1  | awk '{print $1}'| sed -e 's/:.*//g'`
no_lices_to_pars=`echo "$line_from_the_end + $buffor" | bc`

if((${#line_from_the_end} != 0))
then
    tail -n $no_lices_to_pars $outcar | awk -v natoms=$natoms -v tip_begin=$tip_begin -v tip_end=$tip_end 'BEGIN {    
        is_found = 0;
        while(is_found == 0)
        {
            getline;
            if($1 == "POSITION")
            {
                is_found = 1;
            }
        }
        getline
        i=1
        force_sum[1] = 0.0
        force_sum[2] = 0.0
        force_sum[3] = 0.0
    }
    {
        if( i>=tip_begin && i<=tip_end && i <= natoms)
        {
            force_sum[1] = force_sum[1] + $4
            force_sum[2] = force_sum[2] + $5
            force_sum[3] = force_sum[3] + $6    
        }
        i = i+1
    }
    END {
        printf "%e   %e   %e \n", force_sum[1], force_sum[2], force_sum[3]; 
    }'
#else
#    echo "ssss"
fi
