import os


def is_appstore_app(content_path: str) -> bool:
    receipt_path = os.path.join(content_path, '_MASReceipt', 'receipt')
    return os.path.exists(receipt_path)


def is_wrapper_app(application_path: str) -> bool:
    receipt_path = os.path.join(application_path, 'Wrapper', 'iTunesMetadata.plist')
    return os.path.exists(receipt_path)

