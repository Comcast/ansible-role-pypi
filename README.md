comcast.pypi
============

A role for provisioning a minimal pypi-server

Role Variables
--------------

* `pypi_server_version`: 'The version of the pypiserver wheel to install and
  use. Default: `1.2.0`.'
* `pypi_user`: 'The user running the pypi-server service. It will be created if
  it doesn't exist. Default: `pypi`.'
* `pypi_group`: 'The group of which pypi_user is a member. Default: `pypi`.'
* `pypi_server_port`: 'The port in which the pypi-server will listen on.
  Default: `7974`.'
* `pypi_home_dir`: 'The home directory of the pypi user. Default: `/srv/pypi`.'
* `pypi_work_dir`: 'The workspace directory of the pypi-server. Default: `{{
  pypi_home_dir }}`.'
* `pypi_packages_directory`: 'The directory that will store uploaded python
  packages. Default: `{{ pypi_work_dir }}/packages`.'
* `pypi_log_file`: 'The log file the pypi-server will write to. Defautlt: `{{
  pypi_work_dir }}/pypi-server.log`.'
* `pypi_init_script_dir`: 'The directory that will store the pypi-server init
  script (sys-v only). Default: `/etc/init.d`.'
* `pypi_server_pid_file`: 'The location of the . Default: `{{ pypi_work_dir
  }}/pypi.pid`.'
* `pypi_requirements_template`: 'Template listing the required packages for
  the pypi-server. Default: `templates/pypi-server-requirements.txt.j2`.'
* `pypi_server_authenticate`: Comma-separated list of actions to authenticate
  a client, ex.: `download,list,update`. Default: `update`.
* `htaccess_dir`: 'The location of the generated `.htaccess` file. Default: `{{
  pypi_home_dir }}`.'
* `enable_anonymous_auth`: 'A boolean value that determines whether to use
  username/password authentication for uploads to the pypi-server. Note:
  Enabling this is not recommended as it will allow anyone to upload artifacts
  to pypi. Default: `false`.'
* `htaccess_username`: 'Username to use when authenticating to the pypi-server
  (only used when `enable_anonymous_auth is false`). Default: `test`.'
* `htaccess_password`: 'Password to use when authenticating to the pypi-server
  (only used when `enable_anonymous_auth is false`). Default: `test`.'

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

```yaml
    - hosts: servers
      roles:
         - role: comcast.pypi
```

Testing
-------

The following tools are required for testing this role.

1. [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
1. [Vagrant](https://www.vagrantup.com/downloads.html)
1. [Python 2.7](https://www.python.org/downloads/release/python-2712/)
1. [virtualenv](https://pypi.org/project/virtualenv/)


Create test environment:

```bash
virtualenv --python=$(which python2.7) .venv
source .venv/bin/activate
pip install -r test-reqs.txt
```

Run tests:

```bash
molecule test
```

Test against a specific platform:

```bash
molecule test --platform centos/7
molecule test --platform debian/jessie64
```

Test uploads:

Any python package can be used to test uploading. In this case BeautifulSoup4
is used as an example.

1. Stand up local pypi server

```bash
molecule converge
```
This should leave the pypi-server running on `http://localhost:8080` with 0
packages stored.

2. Clone a Python source repo

```bash
git clone https://github.com/getanewsletter/BeautifulSoup4.git
```

3. Create/modify the `.pypirc` file in your home directory and add the
`htaccess_username` and `htaccess_password` credentials if using authentication.

The `.pypirc` file should look similar to this:

> Note: If using the playbook defaults for the htaccess_username and
htaccess_password then the credentials should match what is in the playbook.yml

```
[distutils]
index-servers =
  local

[local]
repository: http://localhost:8080
username: <htaccess_username>
password: <htaccess_password>
```
4. Upload python package

From the Python source code repo execute the following command.

```bash
python setup.py sdist upload -r local
```

This should upload the python package to the pypi-server specified in the
`.pypirc` file using the credentials specified in the `[local]` block.


Test download:

To test package downloads from the local pypi-server the command below can be
executed after successfully uploading a package. Following the upload example
beautifulsoup4 can be downloaded as follows:

> Change version_number for the example below to match the version of the
package that was uploaded.

```bash
pip install --extra-index-url http://localhost:8080/ beautifulsoup4==<version_number>
```

License
-------

[Apache 2.0](LICENSE)

Author Information
------------------

* [Luis Ortiz][lortiz]
* [Elliot Weiser][elliotweiser]
* [Comcast][comcast]

[comcast]: https://github.com/Comcast
[elliotweiser]: https://github.com/elliotweiser
[lortiz]: https://github.com/skippyPeanutButter
