use std::collections::VecDeque;
use std::fs;

use rayon::iter::{IntoParallelRefIterator, ParallelIterator};

fn main() {
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        let answer = part1(&contents);
        println!("Day 7 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 7 Part 2: {answer}");
    }
}

struct Equation {
    result: u64,
    operands: VecDeque<u64>,
}

fn concat(a: u64, b: u64) -> u64 {
    format!("{}{}", a, b).parse().unwrap()
}

fn solve_with_concat(target: u64, operands: VecDeque<u64>) -> Option<u64> {
    if operands.len() < 2 {
        operands.front().copied().take_if(|&mut v| v == target)
    } else if operands.len() == 2 {
        if operands[0] + operands[1] == target
            || operands[0] * operands[1] == target
            || concat(operands[0], operands[1]) == target
        {
            Some(target)
        } else {
            None
        }
    } else {
        let mut to_add = operands.clone();
        let mut last = to_add.split_off(2);
        last.push_front(to_add[0] + to_add[1]);
        let adds = solve_with_concat(target, last);

        let mut to_multiply = operands.clone();
        let mut last = to_multiply.split_off(2);
        last.push_front(to_multiply[0] * to_multiply[1]);
        let multiplies = solve_with_concat(target, last);

        let mut to_concatenate = operands.clone();
        let mut last = to_concatenate.split_off(2);
        last.push_front(concat(to_concatenate[0], to_concatenate[1]));
        let concatenates = solve_with_concat(target, last);

        adds.or(multiplies.or(concatenates))
    }
}

fn solve(target: u64, operands: VecDeque<u64>) -> Option<u64> {
    if operands.len() < 2 {
        operands.front().copied().take_if(|&mut v| v == target)
    } else if operands.len() == 2 {
        if operands[0] + operands[1] == target || operands[0] * operands[1] == target {
            Some(target)
        } else {
            None
        }
    } else {
        let mut to_add = operands.clone();
        let mut last = to_add.split_off(2);
        last.push_front(to_add[0] + to_add[1]);
        let adds = solve(target, last);

        let mut to_multiply = operands.clone();
        let mut last = to_multiply.split_off(2);
        last.push_front(to_multiply[0] * to_multiply[1]);
        let multiplies = solve(target, last);

        adds.or(multiplies)
    }
}

fn parse(input: &str) -> Vec<Equation> {
    input
        .lines()
        .filter_map(|line| line.split_once(":"))
        .map(|(before, after)| Equation {
            result: before.parse::<u64>().unwrap(),
            operands: after
                .split_whitespace()
                .map(|v| v.parse::<u64>().unwrap())
                .collect::<VecDeque<_>>(),
        })
        .collect()
}

fn part1(input: &str) -> usize {
    let answer: u64 = parse(input)
        .par_iter()
        .filter_map(|eq| solve(eq.result, eq.operands.clone()))
        .sum();
    answer as usize
}

fn part2(input: &str) -> usize {
    let answer: u64 = parse(input)
        .par_iter()
        .filter_map(|eq| solve_with_concat(eq.result, eq.operands.clone()))
        .sum();
    answer as usize
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20";

    #[test]
    fn test_part1() {
        let answer = part1(INPUT);
        assert_eq!(3749, answer);
    }

    #[test]
    fn test_part2() {
        let answer = part2(INPUT);
        assert_eq!(11387, answer);
    }
}
