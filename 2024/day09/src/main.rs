use std::fs;

use itertools::Itertools;

fn main() {
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        let answer = part1(&contents);
        println!("Day 9 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 9 Part 2: {answer}");
    }
}

fn expand(compressed: &str) -> (Vec<Option<usize>>, Vec<(usize, usize)>) {
    let mut slots: Vec<(usize, usize)> = Vec::new();
    let mut output = Vec::new();
    compressed
        .chars()
        .chunks(2)
        .into_iter()
        .enumerate()
        .for_each(|(i, mut chunk)| {
            if let Some(c) = chunk.next() {
                let count = c.to_digit(10).unwrap();
                for _ in 0..count {
                    output.push(Some(i));
                }
            }
            if let Some(c) = chunk.next() {
                let count: usize = c.to_digit(10).unwrap().try_into().unwrap();
                let start = output.len();
                for _ in 0..count {
                    output.push(None);
                }
                slots.push((start, count));
            }
        });
    (output, slots)
}

fn frag(expanded: Vec<Option<usize>>) -> Vec<Option<usize>> {
    let mut output: Vec<Option<usize>> = expanded.clone();
    let mut front: usize = 0;
    let mut back: usize = output.len() - 1;
    while front < back {
        while output[back].is_none() {
            back -= 1;
        }
        while output[front].is_some() {
            front += 1;
        }
        if front < back {
            output[front] = output[back];
            output[back] = None;
            front += 1;
            back -= 1;
        }
    }
    output
}

fn checksum(filesystem: Vec<Option<usize>>) -> usize {
    filesystem
        .iter()
        .enumerate()
        .filter(|&(_, c)| c.is_some())
        .map(|(i, c)| i * c.unwrap())
        .sum()
}

fn defrag(expanded: Vec<Option<usize>>, mut slots: Vec<(usize, usize)>) -> Vec<Option<usize>> {
    let mut output = expanded.clone();
    let mut back = output.len() - 1;
    while back > 0 {
        while output[back].is_none() {
            back -= 1;
        }
        let target = output[back];
        let mut chunk_size = 0;
        while target == output[back] && back > 0 {
            back -= 1;
            chunk_size += 1;
        }
        let replacement_start = back + 1;
        for i in 0..slots.len() {
            let (start, size) = slots[i];
            if chunk_size <= size && start < replacement_start {
                println!(
                    "Swapping {} from {} into {}",
                    target.unwrap(),
                    replacement_start,
                    start
                );
                for j in 0..chunk_size {
                    output[start + j] = target;
                    output[replacement_start + j] = None;
                }
                let delta = size - chunk_size;
                slots.remove(i);
                if delta > 0 {
                    let new = (start + chunk_size, delta);
                    slots.insert(i, new);
                }
                break;
            }
        }
    }
    output
}

fn part1(input: &str) -> usize {
    let (expanded, _) = expand(input);
    checksum(frag(expanded))
}

fn part2(input: &str) -> usize {
    let (expanded, slots) = expand(input);
    println!("{:?}", slots);
    checksum(defrag(expanded, slots))
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "2333133121414131402";

    #[test]
    fn test_part1() {
        let answer = part1(INPUT);
        assert_eq!(1928, answer);
    }

    #[test]
    fn test_part2() {
        let answer = part2(INPUT);
        assert_eq!(2858, answer);
    }
}
