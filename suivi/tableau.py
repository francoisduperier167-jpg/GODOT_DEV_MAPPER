"""Tableau de bord : suivi/tableau.html, instantané de SUIVI.md, des fiches et des branches tache/*.

La page relit elle-même SUIVI.md et les branches sur GitHub quand on clique « Actualiser » (page ouverte
depuis une copie du dépôt ; dans claude.ai, le cadre de la page bloque l'accès à GitHub).
"""
import datetime
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


def collecter(fetch=True, ref="origin/main"):
    """Tout se lit dans Git, de façon cohérente : SUIVI.md, les fiches sans branche et ARRET.md sur ref (origin/main
    par défaut), les branches tache/* et le verrou sur le dépôt distant, d'après le dernier fetch (fait ici, sauf
    --sans-fetch). La copie de travail, qui peut être en retard ou sur une autre branche, n'est jamais lue."""
    if fetch:
        C.fetch()
    lire = lambda chemin: C.montrer(ref, chemin)
    suivi = lire("SUIVI.md") or ""
    S = C.lire_suivi(suivi)
    dist = C.branches_distantes()
    fiches, rapports, verdicts = {}, {}, {}
    for uid, u in S["unites"].items():
        br = C.branche_de(u)
        if br in dist:
            fiches[uid] = filtrer(C.montrer("origin/" + br, u["fiche"]))
            rapports[uid] = C.montrer("origin/" + br, f"rapports/{uid}.md")
            t = C.lire_rapport(rapports[uid])["tentative"]
            verdicts[uid] = C.montrer("origin/" + br, f"rapports/{uid}-verif-{t}.md")
        else:
            fiches[uid] = filtrer(lire(u["fiche"]))
    if fetch:
        import travail
        e = travail.etat_verrou()
        verrou = e["message"] if e else None
    else:
        p = C.git("log", "-1", "--format=%s", "refs/remotes/origin/verrou/main", check=False)
        verrou = p.stdout.strip() if p.returncode == 0 and p.stdout.strip() else None
    fh = pathlib.Path(C.git("rev-parse", "--path-format=absolute", "--git-common-dir", check=False).stdout.strip() or ".") / "FETCH_HEAD"
    quand = C.horodatage(datetime.datetime.fromtimestamp(fh.stat().st_mtime, datetime.timezone.utc)) + " UTC" if fh.exists() else ""
    source = (f"{ref} et branches du dépôt distant, " + ("lus maintenant" if fetch else f"d'après le dernier fetch{' (' + quand + ')' if quand else ''}"))
    return dict(depot=C.DEPOT, genere=C.horodatage() + " UTC", source=source,
                suivi=suivi, fiches=fiches, rapports=rapports, verdicts=verdicts, branches=sorted(dist),
                verrou=verrou, arret=lire("rapports/ARRET.md"), prompt_creneau=prompt_creneau(),
                abandon_h=C.ABANDON_H, relais_h=C.RELAIS_H, verrou_min=C.VERROU_MIN)


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


def ecrire(fetch=True, sortie=None, ref="origin/main"):
    d = collecter(fetch, ref)
    p = pathlib.Path(sortie) if sortie else SORTIE
    fragment = p.name.endswith("-fragment.html")
    p.write_text(page(d, fragment), encoding="utf-8")
    print(f"{p} écrit : {len(C.lire_suivi(d['suivi'])['unites'])} unités, {len([b for b in d['branches'] if b.startswith('tache/')])} branches de tâche, "
          f"{len(p.read_bytes()) // 1024} Ko")
