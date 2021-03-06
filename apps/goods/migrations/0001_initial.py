# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-23 18:49
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
                ('ac_name', models.CharField(max_length=150, verbose_name='活动商品名称')),
                ('img', models.ImageField(upload_to='activity/%Y%m/%d', verbose_name='商品图片')),
                ('url', models.URLField(verbose_name='商品地址')),
            ],
            options={
                'verbose_name': '首页活动表',
                'verbose_name_plural': '首页活动表',
            },
        ),
        migrations.CreateModel(
            name='ActivateGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
            ],
            options={
                'verbose_name': '首页活动专区商品列表',
                'verbose_name_plural': '首页活动专区商品列表',
            },
        ),
        migrations.CreateModel(
            name='ActivityZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
                ('title', models.CharField(max_length=150, verbose_name='活动专区名称')),
                ('brief', models.CharField(blank=True, max_length=200, null=True, verbose_name='活动专区的简介')),
                ('order', models.SmallIntegerField(default=0, verbose_name='排序')),
                ('is_on_sale', models.BooleanField(choices=[(0, '下架'), (1, '上架')], default=0, verbose_name='上否上线')),
            ],
            options={
                'verbose_name': '活动管理',
                'verbose_name_plural': '活动管理',
            },
        ),
        migrations.CreateModel(
            name='DisplayGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
                ('dis_name', models.CharField(max_length=50, verbose_name='商品名称')),
                ('pic', models.ImageField(upload_to='img/%Y%m/%d', verbose_name='图片')),
                ('good_order', models.SmallIntegerField(default=0, verbose_name='排序')),
            ],
            options={
                'verbose_name': '首页轮播商品表',
                'verbose_name_plural': '首页轮播商品表',
            },
        ),
        migrations.CreateModel(
            name='Goods_Photography',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
                ('img', models.ImageField(upload_to='goods/%Y%m/%d', verbose_name='商品图片')),
            ],
            options={
                'verbose_name': '商品相册名',
                'verbose_name_plural': '商品相册名',
            },
        ),
        migrations.CreateModel(
            name='GoodsCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
                ('classname', models.CharField(max_length=50, verbose_name='分类名')),
                ('classinfor', models.CharField(blank=True, max_length=100, null=True, verbose_name='分类简介')),
            ],
            options={
                'verbose_name': '商品分类表',
                'verbose_name_plural': '商品分类表',
            },
        ),
        migrations.CreateModel(
            name='GoodsSku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
                ('goodname', models.CharField(max_length=50, verbose_name='商品名字')),
                ('goodcontent', models.TextField(blank=True, null=True, verbose_name='商品介绍')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='商品价格')),
                ('num', models.PositiveIntegerField(default=0, verbose_name='库存')),
                ('sellnum', models.PositiveIntegerField(default=0, verbose_name='销售量')),
                ('logo', models.ImageField(upload_to='goods/%Y%m/%d', verbose_name='封面图片')),
                ('is_putaway', models.BooleanField(choices=[(0, '下架'), (1, '上架')], default=0, verbose_name='是否上架')),
                ('goodcate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategories', verbose_name='商品分类')),
            ],
            options={
                'verbose_name': '商品spu表',
                'verbose_name_plural': '商品spu表',
            },
        ),
        migrations.CreateModel(
            name='GoodsSpu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
                ('sp_name', models.CharField(max_length=50, verbose_name='商品spu名称')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品spu表',
                'verbose_name_plural': '商品spu表',
            },
        ),
        migrations.CreateModel(
            name='GoodsUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='假删除')),
                ('unitname', models.CharField(max_length=50, verbose_name='单位名称')),
            ],
            options={
                'verbose_name': '商品单位表',
            },
        ),
        migrations.AddField(
            model_name='goodssku',
            name='goodspu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSpu', verbose_name='商品spu分类'),
        ),
        migrations.AddField(
            model_name='goodssku',
            name='unitinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsUnit', verbose_name='商品单位'),
        ),
        migrations.AddField(
            model_name='goods_photography',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSku', verbose_name='商品sku'),
        ),
        migrations.AddField(
            model_name='displaygoods',
            name='skuinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSku', verbose_name='商品sku'),
        ),
        migrations.AddField(
            model_name='activategoods',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.ActivityZone', verbose_name='活动专区'),
        ),
        migrations.AddField(
            model_name='activategoods',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsSku', verbose_name='商品sku'),
        ),
    ]
