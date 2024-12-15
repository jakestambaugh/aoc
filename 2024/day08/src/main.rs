use itertools::Itertools;
use std::{
    collections::HashSet,
    fmt::{self, Debug},
    fs,
    iter::Iterator,
    ops::{Index, IndexMut},
};

fn main() {
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        let answer = part1(&contents);
        println!("Day 1 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 1 Part 2: {answer}");
    }
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Square {
    Empty,
    Station(char),
}

impl Square {
    fn to_char(&self) -> char {
        match self {
            Self::Empty => '.',
            Self::Station(c) => *c,
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
struct Point {
    x: isize,
    y: isize,
}

impl Point {
    fn new(x: isize, y: isize) -> Self {
        Self { x, y }
    }
}

#[derive(Clone)]
struct Grid {
    g: Vec<Vec<Square>>,
}

impl Index<Point> for Grid {
    type Output = Square;
    fn index(&self, Point { x, y }: Point) -> &Self::Output {
        &self.g[y as usize][x as usize]
    }
}

impl IndexMut<Point> for Grid {
    fn index_mut(&mut self, Point { x, y }: Point) -> &mut Self::Output {
        &mut self.g[y as usize][x as usize]
    }
}

impl Grid {
    fn height(&self) -> isize {
        self.g.len() as isize
    }

    fn width(&self) -> isize {
        self.g[0].len() as isize
    }

    fn within_bounds(&self, &Point { x, y }: &Point) -> bool {
        x >= 0 && y >= 0 && x < self.width() && y < self.height()
    }

    fn frequencies(&self) -> HashSet<char> {
        let mut freqs: HashSet<char> = HashSet::new();
        for point in self {
            if let Square::Station(c) = self[point] {
                freqs.insert(c);
            }
        }
        freqs
    }

    fn single_frequency_grid(&self, frequency: char) -> Self {
        let mut grid = self.clone();
        for point in self {
            if let Square::Station(c) = self[point] {
                if c != frequency {
                    grid[point] = Square::Empty;
                }
            };
        }
        grid
    }

    fn antinode_points(&self, frequency: char) -> HashSet<Point> {
        self.into_iter()
            .filter(|point| self[*point] == Square::Station(frequency))
            .combinations(2)
            .map(|pair| antinodes(self, pair[0], pair[1]))
            .flatten()
            .collect()
    }

    fn resonant_antinode_points(&self, frequency: char) -> HashSet<Point> {
        self.into_iter()
            .filter(|point| self[*point] == Square::Station(frequency))
            .combinations(2)
            .map(|pair| resonant_antinodes(self, pair[0], pair[1]))
            .flatten()
            .collect()
    }
}

fn antinodes(grid: &Grid, a: Point, b: Point) -> Vec<Point> {
    let delta_x = a.x - b.x;
    let delta_y = a.y - b.y;
    vec![
        Point::new(a.x + delta_x, a.y + delta_y),
        Point::new(b.x - delta_x, b.y - delta_y),
    ]
    .into_iter()
    .filter(|p| grid.within_bounds(p))
    .collect()
}

fn resonant_antinodes(grid: &Grid, a: Point, b: Point) -> Vec<Point> {
    let delta_x = a.x - b.x;
    let delta_y = a.y - b.y;
    let mut nodes: Vec<Point> = vec![];
    // Look up
    let mut curr = a;
    while grid.within_bounds(&curr) {
        nodes.push(curr);
        curr = Point::new(curr.x + delta_x, curr.y + delta_y);
    }
    // Look down
    curr = b;
    while grid.within_bounds(&curr) {
        nodes.push(curr);
        curr = Point::new(curr.x - delta_x, curr.y - delta_y);
    }
    nodes
}

struct GridIterator {
    currx: usize,
    curry: usize,
    width: usize,
    height: usize,
}

impl Iterator for GridIterator {
    type Item = Point;

    fn next(&mut self) -> Option<Self::Item> {
        let x = self.currx;
        let y = self.curry;

        if self.currx < self.width {
            if self.curry < self.height - 1 {
                self.curry += 1
            } else {
                self.curry = 0;
                self.currx += 1;
            }
        } else {
            return None;
        }

        Some(Point::new(x as isize, y as isize))
    }
}

impl IntoIterator for &Grid {
    type Item = Point;
    type IntoIter = GridIterator;

    fn into_iter(self) -> Self::IntoIter {
        GridIterator {
            currx: 0,
            curry: 0,
            width: self.width() as usize,
            height: self.height() as usize,
        }
    }
}

impl Debug for Grid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut sb = String::new();
        for i in &self.g {
            for j in i {
                sb.push(j.to_char());
            }
            sb.push('\n');
        }
        write!(f, "{}", sb)
    }
}

fn parse(input: &str) -> Grid {
    let mut rows = Vec::new();
    for line in input.lines().map(|l| l.trim()) {
        let mut row = Vec::new();
        for c in line.chars() {
            let square = match c {
                '.' => Square::Empty,
                c => Square::Station(c),
            };
            row.push(square);
        }
        rows.push(row);
    }
    Grid { g: rows }
}

fn part1(input: &str) -> usize {
    let grid = parse(input);
    let antinodes: HashSet<Point> = grid
        .frequencies()
        .into_iter()
        .map(|f| (f, grid.single_frequency_grid(f)))
        .flat_map(|(f, fgrid)| fgrid.antinode_points(f))
        .collect();
    antinodes.len()
}

fn part2(input: &str) -> usize {
    let grid = parse(input);
    let antinodes: HashSet<Point> = grid
        .frequencies()
        .into_iter()
        .map(|f| (f, grid.single_frequency_grid(f)))
        .flat_map(|(f, fgrid)| fgrid.resonant_antinode_points(f))
        .collect();
    antinodes.len()
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............";

    #[test]
    fn test_part1() {
        let answer = part1(INPUT);
        assert_eq!(14, answer);
    }

    #[test]
    fn test_part2() {
        let answer = part2(INPUT);
        assert_eq!(34, answer);
    }
}
