from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'pomeliahotel' 
    account_key = '1xR0hoj27ttBFodBDqcIwq4Lc6WyzKiv5sEf+pp33myWAnw0mDCrB3l0ie5nfSTKmYX7jxXT+fHm+AStVr/RQw=='
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'pomeliahotel'
    account_key = '1xR0hoj27ttBFodBDqcIwq4Lc6WyzKiv5sEf+pp33myWAnw0mDCrB3l0ie5nfSTKmYX7jxXT+fHm+AStVr/RQw=='
    azure_container = 'static'
    expiration_secs = None