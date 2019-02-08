from crawling import crawling_items
from upload_data import upload_data


def main():
    crawling_items.start_crawling()
    upload_data.start_upload()


if __name__ == '__main__':
    main()