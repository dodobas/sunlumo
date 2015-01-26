# What is Sunlumo?

Sunlumo is a platform built on top of QGIS that enables users to manage their
spatial data. The core concept of the platform is to use a single QGIS Project
file and provide services to various user groups. For example, an expert user
would use QGIS Desktop for any purpose, a basic user could use the same
project on a customized QGIS application with limited functionality and an
anonymous (web user) could use a WebGIS interface to browse and query spatial
data.

Current development endeavours are focused on recreating QGIS Server and QGIS
WebClient on Django framework by utilizing QGIS Python API.

## Concepts

Sunlumo Mapserver responds to WMS GetMap requests, but it's will probably
never be a fully compliant WMS service. The main reason why we opted to WMS
requests is support for WMS protocol in JavaScript WebMapping clients. Almost
all requests use some non standard request parameters which foster tighter
integration with QGIS platform through QGIS API.

Every request must reference a QGS project file, and at the moment it's
referenced as a *MAP* request parameter. In theory, a Sunlumo Mapserver should
be able to provide services for an arbitrary QGS project file.

## Supported features

### LayerControl

* every layer or a group of layers has following functionality:
  * 'eye' icon toggles visibility
  * 'info' icon toggles map search (GetFeatureInfo)
  * 'gear' icon opens layer options panel that enables setting layer transparency

* a layer group can be expanded or collapsed (initially this is read from the QGS project file)
* click and drag enables layer/group reordering (only works in Mozilla Firefox)

### MapSearchControl

* layers that have active 'info' icon will be searched on map click
* results will be shown in a panel
  * initially, every record is closed, clicking on it will show it's attributes
  * clicking on the 'location' icon will zoom the map to record location and highlight it

### SimilaritySearchControl

* similarity search is based on PostgreSQL pg_trgm index and based by prebuilt indices which are simple attribute concatenations
* '+' operator allows further search specialization, for example, results for the search string 'nik + 4' are going to include all records that have a string 'nik' followed by a string '4'
* clicking on the search result will zoom the map to the clicked record

### Toolbox

* measuring distances and areas
  * it's working but it needs a lot of work

### PrintControl

* select scale and prepared print layout (QGIS Composer)
  * after showing the area, it's possible to move the print frame
  * printing will produce a PDF file

## Planned features

### Administrative interface

* manage everything about a QGIS Project, layers, search indices
* user access privileges for project/layer/index

## Ideas

# Development

## Initialize development environment

This project is based on Ubuntu 14.04 and official QGIS community repository.
At the moment it's best to use to use a container or a virtual machine for
development.

On a clean Ubuntu 14.04 (trusty), add QGIS community repository:

```
gpg --keyserver keyserver.ubuntu.com --recv DD45F6C3
gpg --export --armor DD45F6C3 | apt-key add -

printf "deb http://qgis.org/debian trusty main\ndeb-src http://qgis.org/debian trusty main\n" > /etc/apt/sources.list.d/qgis.list

apt-get update
```

Then install packages from the repository:

```
apt-get install vim qgis qgis-server python-pip libpq-dev libpython-dev git curl
```


## Getting started

After forking and cloning the repository, everything else is pretty much
standard for every Python Django project.

However, as QGIS Python binding can't be installed in the *virtualenv*, you
can either create one using `--system-site-packages` or simply install
everything directly on the system. If you are using a container or a virtual
machine this should not be a problem.

```
pip install -r REQUIREMENTS-dev.txt
nodeenv -n 0.10.33 -v
npm install -g grunt-cli
```

Then `cd django_project` and install JS/CSS development utilties:

```
npm install .
```


It's probably best to simply copy another developer's specific settings and
customize it to your liking.

```
cp core/settings/dev_dodobas.py core/settings/dev_username.py
```

You also need to generate JS and CSS resources by using *grunt* JS task runner:

```
grunt
```

When developing JS or CSS is probably best to open a new terminal and execute:
`grunt watch:project`. This command will constantly watch JS and CSS files in
the project folders and run a set of tasks that will browserify JS and combine
and compress CSS.

### Development server

QGIS is based on QT framework and as such it's not really friendly towards
Python threads (GIL). To work around these issues we need to execute it in a
single thread environment. This also applies to the deployment environment.

```
export DJANGO_SETTINGS_MODULE=core.settings.dev_username
python manage.py runserver 0.0.0.0:8000 --nothreading
```

### Running tests

Tests are executed in the *production like* environment. Create your own
developer specific settings and customize to it to your liking.

```
cp core/settings/test_dodobas.py core/settings/test_username.py
```

We also need to aggregate and optimize static files:

```
python manage.py collectstatic --settings=core.settings.test_username --noinput
```

And then you can simply run test by executing `test.bash` in django_project
directory:

```
USER=username ./test.bash
```
