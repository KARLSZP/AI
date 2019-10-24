# README

Please Run `benchmarks.py` for auto tests.

`python benchmarks.py`

Be AWARE:

1. The script is built based on pyautogui, so I’m sorry to remind you **please leave your PC alone** till the script is done.
2. Since the hot-key for **The BoxMan** to select level is ‘F3’, which is the same hot-key to raise QQ, **please ensure your QQ is shut down when testing.**
3. You don’t need to do ANYTHING while benchmarking, please have fun and take a rest XD.

---

Further More, the main strategy of my designs is to judge **if the target is captured by a box**.

Whether a position is captured or not is a state that would be changed **by and only by** the action **push_[dir]**, a box will capture the new position it’s going to and set its former position free.

Take **Case 5** as an example:

```pddl
(define (problem prob)
    (:domain boxman)
    (:objects m b1 b2 b3 x1 x2 x3 x4 x5 x6 y1 y2 y3 y4 y5 y6 - physob)
    (:init
    	(man m)
        (box b1) (box b2) (box b3)
        (position x1) (position y1) (position x2) (position y2)
        (position x3) (position y3) (position x4) (position y4)
        (position x5) (position y5) (position x6) (position y6)
        (blank x1 y1) (blank x1 y2)
        (blank x2 y1) (blank x2 y2)
        (blank x3 y1) (blank x3 y2) (blank x3 y4) (blank x3 y5) (blank x3 y6)
        (blank x4 y3) (blank x4 y4) (blank x4 y5) (blank x4 y6)
        (blank x5 y2)
        (blank x6 y2) (blank x6 y3)
        (at  m x6 y4) (at b1 x3 y3) (at b2 x4 y2) (at b3 x5 y4)
        (capture x3 y3) (capture x4 y2) (capture x5 y4)
        (add x1 x2) (add x2 x3) (add x3 x4) (add x4 x5) (add x5 x6)
        (add y1 y2) (add y2 y3) (add y3 y4) (add y4 y5) (add y5 y6)
        (sub x2 x1) (sub x3 x2) (sub x4 x3) (sub x5 x4) (sub x6 x5)
        (sub y2 y1) (sub y3 y2) (sub y4 y3) (sub y5 y4) (sub y6 y5)
    )
    (:goal (
        and (capture x3 y2) (capture x3 y3) (capture x6 y2)
    )))
```

Apparently, the goal state is easy and simple to describe as above.

---

**Test Log**

**TestLog.txt** will be automatically generated:

```
Current Test Case: Level 1
Clear in 11 steps.
Level 1 Cleared.

Current Test Case: Level 10
Clear in 36 steps.
Level 10 Cleared.

Current Test Case: Level 30
Clear in 141 steps.
Level 30 Cleared.

Current Test Case: Level 40
Clear in 124 steps.
Level 40 Cleared.

Current Test Case: Level 50
Clear in 48 steps.
Level 50 Cleared.
```

---

17341137 宋震鹏