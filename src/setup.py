from setuptools import setup

setup(name='protomate',
      version='0.1',
      description='Automating project initialization',
      url='http://github.com/rednafi/protomate',
      author='Redowan Delowar',
      author_email='redowan.nafi@gmail.com',
      license='MIT',
      packages=['protomate'],
      install_requires=[
          'PyGithub',
      ],
      zip_safe=False)