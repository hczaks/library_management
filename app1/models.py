from django.db import models


class Book(models.Model):
    title = models.CharField(verbose_name='书名', max_length=50)
    author = models.CharField(verbose_name='作者', max_length=50)
    published_date = models.DateField(verbose_name='入库时间')
    price = models.DecimalField(verbose_name='价格', max_digits=6, decimal_places=2)
    number = models.CharField(verbose_name='编号', max_length=8)

    def __str__(self):
        return self.title


class Borrower(models.Model):
    name = models.CharField(verbose_name='名字', max_length=100)
    student_id = models.CharField(verbose_name='学号', max_length=8)
    college_choice = (
        (1, '电子学院'),
        (2, '艺术学院'),
        (3, '文化学院'),
    )
    college = models.SmallIntegerField(verbose_name='学院', choices=college_choice)
    gender_choice = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)
    username = models.CharField(verbose_name='账号', max_length=12)
    password = models.CharField(verbose_name='密码', max_length=12)

    def __str__(self):
        return self.name


class Borrowing(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='书名')
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, verbose_name='借阅人')
    borrowed_date = models.DateField(verbose_name='借阅时间')
    returned_date = models.DateField(null=True, blank=True, verbose_name='归还时间')

    def __str__(self):
        return str(self.borrower.name)

