import logging
import random
import sys

from google.cloud import datastore
from fiistudentrest.models import Link


def test_model():
    # This is how to create a model instance
    link = Link(link="https://google.com")

    # When doing put, you save it to datastore and get its identifier
    key = link.put()
    print("Link with key", key)

    # Urlsafe is another identifier
    usafe = link.urlsafe
    print("urlsafe", usafe)

    # This is how you can retrieve an instance based on urlsafe
    link = Link.get(usafe)
    print("link", link)

    # Remove an instance of a model
    link.remove()

    # Retrieve all items of a kind (.all)
    print("removed; remaining", Link.all(keys_only=True))


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} FUNC")
        return

    global client
    client = datastore.Client(project="fiistudent", namespace="development")

    funcs = {
        "test_model": test_model,
    }
    funcs[sys.argv[1]]()


if __name__ == "__main__":
    main()

# Example: $ python dstore.py test_link_model
