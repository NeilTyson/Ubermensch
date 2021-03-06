from django.contrib.auth.models import User
from datetime import datetime, date
import datetime as dtime
from collections import namedtuple
import pendulum
from core.models import Profile
from orders.models import OrderLine, InspectorReport, Contract, BillingStatement, Order, OfficialReceipt, \
    DeliveryReceipt, ProgressReport, AcceptanceLetter, CertificateOfWarranty, PullOutSlip
from schedule.models import Schedule
from inventory.models import PurchaseOrder


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

    elif report == "official":

        dup = 0
        reports = OfficialReceipt.objects.all()

        for x in reports:
            if number == x.number:
                dup = 1

        if dup > 0:
            return True

    elif report == "deliver":

        dup = 0
        reports = DeliveryReceipt.objects.all()

        for x in reports:
            if number == x.number:
                dup = 1

        if dup > 0:
            return True

    elif report == "progress":

        dup = 0
        reports = ProgressReport.objects.all()

        for x in reports:
            if number == x.number:
                dup = 1

        if dup > 0:
            return True
    elif report == "purchase":

        dup = 0
        reports = PurchaseOrder.objects.all()

        for x in reports:
            if number == x.number:
                dup = 1

        if dup > 0:
            return True
    elif report == "purchase":

        dup = 0
        reports = PurchaseOrder.objects.all()

        for x in reports:
            if number == x.number:
                dup = 1

        if dup > 0:
            return True

    elif report == "acceptance":

        dup = 0
        reports = AcceptanceLetter.objects.all()

        for x in reports:
            if number == x.number:
                dup = 1

        if dup > 0:
            return True

    elif report == "certificate":

        dup = 0
        reports = CertificateOfWarranty.objects.all()

        for x in reports:
            if number == x.number:
                dup = 1

        if dup > 0:
            return True

    elif report == "pullout":

        dup = 0
        reports = PullOutSlip.objects.all()

        for x in reports:
            if number == x.number:
                dup = 1

        if dup > 0:
            return True

    return False


# template to return
def get_payment_template(number):

    if number == "1":
        return "orders/purchase_order_phase.html"
    elif number == "2":
        return "orders/delivery.html"
    elif number == "3":
        return "orders/installation.html"


# get billing statement item
def get_item_description(number, order_id):

    order = Order.objects.get(id=order_id)

    if number == "1":
        return str(order.contract.first_percentage) + "% DOWN PAYMENT FOR PROJECT"

    elif number == "2":
        return str(order.contract.second_percentage) + "% DOWN PAYMENT FOR PROJECT"

    elif number == "3":
        return str(order.contract.third_percentage) + "% DOWN PAYMENT FOR PROJECT"


# add year thanks to StackOverflow
def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))


# payment intervals thanks to StackOverflow
def get_date_intervals(start_date, end_date, terms):
    start_day = start_date.day
    start_month = start_date.month
    start_year = start_date.year

    end_day = end_date.day
    end_month = end_date.month
    end_year = end_date.year

    start = pendulum.Pendulum(start_year, start_month, start_day)
    end = pendulum.Pendulum(end_year, end_month, end_day)
    period = pendulum.period(start, end)

    if terms == 'Monthly':
        return [dt.format('%B %d, %Y') for dt in period.range('months')][1:]

    elif terms == 'Quarterly':
        return [dt.format('%B %d, %Y') for dt in period.range('months', 3)][1:]

    elif terms == 'Semi-Annually':
        return [dt.format('%B %d, %Y') for dt in period.range('months', 6)][1:]

    elif terms == 'Annually':
        return [dt.format('%B %d, %Y') for dt in period.range('months', 12)][1:]


def merge_list(list):
    new_dict = {}

    for item in list:
        id = item['id']

        if not id in new_dict:
            new_dict[id] = item['quantity']
        else:
            new_dict[id] += item['quantity']

    new_list = []
    for id, quantity in new_dict.items():
        new_list.append({'id': id, 'quantity': quantity})

    return new_list