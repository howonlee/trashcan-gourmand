from setuptools import setup

setup(
        name="trashcangourmand",
        version="1.2.0",
        description="A scheduler to email you your own code to read",
        url="https://github.com/howonlee/trashcan-gourmand",
        author="Howon Lee",
        license="MIT",
        py_modules=["trash_cli"],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Other Audience',
            'License :: OSI Approved :: MIT License',
            'Operating System :: POSIX',
        ],
        project_urls={
            'Documentation':"https://github.com/howonlee/trashcan-gourmand",
            'Source':"https://github.com/howonlee/trashcan-gourmand",
            'Tracker':"https://github.com/howonlee/trashcan-gourmand/issues",
        },
        python_requires='>3.7',
        install_requires=[
            "pygments",
            "pytest",
            "hypothesis",
            "click",
            "python-crontab",
        ],
        entry_points = """
        [console_scripts]
        trashcangourmand=trash_cli:cli
        """,
        )
