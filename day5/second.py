bitfield = [pow(2, n) for n in range(6, -1, -1)]
seatfield = bitfield[-3:]


def seat_id(encoded):
    row = encoded[:7]
    seat = encoded[7:10]
    row_num = 0
    seat_num = 0
    for i, letter in enumerate(row):
        if letter == 'B':
            row_num += bitfield[i]
    for j, letter in enumerate(seat):
        if letter == 'R':
            seat_num += seatfield[j]
    return row_num * 8 + seat_num

def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.readlines()
        seat_ids = [seat_id(line) for line in content]
        seat_ids.sort()
        for x in range(len(seat_ids) - 1):
            if not seat_ids[x] + 1 == seat_ids[x + 1]:
                missing_seat = seat_ids[x] + 1
                print("Your seat is {}".format(missing_seat))

if __name__ == "__main__":
    main()
