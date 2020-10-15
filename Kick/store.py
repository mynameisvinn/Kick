import pickle
import boto3


class PySwiss(object):
    def __init__(self, bucket):
        self.client = boto3.client('s3')
        self.bucket = bucket
        self._check_bucket()


    def _check_bucket(self):
        """check if bucket exists in s3.
        """
        response = self.client.list_buckets()
        buckets = {bucket['Name'] for bucket in response['Buckets']}
        if self.bucket not in buckets:
            raise ValueError("Bucket does not exist")


    def put(self, obj, key):
        pickled_obj = pickle.dumps(obj)
        self.client.put_object(Body=pickled_obj, Bucket=self.bucket, Key=key)


    def get(self, key):
        try:
            obj = self.client.get_object(Bucket=self.bucket, Key=key)
            new_pickled_obj = obj['Body'].read()
            return pickle.loads(new_pickled_obj)
        except Exception as e:
            # print(e)
            print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, self.bucket))