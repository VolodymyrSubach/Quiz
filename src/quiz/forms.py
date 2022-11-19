from django import forms
from django.core.exceptions import ValidationError

from .models import Choice


class QuestionInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        if not (self.instance.QUESTION_MIN_LIMIT <= len(self.forms) <= self.instance.QUESTION_MAX_LIMIT):
            raise ValidationError(
                f'Questions count must be in range '
                f'from {self.instance.QUESTION_MIN_LIMIT} '
                f'to {self.instance.QUESTION_MAX_LIMIT} inclusive'
            )

        order_num_lst = []

        for form in self.forms:
            if form.cleaned_data['order_num'] > self.instance.QUESTION_MAX_LIMIT:
                raise ValidationError(
                    f'Questions number must be not more then '
                    f'to {self.instance.QUESTION_MAX_LIMIT} inclusive'
                )
            if not (1 <= form.cleaned_data['order_num'] <= 100):
                raise ValidationError(
                    'Questions number must be between 1 to 100 inclusive'
                )
            order_num_lst.append(form.cleaned_data['order_num'])
            order_num_lst.sort()

        for n in range(len(order_num_lst) - 1):
            if order_num_lst[0] != 1:
                raise ValidationError(
                    'Question numbering does not start from 1')
            if order_num_lst[n] + 1 != order_num_lst[n + 1]:
                raise ValidationError(
                    f'Ascending order of question\'s number {order_num_lst[n]} '
                    f'and {order_num_lst[n + 1]} does not increase by 1!')


class ChoiceInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        # lst = []
        # for form in self.forms:
        #     if form.cleaned_data['is_correct']:
        #         lst.append(1)
        #     else:
        #         lst.append(0)
        #
        # num_correct_answers = sum(lst)

        # num_correct_answers = sum(1 for form in self.forms if form.cleaned_data['is_correct'])

        num_correct_answers = sum(form.cleaned_data['is_correct'] for form in self.forms)

        if num_correct_answers == 0:
            raise ValidationError('Need to choose one option minimum')

        if num_correct_answers == len(self.forms):
            raise ValidationError('It is not allowed to select all options')


class ChoiceForm(forms.ModelForm):
    is_selected = forms.BooleanField(required=False)

    class Meta:
        model = Choice
        fields = ('text',)


ChoicesFormSet = forms.modelformset_factory(
    model=Choice,
    form=ChoiceForm,
    extra=0
)
