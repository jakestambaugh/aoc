use std::fs;

fn main() {
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        let answer = part1(&contents);
        println!("Day 10 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 10 Part 2: {answer}");
    }
}

struct TopographicMap {
    rows: Vec<Vec<u8>>,
}

type Visited = Vec<Vec<bool>>;

impl TopographicMap {
    fn trailheads(&self) -> Vec<(usize, usize)> {
        self.rows
            .iter()
            .enumerate()
            .flat_map(|(i, row)| {
                row.iter()
                    .enumerate()
                    .filter(|(_, &elevation)| elevation == 0)
                    .map(move |(j, _)| (i, j))
            })
            .collect()
    }

    fn find_peaks(&self, y: usize, x: usize) -> usize {
        let mut visited: Visited = self.rows.iter().map(|row| vec![false; row.len()]).collect();
        self.find_peaks_recursive(y, x, &mut visited)
    }

    fn find_peaks_recursive(&self, y: usize, x: usize, visited: &mut Visited) -> usize {
        if visited[y][x] {
            0
        } else {
            visited[y][x] = true;
            let value = self.rows[y][x];
            if value == 9 {
                1
            } else {
                let mut paths = 0;
                if y > 0 && self.rows[y - 1][x] == value + 1 {
                    paths += self.find_peaks_recursive(y - 1, x, visited);
                }
                if y < self.rows.len() - 1 && self.rows[y + 1][x] == value + 1 {
                    paths += self.find_peaks_recursive(y + 1, x, visited);
                }
                if x > 0 && self.rows[y][x - 1] == value + 1 {
                    paths += self.find_peaks_recursive(y, x - 1, visited);
                }
                if x < self.rows[0].len() - 1 && self.rows[y][x + 1] == value + 1 {
                    paths += self.find_peaks_recursive(y, x + 1, visited);
                }
                paths
            }
        }
    }

    fn find_ratings(&self, y: usize, x: usize) -> usize {
        self.find_ratings_recursive(y, x)
    }

    fn find_ratings_recursive(&self, y: usize, x: usize) -> usize {
        let value = self.rows[y][x];
        if value == 9 {
            1
        } else {
            let mut paths = 0;
            if y > 0 && self.rows[y - 1][x] == value + 1 {
                paths += self.find_ratings_recursive(y - 1, x);
            }
            if y < self.rows.len() - 1 && self.rows[y + 1][x] == value + 1 {
                paths += self.find_ratings_recursive(y + 1, x);
            }
            if x > 0 && self.rows[y][x - 1] == value + 1 {
                paths += self.find_ratings_recursive(y, x - 1);
            }
            if x < self.rows[0].len() - 1 && self.rows[y][x + 1] == value + 1 {
                paths += self.find_ratings_recursive(y, x + 1);
            }
            paths
        }
    }
}

fn parse(input: &str) -> TopographicMap {
    TopographicMap {
        rows: input
            .lines()
            .map(|line| {
                line.chars()
                    .map(|c| c.to_digit(10).unwrap() as u8)
                    .collect()
            })
            .collect(),
    }
}

fn part1(input: &str) -> usize {
    let map = parse(input);
    let trailheads = map.trailheads();
    trailheads
        .into_iter()
        .map(|(y, x)| map.find_peaks(y, x))
        .sum()
}

fn part2(input: &str) -> usize {
    let map = parse(input);
    let trailheads = map.trailheads();
    trailheads
        .into_iter()
        .map(|(y, x)| map.find_ratings(y, x))
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    const SMALL: &str = "0123
1234
8765
9876";

    const LARGE: &str = "89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732";

    #[test]
    fn test_part1_small() {
        let answer = part1(SMALL);
        assert_eq!(1, answer);
    }

    #[test]
    fn test_part1_large() {
        let answer = part1(LARGE);
        assert_eq!(36, answer);
    }

    #[test]
    fn test_part2_large() {
        let answer = part2(LARGE);
        assert_eq!(81, answer);
    }
}
