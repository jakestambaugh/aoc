use std::fs;

use regex::Regex;

fn main() {
    // File hosts.txt must exist in the current path
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        // Consumes the iterator, returns an (Optional) String
        let answer = part1(&contents);
        println!("Day 1 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 1 Part 2: {answer}");
    }
}

fn part1(input: &str) -> usize {
    let re = Regex::new(r"mul\(([0-9]+),([0-9]+)\)").unwrap();
    re.captures_iter(input)
        .map(|c| c.extract())
        .map(|(_, [val1, val2])| val1.parse::<usize>().unwrap() * val2.parse::<usize>().unwrap())
        .sum()
}

fn part2(input: &str) -> usize {
    let donts: Vec<&str> = input.split("don't").collect();
    let first = donts.first().unwrap();
    let dos: String = donts
        .iter()
        .map(|l| l.split("do").skip(1).collect::<Vec<&str>>().join(""))
        .collect::<Vec<String>>()
        .join("");
    part1(&format!("{first}{dos}"))
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))";
    const INPUT2: &str =
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";

    #[test]
    fn test_part1() {
        let answer = part1(INPUT);
        assert_eq!(161, answer);
    }

    #[test]
    fn test_part2() {
        let answer = part2(INPUT2);
        assert_eq!(48, answer);
    }
}
