from invoke import task


@task
def install(c):
    print("🚀 Creating virtual environment using pyenv and poetry")
    c.run("poetry install")
    c.run("poetry run pre-commit install")
    c.run("poetry shell")


@task
def check(c):
    print("🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check")
    c.run("poetry lock --check")

    print("🚀 Linting code: Running pre-commit")
    c.run("poetry run pre-commit run -a")

    print("🚀 Static type checking: Running mypy")
    c.run("poetry run mypy")

    print("🚀 Checking for obsolete dependencies: Running deptry")
    c.run("poetry run deptry .")


@task
def test(c):
    print("🚀 Testing code: Running pytest")
    c.run("poetry run pytest --cov --cov-config=pyproject.toml --cov-report=xml")


@task
def build(c):
    clean(c)
    print("🚀 Creating wheel file")
    c.run("poetry build")


@task
def publish(c):
    # check to make sure there are no surprises
    print("🚀 Publishing: Dry run.")
    c.run("poetry publish --dry-run")

    # everything is in order so lets publish for real
    print("🚀 Publishing to PyPI")
    c.run("poetry publish")


@task
def build_and_publish(c, rule=""):
    # 1. Bump the current version using the specified rule. (https://python-poetry.org/docs/cli/#version)
    c.run(f"poetry version {rule}")

    # 2. Build the source and wheels archive (https://python-poetry.org/docs/cli/#build)
    build(c)

    # 3. Publish the package, using the build files we just created (https://python-poetry.org/docs/cli/#publish)
    c.run("poetry publish")


@task
def clean_build(c):
    print("🚀 Removing old build artifacts")
    c.run("rm -fr build/")
    c.run("rm -fr dist/")
    c.run("rm -fr *.egg-info")


@task
def clean_pyc(c):
    """
    Remove python file artifacts
    """
    print("🚀 Removing python file artifacts")
    c.run("find . -name '*.pyc' -exec rm -f {} +")
    c.run("find . -name '*.pyo' -exec rm -f {} +")
    c.run("find . -name '*~' -exec rm -f {} +")


@task
def coverage(c):
    """
    check code coverage quickly with the default Python
    """
    c.run("coverage run --source literature runtests.py tests")
    c.run("coverage report -m")
    c.run("coverage html")
    c.run("open htmlcov/index.html")


@task
def docs(c):
    """
    Build the documentation and open it in the browser
    """
    # c.run("rm -f docs/django-literature.rst")
    # c.run("rm -f docs/modules.rst")
    c.run("sphinx-apidoc -o docs/ literature **/migrations/*")
    c.run("sphinx-build -E -b html docs docs/_build")


@task
def test_all(c):
    """
    Run tests on every python version with tox
    """
    c.run("tox")


@task
def clean(c):
    """
    Remove python file and build artifacts
    """
    clean_build(c)
    clean_pyc(c)


# @task(help={"bumpsize": 'Bump either for a "feature" or "breaking" change'})
# def release(c, bumpsize=""):
#     """
#     Package and upload a release
#     """
#     clean(c)
#     if bumpsize:
#         bumpsize = "--" + bumpsize

#     c.run("bumpversion {bump} --no-input".format(bump=bumpsize))

#     import literature

#     c.run("python setup.py sdist bdist_wheel")
#     c.run("twine upload dist/*")

#     c.run(
#         'git tag -a {version} -m "New version: {version}"'.format(
#             version=literature.__version__
#         )
#     )
#     c.run("git push --tags")
#     c.run("git push origin master")


@task
def release(c, rule=""):
    clean(c)

    #     c.run(
    #         'git tag -a {version} -m "New version: {version}"'.format(
    #             version=literature.__version__
    #         )
    #     )
    #     c.run("git push --tags")
    #     c.run("git push origin master")

    # 1. bump the current version using the specified rule
    # see https://python-poetry.org/docs/cli/#version for rules on bumping version
    c.run(f"poetry version {rule}")

    # 2. Build the source and wheels archive
    # https://python-poetry.org/docs/cli/#build
    c.run("poetry build")

    # This command publishes the package, previously built with the build command, to the remote repository. It will automatically register the package before uploading if this is the first time it is submitted.
    # https://python-poetry.org/docs/cli/#publish
    c.run("poetry publish")
