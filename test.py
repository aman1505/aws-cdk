import yaml

with open(f"config/dev.yaml", 'r') as stream:
            try:
                a = yaml.safe_load(stream)
                print(a["modules"][0]["stack_name"])
            except yaml.YAMLError as exc:
                print(exc)