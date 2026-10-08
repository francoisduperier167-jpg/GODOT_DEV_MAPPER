"""Tableau de bord : suivi/tableau.html, instantané de SUIVI.md, des fiches et des branches tache/*.

La page relit elle-même SUIVI.md et les branches sur GitHub quand on clique « Actualiser » (page ouverte
depuis une copie du dépôt ; dans claude.ai, le cadre de la page bloque l'accès à GitHub).
"""
import json
import pathlib
import re

import commun as C

MODELE = pathlib.Path(__file__).resolve().parent / "tableau_modele.html"
SORTIE = pathlib.Path(__file__).resolve().parent / "tableau.html"


def filtrer(t):
    return "\n".join(l for l in (t or "").splitlines() if C.RE_ETAPE.match(l))


def prompt_creneau():
    t = (C.RACINE / "docs" / "construction" / "sequence.md").read_text(encoding="utf-8")
    m = re.search(r"## 4\. Prompt de créneau.*?```text\n(.*?)```", t, re.S)
    return m.group(1) if m else ""


def collecter(fetch=True):
    if fetch:
        C.fetch()
    suivi = (C.RACINE / "SUIVI.md").read_text(encoding="utf-8")
    S = C.lire_suivi(suivi)
    dist = C.branches_distantes()
    fiches, rapports = {}, {}
    for uid, u in S["unites"].items():
        br = C.branche_de(u)
        if br in dist:
            fiches[uid] = filtrer(C.montrer("origin/" + br, u["fiche"]))
            rapports[uid] = C.montrer("origin/" + br, f"rapports/{uid}.md")
        else:
            p = C.RACINE / u["fiche"]
            fiches[uid] = filtrer(p.read_text(encoding="utf-8") if p.exists() else "")
    arret = C.RACINE / "rapports" / "ARRET.md"
    verrou = None
    if fetch:
        import travail
        e = travail.etat_verrou()
        verrou = e["message"] if e else None
    return dict(depot=C.DEPOT, genere=C.horodatage() + " UTC", source="instantané du dépôt",
                suivi=suivi, fiches=fiches, rapports=rapports, branches=sorted(dist),
                verrou=verrou, arret=arret.read_text(encoding="utf-8") if arret.exists() else None,
                prompt_creneau=prompt_creneau())


def page(donnees, fragment=False):
    m = MODELE.read_text(encoding="utf-8")
    js = json.dumps(donnees, ensure_ascii=False).replace("</", "<\\/")
    m = m.replace("/*DONNEES*/null", js)
    if fragment:
        return m.replace("<!--CORPS-->\n", "")
    tete, corps = m.split("<!--CORPS-->\n", 1)
    return ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + tete + "</head>\n<body>\n" + corps + "</body>\n</html>\n")


def ecrire(fetch=True, sortie=None):
    d = collecter(fetch)
    p = pathlib.Path(sortie) if sortie else SORTIE
    fragment = p.name.endswith("-fragment.html")
    p.write_text(page(d, fragment), encoding="utf-8")
    print(f"{p} écrit : {len(C.lire_suivi(d['suivi'])['unites'])} unités, {len([b for b in d['branches'] if b.startswith('tache/')])} branches de tâche, "
          f"{len(p.read_bytes()) // 1024} Ko")
