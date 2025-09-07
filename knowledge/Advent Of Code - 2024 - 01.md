
# Pitch

We have an entry such as : 
```
3   4
4   3
2   5
1   3
3   9
3   3
```

The goal is to substract each smallest number from column one to columns to and then make the sum. The result here would be 11.

# Solution
`cat entry.txt | ./solve.sh`

``` bash
#!/bin/bash

col1=() ## Define Arrays
col2=()

## Browse the command pass through pipe
while IFS= read -r ligne; do
  val1=$(echo "$ligne" | awk '{print $1}') # Get first arg
  val2=$(echo "$ligne" | awk '{print $2}') # Get second arg

  col1+=("$val1")
  col2+=("$val2")
done

## Sort columns
sorted_col1=($(printf "%s\n" "${col1[@]}" | sort -n))
sorted_col2=($(printf "%s\n" "${col2[@]}" | sort -n))

## ${#sorted_col1[@]} used to get the length of the array
result=0
for ((i=0; i < ${#sorted_col1[@]}; i++)); do
        if (( sorted_col1[i] < sorted_col2[i] )); then
                result=$(( result + sorted_col2[i] - sorted_col1[i] ))
        else
                result=$(( result + sorted_col1[i] - sorted_col2[i] ))
        fi
done

echo "$result"
```