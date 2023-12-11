#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>

void part1(char *filename)
{
  printf("Part 1: %s\n", filename);
}

void part2(char *filename)
{
  printf("Part 2: %s\n", filename);
}

int main(int argc, char *argv[])
{
  int part = 1;
  char *filename = "input.txt";

  int opt;
  int indexptr;
  struct option longopts[] = {
      {"part", required_argument, NULL, 'p'},
      {"test", no_argument, NULL, 't'},
      {NULL, 0, NULL, 0}};
  while ((opt = getopt_long(argc, argv, "p:t:", longopts, &indexptr)) != -1)
  {
    // printf("opt: %c\n", (char)opt);
    switch (opt)
    {
    case 'p':
      // printf("Option p with argument %s\n", optarg);
      // printf("part: %d\n", part);
      part = atoi(optarg);
      break;
    case 't':
      // printf("Option t with argument %s\n", optarg);
      filename = "test.txt";
      break;
    default:
      fprintf(stderr, "Usage: %s [--part arg] [--test]\n", argv[0]);
      return 1;
    }
  }
  // printf("Filename: %s\n", filename);

  if (part == 1)
  {
    // printf("Part 1\n");
    part1(filename);
  }
  else if (part == 2)
  {
    // printf("Part 2\n");
    part2(filename);
  }
  else
  {
    fprintf(stderr, "Invalid part: %d\n", part);
    return 1;
  }

  return 0;
}
