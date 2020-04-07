# Overview
Visualize outcomes under different voting schemes, assuming each voter has one vote.

# Dependencies
Python 3 and matplotlib

# Input
`python voting.py` takes the first csv file it finds (relative to the current/working directory) as input. It expects the following format of csv file:
| Name           | <Candidate 0 name>                         | <Candidate 1 name>                         | ... |
|----------------|--------------------------------------------|--------------------------------------------|-----|
| <Voter 0 name> | <Voter 0 preference value for Candidate 0> | <Voter 0 preference value for Candidate 1> | ... |
| <Voter 1 name> | <Voter 1 preference value for Candidate 0> | <Voter 1 preference value for Candidate 1> | ... |
| ...            | ...                                        | ...                                        | ... |

# Output
`python voting.py` prints the results of plurality, instant-runoff, Borda count, approval, and positive-negative voting, in that order. It also generates images according to those results.

# Example
Example input and output is provided in the `example` directory of this repo.
