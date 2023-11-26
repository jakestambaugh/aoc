#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int basementCount(const char* buffer, int floor, int character) {
    int i = 0;
    while (buffer[i] != '\0') {
        if (buffer[i] == '(') {
            floor += 1;
        } else if (buffer[i] == ')') {
            floor -= 1;
        }
        if (floor == -1) {
            printf("Entered basement at character %d\n", (character + i));
            return -1;
        }
        i++;
    }
    return floor;
}

int floorCount(const char* buffer, int floor) {
    int i = 0;
    while (buffer[i] != '\0') {
        if (buffer[i] == '(') {
            floor += 1;
        } else if (buffer[i] == ')') {
            floor -= 1;
        }
        i = i + 1;
        printf("i == %d\n", i);
    }
    if (i != 1023) {
        printf("i is %d instead of 1024\n", i);
    }
    return floor;
}

int main() {
    FILE* file;
    file = fopen("input.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
    
    fseek(file, 0, SEEK_END);
    int file_size = ftell(file);
    rewind(file);

    char buffer[1024];
    memset(buffer, 0, sizeof(buffer));
    size_t bytesRead = 0;
    size_t totalBytesRead = 0;
    int floor = 0;
    int character = 1;
    while ((bytesRead = fread(buffer, 1, 1023, file)) > 0) {
        totalBytesRead += bytesRead;
        buffer[bytesRead] = '\0';
        floor = basementCount(buffer, floor, character);  
        if (floor == -1) {
            break;
        }
        character = character + bytesRead;
    }

    printf("Floor number %d\n", floor);

    fclose(file);
    return 0;
}
