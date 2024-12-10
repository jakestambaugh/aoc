use std::collections::HashSet;
use std::fmt::{self, Debug};
use std::fs;
use std::ops::{Add, AddAssign, Index, IndexMut};

use itertools::Itertools;
use rayon::iter::{ParallelBridge, ParallelIterator};

fn main() {
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        let answer = part1(&contents);
        println!("Day 1 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 1 Part 2: {answer}");
    }
}

#[derive(Copy, Clone, Debug, PartialEq, Eq, Hash)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
}

impl Direction {
    pub const fn delta(&self) -> (isize, isize) {
        match self {
            Self::Up => (0, -1),
            Self::Right => (1, 0),
            Self::Down => (0, 1),
            Self::Left => (-1, 0),
        }
    }

    fn turn(&self) -> Self {
        match self {
            Self::Up => Self::Right,
            Self::Right => Self::Down,
            Self::Down => Self::Left,
            Self::Left => Self::Up,
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Square {
    Empty,
    Wall,
    Player,
}

impl Square {
    fn to_char(&self) -> char {
        match self {
            Self::Empty => '.',
            Self::Wall => '#',
            Self::Player => '^',
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

impl Add<Direction> for Point {
    type Output = Self;

    fn add(self, rhs: Direction) -> Self::Output {
        let (dx, dy) = rhs.delta();
        Point::new(self.x + dx, self.y + dy)
    }
}

impl AddAssign<Direction> for Point {
    fn add_assign(&mut self, rhs: Direction) {
        *self = *self + rhs;
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
            if let Some(square) = match c {
                '.' => Some(Square::Empty),
                '#' => Some(Square::Wall),
                '^' => Some(Square::Player),
                _ => None,
            } {
                row.push(square);
            }
        }
        rows.push(row);
    }
    Grid { g: rows }
}

fn find_player(grid: &Grid) -> Option<Point> {
    for j in 0..grid.height() {
        for i in 0..grid.width() {
            let point = Point::new(i, j);
            if grid[point] == Square::Player {
                return Some(point);
            }
        }
    }
    None
}

fn part1(input: &str) -> usize {
    let grid = parse(input);
    let mut curr: Point = find_player(&grid).unwrap();
    let mut direction = Direction::Up;
    let mut visited: HashSet<Point> = HashSet::new();
    while grid.within_bounds(&curr) {
        visited.insert(curr);
        let next = curr + direction;
        if grid.within_bounds(&next) {
            if grid[next] == Square::Wall {
                direction = direction.turn();
            }
            curr = curr + direction;
        } else {
            break;
        }
    }
    visited.len()
}

fn part2(input: &str) -> usize {
    let grid = parse(input);
    let start_point: Point = find_player(&grid).unwrap();
    (0..grid.width())
        .cartesian_product(0..grid.height())
        .par_bridge()
        .flat_map(|(i, j)| {
            let p = Point::new(i, j);
            let mut new_grid = grid.clone();
            if new_grid[p] == Square::Player || new_grid[p] == Square::Wall {
                return None;
            }
            new_grid[p] = Square::Wall;
            let mut curr = start_point;
            let mut direction = Direction::Up;
            let mut visited: HashSet<(Point, Direction)> = HashSet::new();
            while new_grid.within_bounds(&curr) {
                visited.insert((curr, direction));
                let mut next = curr + direction;
                if new_grid.within_bounds(&next) {
                    while new_grid[next] == Square::Wall {
                        direction = direction.turn();
                        next = curr + direction;
                    }
                    if visited.contains(&(next, direction)) {
                        return Some(curr);
                    }
                    curr = curr + direction;
                } else {
                    break;
                }
            }
            None
        })
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...";

    #[test]
    fn test_part1() {
        let answer = part1(INPUT);
        assert_eq!(41, answer);
    }

    #[test]
    fn test_part2() {
        let answer = part2(INPUT);
        assert_eq!(6, answer);
    }
}
