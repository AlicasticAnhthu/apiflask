import json
from jinja2 import Template

def get_mongodb_agent_sample():
    with open("grafana-agent/mongodb/agent.yaml", 'r', encoding='UTF-8') as file:
        return file.read()

def get_template_sample():
    with open("grafana-agent/mongodb/agent.yaml", 'r', encoding='UTF-8') as file:
        return file.read()

def save_report(yaml_content):
    with open("grafana-agent/mongodb/agent.yaml", 'w', encoding='UTF-8') as file:
        file.write(yaml_content)
    

def build_report():
    input = {
        "your_name": "Nguyen Van A",
    }
    input_data = json.loads(input)
    html_template = get_template_sample()
    jinja2_template = Template(html_template)
    html_content = jinja2_template.render(**input_data)
    save_report(html_content)
    print("create `report.html` success!")

if __name__ == "__main__":
    build_report();

