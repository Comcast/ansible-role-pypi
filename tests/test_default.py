import yaml
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')

stream = file('defaults/main.yml', 'r')
defaults = yaml.load(stream)
stream.close()

user = defaults['pypi_user']
group = defaults['pypi_group']
pypi_packages_dir = defaults['pypi_home_dir'] + '/packages'
pypi_port = defaults['pypi_server_port']
pypi_log_file = defaults['pypi_log_file']
use_htaccess_file = defaults['use_htaccess_file']
htaccess_dir = defaults['pypi_home_dir']


def test_pypi_user(User):
    pypi_user = User(user)
    assert pypi_user.exists


def test_pypi_packages_dir(File):
    pypi_packages = File(pypi_packages_dir)
    print(pypi_packages_dir)
    assert pypi_packages.exists
    assert pypi_packages.is_directory
    assert pypi_packages.user == user
    assert pypi_packages.group == group
    assert pypi_packages.mode == 0755


def test_pypi_server_service_unit_file(File):
    pypi_init = File('/etc/systemd/system/pypi-server.service')
    assert pypi_init.exists
    assert pypi_init.user == 'root'
    assert pypi_init.group == 'root'
    assert pypi_init.mode == 0755


def test_pypi_service(Service):
    service = Service('pypi-server')
    assert service.is_running
    assert service.is_enabled


def test_htaccess_file(File):
    if use_htaccess_file:
        htaccess = File(htaccess_dir + '/.htaccess')
        assert htaccess.exists
        assert htaccess.is_file
        assert htaccess.mode == 0600
