# ligmol

A simple complex database

## Getting Started

These instructions will guide you on how to install a local copy of LigMol.

### Prerequisites

The system setup is:

|  **Category**   |   **Version**    |
|  :----------:   | :--------------: |
|       OS        |   Ubuntu 18.04   |
|     DJANGO      |       2.1        |
|     Python      |      3.6.7       |

### Installing

Make sure that your system is up to date.

```
sudo apt-get update && sudo apt-get -y upgrade
```

Then install python3, pip3 and virtualenv packages

```
sudo apt-get install -y python3 python3-pip virtualenv
```

Now create a folder to hold LigMol files (for example DjangoSites), then enter it.

```
mkdir DjangoSites && cd DjangoSites
```

Install the python3 virtualenv to set up the packages, so packages from the Django website wont mess up with system packages (image how painful would be if you need an specific older version of a package in a site then a newer one of the same package in another site)

```
sudo virtualenv -p python3 env
```

Activate it

```
. env/bin/activate
```

Install Python 3 packages with pip3

```
sudo pip3 install <packagename>
```

Here it is the list of packages which are needed to run LigMol:

| **Package**| **Version** | **Package**| **Version** | **Package**| **Version** |
| :---------: | :---------: | :---------: | :---------: | :---------: | :---------: | 
| asn1crypto | 0.24.0 | Jinja2 | 2.10 | pyOpenSSL | 17.5.0 |
| attrs | 17.4.0 | jsonpointer | 1.10 | pyparsing | 2.3.1 |
| blinker | 1.4 | jsonschema | 2.6.0 | pyserial | 3.4 |
| certifi | 2018.1.18 | keyring | 10.6.0 | python-apt | 1.6.3 |
| chardet | 3.0.4 | keyrings.alt | 3.0 | python-dateutil | 2.8.0 |
| click | 6.7 | kiwisolver | 1.0.1 | python-debian | 0.1.32 |
| cloud-init | 18.4 | language-selector | 0.1 | pytz | 2018.9 |
| colorama | 0.3.7 | MarkupSafe | 1.0 | pyxdg | 0.25 |
| command-not-found | 0.3 | matplotlib | 3.0.2 | PyYAML | 3.12 |
| configobj | 5.0.6 | netifaces | 0.10.4 | requests | 2.18.4 |
| constantly | 15.1.0 | numpy | 1.16.1 | requests-unixsocket | 0.1.5 |
| cryptography | 2.1.4 | oauthlib | 2.0.6 | SecretStorage | 2.3.1 |
| cycler | 0.10.0 | PAM | 0.4.2 | service-identity | 16.0.0 |
| distro-info | 0.18 | pandas | 0.24.1 | six | 1.11.0 |
| Django | 2.1.5 | psycopg2 | 2.7.7 | ssh-import-id | 5.7 |
| django-crispy-forms | 1.7.2 | psycopg2-binary | 2.7.7 | systemd-python | 234 |
| django-rdkit | 0.1.0 | pyasn1 | 0.4.2 | Twisted | 17.9.0 |
| httplib2 | 0.9.2 | pyasn1-modules | 0.2.1 | ufw | 0.35 |
| hyperlink | 17.3.1 | pycrypto | 2.6.1 | unattended-upgrades | 0.1 |
| idna | 2.6 | pygobject | 3.26.1 | urllib3 | 1.22 |
| incremental | 16.10.1 | PyJWT | 1.5.3 | virtualenv | 16.2.0 |
|             |         |       |       | zope.interface | 4.3.2 |

Allow django trough the port 8000

```
sudo ufw allow 8000
```

Edit the file *settings.py* the line 

```
"ALLOWED_HOSTS = ['your_server_ip_here']"
```

and put your server ip inside array as a string (use the quotes ' like in sample above)

Now run the server

```
sudo python3 manage.py runserver
```

## Running the tests

TODO

## Deployment

TODO

## Built With

* TODO

## Contributing

TODO

## Versioning

TODO

## Authors

* **Artur Rossi** - *Initial work*
* **Diego Gomes** - *Conception*

## License

TODO

## Acknowledgments

* TODO
