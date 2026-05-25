"""Constants for the team-finder project."""

# Project status choices
STATUS_OPEN = 'open'
STATUS_CLOSED = 'closed'
STATUS_CHOICES = [
    (STATUS_OPEN, 'Открыт'),
    (STATUS_CLOSED, 'Закрыт'),
]

# Field lengths
TITLE_MAX_LENGTH = 200
STATUS_MAX_LENGTH = 6
PHONE_MAX_LENGTH = 12
NAME_MAX_LENGTH = 150
SURNAME_MAX_LENGTH = 150

# Pagination
ITEMS_PER_PAGE = 12
