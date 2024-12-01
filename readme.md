# Advent of Code 2024

Here we go again! Christmas needs saving and what a better way to save it than solving [Advent of Code](https://adventofcode.com) puzzles.

This year, I'm doing a few of things:

1. I'm solving these puzzles with Python
2. I'm writing explanations to help people learn Python and software development
3. I'm publishing all my notes as a digital garden on my website

I've been writing and talking about the benefits of taking good notes as a software developer. I want to show how Advent of Code can be a good way to get started. To inspire new people to start taking notes, I'm sharing all of my notes: solution explanations and technical notes about relavant topics. Those notes would normally live in my full notes system but for example's sake I've created a new, isolated environment to share here.

From this repository in GitHub, you can find the code solutions. For explanations and my full Advent of Code Digital Garden, head over to [my website](https://hamatti.org/adventofcode/2024/) and dive in!

## Personal scoreboard

- Day 1: ⭐️⭐️ [code](/src/day_1.py) : [explanation](https://hamatti.org/adventofcode/2024/Solutions/Day-01)

## How to run my code

1. Create a folder `inputs/` in the root.
2. For each day's input, create a `inputs/day_{daynro}.txt` file.
3. Optionally, create `inputs/day_{daynro}_example.txt` file with an example input from the puzzle description.
4. `cd src/`
5. `uv run day_1.py` (replace 1 with the day you want to run)
6. To run with the example code, add `example=True` to `read_input` call in that day's code.
