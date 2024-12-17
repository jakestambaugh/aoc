use std::collections::{BTreeMap, BTreeSet};
use std::fs;

fn main() {
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        let answer = part1(&contents);
        println!("Day 5 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 5 Part 2: {answer}");
    }
}

struct Rules {
    map: BTreeMap<usize, BTreeSet<usize>>,
}

impl Rules {
    fn new() -> Self {
        Rules {
            map: BTreeMap::default(),
        }
    }

    fn insert(&mut self, a: usize, b: usize) {
        if let Some(v) = self.map.get_mut(&a) {
            v.insert(b);
        } else {
            self.map.insert(a, BTreeSet::from([b]));
        }
    }

    fn ordered(&self, a: &usize, b: &usize) -> bool {
        !self.map.get(b).map_or(false, |v| v.contains(a))
    }
}

impl FromIterator<(usize, usize)> for Rules {
    fn from_iter<T: IntoIterator<Item = (usize, usize)>>(iter: T) -> Self {
        let mut rules = Self::new();
        for (k, v) in iter {
            rules.insert(k, v);
        }
        rules
    }
}

struct Update {
    pages: Vec<usize>,
}

impl Update {
    fn get_middle(&self) -> usize {
        self.pages[self.pages.len() / 2]
    }
}

impl FromIterator<usize> for Update {
    fn from_iter<T: IntoIterator<Item = usize>>(iter: T) -> Self {
        let mut x = vec![];
        for i in iter {
            x.push(i);
        }
        Self { pages: x }
    }
}

fn parse(input: &str) -> (Rules, Vec<Update>) {
    let (ordering, pages) = input.split_once("\n\n").unwrap();
    let rules: Rules = ordering
        .lines()
        .map(|l| l.split_once("|").unwrap())
        .map(|(a, b)| (a.parse::<usize>().unwrap(), b.parse::<usize>().unwrap()))
        .collect();
    let updates = pages
        .lines()
        .map(|l| l.split(",").map(|i| i.parse::<usize>().unwrap()).collect())
        .collect();
    (rules, updates)
}

fn is_correct(rules: &Rules, update: &Update) -> bool {
    update.pages.iter().enumerate().all(|(idx, p)| {
        let slice = &update.pages[idx + 1..];
        slice.iter().all(|t| rules.ordered(p, t))
    })
}

fn fix<'a>(rules: &Rules, update: &'a mut Update) -> &'a mut Update {
    let mut swaps: Option<((usize, usize), (usize, usize))> = None;
    'outer: for (idx, p) in update.pages.iter().enumerate() {
        for (jdx, t) in update.pages[idx..].iter().enumerate() {
            let jdx = jdx + idx;
            if !rules.ordered(p, t) {
                swaps = Some(((idx, *p), (jdx, *t)));
                break 'outer;
            }
        }
    }

    if let Some(((idx, p), (jdx, t))) = swaps {
        update.pages[idx] = t;
        update.pages[jdx] = p;
        return fix(rules, update);
    }
    update
}

fn part1(input: &str) -> usize {
    let (rules, updates) = parse(input);

    updates
        .iter()
        .filter(|&update| is_correct(&rules, update))
        .map(|u| u.get_middle())
        .sum()
}

fn part2(input: &str) -> usize {
    let (rules, mut updates) = parse(input);

    updates
        .iter_mut()
        .filter(|u| !is_correct(&rules, u))
        .map(|u| fix(&rules, u))
        .map(|u| u.get_middle())
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47";

    #[test]
    fn test_part1() {
        let answer = part1(INPUT);
        assert_eq!(143, answer);
    }

    #[test]
    fn test_part2() {
        let answer = part2(INPUT);
        assert_eq!(123, answer);
    }
}
