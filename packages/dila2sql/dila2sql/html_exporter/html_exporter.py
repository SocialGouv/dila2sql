from jinja2 import Environment, PackageLoader, select_autoescape
from tqdm import tqdm
from argparse import ArgumentParser
import pathlib
import datetime
from dila2sql.monitoring import init_monitoring
import requests
init_monitoring()

DEFAULT_API_URL = "https://api.dila2sql.num.social.gouv.fr"
DEFAULT_OUTPUT_DIR = "/var/lib/dila2sql/generated_dumps"

CONTENEURS_PATH = "v1/base/KALI/conteneurs?active=true"
TEXTES_PATH = "v1/base/KALI/conteneur/%s/textes/%s"
TEXTE_PATH = "v1/base/KALI/texte/%s"


class HtmlExporter:

    def __init__(self, api_url, output_dir):
        self.api_url = api_url
        self.output_dir = output_dir
        self.jinja_env = Environment(
            loader=PackageLoader('dila2sql.html_exporter', 'templates'),
            autoescape=select_autoescape(['html'])
        )
        self.conteneur_template = self.jinja_env.get_template('conteneur.html')
        super()

    def run(self):
        self.build_output_path()
        self.export_all_conteneurs()

    def build_output_path(self):
        output_path = pathlib.Path(self.output_dir) / datetime.datetime.now().strftime("%Y-%m-%d")
        self.html_path = pathlib.Path(output_path) / 'exports_html'
        self.html_path.mkdir(parents=True, exist_ok=True)
        return self.html_path

    def export_all_conteneurs(self):
        conteneurs_url = f"{self.api_url}/{CONTENEURS_PATH}"
        conteneurs = requests.get(conteneurs_url).json()
        conteneurs.reverse()
        for conteneur in tqdm(conteneurs):
            self.export_conteneur_to_html(conteneur)

    def export_conteneur_to_html(self, conteneur):
        html_file = open(self.html_path / ('convention_%s.html' % conteneur["num"]), 'w')
        textes_by_type = {
            "base": self.get_textes("base", conteneur),
            "attaches": self.get_textes("attaches", conteneur),
            "salaires": self.get_textes("salaires", conteneur)
        }
        res = self.conteneur_template.render(
            conteneur=conteneur,
            textes_by_type=textes_by_type
        )
        html_file.write(res)
        html_file.close()

    def get_textes(self, type_texte, conteneur):
        textes_url = f"{self.api_url}/{TEXTES_PATH % (conteneur['id'], type_texte)}"
        all_textes = requests.get(textes_url).json()["textes"]
        textes_vigueur = [t for t in all_textes if t["etat"].startswith("VIGUEUR")]
        return [self.get_texte(t["id"]) for t in textes_vigueur]

    def get_texte(self, texte_id):
        texte_url = f"{self.api_url}/{TEXTE_PATH % texte_id}"
        return requests.get(texte_url).json()


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('--api-url', default=DEFAULT_API_URL)
    p.add_argument('--output-dir', default=DEFAULT_OUTPUT_DIR)
    args = p.parse_args()
    HtmlExporter(args.api_url, args.output_dir).run()
