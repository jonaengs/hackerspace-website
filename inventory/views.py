from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import View


from .forms import ItemForm, LoanForm, TagForm
from .models import Tag, Item, Loan

def index(request):
    tags = Tag.objects.filter(visible=True)
    itemForm =  ItemForm()
    tagForm = TagForm()


    if request.method == "POST":
        if 'item' in request.POST:
            formdata = ItemForm(request.POST)
            formdata.save()
        elif 'tag' in request.POST:
            formdata = TagForm(request.POST)
            formdata.save()

    context = {'itemform': itemForm,
               'tagform': tagForm,
               'tags': tags,
               }

    return render(request, 'inventory/index.html', context)


def search(request):
    # TODO denne må oppdateres slik at den tar hensyn til subtags

    search_text = request.GET['q']
    if search_text.strip() == '/all':
        return render(request, 'inventory/search.html', show_all_items())
    search_words = search_text.split()
    return_set = []
    tags = []
    for word in search_words:
        return_set += Item.objects.filter(visible=True, tags__name__icontains=word)
        return_set += Item.objects.filter(visible=True, name__icontains=word)
        return_set += Item.objects.filter(visible=True, description__icontains=word)
        tags += Tag.objects.filter(name__icontains=word, visible=True)

    for tag in tags:
        return_set += tag.item_set.all().filter(visible=True)

    return_set = list(set(return_set))
    return_set.sort(key=lambda i: i.name.lower())

    context = {
        'hits': return_set,
        'search_text': search_text,
        'tags': tags,
    }
    return render(request, 'inventory/search.html', context)


def show_all_items():
    """ Returns context with every item. """
    items = list(Item.objects.all().filter(visible=True))
    items.sort(key=lambda i: i.name.upper())

    return {
        'hits': items,
        'search_text': '/all',
        'tags': Tag.objects.all().filter(visible=True)
    }

@permission_required(['inventory.change_item', 'inventory.delete_item'])
def change_multiple_items(request):
    """ For å endre flere itmes, tilgjengelig hvis man merker gjenstander i search og trykker 'endre'. """
    # TODO søk på "arduino": hverken arduino eller OculusRift lar seg avmerke i boksen, det fungerer på resten
    # TODO endre her så man også kan lage nye tags
    # TODO endre så man kan endre zone og/eller shelf
    # TODO lag en form og gjør viewet lesbart.
    if request.method == "POST":
        try:
            """ Items marked in search-view for changing """
            # items_for_changing: String of all item_id's to be changed, separated with '_' (also one at the end)
            items_for_changing = request.POST['items']
        except KeyError:
            form = ItemForm(request.POST)
            # TODO is_valid() returnerer ikke true
            form.is_valid()
            items = form.cleaned_data['tags_chips']
            try:
                new_tags = form.cleaned_data['name']
            except KeyError:
                """ Deletes all marked items """
                ItemForm.delete_all_items(items)
                messages.add_message(request, messages.SUCCESS, "Gjenstander ble slettet.")
                return HttpResponseRedirect(reverse('inventory:index'))
            else:
                """ Changes tag on all marked items """
                ItemForm.change_tags(items, new_tags)
                messages.add_message(request, messages.SUCCESS, "Tagger ble oppdatert.")
                return HttpResponseRedirect(reverse('inventory:index'))
        else:
            items = [get_object_or_404(Item, pk=item_id) for item_id in items_for_changing.split('_')[:-1]]
            context = {
                'autocomplete_dict': ItemForm.get_autocomplete_dict(),
                'form': ItemForm(initial={'tags_chips': items_for_changing, 'name': 'skip'}),
                'items': items,
            }
            return render(request, 'inventory/change_multiple_items.html', context)
    else:
        return render(request, 'inventory/search.html', show_all_items())


class RegisterLoan(View):
    """ @permission_required('inventory.add_loan') er satt i urls.py """

    context = {
        'chosen_item': {}
    }

    def get(self, request, item_id=0):
        self.context['form'] = LoanForm()

        if int(item_id) > 0:
            item = Item.objects.get(pk=item_id)
            self.context['chosen_item'] = {'id': item.id, 'text': item.name}

        return HttpResponse(render(request, 'inventory/register_loan.html', self.context))

    def post(self, request, item_id=0):
        form = LoanForm(data=request.POST)
        if form.is_valid():
            loan_items = form.cleaned_data['items']
            del form.cleaned_data['items']

            loan = Loan.objects.create(**form.cleaned_data)
            loan.loanitem_set.add(*loan_items)
            loan.lender = request.user
            loan.loan_date = timezone.now()
            loan.save()

            messages.add_message(request, messages.SUCCESS, 'Lånet ble registrert')
            return HttpResponseRedirect(reverse('inventory:index'))

        self.context['form'] = form
        return HttpResponse(render(request, 'inventory/register_loan.html', self.context))


@permission_required('inventory.add_loan')
def administrate_loans(request):
    """ return HttpResponse("liste over nåværende, for sene og gamle utlån") """

    all_loans = Loan.objects.filter(date_returned__isnull=True)
    active_loans = all_loans.filter(return_date__gte=timezone.now()).order_by('return_date')
    late_loans = all_loans.filter(return_date__lte=timezone.now()).order_by('return_date')
    old_loans = Loan.objects.filter(date_returned__isnull=False).order_by('date_returned')

    context = {
        'active_loans': active_loans,
        'late_loans': late_loans,
        'old_loans': old_loans,
    }
    return render(request, 'inventory/administrate_loans.html', context)


@login_required
def my_loans(request):
    user = request.user

    all_loans = user.loan_set.filter(date_returned__isnull=True)
    active_loans = all_loans.filter(return_date__gte=timezone.now()).order_by('return_date')
    late_loans = all_loans.filter(return_date__lte=timezone.now()).order_by('return_date')
    old_loans = user.loan_set.filter(date_returned__isnull=False).order_by('date_returned')

    context = {
        'active_loans': active_loans,
        'late_loans': late_loans,
        'old_loans': old_loans,
    }
    return render(request, 'inventory/my_loans.html', context)


@permission_required(['inventory.add_loan', 'inventory.change_loan', 'inventory.delete_loan'])
def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id)
    if request.method == 'POST':
        if not loan.date_returned:
            loan.date_returned = timezone.now()
        else:
            loan.date_returned = None
        loan.save()
        return HttpResponseRedirect(reverse('inventory:loan_detail', args=(loan.id,)))

    return render(request, 'inventory/loan_detail.html', {'loan': loan})

# TODO listener for å sende ut mail med purring når det har gått litt over fristen, ..?
