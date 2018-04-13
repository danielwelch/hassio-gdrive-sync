import argparse

from jinja2 import Template


def main(client_id, secret):
    print("[Info] Saving client ID and secret to /settings.yaml...")
    with open('/settings.template', 'r') as t:
        template = Template(t.read())
        with open('/settings.yaml', 'w') as out:
            out.write(
                template.render(client_id=client_id, client_secret=secret))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Write client id and secret to jinja template.')
    parser.add_argument('id', type=str, help='Client ID')
    parser.add_argument('secret', type=str, help='Client secret')
    args = parser.parse_args()
    main(args.id, args.secret)
