from easy_reservation import easy_reservation
from hard_reservation import hard_reservation

def reservation(driver, config):
    reservation_type = config.get('reservation_type')

    if reservation_type in ['swim', 'gym']:
        easy_reservation(driver, config)
    elif reservation_type == 'badminton':
        hard_reservation(driver, config)
    else:
        raise ValueError("Invalid reservation type")