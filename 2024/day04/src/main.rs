use std::fmt::{self, Debug};
use std::fs;
use std::ops::Index;

fn main() {
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        let answer = part1(&contents);
        println!("Day 1 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 1 Part 2: {answer}");
    }
}

#[derive(Copy, Clone, Debug)]
enum Direction {
    Up,
    UpRight,
    Right,
    DownRight,
    Down,
    DownLeft,
    Left,
    UpLeft,
}

impl Direction {
    pub const fn all() -> [Self; 8] {
        [
            Self::Up,
            Self::UpRight,
            Self::Right,
            Self::DownRight,
            Self::Down,
            Self::DownLeft,
            Self::Left,
            Self::UpLeft,
        ]
    }

    pub const fn delta(&self) -> (isize, isize) {
        match self {
            Self::Up => (0, -1),
            Self::UpRight => (1, -1),
            Self::Right => (1, 0),
            Self::DownRight => (1, 1),
            Self::Down => (0, 1),
            Self::DownLeft => (-1, 1),
            Self::Left => (-1, 0),
            Self::UpLeft => (-1, -1),
        }
    }
}

struct Grid {
    g: Vec<Vec<char>>,
}

impl Debug for Grid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut sb = String::with_capacity(self.height() * self.width() * 2);
        for i in &self.g {
            for j in i {
                sb.push(*j);
            }
            sb.push('\n');
        }
        write!(f, "{}", sb)
    }
}

impl Index<[usize; 2]> for Grid {
    type Output = char;
    fn index(&self, [x, y]: [usize; 2]) -> &Self::Output {
        &self.g[y][x]
    }
}

impl Grid {
    fn height(&self) -> usize {
        self.g.len()
    }

    fn width(&self) -> usize {
        self.g[0].len()
    }

    fn look(&self, dir: Direction, (x, y): (isize, isize), dist: isize) -> Option<String> {
        let (dx, dy) = dir.delta();
        if x + (dist - 1) * dx >= 0
            && x + (dist - 1) * dx < self.width() as isize
            && y + (dist - 1) * dy >= 0
            && y + (dist - 1) * dy < self.height() as isize
        {
            let mut sb = String::with_capacity(dist as usize);
            for i in 0..dist {
                let ux = (x + i * dx) as usize;
                let uy = (y + i * dy) as usize;
                sb.push(self[[ux, uy]]);
            }
            Some(sb)
        } else {
            None
        }
    }
}

fn parse(input: &str) -> Grid {
    Grid {
        g: input.lines().map(|l| l.trim().chars().collect()).collect(),
    }
}

fn part1(input: &str) -> usize {
    let grid: Grid = parse(input);
    let mut xs = vec![];

    for i in 0..grid.width() {
        for j in 0..grid.height() {
            if grid[[i, j]] == 'X' {
                xs.push((i as isize, j as isize));
            }
        }
    }

    let mut hits = 0;
    for x in xs {
        for dir in Direction::all() {
            if let Some(candidate) = grid.look(dir, x, 4) {
                if candidate == "XMAS" {
                    hits += 1
                }
            }
        }
    }
    hits
}

fn part2(input: &str) -> usize {
    let grid: Grid = parse(input);
    let mut aa = vec![];

    for i in 0..grid.width() {
        for j in 0..grid.height() {
            if grid[[i, j]] == 'A' {
                aa.push((i as isize, j as isize))
            }
        }
    }

    let mut hits = 0;
    for a in aa {
        if let (Some(ur), Some(ul), Some(dr), Some(dl)) = (
            grid.look(Direction::UpRight, a, 2),
            grid.look(Direction::UpLeft, a, 2),
            grid.look(Direction::DownRight, a, 2),
            grid.look(Direction::DownLeft, a, 2),
        ) {
            if (ur == "AM" && ul == "AM" && dr == "AS" && dl == "AS")
                || (ur == "AM" && ul == "AS" && dr == "AM" && dl == "AS")
                || (ur == "AS" && ul == "AS" && dr == "AM" && dl == "AM")
                || (ur == "AS" && ul == "AM" && dr == "AS" && dl == "AM")
            {
                hits += 1;
            }
        }
    }
    hits
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX";

    #[test]
    fn test_part1() {
        let answer = part1(INPUT);
        assert_eq!(18, answer);
    }

    #[test]
    fn test_part2() {
        let answer = part2(INPUT);
        assert_eq!(9, answer);
    }
}
