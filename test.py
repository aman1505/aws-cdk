import yaml

with open(f"buildspec.yml", 'r') as stream:
            try:
                a = yaml.safe_load(stream)
                print(a)
            except yaml.YAMLError as exc:
                print(exc)