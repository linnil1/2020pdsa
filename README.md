# 2020 PDSA

This repo stored judge and solution of NTU BIME PDSA in 2020.


## Problem Set
### HW1
https://hackmd.io/nxED7UQJSw6YWWK5QA3YGA
### HW2
https://hackmd.io/KJCHp-HDTjSY9SBGyJV-3w
### HW3
https://hackmd.io/8Ru_zm_oSeC3bLwsiJWGow
### HW4
https://hackmd.io/lyo5V8XFQIOr3cfEp0n1rg
### HW5
https://hackmd.io/SlAPLkYUSQ6abqgr31ihbg
### HW6
https://hackmd.io/ZlZCexfvSmakl06qLG7COA
### HW7
https://hackmd.io/NPDNSN8TRO-UHeitGxnmiw
### HW8
https://hackmd.io/3LLeJJonRROPWed9ffGWvg


## How it work
### Main
`JudgeControll.py`

* Read testcase (JSON format)
* Compile the code if needed
* Execute judger with time_limit
* Get the status and score from judge
* Write log and score into file

### Judger
#### Python Judger
`Judger.py`

* A abstract class for inheritance
* Implement `run` `compare` for each problem (In `xx.judge.py`)
* Read one testcase (JSON format)
* Calculate the time each sample run
* Output the result(Actullay it's a file)

### Java Judger
`Judger.java`

* Same as Python Judger
* Need to implement `class` to read JSON input. (In `xx.judge.java`)

### Testcase generator
I use python and numpy random to genereate testcase.
`xx.test.py`

and the testcase data will store in `xx.json`

### Answer
`xx.sol.py`
`xx.sol.java`

### Run
```
python3 xx.judge.py
dk openjdk:14-slim javac -cp gson.jar:algs4.jar:. xx.judge.java xx.sol.java Judger.java
dk openjdk:14-slim java  -cp gson.jar:algs4.jar:. Judge
```
