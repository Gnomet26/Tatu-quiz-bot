import random

def generate(data):

    variantlar = data

    togri_javob = variantlar[0]

    random.shuffle(variantlar)

    togri_javob_yangi_index = variantlar.index(togri_javob)

    return {"new_variant":variantlar, "true_index":togri_javob_yangi_index }
