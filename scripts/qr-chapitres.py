#!/usr/bin/env python3
"""Genere un QR code par chapitre, pointant vers la branche correspondante.

Sortie en **SVG vectoriel** : un QR code destine a l'impression ne doit jamais
etre une image matricielle, sinon il se pixellise et devient illisible au
scanner selon la taille de reproduction.

    python3 scripts/qr-chapitres.py mon-compte escale-livre
    python3 scripts/qr-chapitres.py mon-compte escale-livre --sortie qr/

Chaque fichier produit :
    qr/ch01.svg  ->  https://github.com/<compte>/<depot>/tree/ch01
    qr/depot.svg ->  https://github.com/<compte>/<depot>
"""
from __future__ import annotations

import argparse
import pathlib

import qrcode
import qrcode.image.svg

CHAPITRES = {
    "ch01": "Pourquoi les conteneurs ?",
    "ch02": "Construire des images Docker",
    "ch03": "Stockage, reseaux et donnees",
    "ch04": "Docker Compose et applications multi-conteneurs",
    "ch05": "Introduction a Kubernetes",
    "ch06": "Deployer une application sur Kubernetes",
    "ch07": "Configuration et donnees dans Kubernetes",
    "ch08": "Exposition des applications et trafic reseau",
    "ch09": "Deploiement avance et industrialisation",
    "ch10": "Monitoring et observabilite",
    "ch11": "Securite des conteneurs et de Kubernetes",
    "ch12": "CI/CD et deploiement automatise",
    "ch13": "Bonnes pratiques et projet final",
}


def generer(url: str, chemin: pathlib.Path, taille_mm: float = 22.0) -> int:
    """Un QR imprime dans un livre doit tolerer l'encre qui bave et le papier
    qui jaunit : correction d'erreur haute (30 % de redondance) et marge
    silencieuse de 4 modules, conformement a la norme."""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    image = qr.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    image.save(str(chemin))

    # Taille physique imposee : le SVG doit s'imprimer a la dimension voulue,
    # independamment du logiciel de mise en page.
    import re
    contenu = chemin.read_text()
    # La bibliotheque impose sa propre taille : on la remplace, on ne l'empile pas.
    contenu = re.sub(r'width="[^"]*"\s+height="[^"]*"',
                     f'width="{taille_mm}mm" height="{taille_mm}mm"', contenu, count=1)
    chemin.write_text(contenu)
    return qr.version


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("compte", help="compte ou organisation GitHub")
    p.add_argument("depot", nargs="?", default="escale-livre")
    p.add_argument("--sortie", default="qr", help="repertoire de sortie")
    p.add_argument("--taille-mm", type=float, default=22.0,
                   help="taille imprimee, en millimetres (22 mm recommande)")
    p.add_argument("--branche-index", default="main",
                   help="branche portant les fiches de chapitre")
    p.add_argument("--vers-branche", action="store_true",
                   help="viser l arborescence de la branche plutot que la fiche")
    args = p.parse_args()

    base = f"https://github.com/{args.compte}/{args.depot}"
    sortie = pathlib.Path(args.sortie)
    sortie.mkdir(parents=True, exist_ok=True)

    version = generer(base, sortie / "depot.svg", args.taille_mm)
    print(f"{'fichier':14} {'version':>7}  cible")
    print("-" * 76)
    print(f"{'depot.svg':14} {version:>7}  {base}")

    lignes = ["| Ch. | Titre | Branche | QR |", "|---|---|---|---|"]
    for branche, titre in CHAPITRES.items():
        # La fiche du chapitre, et non l arborescence brute : elle indique ce que
        # le chapitre ajoute, les commandes cles et les points de controle, et
        # elle renvoie vers la branche. C est la bonne porte d entree.
        url = (f"{base}/tree/{branche}" if args.vers_branche
               else f"{base}/tree/{args.branche_index}/chapitres/{branche}")
        version = generer(url, sortie / f"{branche}.svg", args.taille_mm)
        print(f"{branche + '.svg':14} {version:>7}  {url}")
        lignes.append(f"| {branche[2:]} | {titre} | `{branche}` | `qr/{branche}.svg` |")

    (sortie / "INDEX.md").write_text(
        "# QR codes par chapitre\n\n"
        f"Depot : {base}\n\n"
        "Chaque QR code pointe vers la **fiche du chapitre** : ce que le chapitre\n"
        "ajoute au depot, les commandes cles, les points de controle, et un lien\n"
        "vers la branche correspondante. Le lecteur arrive oriente, et non devant\n"
        "une arborescence de fichiers.\n\n"
        "Option `--vers-branche` pour viser directement l arborescence.\n\n"
        "**A placer en ouverture de chapitre**, en marge exterieure, a 22 mm de\n"
        "cote. Format SVG vectoriel : ne jamais convertir en JPEG.\n\n"
        + "\n".join(lignes) + "\n"
    )
    print("-" * 76)
    print(f"{len(CHAPITRES) + 1} QR codes SVG dans {sortie}/ — index dans {sortie}/INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
