#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>
#include <string.h>

/**
 * Read the content of a file into a buffer.
 *
 * This function dynamically allocates memory for the buffer.
 * Remember to free it.
 */
char *read_file_into_memory(const char *filename)
{
  FILE *file = fopen(filename, "r");
  if (file == NULL)
  {
    printf("Failed to open file %s\n", filename);
    return NULL;
  }

  // Get the file size
  fseek(file, 0, SEEK_END);
  long file_size = ftell(file);
  rewind(file);

  // Allocate memory for the file content
  char *buffer = (char *)malloc(file_size + 1);
  if (buffer == NULL)
  {
    printf("Failed to allocate memory\n");
    fclose(file);
    return NULL;
  }

  // Read the file into the buffer
  size_t result = fread(buffer, 1, file_size, file);
  if (result != file_size)
  {
    printf("Failed to read file\n");
    free(buffer);
    fclose(file);
    return NULL;
  }

  // Null-terminate the buffer
  buffer[file_size] = '\0';

  fclose(file);
  return buffer;
}

// Size is an out pointer
char **split_string_into_lines(char *buffer, size_t *num_lines)
{
  // Count the number of lines in the string
  size_t lines_alloc = 1;
  for (char *c = buffer; *c != '\0'; c++)
  {
    if (*c == '\n')
    {
      lines_alloc++;
    }
  }
  *num_lines = lines_alloc;

  // Allocate memory for the line pointers
  char **lines = malloc(lines_alloc * sizeof(char *));
  if (lines == NULL)
  {
    printf("Failed to allocate memory\n");
    return NULL;
  }

  // Split the string into lines
  size_t line_index = 0;
  char *line = strtok(buffer, "\n");
  while (line != NULL)
  {
    lines[line_index++] = line;
    line = strtok(NULL, "\n");
  }

  return lines;
}

static char num_chars[] = {'1', '2', '3', '4', '5', '6', '7', '8', '9'};
static char *num_words[] = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};

typedef struct pair
{
  int first;
  int last;
} pair_t;

pair_t find_first_and_last(char *line)
{
  pair_t pair;
  pair.first = -1;
  pair.last = -1;
  for (int i = 0; i < strlen(line); i++)
  {
    for (int j = 0; j < 9; j++)
    {
      if (line[i] == num_chars[j])
      {
        pair.first = j + 1;
        goto found_first;
      }
    }
  }
found_first:

  for (int m = strlen(line) - 1; m >= 0; m--)
  {
    for (int n = 0; n < 9; n++)
    {
      if (line[m] == num_chars[n])
      {
        pair.last = n + 1;
        goto found_last;
      }
    }
  }
found_last:

  return pair;
}

pair_t find_first_and_last_with_replacement(char *line, int line_index)
{
  char *new_line = (char *)malloc((strlen(line) + 1) * sizeof(char));
  if (new_line == NULL)
  {
    printf("Failed to allocate memory\n");
    exit(1);
  }

  size_t index = 0;
  while (index < strlen(line))
  {
    int found = 0;
    for (int i = 0; i < 9; i++)
    {
      if (strncmp(line + index, num_words[i], strlen(num_words[i])) == 0)
      {
        new_line[index] = num_chars[i];
        found = 1;
      }
    }
    if (!found)
    {
      new_line[index] = line[index];
    }
    index++;
  }
  new_line[index] = '\0';

  pair_t pair = find_first_and_last(new_line);
  free(new_line);
  return pair;
}

void part1(char *filename)
{
  char *buffer = read_file_into_memory(filename);
  size_t num_lines;
  char **lines = split_string_into_lines(buffer, &num_lines);
  int sum = 0;
  for (size_t i = 0; i < num_lines; i++)
  {
    pair_t pair = find_first_and_last(lines[i]);
    sum += (pair.first * 10) + pair.last;
  }
  free(buffer);
  free(lines);
  printf("Part 1: %d\n", sum);
}

void part2(char *filename)
{
  char *buffer = read_file_into_memory(filename);
  size_t num_lines;
  char **lines = split_string_into_lines(buffer, &num_lines);
  int sum = 0;

  for (size_t i = 0; i < num_lines; i++)
  {
    pair_t pair = find_first_and_last_with_replacement(lines[i], i);
    sum += (pair.first * 10) + pair.last;
  }
  free(buffer);
  free(lines);
  printf("Part 2: %d\n", sum);
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
  while ((opt = getopt_long(argc, argv, "p:t", longopts, &indexptr)) != -1)
  {
    switch (opt)
    {
    case 'p':
      part = atoi(optarg);
      break;
    case 't':
      filename = "test.txt";
      break;
    default:
      fprintf(stderr, "Usage: %s [--part arg] [--test]\n", argv[0]);
      return 1;
    }
  }

  if (part == 1)
  {
    part1(filename);
  }
  else if (part == 2)
  {
    part2(filename);
  }
  else
  {
    fprintf(stderr, "Invalid part: %d\n", part);
    return 1;
  }

  return 0;
}
