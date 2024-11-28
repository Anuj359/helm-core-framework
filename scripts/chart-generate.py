# Run as python3 chart-generate7.py v1.1.1 v1.1.0
import yaml
import json
import os
import sys
from jinja2 import Template

# Paths to the values.yaml and values.schema.json files
values_file = 'values.yaml'
schema_file = 'values.schema.json'

# Load values.yaml
def load_values_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Load the values.yaml file
with open(values_file, 'r') as file:
    values_yaml = yaml.safe_load(file)

# Load the values.schema.json file
with open(schema_file, 'r') as file:
    schema_json = json.load(file)

# Function to fetch schema type and default
def get_schema_type_and_default(schema, key_path):
    keys = key_path.split(".")
    current_schema = schema
    
    for key in keys:
        if "properties" in current_schema:
            current_schema = current_schema["properties"].get(key, {})
        elif "items" in current_schema and isinstance(current_schema["items"], dict):
            current_schema = current_schema["items"]
        else:
            break
    
    value_type = current_schema.get("type", "unknown")
    schema_default = current_schema.get("default", None)
    
    return value_type, schema_default

# Recursive function to process values.yaml and fetch types and defaults
def process_values_yaml(values, schema, parent_key=""):
    result = []
    
    for key, value in values.items():
        key_path = f"{parent_key}{key}" if parent_key else key
        
        value_type, schema_default = get_schema_type_and_default(schema, key_path)
        
        if isinstance(value, dict):
            if key in ["deployment", "service"]:
                continue
            sub_result = process_values_yaml(value, schema, key_path + ".")
            result.extend(sub_result)
        else:
            default_value = schema_default if schema_default is not None else value
            result.append({
                "key": key_path,
                "type": value_type,
                "default": default_value
            })
    
    return result

# Generate HTML rows for each key-value pair from values.yaml
def generate_table_rows(data):
    rows = ""
    for item in data:
        rows += f"<tr><td>{item['key']}</td><td>{item['type']}</td><td>{item['default']}</td></tr>\n"
    
    return rows

# Generate Supported Features Table
def generate_supported_features_table(schema):
    features = []
    exclude_features = ['replicaCount', 'image']
    
    for feature in schema['properties']:
        if feature in exclude_features:
            continue
        
        feature_schema = schema['properties'][feature]
        feature_display_name = feature_schema.get('featureDisplayName', feature)

        feature_value = values_yaml.get(feature)
        if isinstance(feature_value, dict):
            enabled = "Enabled" if feature_value.get('enabled', False) else "Disabled"
        else:
            enabled = "Disabled"
        
        features.append((feature_display_name, enabled))
    return features

# HTML Template with Jinja2 syntax
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ version }}</title>
    <link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>
    <h1>Version {{ version }}</h1>
    <p>{{ version }} of Helm Core Framework.</p>
    <pre>
        This version supports cloudStorageMount which the previous version {{ prev_version }} doesn't support.
    </pre>

    <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 50%;">
        <thead>
          <tr style="background-color: #f2f2f2;">
            <th style="text-align: left;">Supported Feature</th>
            <th style="text-align: center;">Default State</th>
          </tr>
        </thead>
        <tbody>
          {% for feature, status in features %}
          <tr>
            <td>{{ feature }}</td>
            <td style="text-align: center; color: {{ 'green' if status == 'Enabled' else 'red' }};">{{ '✓ Enabled' if status == 'Enabled' else '✗ Disabled' }}</td>
          </tr>
          {% endfor %}
        </tbody>
      </table>

    <h2>Helm-Core-Framework Default Values</h2>
    <table border="1" cellpadding="10" cellspacing="0" style="border-collapse: collapse; width: 100%;">
        <thead>
          <tr style="background-color: #f2f2f2;">
            <th style="text-align: left;">Key</th>
            <th style="text-align: left;">Type</th>
            <th style="text-align: left;">Default</th>
          </tr>
        </thead>
        <tbody>
          {{ table_rows }}
        </tbody>
    </table>
    
    <br>
    <a href="../../index.html">Back to Main</a>
</body>
</html>
"""

# Main function
def main():
    # Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python chart-generate.py <current_version> <previous_version>")
        sys.exit(1)

    # Get the current and previous versions from arguments
    current_version = sys.argv[1]
    previous_version = sys.argv[2]

    # Process the values.yaml against the schema.json
    processed_values = process_values_yaml(values_yaml, schema_json)

    # Generate the table rows for the values.yaml
    table_rows = generate_table_rows(processed_values)

    # Generate the supported features table
    supported_features = generate_supported_features_table(schema_json)

    # Create a Jinja2 template object
    template = Template(html_template)

    # Fill in the template with data
    html_output = template.render(version=current_version, prev_version=previous_version, table_rows=table_rows, features=supported_features)

    # Output the HTML content to a file
    output_file = f"docs/pages/versions/{current_version}.html"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as file:
        file.write(html_output)

    print(f"Version page generated at {output_file}")

# Run the script
if __name__ == "__main__":
    main()
