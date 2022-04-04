from django import forms


class BuscaProdutoForm(forms.Form):
    descricao = forms.CharField(label='Descrição', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}))
    numero_resultados = forms.IntegerField(
        label='Número de resultados',
        min_value=100,
        max_value=1000,
        widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'value': 100}),
        )
