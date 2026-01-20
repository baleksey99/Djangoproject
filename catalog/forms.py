from django import forms
from .models import Product

FORBIDDEN_WORDS = {
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
}

class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': f'Введите {field.label.lower()}...',
                'aria-label': field.label
            })
        self.fields['name'].widget.attrs.update({
            'autofocus': True,
            'maxlength': '255',
            'placeholder': 'Например: Смартфон Apple iPhone 15',
            'style': 'font-size: 1.1rem; font-weight: 500;'
        })
        self.fields['description'].widget.attrs.update({
            'rows': 6,
            'style': 'resize: vertical; font-size: 1rem; line-height: 1.5;',
            'placeholder': 'Подробно опишите товар, его особенности и преимущества...'
        })
        self.fields['price'].widget.attrs.update({
            'step': '0.01',
            'min': '0',
            'style': 'text-align: right; font-weight: bold; font-size: 1.2rem;',
            'placeholder': '0.00',
            'aria-describedby': 'priceHelp'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-select',
            'placeholder': 'Выберите категорию...',
            'aria-label': 'Категория товара'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control-file',
            'accept': 'image/*',
            'title': 'Загрузите изображение товара (JPG, PNG)',
            'aria-label': 'Изображение товара'
        })
        if 'is_published' in self.fields:
            self.fields['is_published'].widget.attrs.update({
                'class': 'form-check-input',
                'style': 'margin-left: 0.5rem;'
            })

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']


    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name and self.contains_forbidden_words(name):
            raise forms.ValidationError('Название содержит запрещённые слова.')
        return name


    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and self.contains_forbidden_words(description):
            raise forms.ValidationError('Описание содержит запрещённые слова.')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price

    def contains_forbidden_words(self, text: str) -> bool:
        if not text:
            return False
        words = text.lower().split()
        return any(word in FORBIDDEN_WORDS for word in words)
