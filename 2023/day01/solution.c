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

  // Null-terminate the array
  lines[line_index] = NULL;

  return lines;
}

static char *[] num_chars = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"};

void part1(char *filename)
{
  printf("Part 1: %s\n", filename);
  char *buffer = read_file_into_memory(filename);
  size_t num_lines;
  char **lines = split_string_into_lines(buffer, &num_lines);
  for (size_t i = 0; i < num_lines; i++)
  {
    printf("%s\n", lines[i]);
  }
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
