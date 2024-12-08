use std::collections::HashSet;
use std::fmt::{self, Debug};
use std::fs;
use std::ops::{Index, IndexMut};

fn main() {
    if let Ok(contents) = fs::read_to_string("./input.txt") {
        let answer = part1(&contents);
        println!("Day 1 Part 1: {answer}");
        let answer = part2(&contents);
        println!("Day 1 Part 2: {answer}");
    }
}

#[derive(Copy, Clone, Debug, PartialEq, Eq)]
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
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Square {
    Empty,
    Wall,
    Player(Direction),
    Visited(Direction),
    Blockage,
}

impl Square {
    fn to_char(&self) -> char {
        match self {
            Self::Empty => '.',
            Self::Wall => '#',
            Self::Player(Direction::Up) => '^',
            Self::Player(Direction::Right) => '>',
            Self::Player(Direction::Down) => 'v',
            Self::Player(Direction::Left) => '<',
            Self::Visited(_) => 'X',
            Self::Blockage => '@',
        }
    }
}

struct Grid {
    g: Vec<Vec<Square>>,
}

impl Index<[usize; 2]> for Grid {
    type Output = Square;
    fn index(&self, [x, y]: [usize; 2]) -> &Self::Output {
        &self.g[y][x]
    }
}

impl IndexMut<[usize; 2]> for Grid {
    fn index_mut(&mut self, [x, y]: [usize; 2]) -> &mut Self::Output {
        &mut self.g[y][x]
    }
}

impl Grid {
    fn height(&self) -> usize {
        self.g.len()
    }

    fn width(&self) -> usize {
        self.g[0].len()
    }

    fn look(&self, dir: Direction, (x, y): (isize, isize)) -> Option<(usize, usize)> {
        let (dx, dy) = dir.delta();
        let mut distance = 0;
        while x + distance * dx >= 0
            && x + distance * dx < self.width() as isize
            && y + distance * dy >= 0
            && y + distance * dy < self.height() as isize
        {
            let coords = ((x + distance * dx) as usize, (y + distance * dy) as usize);
            if let Square::Visited(d) = self[[coords.0, coords.1]] {
                if d == dir {
                    return Some(coords);
                }
            }
            distance += 1;
        }
        None
    }

    fn find(&self, target: Square) -> Option<(isize, isize)> {
        for (i, row) in self.g.iter().enumerate() {
            for (j, &square) in row.iter().enumerate() {
                if square == target {
                    return Some((j as isize, i as isize));
                }
            }
        }
        None
    }

    fn count_all_visited(&self) -> usize {
        self.g
            .iter()
            .flat_map(|rows| rows.iter())
            .filter(|&&s| match s {
                Square::Visited(_) => true,
                _ => false,
            })
            .count()
    }
}

impl Debug for Grid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut sb = String::with_capacity(self.height() * self.width() * 2);
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
    for line in input.lines() {
        let mut row = Vec::new();
        for c in line.chars() {
            if let Some(square) = match c {
                '.' => Some(Square::Empty),
                '#' => Some(Square::Wall),
                '^' => Some(Square::Player(Direction::Up)),
                _ => None,
            } {
                row.push(square);
            }
        }
        rows.push(row);
    }
    Grid { g: rows }
}

fn part1(input: &str) -> usize {
    let mut grid = parse(input);
    if let Some((pix, piy)) = grid.find(Square::Player(Direction::Up)) {
        let mut px = pix;
        let mut py = piy;
        while px >= 0 && py >= 0 && px < grid.width() as isize && py < grid.height() as isize {
            if let Square::Player(d) = grid[[px as usize, py as usize]] {
                let mut direction = d;
                let mut nx = px as isize + direction.delta().0;
                let mut ny = py as isize + direction.delta().1;
                grid[[px as usize, py as usize]] = Square::Visited(direction);
                if nx >= 0 && ny >= 0 && nx < grid.width() as isize && ny < grid.height() as isize {
                    if grid[[nx as usize, ny as usize]] == Square::Wall {
                        direction = match direction {
                            Direction::Up => Direction::Right,
                            Direction::Right => Direction::Down,
                            Direction::Down => Direction::Left,
                            Direction::Left => Direction::Up,
                        }
                    }
                    nx = px as isize + direction.delta().0;
                    ny = py as isize + direction.delta().1;
                    grid[[nx as usize, ny as usize]] = Square::Player(direction);
                }
                px = nx;
                py = ny;
            }
        }
    }
    grid.count_all_visited()
}

fn part2(input: &str) -> usize {
    let mut grid = parse(input);
    let mut blockages: HashSet<(usize, usize)> = HashSet::new();
    if let Some((pix, piy)) = grid.find(Square::Player(Direction::Up)) {
        let mut px = pix;
        let mut py = piy;
        while px >= 0 && py >= 0 && px < grid.width() as isize && py < grid.height() as isize {
            if let Square::Player(facing) = grid[[px as usize, py as usize]] {
                let mut direction = facing;
                let mut nx = px as isize + direction.delta().0;
                let mut ny = py as isize + direction.delta().1;
                grid[[px as usize, py as usize]] = Square::Visited(facing);
                if nx >= 0 && ny >= 0 && nx < grid.width() as isize && ny < grid.height() as isize {
                    let righthand = match direction {
                        Direction::Up => Direction::Right,
                        Direction::Right => Direction::Down,
                        Direction::Down => Direction::Left,
                        Direction::Left => Direction::Up,
                    };
                    if grid[[nx as usize, ny as usize]] == Square::Wall {
                        direction = righthand;
                    } else if let Some(_) = grid.look(righthand, (px, py)) {
                        blockages.insert((nx as usize, ny as usize));
                    }
                    nx = px as isize + direction.delta().0;
                    ny = py as isize + direction.delta().1;
                    grid[[nx as usize, ny as usize]] = Square::Player(direction);
                }
                px = nx;
                py = ny;
            }
        }
    }

    for (x, y) in blockages.iter() {
        grid[[*x, *y]] = Square::Blockage;
    }
    println!("{:?}", grid);
    blockages.len()
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
        assert_eq!(7, answer);
    }
}
