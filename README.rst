=============
FastAPI Admin
=============

.. image:: https://img.shields.io/pypi/v/fastapi-admin.svg?style=flat
   :target: https://pypi.python.org/pypi/fastapi-admin
.. image:: https://img.shields.io/github/license/long2ice/fastapi-admin
   :target: https://github.com/long2ice/fastapi-admin
.. image:: https://github.com/long2ice/fastapi-admin/workflows/gh-pages/badge.svg
   :target: https://github.com/long2ice/fastapi-admin/actions?query=workflow:gh-pages
.. image:: https://github.com/long2ice/fastapi-admin/workflows/pypi/badge.svg
   :target: https://github.com/long2ice/fastapi-admin/actions?query=workflow:pypi

`中文文档 <https://blog.long2ice.cn/2020/05/fastapi-admin%E5%BF%AB%E9%80%9F%E6%90%AD%E5%BB%BA%E5%9F%BA%E4%BA%8Efastapi%E4%B8%8Etortoise-orm%E7%9A%84%E7%AE%A1%E7%90%86%E5%90%8E%E5%8F%B0/>`_


Introduction
============

FastAPI-Admin is a admin dashboard based on `fastapi <https://github.com/tiangolo/fastapi>`_ and `tortoise-orm <https://github.com/tortoise/tortoise-orm>`_ and `rest-admin <https://github.com/wxs77577/rest-admin>`_.

FastAPI-Admin provide crud feature out-of-the-box with just a few config.

Live Demo
=========
Check a live Demo here `https://fastapi-admin.long2ice.cn <https://fastapi-admin.long2ice.cn/>`_.

* username: ``admin``
* password: ``123456``

Data in database will restore every day.

Screenshots
===========

.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/login.png
.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/list.png
.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/view.png
.. image:: https://github.com/long2ice/fastapi-admin/raw/master/images/create.png

Requirements
============

* `FastAPI <https://github.com/tiangolo/fastapi>`_ framework as your backend framework.
* `Tortoise-ORM <https://github.com/tortoise/tortoise-orm>`_ as your orm framework, by the way, which is best asyncio orm so far and I'm one of the contributors😋.

Quick Start
===========

Run Example Local
~~~~~~~~~~~~~~~~~
Look at `examples <https://github.com/long2ice/fastapi-admin/tree/master/examples>`_.

1. ``git clone https://github.com/long2ice/fastapi-admin.git``.
2. create database ``fastapi-admin`` and import from ``examples/example.sql``.
3. ``python setup.py install``.
4. ``env DATABASE_URL=mysql://root:123456@127.0.0.1:3306/fastapi-admin python3 examples/main.py``,then you can see:

.. code-block:: python

    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [89005]
    INFO:     Started server process [89009]
    INFO:     Waiting for application startup.
    INFO:     Tortoise-ORM startup
        connections: {'default': 'mysql://root:123456@127.0.0.1:3306/fastapi-admin'}
        apps: {'models': {'models': ['examples.models'], 'default_connection': 'default'}}
    INFO:     Tortoise-ORM started, {'default': <tortoise.backends.mysql.client.MySQLClient object at 0x110ed6760>}, {'models': {'Category': <class 'examples.models.Category'>, 'Product': <class 'examples.models.Product'>, 'User': <class 'examples.models.User'>}}
    INFO:     Tortoise-ORM generating schema
    INFO:     Application startup complete.

5. ``cd front && npm install && npm run serve``,then you can see:

.. code-block:: shell

    App running at:
    - Local:   http://localhost:8080/
    - Network: http://192.168.10.23:8080/

    Note that the development build is not optimized.
    To create a production build, run yarn build.

Open ``http://localhost:8080/`` in browser and enjoy it!

Backend Integration
~~~~~~~~~~~~~~~~~~~

.. code-block:: shell

    $ pip3 install fastapi-admin

.. code-block:: python

    from fastapi_admin.factory import app as admin_app

    fast_app = FastAPI()

    register_tortoise(fast_app, config=TORTOISE_ORM, generate_schemas=True)

    fast_app.mount('/admin', admin_app)

    @fast_app.on_event('startup')
    async def startup():
        admin_app.init(
            user_model='User',
            tortoise_app='models',
            admin_secret='test',
            permission=True,
            site=Site(...)
        )

Front
~~~~~
``cd front && cp .env.example .env`` and modify,then just run ``npm run serve``.

Features
========

Builtin Auth And Permissions Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Inherit ``fastapi_admin.models.User`` and add you own fields,must contains ``is_active`` and ``is_superuser``.

.. code-block:: python

    from fastapi_admin.models import User as AdminUser

    class AdminUser(AdminUser,Model):
        is_active = fields.BooleanField(default=False, description='Is Active')
        is_superuser = fields.BooleanField(default=False, description='Is Superuser')
        status = fields.IntEnumField(Status, description='User Status')
        created_at = fields.DatetimeField(auto_now_add=True)
        updated_at = fields.DatetimeField(auto_now=True)

Then add ``fastapi_admin.models`` to ``Tortoise-ORM`` config, example:

.. code-block:: python

    TORTOISE_ORM = {
        'connections': {
            'default': os.getenv('DATABASE_URL')
        },
        'apps': {
            'models': {
                'models': ['examples.models', 'fastapi_admin.models'],
                'default_connection': 'default',
            }
        }
    }

And set ``permission=True`` to active it:

.. code-block:: python

        admin_app.init(
            user_model='AdminUser',
            admin_secret='123456',
            models='examples.models',
            permission=True,
            site=Site(
                ...
            )
        )

And register permissions and createsuperuser:

.. code-block:: shell

    $ fastapi-admin -h
    usage: fastapi-admin [-h] -c CONFIG {register_permissions,createsuperuser} ...

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            Tortoise-orm config dict import path,like settings.TORTOISE_ORM.

    subcommands:
      {register_permissions,createsuperuser}


Enum Support
~~~~~~~~~~~~
When you define a enum field of tortoise-orm,like ``IntEnumField``,you can inherit ``fastapi_admin.enums.EnumMixin`` and impl ``choices()`` method,
FastAPI-Admin will auto read and display and render a ``select`` widget in front.

.. code-block:: python

    class Status(EnumMixin, IntEnum):
        on = 1
        off = 2

        @classmethod
        def choices(cls):
            return {
                cls.on: 'ON',
                cls.off: 'OFF'
            }

Verbose Name
~~~~~~~~~~~~
FastAPI-Admin will auto read ``description`` defined in tortoise-orm model ``Field`` and display in front.

ForeignKeyField Support
~~~~~~~~~~~~~~~~~~~~~~~
If ``ForeignKeyField`` not passed in ``menu.raw_id_fields``,FastAPI-Admin will get all related objects and display ``select`` in front with ``Model.__str__``.

ManyToManyField Support
~~~~~~~~~~~~~~~~~~~~~~~
FastAPI-Admin will render ``ManyToManyField`` with multiple ``select`` in ``form`` edit with ``Model.__str__``.

JSONField Render
~~~~~~~~~~~~~~~~
FastAPI-Admin will render ``JSONField`` with ``jsoneditor`` as beauty interface.

Search Fields
~~~~~~~~~~~~~
Defined ``menu.search_fields`` in ``menu`` will render a search form by fields.

Xlsx Export
~~~~~~~~~~~
FastAPI-Admin can export searched data to excel file when define ``export=True`` in ``menu``.

Bulk Actions
~~~~~~~~~~~~
Current FastAPI-Admin support builtin bulk action ``delete_all``,if you want write your own bulk actions:

1. pass ``bulk_actions`` in ``Menu``,example:

.. code-block:: python

    Menu(
        ...
        bulk_actions=[{
            'value': 'delete', # this is fastapi router path param.
            'text': 'delete_all', # this will show in front.
        }]
    )

2. write fastapi route,example:

.. code-block:: python

    from fastapi_admin.schemas import BulkIn
    from fastapi_admin.factory import app as admin_app

    @admin_app.post(
        '/rest/{resource}/bulk/delete' # `delete` is defined in Menu before.
    )
    async def bulk_delete(
            bulk_in: BulkIn,
            model=Depends(get_model)
    ):
        await model.filter(pk__in=bulk_in.pk_list).delete()
        return {'success': True}

Default Menus
~~~~~~~~~~~~~
Default, FastAPI-Admin provide default menus by your models, without doing tedious works.

Deployment
==========
1. Deploy fastapi app by gunicorn+uvicorn or reference https://fastapi.tiangolo.com/deployment/.
2. ``cp .env.example .env`` and modify,run ``npm run build`` in ``front`` dir,then copy static files in ``dists`` to you server,deployment by ``nginx``.

ThanksTo
========

* `fastapi <https://github.com/tiangolo/fastapi>`_ ,high performance async api framework.
* `tortoise-orm <https://github.com/tortoise/tortoise-orm>`_ ,familiar asyncio ORM for python.
* `rest-admin <https://github.com/wxs77577/rest-admin>`_,restful Admin Dashboard Based on Vue and Boostrap 4.

License
=======

This project is licensed under the `MIT <https://github.com/long2ice/fastapi-admin/blob/master/LICENSE>`_ License.
