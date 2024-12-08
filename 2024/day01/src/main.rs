use std::collections::HashMap;
use std::fs;

fn main() {
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        let answer = part1(&contents);
        println!("Day 1 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 1 Part 2: {answer}");
    }
}

fn parse(input: &str) -> (Vec<usize>, Vec<usize>) {
    let lines = input.lines();
    let mut left_list = Vec::new();
    let mut right_list = Vec::new();
    for line in lines {
        if let Some((l, r)) = line.trim().split_once("   ") {
            left_list.push(l.parse::<usize>().unwrap());
            right_list.push(r.parse::<usize>().unwrap());
        }
    }
    (left_list, right_list)
}

fn part1(input: &str) -> usize {
    let (mut left_list, mut right_list) = parse(input);
    left_list.sort();
    right_list.sort();
    left_list
        .iter()
        .zip(right_list.iter())
        .fold(0, |acc, (&l, &r)| {
            acc + (l as isize - r as isize).unsigned_abs()
        })
}

fn part2(input: &str) -> usize {
    let (left_list, right_list) = parse(input);
    let mut frequencies = HashMap::new();
    for val in &left_list {
        frequencies.insert(val, 0);
    }
    for val in &right_list {
        frequencies.entry(val).and_modify(|old| *old += 1);
    }
    left_list
        .iter()
        .fold(0, |acc, &x| acc + frequencies[&x] * x)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        let input = "
        3   4
        4   3
        2   5
        1   3
        3   9
        3   3";

        let answer = part1(input);
        assert_eq!(11, answer);
    }

    #[test]
    fn test_part2() {
        let input = "
        3   4
        4   3
        2   5
        1   3
        3   9
        3   3";

        let answer = part2(input);
        assert_eq!(31, answer);
    }
}
