from django.contrib.auth.models import User
from datetime import datetime
from collections import namedtuple
from core.models import Profile
from orders.models import OrderLine, InspectorReport, Contract, BillingStatement
from schedule.models import Schedule


# This file contains functions that you may call throughout the system
# Feel free to add functions here

# Makes sure that the username is unique


def is_unique(username):
    try:
        User.objects.get(username=username)
        return False
    except User.DoesNotExist:
        return True


# check if two date instances overlap
def is_overlap(start1, start2, end1, end2):

    Range = namedtuple('Range', ['start', 'end'])
    range1 = Range(start=start1, end=end1)
    range2 = Range(start=start2, end=end2)

    latest_start = max(range1.start, range2.start)
    earliest_end = min(range1.end, range2.end)
    overlap = (earliest_end - latest_start).days + 1

    return overlap > 0


# checks if the input start and end dates conflict with other schedules
# considering the people
def check_overlaps(involved_people, start, end):

    people = Profile.objects.all()

    for person in involved_people:
        for profile in people:

            a = Profile.objects.get(pk=person)
            if a == profile:
                scheds = profile.schedule_set.all()

                for x in scheds:
                    if is_overlap(start.date(), x.start_date.date(), end.date(), x.end_date.date()):
                        return True

    return False


# gets the total price of an order
def get_total_price(order):

    order_line = OrderLine.objects.filter(order=order)
    total = 0

    for line in order_line:
        total += (line.quantity * line.product.selling_price)

    return total


# gets grand total price
# includes fees

def get_grand_total_price(order):

    sub_total = get_total_price(order)

    installation = order.contract.installation_fee / 100 * sub_total
    engineering = order.contract.engineering_fee / 100 * sub_total
    consumables = order.contract.consumables_fee / 100 * sub_total

    return sub_total + installation + engineering + consumables


# check documents numbers
# methods for them
# returns True if there are duplicates
def check_duplicate_numbers(number, report):

    if report == "inspector":

        dup = 0
        reports = InspectorReport.objects.all()

        for x in reports:
            if number == x.inspector_report_no:
                dup = 1

        if dup > 0:
            return True

    elif report == "contract":

        dup = 0
        reports = Contract.objects.all()

        for x in reports:
            if number == x.number:
                dup = 1

        if dup > 0:
            return True

    elif report == "billing":

        dup = 0
        reports = BillingStatement.objects.all()

        for x in reports:
            if number == x.number:
                dup = 1

        if dup > 0:
            return True

    return False






