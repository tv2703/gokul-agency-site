# ads/forms.py
from django import forms
from .models import Product


# 1. Widget to allow multiple selections in the HTML
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


# 2. Custom Field to teach Django how to validate a LIST of files without panicking
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ProductForm(forms.ModelForm):
    # 3. Apply our new smart MultipleFileField here!
    extra_images = MultipleFileField(
        required=False,
        help_text="You can upload up to 10 images for this product gallery."
    )

    class Meta:
        model = Product
        fields = ['title', 'category', 'short_description', 'detailed_description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style_classes = "w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition text-sm text-gray-700"

        for field_name in self.fields:
            if field_name != 'extra_images':
                self.fields[field_name].widget.attrs.update({'class': style_classes})

        self.fields['extra_images'].widget.attrs.update({
            'class': 'w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer',
            'accept': 'image/*'
        })