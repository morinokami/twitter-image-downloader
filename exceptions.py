class Error(Exception):
    '''Base-class for all exceptions raised by this module.'''


class ConfidentialsNotSuppliedError(Error):
    '''An API key and an API sectret must be supplied.'''


class BearerTokenNotFetchedError(Error):
    '''Couldn't fetch the bearer token.'''


class InvalidDownloadPathError(Error):
    '''Download path must be a directory.'''
