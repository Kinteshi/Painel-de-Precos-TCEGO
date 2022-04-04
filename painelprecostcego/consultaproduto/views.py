from multiprocessing import context
from django.shortcuts import render

from consultaproduto.forms import BuscaProdutoForm
from consultaproduto.search import search_produto

# Create your views here.


def index(request):
    return render(request, 'consultaproduto/index.html')


def consulta(request):
    form = BuscaProdutoForm()
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = BuscaProdutoForm(request.POST)
        if form.is_valid():
            descricao = form.cleaned_data['descricao']
            numero_resultados = form.cleaned_data['numero_resultados']
            print(numero_resultados)
            results = search_produto(descricao, numero_resultados)

            # group results by ean
            results_grouped = {}
            for result in results:
                if result['ean'] in results_grouped:
                    if result['description'] not in results_grouped[result['ean']][0]:
                        results_grouped[result['ean']][0].append(result['description'].title())
                    results_grouped[result['ean']][1].append(float(result['price']))
                else:
                    results_grouped[result['ean']] = [
                        [result['description'].title()],
                        [float(result['price'])]
                    ]
            # calculate average price and concatenate descriptions
            produtos = []
            for ean in results_grouped.keys():
                price = sum(results_grouped[ean][1]) / len(results_grouped[ean][1])
                std = sum((x - price) ** 2 for x in results_grouped[ean][1]) / len(results_grouped[ean][1])
                produtos.append({
                    'ean': f'{ean} (x{len(results_grouped[ean][1])})',
                    'descricao':  ' || '.join(results_grouped[ean][0]),
                    'preco': f'R${price:.2f}+/-{std:.2f}',
                }
                )


            # produtos = []
            # for hit in results:
            #     price = hit['price']
            #     produtos.append({
            #         'ean': hit['ean'],
            #         'descricao': hit['description'].title(),
            #         'preco': f'R$ {price:.2f}',
            #     }
            #     )
            context['produtos'] = produtos
    return render(request, 'consultaproduto/consulta.html', context)
