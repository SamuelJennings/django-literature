from invoke import task


@task
def install(c):
    """
    Install the project dependencies
    """
    print("🚀 Creating virtual environment using pyenv and poetry")
    c.run("poetry install")
    c.run("poetry run pre-commit install")
    c.run("poetry shell")


@task
def check(c):
    """
    Check the consistency of the project using various tools
    """
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
    """
    Run the test suite
    """
    print("🚀 Testing code: Running pytest")
    c.run("poetry run pytest --cov --cov-config=pyproject.toml --cov-report=xml")


@task
def build(c):
    clean(c)
    print("🚀 Creating wheel file")
    c.run("poetry build")


# @task
# def publish(c):
#     # check to make sure there are no surprises
#     print("🚀 Publishing: Dry run.")
#     c.run("poetry publish --dry-run")

#     # everything is in order so lets publish for real
#     print("🚀 Publishing to PyPI")
#     c.run("poetry publish")


# @task
# def build_and_publish(c, rule=""):
#     # 1. Bump the current version using the specified rule. (https://python-poetry.org/docs/cli/#version)
#     c.run(f"poetry version {rule}")

#     # 2. Build the source and wheels archive (https://python-poetry.org/docs/cli/#build)
#     build(c)

#     # 3. Publish the package, using the build files we just created (https://python-poetry.org/docs/cli/#publish)
#     c.run("poetry publish")


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


@task
def publish(c, rule=""):
    """
    Publish a new version of the package to PyPI
    """

    # 1. Set the current version using the specified rule
    # see https://python-poetry.org/docs/cli/#version for rules on bumping version
    if rule:
        c.run(f"poetry version {rule}")

    # 2. Build the source and wheels archive
    # https://python-poetry.org/docs/cli/#build
    print("🔧 Building: Creating wheel file.")
    c.run("poetry build")

    # 3. Dry run first to make sure everything is working
    print("🚀 Publishing: Dry run.")
    c.run("poetry publish --dry-run")

    # This command publishes the package, previously built with the build command, to the remote repository. It will automatically register the package before uploading if this is the first time it is submitted.
    # https://python-poetry.org/docs/cli/#publish
    print("📦 Publishing to PyPI")
    c.run("poetry publish")


@task
def tag(c, rule=""):
    """
    Create a new git tag and push it to the remote repository
    """
    if rule:
        # bump the current version using the specified rule
        c.run(f"poetry version {rule}")

    # 1. Get the current version number as a variable
    version_short = c.run("poetry version -s", hide=True).stdout.strip()
    version = c.run("poetry version", hide=True).stdout.strip()

    # 2. create a tag and push it to the remote repository
    c.run(f'git tag -a v{version_short} -m "{version}"')
    c.run("git push --tags")
    c.run("git push origin main")


@task
def live_docs(c):
    """
    Build the documentation and open it in a live browser
    """
    c.run("sphinx-autobuild -b html --host 0.0.0.0 --port 9000 --watch . -c . . _build/html")
