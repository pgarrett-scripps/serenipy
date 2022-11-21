from serenipy.census import from_census

if __name__ == '__main__':
    with open('data\census.txt') as f:
        header_lines, census_lines = from_census(f.read())

    print(census_lines)