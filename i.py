from faker import Faker

fake = Faker('fa_IR')

for i in range(10):
    print(fake.word(part_of_speech=3))
