def read_interest_details(file_data):
    interests = {}
    for line in file_data:
        line = line.split(' ')
        interest_id = line[1]
        amount = float(line[-1].strip())
        if interest_id in interests:
            interests[interest_id]['amount'] += amount
        else:
            interest = {}
            deposit_type = line[2]
            interest['deposit_type'] = deposit_type
            interest['amount'] = amount
            interests[interest_id] = interest

    print(interests)


with open('../axis_interest_certificate_2022-2023.txt', 'r') as file:
    file_data = file.readlines()
    file.close()
read_interest_details(file_data)
