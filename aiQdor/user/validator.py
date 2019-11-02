import re
def validar_cpf(cpf: str) -> bool:

    """ 
        Valida o Cpf no formato NNN.NNN.NNN-NN
    """

    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False

    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se o CPF possui 11 números:
    if len(numbers) != 11:
        return False

    # Validação do primeiro dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    # Validação do segundo dígito verificador:
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True

    #if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
    #    return False


def validar_celular(cel: str) -> bool:
    """
        Valida Celular
    """
    if not re.match(r'^\([1-9]{2}\) [9]{0,1}[6-9]{1}[0-9]{3}\-[0-9]{4}$', cel):
       return False
    else:
        return True 