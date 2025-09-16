import time

records = []
cities = {}
years = {}
data_grid = []
missing_val = -999

def add_record(d, c, t):
    new_rec = {}
    new_rec['date'] = d
    new_rec['city'] = c  
    new_rec['temp'] = t
    records.append(new_rec)
    
    yr = int(d.split('/')[2])
    
    if c not in cities:
        cities[c] = len(cities)
    if yr not in years:
        years[yr] = len(years)
    
    put_in_grid(yr, c, t)

def put_in_grid(yr, c, temp):
    y_pos = years[yr]
    c_pos = cities[c]
    
    while len(data_grid) <= y_pos:
        data_grid.append([])
    
    while len(data_grid[y_pos]) <= c_pos:
        data_grid[y_pos].append(missing_val)
    
    data_grid[y_pos][c_pos] = temp

def remove_record(city, date):
    found = False
    i = 0
    while i < len(records):
        if records[i]['city'] == city and records[i]['date'] == date:
            records.pop(i)
            found = True
            break
        i += 1
    
    if found:
        yr = int(date.split('/')[2])
        if yr in years and city in cities:
            y_pos = years[yr]
            c_pos = cities[city]
            data_grid[y_pos][c_pos] = missing_val
    
    return found

def get_data(city, year):
    result = []
    for rec in records:
        rec_year = int(rec['date'].split('/')[2])
        if rec['city'] == city and rec_year == year:
            result.append(rec)
    return result

def load_some_data():
    sample_stuff = [
        ("15/01/2020", "Delhi", 12.5),
        ("15/01/2020", "Mumbai", 23.0),
        ("15/06/2020", "Delhi", 38.2),
        ("10/01/2021", "Delhi", 10.8),
        ("10/01/2021", "Kolkata", 16.9),
        ("22/06/2021", "Mumbai", 29.1),
    ]
    
    for dt, ct, tmp in sample_stuff:
        add_record(dt, ct, tmp)

def read_by_rows():
    start = time.time()
    all_data = []
    
    for row in data_grid:
        row_vals = []
        for val in row:
            row_vals.append(val)
        all_data.append(row_vals)
    
    end = time.time()
    return all_data, end - start

def read_by_cols():
    start = time.time()
    all_cols = []
    
    if len(data_grid) == 0:
        return [], 0
    
    max_cols = 0
    for row in data_grid:
        if len(row) > max_cols:
            max_cols = len(row)
    
    for col_idx in range(max_cols):
        col_vals = []
        for row_idx in range(len(data_grid)):
            if col_idx < len(data_grid[row_idx]):
                col_vals.append(data_grid[row_idx][col_idx])
            else:
                col_vals.append(missing_val)
        all_cols.append(col_vals)
    
    end = time.time()
    return all_cols, end - start

def make_sparse():
    sparse_list = []
    
    for r in range(len(data_grid)):
        for c in range(len(data_grid[r])):
            if data_grid[r][c] != missing_val:
                sparse_list.append([r, c, data_grid[r][c]])
    
    return sparse_list

def check_sparseness():
    total = 0
    filled = 0
    
    for row in data_grid:
        total += len(row)
        for val in row:
            if val != missing_val:
                filled += 1
    
    if total > 0:
        empty_ratio = (total - filled) / total
    else:
        empty_ratio = 0
    
    return total, filled, empty_ratio

def show_records():
    print("All Weather Records:")
    count = 1
    for r in records:
        print(f"{count}. {r['date']} - {r['city']}: {r['temp']}C")
        count += 1

def show_grid():
    print("\nTemperature Grid:")
    
    city_list = []
    for c in cities:
        city_list.append(c)
    city_list.sort()
    
    year_list = []
    for y in years:
        year_list.append(y)
    year_list.sort()
    
    print("Year    ", end="")
    for c in city_list:
        print(f"{c:>8}", end=" ")
    print()
    
    for y in year_list:
        print(f"{y}    ", end="")
        y_idx = years[y]
        for c in city_list:
            c_idx = cities[c]
            if c_idx < len(data_grid[y_idx]):
                temp = data_grid[y_idx][c_idx]
                if temp != missing_val:
                    print(f"{temp:>8.1f}", end=" ")
                else:
                    print("     ---", end=" ")
            else:
                print("     ---", end=" ")
        print()

def compare_access():
    print("\nTesting access methods:")
    
    row_data, row_time = read_by_rows()
    col_data, col_time = read_by_cols()
    
    print(f"Row access took: {row_time:.8f} seconds")
    print(f"Col access took: {col_time:.8f} seconds")

def analyze_sparse():
    print("\nSparse data info:")
    
    sparse_data = make_sparse()
    total, filled, empty_pct = check_sparseness()
    
    print(f"Total spots: {total}")
    print(f"Filled spots: {filled}")
    print(f"Empty percentage: {empty_pct*100:.1f}%")
    
    print("Non-empty entries:")
    for entry in sparse_data:
        y_keys = sorted(years.keys())
        c_keys = sorted(cities.keys())
        yr = y_keys[entry[0]]
        city = c_keys[entry[1]]
        print(f"  {yr}, {city}: {entry[2]}C")

def test_operations():
    print("Testing some operations...")
    
    print("Getting Delhi data for 2020:")
    delhi_data = get_data("Delhi", 2020)
    for d in delhi_data:
        print(f"  {d['date']}: {d['temp']}C")
    
    print("\nAdding Bangalore data...")
    add_record("05/03/2021", "Bangalore", 25.5)
    
    print("Removing Mumbai record...")
    removed = remove_record("Mumbai", "15/01/2020")
    if removed:
        print("  Successfully removed")
    else:
        print("  Record not found")

def main():
    print("Weather Storage System")
    print("=" * 30)
    
    load_some_data()
    show_records()
    show_grid()
    
    test_operations()
    compare_access()
    analyze_sparse()

main()