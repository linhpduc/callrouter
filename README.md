# callrouter

The programming exercise with valuechecker{dot}ai

* Challenge: https://docs.google.com/document/d/1t8BSicFnJellmzg2tBNoAL4hoes3hkyBljowWbBeVrg/edit
* Start date: 8/4/2023
* Deadline: 8/10/2023

## Data sample

```python
price_list_sample = {
    "A": [
        ("1", 0.9),
        ("268", 5.1),
        ("46", 0.17),
        ("4620", 0.0),
        ("468", 0.15),
        ("4631", 0.15),
        ("4673", 0.9),
        ("46732", 1.1),
    ],
    "B": [
        ("1", 0.92),
        ("44", 0.5),
        ("46", 0.2),
        ("467", 1.0),
        ("48", 1.2),
    ],
}
```

## Intuition

This challenge is similar with the autocomplete searching problem using trie. Intuitively, trie (maybe) is a good fit
data structure to solve this challenge.

We can use a bruteforce approach to determine the answer, however, using a certain data structure, I believe there will
be a more efficient solution.

## Approach

### #1

Very first idea, we can build a trie to store price list for each operator. With a certain phone number needs routing,
using the trie to search the price of the longest matching prefix with it.

Do the same for all the remaining operators, then compare the results to find out which operator has the cheapest price,
and how much the cheapest is.

![Illustration for the first idea](./assests/calllrouter-appr01.png "Build an array of trie")

### #2

Having many trie objects and doing search on all trie is not really efficient, both in time and space complexity. It
would be better if we have only one trie object to manipulate.

In combined trie, each node in trie will store a hashmap of `<operator: price>`.

With a certain phone number, traverse the nodes until reaching the leaf node, at each step, save the most recent price
of each operator (if any).

In the end, we have a **hashmap** that stores the prices of all the operators whose prefix matches that phone number.
The last thing is to determine which price is the cheapest in this **hashmap**.

![Illustration for the 2nd idea](./assests/calllrouter-appr02.png "Build a combined trie for all operators")

## How to run

### Required

* Python: 3.10+
* Packages: `coverage`

### Run test

```console
% coverage run -m unittest -v
test_init_trie (testcases.FindCheapestPriceTestCase) ... ok
test_mul_operator_combine_trie (testcases.FindCheapestPriceTestCase) ... ok
test_single_trie (testcases.FindCheapestPriceTestCase) ... ok
test_prefix_namedtuple (testcases.ModelTestCase) ... ok
test_create_combine_trie (testcases.TrieTestCase) ... ok
test_create_single_trie (testcases.TrieTestCase) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.000s

OK
% coverage report
Name                   Stmts   Miss  Cover
------------------------------------------
router.py                 28      0   100%
testcases.py              36      1    97%
utils/__init__.py          0      0   100%
utils/data_sample.py       1      0   100%
utils/models.py            8      0   100%
utils/trie.py             47      2    96%
------------------------------------------
TOTAL                    120      3    98%
```

### Run program

```console
% python3 main.py 4673212345 449102837332 84987654321
Results: 
        [(prefix: '467', operator: 'B', price: 1.0), (prefix: '44', operator: 'B', price: 0.5), None]
Single Trie:
        +time elapsed: 0.000060s
        +size of trie: 232 bytes
--------------------------------------------------
Results: 
        [(prefix: '467', operator: 'B', price: 1.0), (prefix: '44', operator: 'B', price: 0.5), None]
Combine Trie:
        +time elapsed: 0.000032s
        +size of trie: 48 bytes
--------------------------------------------------
```

## Discussions

- If we just have only one process and one thread program, the **appr#2** can reduce memory space to store trie object,
  we also need only one searching operation (per phone number) to determine the cheapest price. So that, it's really
  better than **appr#01**. Here is the test result with 10_000_000 input random numbers: 
```console
Single Trie:
        +time elapsed: 6.993801s
        +size of trie: 232 bytes
--------------------------------------------------
Combine Trie:
        +time elapsed: 4.931440s
        +size of trie: 48 bytes
--------------------------------------------------
```
- In both approaches, multithreading does not help speed up the program, because it's **CPU bound** task and limitation
  of Python **GIL** (Global Interpreter Locking).
- With single request, using **appr#1** we have a good chance to run the program in parallel for a part of program (
  build trie and search on it), taking advantage of the cpu with many cores, each trie and search operation on it (for a
  certain operator) can be handled by a completely separate process. Or imagine a scenario using **map-reduce
  architecture** if the problem needs to scale indefinitely.
- If we need to handle a large number of phone number routing requests simultaneously, the **appr#02** is a good
  candidate to choose. Using multiprocessing, each request is handled by 1 separate process. But we won't reduce the
  memory space anymore (even increase), because each "fork" process will clone the memory.
