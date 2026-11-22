"""TikToks de Sciences économiques L1 AES (Toulouse Capitole) en FRANCÉS. Voz gratis fr-FR-DeniseNeural (tts_gratis.py con VOZ=fr-FR-DeniseNeural VOZ_RATE=-10%).
Uso: python3 generar_specs_eco.py → specs/eco/*.json"""
import json, os

def A(i, l1, l2, st=None):
    v = {"tipo": "alerta", "icono": i, "linea1": l1, "linea2": l2}
    if st: v["stamp"] = st
    return v
def F(*filas, st=None):
    v = {"tipo": "filas", "filas": [{"icono": f[0], "izq": f[1], "der": f[2], **({"rojo": True} if len(f) > 3 and f[3] else {})} for f in filas]}
    if st: v["stamp"] = st
    return v
def B(big, small, st=None):
    v = {"tipo": "big", "big": big, "small": small}
    if st: v["stamp"] = st
    return v
def S(tag, sub, titulo, visual, num=None):
    s = {"tag": tag, "sub": sub, "titulo": titulo, "visual": visual}
    if num: s["num"] = num
    return s

C, R, RT = "la curiosité", "en résumé", "EN *RÉSUMÉ*"
PRON = {"Qd": "ku de", "Qs": "ku esse", "RT": "erre té", "AES": "a eu esse", "p": "prix"}
V = []
def vid(id, titulo, texto, tema, etiqueta, segs, pron=None):
    p = dict(PRON); p.update(pron or {})
    V.append({"id": "eco-" + id, "titulo": titulo, "texto": texto, "tema": tema, "etiqueta": etiqueta, "examen": "Partiel",
              "pron": p, "voz": "gratis", "segmentos": segs})

OD, EL, MA = "Sciences éco · Offre et demande", "Sciences éco · Élasticité", "Sciences éco · Marché"

vid("sur-ou-de-la-droite", "Sur la droite ou de la droite ?", "Deux déplacements, deux causes", OD, "demande", [
  S(C, "Tu savais que sur un graphique d'offre et de demande... une courbe peut *bouger* de deux façons très différentes ?", "DEUX FAÇONS DE *BOUGER*", A("📈", "une courbe, deux mouvements", "SUR OU DE ?")),
  S("sur la droite", "Si c'est le *prix du bien* qui change... on glisse le long de la courbe. La courbe, elle, ne bouge pas.", "SUR LA *DROITE*",
    A("↘️", "le prix du lait baisse", "ON GLISSE", "PRIX"), 1),
  S("de la droite", "Si c'est *autre chose* qui change... revenu, goûts, publicité... alors toute la courbe se déplace.", "DE LA *DROITE*",
    A("↔️", "revenu, goûts, publicité", "LA COURBE BOUGE", "AUTRE CHOSE"), 2),
  S("l'astuce", "Droite qui va vers la *droite*... la demande augmente. Vers la *gauche*... elle baisse. À chaque prix.", "DROITE OU *GAUCHE*",
    F(("➡️", "vers la droite", "demande ↑"), ("⬅️", "vers la gauche", "demande ↓", True)), 3),
  S("la règle", "Retiens : *toujours* le prix du bien, c'est un glissement. *Jamais* un autre facteur ne fait glisser, il déplace la courbe.", "LA *RÈGLE*",
    F(("💶", "prix du bien", "GLISSEMENT"), ("🧩", "autre déterminant", "DÉPLACEMENT", True)), 4),
  S(R, "Voilà. Le prix du bien : on glisse *sur* la droite. Tout le reste : la droite se *déplace.*", RT,
    F(("💶", "prix du bien", "SUR la droite"), ("🧩", "tout le reste", "DE la droite", True))),
])

vid("substituts-complementaires", "Substituts ou complémentaires ?", "Quand le prix d'un bien bouge la demande d'un autre", OD, "demande", [
  S(C, "Tu savais que le prix des *céréales* peut changer la demande de... *lait ?*", "LE PRIX D'UN *AUTRE* BIEN", A("🥣", "céréales et lait", "LIEN CACHÉ")),
  S("complémentaires", "Les céréales et le lait, on les consomme *ensemble.* Ce sont des biens complémentaires.", "LES *COMPLÉMENTAIRES*",
    A("🥛", "lait + céréales", "ENSEMBLE"), 1),
  S("l'effet", "Si le prix des céréales *baisse*... on en achète plus... et on demande plus de *lait.* La courbe de demande se déplace.", "PRIX ↓ DEMANDE ↑",
    F(("🥣", "céréales moins chères", "lait ↑")), 2),
  S("substituts", "Le lait et le jus d'orange, eux, répondent à la même envie. Ce sont des *substituts.*", "LES *SUBSTITUTS*",
    A("🍊", "lait / jus d'orange", "MÊME ENVIE"), 3),
  S("l'effet inverse", "Si le jus d'orange devient plus *cher*... on se rabat sur le lait. Sa demande *augmente.*", "ORANGE ↑ LAIT ↑",
    F(("🍊", "jus d'orange plus cher", "lait ↑", True)), 4),
  S(R, "Voilà. Complémentaires : *même* sens. Substituts : sens *opposé* pour le prix qui monte... et la demande de l'autre.", RT,
    F(("🥣", "complémentaires", "prix ↓ → demande ↑"), ("🍊", "substituts", "prix ↑ → demande ↑", True))),
])

vid("penurie-ou-exces", "Pénurie ou excédent ?", "Comment le prix revient tout seul à l'équilibre", MA, "équilibre", [
  S(C, "Tu savais que sur un marché... *personne* ne fixe le prix d'équilibre ? Il se trouve tout seul.", "L'ÉQUILIBRE *TOUT SEUL*", A("⚖️", "un seul point d'équilibre", "OFFRE = DEMANDE")),
  S("l'équilibre", "À l'équilibre, l'offre et la demande se *compensent.* Aucune force ne pousse au changement.", "OFFRE *=* DEMANDE",
    B("Qs = Qd", "prix d'équilibre + quantité d'équilibre"), 1),
  S("l'excédent", "Prix trop *haut* : les vendeurs ne vendent pas tout. Les stocks montent... alors le prix *baisse.*", "L'*EXCÉDENT*",
    F(("📦", "offre > demande", "stocks ↑"), ("⬇️", "résultat", "le prix baisse", True)), 2),
  S("la pénurie", "Prix trop *bas* : les acheteurs n'ont pas tout ce qu'ils veulent. Le prix *monte.*", "LA *PÉNURIE*",
    F(("🛒", "offre < demande", "rayons vides"), ("⬆️", "résultat", "le prix monte", True)), 3),
  S("le calcul", "Pour trouver l'équilibre, on pose *Qs égale Qd.* On résout... et on trouve le prix, puis la quantité.", "POSE *Qs = Qd*",
    B("Qs = Qd", "on résout pour p"), 4),
  S(R, "Voilà. Excédent : le prix *baisse.* Pénurie : le prix *monte.* Et à l'équilibre, plus rien ne bouge.", RT,
    F(("📦", "excédent", "prix ↓"), ("🛒", "pénurie", "prix ↑", True))),
])

vid("statique-comparative", "Choc sur le marché : mode d'emploi", "La méthode en 3 étapes", MA, "équilibre", [
  S(C, "Tu savais qu'un été très *chaud* fait monter le prix du lait ? Et il existe une méthode en *trois étapes* pour le prouver.", "LA STATIQUE *COMPARATIVE*", A("☀️", "un choc externe", "3 ÉTAPES")),
  S("étape 1", "Étape un : le choc touche *quoi ?* L'offre, la demande... ou les deux ?", "ÉTAPE *1*",
    F(("🔍", "qui est touché ?", "offre ou demande"))  , 1),
  S("étape 2", "Étape deux : la courbe va vers la *droite* ou vers la *gauche ?*", "ÉTAPE *2*",
    F(("↔️", "quelle direction ?", "droite ou gauche")), 2),
  S("la chaleur", "L'été chaud : on veut plus de glaces et de produits laitiers. La *demande* se déplace vers la droite. Le prix *monte*... et la quantité *aussi.*", "UN ÉTÉ *CHAUD*",
    F(("☀️", "demande vers la droite", "P ↑ Q ↑", True)), 3),
  S("la sécheresse", "Une sécheresse : la nourriture du bétail coûte plus cher. C'est l'*offre* qui va vers la gauche. Le prix *monte*... mais la quantité *baisse.*", "UNE *SÉCHERESSE*",
    F(("🌵", "offre vers la gauche", "P ↑ Q ↓", True)), 4),
  S(R, "Voilà. Demande à droite : prix *et* quantité montent. Offre à gauche : le prix monte, la quantité *baisse.*", RT,
    F(("☀️", "demande →", "P ↑ Q ↑"), ("🌵", "offre ←", "P ↑ Q ↓", True))),
])

vid("point-milieu", "Le piège du point-milieu", "Pourquoi A→B et B→A ne donnent pas pareil", EL, "élasticité", [
  S(C, "Tu savais que l'élasticité entre deux points... n'est *pas la même* dans un sens et dans l'autre ?", "LE *PIÈGE*", A("🔀", "de A vers B, ou de B vers A", "DEUX RÉSULTATS")),
  S("l'exemple", "Prix de quatre à six euros. Quantité de cent vingt à quatre-vingts. De A vers B on trouve environ *zéro virgule soixante-six.*", "A *→* B",
    B("≈ 0,66", "de A (4 €) vers B (6 €)"), 1),
  S("le problème", "Mais de B vers A... on trouve *un virgule cinq.* Pourtant ce sont les mêmes deux points !", "B *→* A",
    B("1,5", "de B (6 €) vers A (4 €)", "PAS PAREIL !"), 2),
  S("la solution", "La solution : le *point-milieu.* On divise la variation non pas par la valeur de départ, mais par la *moyenne* des deux valeurs.", "LE *POINT-MILIEU*",
    A("🎯", "diviser par la moyenne", "PAS LA VALEUR DE DÉPART"), 3),
  S("le résultat", "Prix moyen : cinq. Quantité moyenne : cent. On trouve *un*, dans les deux sens. Problème réglé.", "RÉSULTAT : *1*",
    B("1", "dans les deux sens"), 4),
  S(R, "Voilà. Point-milieu : on divise par la *moyenne.* Résultat identique de A vers B... et de B vers A.", RT,
    A("🎯", "variation ÷ moyenne", "MÊME RÉSULTAT")),
])

vid("recette-totale", "Augmenter le prix : bonne idée ?", "Recette totale et élasticité", EL, "élasticité", [
  S(C, "Tu savais qu'augmenter ses prix peut faire *gagner* de l'argent... ou en faire *perdre* ? Tout dépend de l'élasticité.", "PRIX ↑ = *GAIN ?*", A("💰", "recette = prix × quantité", "ÇA DÉPEND")),
  S("la recette", "La recette totale, c'est le prix *multiplié* par la quantité vendue. Si le prix monte, la quantité baisse. Qui gagne ?", "RECETTE *TOTALE*",
    B("RT = p × Q", "prix fois quantité vendue"), 1),
  S("inélastique", "Demande *inélastique*, plus petite que un : les clients partent peu. La quantité baisse *moins vite* que le prix monte. La recette *augmente.*", "INÉLASTIQUE *< 1*",
    F(("🍞", "pain, lait, tabac", "prix ↑ → RT ↑", True)), 2),
  S("élastique", "Demande *élastique*, plus grande que un : les clients fuient. La quantité baisse *plus vite.* La recette *diminue.*", "ÉLASTIQUE *> 1*",
    F(("🛋️", "meubles, voitures", "prix ↑ → RT ↓", True)), 3),
  S("unitaire", "Et si l'élasticité vaut exactement *un* ? La recette ne bouge *pas.*", "UNITAIRE *= 1*",
    B("= 1", "la recette ne bouge pas"), 4),
  S(R, "Voilà. Inélastique : prix et recette vont dans le *même* sens. Élastique : dans des sens *opposés.*", RT,
    F(("🍞", "inélastique < 1", "même sens"), ("🛋️", "élastique > 1", "sens opposés", True))),
])

vid("determinants-elasticite", "Pourquoi le beurre est plus élastique que les œufs", "Les déterminants de l'élasticité", EL, "élasticité", [
  S(C, "Tu savais que si le beurre augmente, on passe à la *margarine*... mais si les œufs augmentent, on les achète quand même ?", "BEURRE *VS* ŒUFS", A("🧈", "même hausse de prix", "DEUX RÉACTIONS")),
  S("substituts proches", "Le beurre a un substitut *proche :* la margarine. Facile de changer. Sa demande est plus *élastique.*", "SUBSTITUTS *PROCHES*",
    F(("🧈", "beurre + margarine", "plus élastique", True), ("🥚", "œufs sans substitut", "moins élastique")), 1),
  S("essentiels", "Les biens *essentiels*, comme le gaz ou l'électricité : on en a besoin. La demande baisse *peu.* Elle est plutôt *inélastique.*", "BIENS *ESSENTIELS*",
    A("🔥", "gaz, électricité", "INÉLASTIQUE"), 2),
  S("marché étroit", "Plus le marché est défini *étroitement*, plus la demande est élastique. Les glaces sont plus élastiques que *la nourriture.*", "MARCHÉ *ÉTROIT*",
    F(("🍦", "glaces", "très élastique", True), ("🍽️", "nourriture", "peu élastique")), 3),
  S("le temps", "Et le *temps* compte. Si l'essence augmente, au début on change peu. Au bout de quelques années, on achète des voitures économes. L'élasticité *monte.*", "LE *TEMPS*",
    F(("⏳", "court terme", "peu élastique"), ("📅", "long terme", "très élastique", True)), 4),
  S(R, "Voilà. Plus de substituts, un marché étroit, plus de temps... et la demande devient *plus élastique.*", RT,
    A("📈", "substituts · marché étroit · temps", "PLUS ÉLASTIQUE")),
])

vid("elasticite-revenu-croisee", "Normal, de luxe ou inférieur ?", "Élasticité-revenu et élasticité croisée", EL, "élasticité", [
  S(C, "Tu savais qu'il existe des biens que tu achètes *moins*... quand ton revenu *monte ?*", "LES BIENS *INFÉRIEURS*", A("🚌", "revenu ↑", "DEMANDE ↓")),
  S("biens normaux", "La plupart des biens sont *normaux :* quand ton revenu monte, tu en achètes plus. L'élasticité-revenu est *positive.*", "BIENS *NORMAUX*",
    F(("👕", "première nécessité", "positive mais faible"), ("💎", "luxe : caviar, diamants", "positive et élevée", True)), 1),
  S("biens inférieurs", "Les biens *inférieurs*, comme le bus : plus tu gagnes, moins tu en consommes. L'élasticité-revenu est *négative.*", "BIENS *INFÉRIEURS*",
    A("🚌", "trajets en bus", "ÉLASTICITÉ NÉGATIVE"), 2),
  S("l'élasticité croisée", "Autre mesure : l'élasticité-prix *croisée.* C'est la réaction de la demande d'un bien... quand le prix d'un *autre* bien change.", "ÉLASTICITÉ *CROISÉE*",
    A("🔗", "le prix de l'autre bien", "ET MA DEMANDE"), 3),
  S("substituts", "Pour des *substituts*, elle est positive. Les pommes augmentent... et tu manges plus de *poires.*", "SUBSTITUTS *+*",
    F(("🍎", "pommes plus chères", "poires ↑", True)), 4),
  S(R, "Voilà. Bien normal : élasticité-revenu *positive.* Bien inférieur : *négative.* Substituts : élasticité croisée *positive.*", RT,
    F(("👕", "bien normal", "revenu + "), ("🚌", "bien inférieur", "revenu −", True))),
])

os.makedirs(os.path.join(os.path.dirname(__file__), "eco"), exist_ok=True)
for v in V:
    json.dump(v, open(os.path.join(os.path.dirname(__file__), "eco", v["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
print(len(V), "specs")
