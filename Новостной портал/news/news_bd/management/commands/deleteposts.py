from django.core.management.base import BaseCommand, CommandError
from news_bd.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет все товары'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        self.stdout.readable()

        list_of_categories = []

        for category in Category.objects.all():
            list_of_categories.append(category.category_name)

        self.stdout.write('Вы действительно хотите удалить посты? yes/no')  # спрашиваем пользователя действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer=="yes":
            self.stdout.write(f'Выберите категорию из списка {list_of_categories}')

            answer = input()

            if answer.strip().lower() == 'политика':  # в случае подтверждения действительно удаляем все товары
                Post.objects.filter(category=1).delete()
                self.stdout.write(self.style.SUCCESS('Посты успешно удалены!'))
                return
            elif answer.strip().lower() == 'новости санкт-петербурга':
                Post.objects.filter(category=2).delete()
                self.stdout.write(self.style.SUCCESS('Посты успешно удалены!'))
                return
            elif answer.strip().lower() == 'технологии':
                Post.objects.filter(category=3).delete()
                self.stdout.write(self.style.SUCCESS('Посты успешно удалены!'))
                return
            elif answer.strip().lower() == 'культура':
                Post.objects.filter(category=4).delete()
                self.stdout.write(self.style.SUCCESS('Посты успешно удалены!'))
                return
            else:
                self.stdout.write(self.style.ERROR('Ошибка! Выбрана некорректная категория'))
        else:
            self.stdout.write(self.style.ERROR('Доступ запрещён!'))  # в случае неправильного подтверждения, говорим что в доступе отказано