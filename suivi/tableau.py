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
    """Après fetch, tout se lit sur le dépôt distant (origin/main et branches tache/*), jamais dans la copie de
    travail, qui peut être en retard ou sur une autre branche ; --sans-fetch lit la copie de travail."""
    if fetch:
        C.fetch()
        lire = lambda chemin: C.montrer("origin/main", chemin)
        ref, source = "origin/main", "instantané du dépôt distant (origin/main et branches)"
    else:
        lire = lambda chemin: (C.RACINE / chemin).read_text(encoding="utf-8") if (C.RACINE / chemin).exists() else None
        ref, source = "HEAD", "instantané de la copie de travail locale"
    suivi = lire("SUIVI.md") or ""
    S = C.lire_suivi(suivi)
    dist = C.branches_distantes()
    fiches, rapports, verdicts, ajoutees = {}, {}, {}, {}
    for uid, u in S["unites"].items():
        br = C.branche_de(u)
        if br in dist:
            fiches[uid] = filtrer(C.montrer("origin/" + br, u["fiche"]))
            rapports[uid] = C.montrer("origin/" + br, f"rapports/{uid}.md")
            t = C.lire_rapport(rapports[uid])["tentative"]
            verdicts[uid] = C.montrer("origin/" + br, f"rapports/{uid}-verif-{t}.md")
        else:
            fiches[uid] = filtrer(lire(u["fiche"]))
        if not u["coche"] and not C.deps_reelles(S, uid):
            d = C.ligne_ajoutee_le(uid, ref)
            if d:
                ajoutees[uid] = C.horodatage(d)
    verrou = None
    if fetch:
        import travail
        e = travail.etat_verrou()
        verrou = e["message"] if e else None
    return dict(depot=C.DEPOT, genere=C.horodatage() + " UTC", source=source,
                suivi=suivi, fiches=fiches, rapports=rapports, verdicts=verdicts, ajoutees=ajoutees, branches=sorted(dist),
                verrou=verrou, arret=lire("rapports/ARRET.md"), prompt_creneau=prompt_creneau())


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
