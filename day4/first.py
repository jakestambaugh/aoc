def extract_fields(passport):
    passport = passport.replace("\n", " ")
    passport = passport.strip()
    pairs = passport.split(" ")
    print(pairs)
    kvp = {}
    for pair in pairs:
        assert(len(pair.split(":")) == 2)
        k = pair.split(":")[0]
        v = pair.split(":")[1]
        kvp[k] = v
    return kvp


def is_valid(passport):
    fields = extract_fields(passport)
    expected = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    if not expected.difference(fields.keys()):
        return True
    else:
        return False


def main():
    pathname = "input.txt"
    with open(pathname) as f:
        content = f.read()
        passports = content.split("\n\n")
        valid = 0
        for passport in passports:
            if is_valid(passport):
                valid += 1
        print("{} valid passports".format(valid))

if __name__ == "__main__":
    main()
