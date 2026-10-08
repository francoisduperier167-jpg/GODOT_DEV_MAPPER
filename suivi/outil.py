#!/usr/bin/env python3
"""Outil du mode autonome : suivi, trace des sous-étapes, accès simultané, tableau de bord.

Pour les IA, pendant un créneau (toujours avec ton numéro d'IA) :
    python3 suivi/outil.py etat --ia N                       ce que tu peux faire, par ordre de priorité
    python3 suivi/outil.py prendre Sxx --ia N                prendre ou reprendre une unité (coche R0)
    python3 suivi/outil.py prendre Sxx --ia N --verification prendre sa vérification (copie neuve, coche V1)
    python3 suivi/outil.py cocher Sxx R3 --ia N              cocher et signer une sous-étape, commit, push
    python3 suivi/outil.py cocher Sxx V8 --ia N --verdict ACCEPTÉE
    python3 suivi/outil.py fusionner Sxx --ia N [--godot B]  fusion sous le verrou de main (Godot trouvé seul sinon)
    python3 suivi/outil.py publier Sxx --ia N                pousser main, supprimer la branche, rendre le verrou
    python3 suivi/outil.py correction Sxx --fautive Syy --titre "…" --realise N --verifie M --ia N
    python3 suivi/outil.py arreter --ia N --raison "…" [--unite Sxx]   arrêt obligatoire : rapports/ARRET.md sur main
    python3 suivi/outil.py verrou etat | prendre --ia N --motif "…" | rendre --ia N

Pour la cohérence et l'affichage :
    python3 suivi/outil.py verifier                          cohérence de SUIVI.md et des fiches
    python3 suivi/outil.py generer [--force]                 régénère SUIVI.md et les fiches depuis le guide
    python3 suivi/outil.py tableau [--sans-fetch]            régénère suivi/tableau.html
    python3 suivi/outil.py calendrier                        fin estimée du POC, du MVP et de la V1, par simulation

Bibliothèque standard seulement. Règles : docs/construction/sequence.md.
"""
import argparse
import re
import sys
import pathlib

sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))


def numero_ia(v):
    m = re.fullmatch(r"(?i)\s*(?:ia\s*)?([123])\s*", v)
    if not m:
        raise argparse.ArgumentTypeError("numéro d'IA : 1, 2 ou 3")
    return int(m.group(1))


def main():
    ap = argparse.ArgumentParser(prog="python3 suivi/outil.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("verifier")
    g = sp.add_parser("generer")
    g.add_argument("--force", action="store_true")
    t = sp.add_parser("tableau")
    t.add_argument("--sans-fetch", action="store_true")
    t.add_argument("--sortie", default=None)
    e = sp.add_parser("etat")
    e.add_argument("--ia", type=numero_ia, required=True)
    p = sp.add_parser("prendre")
    p.add_argument("unite")
    p.add_argument("--ia", type=numero_ia, required=True)
    p.add_argument("--verification", action="store_true")
    c = sp.add_parser("cocher")
    c.add_argument("unite")
    c.add_argument("etape")
    c.add_argument("--ia", type=numero_ia, required=True)
    c.add_argument("--verdict", default=None)
    f = sp.add_parser("fusionner")
    f.add_argument("unite")
    f.add_argument("--ia", type=numero_ia, required=True)
    f.add_argument("--porte-ko", action="store_true")
    f.add_argument("--godot", default=None)
    pb = sp.add_parser("publier")
    pb.add_argument("unite")
    pb.add_argument("--ia", type=numero_ia, required=True)
    co = sp.add_parser("correction")
    co.add_argument("porte")
    co.add_argument("--fautive", required=True)
    co.add_argument("--titre", required=True)
    co.add_argument("--realise", type=numero_ia, required=True)
    co.add_argument("--verifie", type=numero_ia, required=True)
    co.add_argument("--ia", type=numero_ia, required=True)
    ar = sp.add_parser("arreter")
    ar.add_argument("--ia", type=numero_ia, required=True)
    ar.add_argument("--raison", required=True)
    ar.add_argument("--unite", default=None)
    ar.add_argument("--preuve", default=None)
    ar.add_argument("--humain", default=None, help="ce qu'il faut de l'humain")
    ca = sp.add_parser("calendrier")
    ca.add_argument("--mode", choices=["rotation", "simultane"], default=None)
    ca.add_argument("--ratio", type=float, default=None)
    ca.add_argument("--relais", type=float, default=None, help="heures avant relais (12 par défaut)")
    v = sp.add_parser("verrou")
    v.add_argument("action", choices=["etat", "prendre", "rendre"])
    v.add_argument("--ia", type=numero_ia)
    v.add_argument("--motif", default="écriture sur main")
    a = ap.parse_args()

    if a.cmd in ("verifier", "generer"):
        import generation
        if a.cmd == "generer":
            generation.generer(a.force)
        sys.exit(generation.verifier())
    if a.cmd == "tableau":
        import tableau
        tableau.ecrire(fetch=not a.sans_fetch, sortie=a.sortie)
        return
    if a.cmd == "calendrier":
        import calendrier
        import commun
        calendrier.calendrier(a.mode, a.ratio, a.relais if a.relais is not None else commun.RELAIS_H)
        return
    import travail
    if a.cmd == "etat":
        travail.etat(a.ia)
    elif a.cmd == "prendre":
        travail.prendre(a.unite, a.ia, a.verification)
    elif a.cmd == "cocher":
        travail.cocher(a.unite, a.etape, a.ia, a.verdict)
    elif a.cmd == "fusionner":
        travail.fusionner(a.unite, a.ia, a.porte_ko, a.godot)
    elif a.cmd == "publier":
        travail.publier(a.unite, a.ia)
    elif a.cmd == "correction":
        travail.correction(a.porte, a.fautive, a.titre, a.realise, a.verifie, a.ia)
    elif a.cmd == "arreter":
        travail.arreter(a.ia, a.raison, a.unite, a.preuve, a.humain)
    elif a.cmd == "verrou":
        if a.action != "etat" and a.ia is None:
            ap.error("verrou prendre et verrou rendre demandent --ia")
        travail.verrou(a.action, a.ia, a.motif)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
