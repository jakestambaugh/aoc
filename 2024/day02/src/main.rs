use std::fs;

fn main() {
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        let answer = part1(&contents);
        println!("Day 2 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 2 Part 2: {answer}");
    }
}

struct Report {
    levels: Vec<isize>,
}

impl Report {
    fn is_safe(&self) -> bool {
        let deltas: Vec<isize> = self.levels.windows(2).map(|w| &w[1] - &w[0]).collect();
        deltas.iter().all(|&d| d <= -1 && d >= -3) || deltas.iter().all(|&d| d >= 1 && d <= 3)
    }

    fn is_safe_with_dampener(&self) -> bool {
        if self.is_safe() {
            return true;
        }
        for i in 0..self.levels.len() {
            let mut damped_levels = self.levels.clone();
            damped_levels.remove(i);
            let damped_report = Report {
                levels: damped_levels,
            };
            if damped_report.is_safe() {
                return true;
            }
        }
        false
    }
}

fn parse(input: &str) -> Vec<Report> {
    input
        .lines()
        .map(|line| Report {
            levels: line
                .split_whitespace()
                .map(|l| l.parse::<isize>().unwrap())
                .collect(),
        })
        .collect()
}

fn part1(input: &str) -> usize {
    let reports = parse(input);
    reports.iter().filter(|&r| r.is_safe()).count()
}

fn part2(input: &str) -> usize {
    let reports = parse(input);
    reports
        .iter()
        .filter(|&r| r.is_safe_with_dampener())
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "7 6 4 2 1
    1 2 7 8 9
    9 7 6 2 1
    1 3 2 4 5
    8 6 4 4 1
    1 3 6 7 9";

    #[test]
    fn test_part1() {
        let answer = part1(INPUT);
        assert_eq!(2, answer);
    }

    #[test]
    fn test_part2() {
        let answer = part2(INPUT);
        assert_eq!(4, answer);
    }
}
