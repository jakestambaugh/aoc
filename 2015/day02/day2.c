#include <stdio.h>
#include <string.h>

int minOf(front, side, top) {
    int smaller;
    smaller = front < side ? front : side;
    return smaller < top ? smaller : top;
}

int totalArea(int h, int w, int l) {
    int front = h*w;
    int side = h*l;
    int top = l*w;
    return 2*front + 2*side + 2*top + minOf(front, side, top) ;
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

    char buffer[128];
    memset(buffer, 0, sizeof(buffer));
    while (fgets(buffer, sizeof(buffer) - 1, file)) {
        int x;
        int y;
        int z;
        sscanf(buffer, "%dx%dx%d", &x, &y, &z);
        printf("Area of %dx%dx%d is %d\n", x, y, z, totalArea(x, y, z));
    }

    fclose(file);
    return 0;
}