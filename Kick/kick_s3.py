import boto3
import pickle
import hashlib

def kick_s3(func):
    client = boto3.client('s3')
    def func_wrapper(a):        
        # generate key by hashing input
        key = _generate_key(a)
        print
        
        # do something
        output = func(a)
        
        # pickle results so we can send it over the wire
        pickled_obj = pickle.dumps(output)
        
        # finally, kick to s3 
        client.put_object(Body=pickled_obj, Bucket="vinn-dump", Key=key)
    return func_wrapper

def _generate_key(x):
    encoded_str = str(x).encode()
    return hashlib.md5(encoded_str).hexdigest()