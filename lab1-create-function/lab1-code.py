import os

def lambda_handler(event, context):
    
    numerator = int(event['numerator']) # from event passed in
    denominator = int(os.environ['denominator']) # from environment variable or secret manager
    
    modulo = numerator % denominator
    result = numerator / denominator
    
    message = ' is evenly divisible by ' if modulo == 0 else ' is not evenly divisible by '
    
    return {
        'message': str(numerator) + message + str(denominator),
        'result' : result
    }    
    
