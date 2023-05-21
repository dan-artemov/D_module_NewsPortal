from django import template


register = template.Library()

class FilterException(Exception): # создаем класс, наследуемый от класса Exception
    pass

@register.filter()
def censor(value):
    """
    value: значение, к которому нужно применить фильтр

    """
    # Сделаем проверку соответствия данных строковому типу, передаваемых в функцию censor
    if type(value) is not str:
        raise FilterException(f'Фильтр "Censor" применяется только к данным строкового типа. Проверьте тип данных.')

    check_list = ['python', 'инженер', 'windows', 'pycharm']
    punct = ['.', ',', '-', '!', '?', ':', ';']
    output_list = []
    input_list = list(value.split())
    for word in input_list:
        lw = len(word)
        i = 1
        for check in check_list:
            if check in word.lower():
                if word[lw - 1] in punct:
                    out_word = word[0] + '*' * (len(word) - 2) + word[-1]
                    i -= 1
                    break
                else:
                    out_word = word[0] + '*' * (len(word) - 1)
                    i -= 1
                    break
        if i == 1:
            output_list.append(word)
        else:
            output_list.append(out_word)

    return f'{" ".join(map(str, output_list))}'



