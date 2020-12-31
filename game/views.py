from django.shortcuts import render, redirect
from django.forms import formset_factory
from .forms import CompanyForm, ShareForm, OwnerForm
from .models import Company, Share, Owner

# Create your views here.
def home(request):
    CompanyFormset = formset_factory(CompanyForm, extra=0)
    companies = Company.objects.all()

    ShareFormset = formset_factory(ShareForm, extra=0)
    shares = Share.objects.all()

    PlayerFormset = formset_factory(OwnerForm, extra=1)
    players = Owner.objects.all()
    
    if request.method == 'GET':
        companies_formset = CompanyFormset(initial=[
            {'asset': company.asset, 
            'investment': company.investment, 
            'share': company.share,
            'coefficient': company.coefficient, 
            'owner': company.owner if not bool(company.owner) else company.owner} for company in companies
        ], prefix='companies')

        shares_formset = ShareFormset(initial=[
            {'color': share.color, 'price': share.price} for share in shares
        ], prefix='shares')

        players_formset = PlayerFormset(initial=[
            {'name': player.name} for player in players
        ], prefix='players')

    elif request.method == 'POST':
        if request.POST.get('players-TOTAL_FORMS'):            
            players_formset = PlayerFormset(request.POST, initial=[
                {'name': player.name} for player in players
            ], prefix='players')

            if players_formset.is_valid():
                objs = []
                for form in players_formset:
                    if form.cleaned_data:
                        name = form.cleaned_data['name']
                        if name == 'delete':
                            Owner.objects.all().delete()
                            return redirect('home')
                        if not Owner.objects.filter(name=name).exists():
                            Owner.objects.create(name=name)

        elif request.POST.get('companies-TOTAL_FORMS'):
            companies_formset = CompanyFormset(request.POST, initial=[
                {'asset': company.asset, 
                'investment': company.investment, 
                'share': company.share,
                'coefficient': company.coefficient, 
                'owner': company.owner if not bool(company.owner) else company.owner} for company in companies
            ], prefix='companies')

            if companies_formset.is_valid():
                objs = []
                for form in companies_formset:
                    asset = form.cleaned_data['asset']
                    company = Company.objects.get(asset=asset)
                    company.investment = form.cleaned_data['investment']
                    company.coefficient = form.cleaned_data['coefficient']
                    company.owner = form.cleaned_data['owner']
                    objs.append(company)

                Company.objects.bulk_update(objs, ['investment', 'coefficient', 'owner'])

        else:
            shares_formset = ShareFormset(request.POST, initial=[
                {'color': share.color, 'price': share.price} for share in shares
            ], prefix='shares')
            if shares_formset.is_valid():
                objs = []
                for form in shares_formset:
                    color = form.cleaned_data['color']
                    price = form.cleaned_data['price']
                    share = Share.objects.get(color=color)
                    share.price = price
                    objs.append(share)

                Share.objects.bulk_update(objs, ['price'])

        return redirect('home')

    return render(request, 'home.html', {'companies_formset': companies_formset, 'shares_formset': shares_formset, 'players_formset': players_formset})