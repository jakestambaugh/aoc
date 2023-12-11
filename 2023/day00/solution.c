#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <getopt.h>
#include <string.h>

typedef struct
{
  size_t *data;
  size_t *tail;
  long size;
  long capacity;
} vector;

vector *vector_new()
{
  vector *v = (vector *)malloc(sizeof(vector));

  // Start with 16 elements by default
  long starting_capacity = 16;
  char *data = (char *)malloc(sizeof(size_t) * starting_capacity);
  if (data == NULL || v == NULL)
  {
    printf("Failed to allocate memory for vector\n");
    return NULL;
  }

  v->data = data;
  v->tail = v->data;

  v->size = 0;
  v->capacity = starting_capacity;
  return v;
}

void vector_free(vector *v)
{
  free(v->data);
  free(v);
}

vector *vector_resize(vector *v)
{
  // always double
  long new_capacity = v->capacity * 2;
  size_t *new_buffer = (size_t *)realloc((void *)v->data, new_capacity);
  if (new_buffer == NULL)
  {
    fprintf(stderr, "Failed to reallocated memory for vector expansion\n");
    return NULL;
  }
  v->data = new_buffer;
  v->tail = v->data + (size_t)(sizeof(size_t) * v->size);
  v->capacity = new_capacity;
}

void vector_push(vector *v, char value)
{
  if (v->size + 1 >= v->capacity)
  {
    vector *new = vector_resize(v);
    if (new == NULL)
    {
      fprintf(stderr, "Failed to push element to vector\n");
      return;
    }
  }
}

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

vector *split_lines(char *buffer)
{
  vector *v = vector_new();
  char *current = buffer;
  size_t while (*current != '\0')
  {
    if (*current == '\n')
    {
      *current = '\0';
    }
    current++;
  }
  return buffer;
}

void part1(char *filename)
{
  printf("Part 1: %s\n", filename);
  char *buffer = read_file_into_memory(filename);
  char *lines = split_lines(buffer);
  while (*lines != '\0')
  {
    printf("%s\n", lines);
    lines += strlen(lines) + 1;
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
