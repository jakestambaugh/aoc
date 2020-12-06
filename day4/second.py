import re


def extract_fields(passport):
    passport = passport.replace("\n", " ")
    passport = passport.strip()
    pairs = passport.split(" ")
    kvp = {}
    for pair in pairs:
        assert(len(pair.split(":")) == 2)
        k = pair.split(":")[0]
        v = pair.split(":")[1]
        kvp[k] = v
    return kvp


def height_valid(height):
    pattern = re.compile("^([0-9]+)(cm|in)$")
    matches = pattern.match(height)
    if matches:
        n = int(matches.group(1))
        unit = matches.group(2)
        if unit == "cm":
            return (n >= 150 and n <= 193)
        elif unit == "in":
            return (n >= 59 and n <= 76)
        else:
            return False


def hair_valid(hair):
    pattern = re.compile("^#[0-9a-f]{6}$")
    m = pattern.match(hair)
    return bool(pattern.match(hair))


def passid_valid(pass_id):
    pattern = re.compile("^[0-9]{9}$")
    return bool(pattern.match(pass_id))


def all_fields_valid(f):
    valid = {}
    valid["byr"] = (int(f["byr"]) >= 1920 and int(f["byr"]) <= 2002)
    valid["iyr"] = (int(f["iyr"]) >= 2010 and int(f["iyr"]) <= 2020)
    valid["eyr"] = (int(f["eyr"]) >= 2020 and int(f["eyr"]) <= 2030)
    valid["hgt"] = height_valid(f["hgt"])
    valid["hcl"] = hair_valid(f["hcl"])
    valid["ecl"] = (f["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    valid["pid"] = passid_valid(f["pid"])
    valid["cid"] = True
    return valid


def is_valid(passport):
    fields = extract_fields(passport)
    expected = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    if not expected.difference(fields.keys()):
        valid = all_fields_valid(fields)
        for k, v in valid.items():
            if not v:
                return False
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
