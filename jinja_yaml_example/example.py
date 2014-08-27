'''Example usage of yaml config and jinja2 template'''

from jinja2 import Environment
from jinja2 import FileSystemLoader
import yaml


env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('example.j2')
with open('config.yml') as yf:
    config = yaml.load(yf)
output = template.render(config).encode('utf-8')
print(output)
