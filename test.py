import random

variantlar = ['Toshkent', 'Buxoro', 'Samarqand', 'Navoiy']

togri_javob = variantlar[0]

random.shuffle(variantlar)

togri_javob_yangi_index = variantlar.index(togri_javob)

print(variantlar)

print(f"\n✅ To‘g‘ri javob yangi indeksda: {togri_javob_yangi_index}")
