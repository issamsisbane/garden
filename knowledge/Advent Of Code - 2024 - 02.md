# Part 01
## Pitch
We have this entry :
```
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
```

We want for each line to count lines that respect :
* Numbers must be all **descending** or **increasing** from left to right
* Neighbors numbers differ by at least **1** and at most **3**

For this entry the answer would be 2

## Solution

``` bash
safe=0
while IFS= read -r ligne; do
		
		# Verify if the line must be increasing or descending
        elements=($ligne)
        type=""
        if (( elements[0] < elements[1] )); then
                type="+"
        elif (( elements[0] > elements[1] )); then
                type="-"
        else
                type="="
        fi
        
        isSafe=true
        for ((i=0; i < ${#elements[@]}; i++)); do
                
                if (( i + 1 >= ${#elements[@]} )); then
                        break
                fi

				# Verify that numbers are still increasing or descending
                if (( elements[i] < elements[i+1])) && [[ "$type" == "+" ]]; then
                        difference=$(( elements[i+1] - elements[i] ))
                elif (( elements[i] > elements[i+1])) && [[ "$type" == "-" ]]; then
                        difference=$(( elements[i] - elements[i+1] ))
                else
                        isSafe=false
                        break
                fi

				# Verify the difference between 2 neighbors numbers
                if (( difference < 1 || difference > 3 )); then
                        isSafe=false
                        break
                fi
        done
        
        if $isSafe; then
                safe=$(( safe + 1 ))
        fi
done

echo "$safe"
```