"""Calendrier simulé : fin du POC, du MVP et de la V1 d'après SUIVI.md, les rôles, les prérequis et les estimations.

Modèle (docs/construction/sequence.md §8) :
- six créneaux par jour, de 2 h, entre 8 h et 20 h ; chaque IA en a deux ;
- « rotation » : IA 1, IA 2, IA 3, IA 1, IA 2, IA 3, l'une après l'autre ; « simultané » : les trois IA travaillent en
  même temps, à 8 h et à 14 h (même nombre de créneaux par jour) ;
- un créneau fait au plus une vérification (fusion comprise), puis une réalisation d'un créneau de travail ;
- l'ordre de choix est celui de `outil.py etat` : vérifications, reprises, unités prêtes de son rôle, relais ;
- relais : une unité prête ou terminée depuis 12 h peut être prise par une autre IA (jamais vérifiée par un auteur) ;
- reprises : avec un ratio de 1,5, une unité sur deux est refusée une fois (un créneau de correction de plus et une
  seconde vérification) ;
- pas d'abandon, pas d'attente du verrou de main, pas de quota.
"""
import re

import commun as C

JALONS = (("POC", "S35"), ("MVP", "S41.P"), ("V1", "S49.P"))


def estimation(u):
    p = C.RACINE / u["fiche"]
    if p.exists():
        m = re.search(r"\| Estimation \| (\d+) créneau", p.read_text(encoding="utf-8"))
        if m:
            return int(m.group(1))
    return 1


def simuler(S, mode="rotation", ratio=1.0, relais_h=C.RELAIS_H, jours_max=400):
    ids = [x for x in S["unites"] if not re.search(r"\.c\d+$", x)]
    deps = {x: C.deps_reelles(S, x) for x in ids}
    U = {}
    for i, x in enumerate(ids):
        u = S["unites"][x]
        U[x] = dict(r=u["r"], v=u["v"], reste=estimation(u), refus=1 if (ratio > 1.0 and i % 2 == 1) else 0,
                    etat="attente", auteurs=[], pret=None, fin=None, fait=None, rang=i)
    fini_le = {}

    def maj_pretes(t):
        for x in ids:
            if U[x]["etat"] == "attente" and all(U[d]["etat"] == "faite" for d in deps[x] if d in U):
                U[x]["etat"], U[x]["pret"] = "prete", t

    def creneau(ia, t, t_fin, jour):
        """Une IA, un créneau : une vérification, puis un créneau de réalisation. Effets visibles à t_fin."""
        effets = []
        cand = [x for x in ids if U[x]["etat"] == "a_verifier" and ia not in U[x]["auteurs"]]
        cand = [x for x in cand if U[x]["v"] == ia or U[x]["v"] in U[x]["auteurs"] or t - U[x]["fin"] >= relais_h]
        cand.sort(key=lambda x: (U[x]["v"] != ia and U[x]["v"] not in U[x]["auteurs"], U[x]["rang"]))
        if cand:
            x = cand[0]
            U[x]["etat"] = "en_verification"
            if U[x]["refus"]:
                effets.append((x, "refusee"))
            else:
                effets.append((x, "faite"))
        travail = None
        for x in ids:
            if U[x]["etat"] in ("en_cours", "refusee") and ia in U[x]["auteurs"]:
                travail = x
                break
        if travail is None:
            pretes = [x for x in ids if U[x]["etat"] == "prete" and (U[x]["r"] == ia or t - U[x]["pret"] >= relais_h)]
            pretes.sort(key=lambda x: (U[x]["r"] != ia, U[x]["rang"]))
            if pretes:
                travail = pretes[0]
        if travail is not None:
            x = travail
            if ia not in U[x]["auteurs"]:
                U[x]["auteurs"].append(ia)
            if U[x]["etat"] == "refusee":
                U[x]["refus"], U[x]["reste"] = 0, 1
            U[x]["etat"] = "en_cours"
            U[x]["reste"] -= 1
            if U[x]["reste"] <= 0:
                U[x]["etat"] = "en_travail"
                effets.append((x, "a_verifier"))
        return effets

    def appliquer(effets, t_fin, jour):
        for x, e in effets:
            U[x]["etat"] = e
            if e == "a_verifier":
                U[x]["fin"] = t_fin
            if e == "faite":
                U[x]["fait"] = jour
                fini_le[x] = jour

    maj_pretes(0)
    for jour in range(1, jours_max + 1):
        base = (jour - 1) * 24
        if mode == "rotation":
            for j in range(6):
                t = base + 8 + 2 * j
                appliquer(creneau(j % 3 + 1, t, t + 2, jour), t + 2, jour)
                maj_pretes(t + 2)
        else:
            for j in range(2):
                t = base + 8 + 6 * j
                effets = []
                for ia in (1, 2, 3):
                    effets += creneau(ia, t, t + 2, jour)
                appliquer(effets, t + 2, jour)
                maj_pretes(t + 2)
        if all(U[x]["etat"] == "faite" for x in ids):
            break
    return {nom: fini_le.get(uid) for nom, uid in JALONS}, sum(estimation(S["unites"][x]) for x in ids)


def calendrier(mode=None, ratio=None, relais_h=C.RELAIS_H):
    S = C.lire_suivi((C.RACINE / "SUIVI.md").read_text(encoding="utf-8"))
    modes = [mode] if mode else ["rotation", "simultane"]
    ratios = [ratio] if ratio else [1.0, 1.5]
    print(f"Calendrier simulé d'après SUIVI.md ({len(S['unites'])} unités), relais à {relais_h} h, six créneaux par jour.")
    print("Fin estimée (jour où le jalon est fusionné) :\n")
    print("| Organisation | Reprises | POC (S35) | MVP (S41.P) | V1 (S49.P) |")
    print("| --- | --- | --- | --- | --- |")
    for m in modes:
        for r in ratios:
            fins, _ = simuler(S, m, r, relais_h)
            nom = "IA l'une après l'autre" if m == "rotation" else "trois IA en même temps, deux fois par jour"
            print(f"| {nom} | ratio {str(r).replace('.', ',')} | " + " | ".join(f"jour {fins[k]}" if fins[k] else "—" for k, _ in JALONS) + " |")
