from models import redis
import pickle
import logging
from dividends_request import create_dividend


def read_axis_interest_details(file_data):
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


def read_kotak_interest_certificate(file_data):
    interests = {}
    for line in file_data:
        line = line.split(' ')
        if line:
            interest_id = line[2]
            amount = float(line[-1].strip())
            if interest_id in interests:
                interests[interest_id]['amount'] += amount
            else:
                interest = dict()
                interest['deposit_type'] = line[1]
                interest['amount'] = amount
                interest["credited_date"] = line[0]
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
    success_records = 0
    for key, value in interests.items():
        request_body = {
            'amount': value.get('amount'),
            'dividend_type': value.get('deposit_type'),
            'organisation_name': 'Kotak Mahindra Bank',
            'credited_date': '2022-06-30',
            'interest_id': key
        }
        if not create_dividend(request_body):
            failed_records[key] = value
        else:
            success_records += 1
    return failed_records, success_records


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    file_location = 'kotak_inputs.txt'
    try:
        with open(file_location, 'r') as file:
            file_data = file.readlines()
            file.close()

        logger.info("Successfully read all interest records.")

        # Reading interest certificate
        # all_interests = read_axis_interest_details(file_data)
        all_interests = read_kotak_interest_certificate(file_data)

        # Calling dividends API for each interest object
        logger.info("Calling dividends API for interest records.")
        failed_records, successful_records = call_dividends(all_interests)
        logger.info(f"{successful_records} records were successfully processed.")
        # failed_records = []

        if failed_records:
            # Pickling failed records
            logger.warning(f"{len(failed_records)} records couldn't be processed.")
            pickled_interest = pickle_interests(failed_records)

            # Storing failed records in redis.
            logger.info("Storing failed records in redis.")
            redis_hset_name = 'interests'
            redis_key = file_location.split('.')[0]
            push_to_redis(redis_hset_name, redis_key, pickled_interest)

        logger.info("All interest records process successfully!")

    except Exception as e:
        logger.exception(e)
