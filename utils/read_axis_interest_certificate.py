from models import redis
import pickle
import logging
from dividends_request import create_dividend


logger = logging.getLogger(__name__)


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

    return interests


def pickle_interests(interest):
    return pickle.dumps(interest)


def push_to_redis(name, key, data):
    try:
        redis.hset(name, key, data)
    except Exception as e:
        print(e)


def call_dividends(interests):
    failed_records = {}
    for key, value in interests.items():
        request_body = {
            'amount': value.get('amount'),
            'dividend_type': 'FD' if value.get('deposit_type') in ["RIC", "QIC"] else "SBI",
            'organisation_name': 'Axis Bank',
            'credited_date': '2022-06-30'
        }
        if not create_dividend(request_body):
            failed_records[key] = value
    return failed_records


if __name__ == '__main__':
    file_location = 'axis_interest_certificate_2022_2023.txt'
    try:
        with open(file_location, 'r') as file:
            file_data = file.readlines()
            file.close()

        logger.info("Successfully read all interest records.")

        # Reading interest certificate
        all_interests = read_interest_details(file_data)

        # Calling dividends API for each interest object
        logger.info("Calling dividends API for interest records.")
        failed_records = call_dividends(all_interests)

        # Pickling failed records
        logger.warning(f"{len(failed_records)} records couldn't be processed.")
        pickled_interest = pickle_interests(failed_records)

        # Storing failed records in redis.
        if failed_records:
            logger.info("Storing failed records in redis.")
            redis_hset_name = 'interests'
            redis_key = file_location.split('.')[0]
            push_to_redis(redis_hset_name, redis_key, pickled_interest)

        logger.info("All interest records process successfully!")

    except Exception as e:
        logger.exception(e)
