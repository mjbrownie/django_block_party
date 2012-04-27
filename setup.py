from setuptools import setup, find_packages
setup(name='django_block_party',
        version='0.2',
        description='Template inspector for vim',
        #long_description=readme,
        author="Michael Brown",
        author_email="michael@ascetinteractive.com",
        packages=find_packages(),
         # package_data={'':[
         #    'templates/sparklines/*',
         #    ]},
        include_package_data=True,
        zip_safe=False,
        )
