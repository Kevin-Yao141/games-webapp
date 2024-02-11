import jinja2

enviroment = jinja2.Environment()
template = enviroment.from_string("Hello, {{ name }}!")
template.render(name="World")