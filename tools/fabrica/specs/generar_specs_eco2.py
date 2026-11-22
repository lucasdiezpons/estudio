"""Tanda 2 TikToks Sciences éco (chap. 1 y 4). Uso: python3 generar_specs_eco2.py → specs/eco/*.json"""
import json, os
from generar_specs_eco import A, F, B, S, C, R, RT, vid, V, PRON
V.clear()
INT, MAC, ETA = "Sciences éco · Introduction", "Sciences éco · Macroéconomie", "Sciences éco · L'État"

vid("cout-opportunite", "Le coût d'opportunité", "Ce à quoi tu renonces vraiment", INT, "introduction", [
  S(C, "Tu savais que *rien* n'est gratuit en économie ? Même ce qui ne coûte pas un centime.", "RIEN N'EST *GRATUIT*", A("🎁", "même le gratuit", "A UN COÛT")),
  S("la définition", "Le coût d'opportunité, c'est *ce à quoi tu renonces* pour obtenir quelque chose.", "LE COÛT D'*OPPORTUNITÉ*",
    A("🔄", "ce à quoi tu renonces", "POUR OBTENIR AUTRE CHOSE"), 1),
  S("l'université", "Faire des études t'apporte un meilleur avenir. Mais ça te prive aussi d'un *emploi payé.* Ce salaire perdu fait partie du coût.", "LES *ÉTUDES*",
    F(("🎓", "bénéfice", "plus de métiers possibles"), ("💸", "coût d'opportunité", "le salaire perdu", True)), 2),
  S("l'autoroute", "Autre exemple : l'autoroute A69. Y renoncer fait perdre environ *vingt minutes* de trajet.", "L'*A69*",
    B("20 min", "le coût d'opportunité de l'abandon"), 3),
  S("la règle", "Retiens : un choix, c'est *toujours* un renoncement. Tu compares ce que tu gagnes... et ce que tu perds.", "TOUJOURS *UN RENONCEMENT*",
    F(("⚖️", "gagner", "bénéfices"), ("🕳️", "perdre", "coût d'opportunité", True)), 4),
  S(R, "Voilà. Coût d'opportunité : la valeur de *ce à quoi on renonce.* Pas ce qu'on paie... mais ce qu'on perd.", RT,
    A("🔄", "valeur de ce à quoi on renonce", "COÛT D'OPPORTUNITÉ")),
])

vid("raisonnement-marge", "Penser à la marge", "Pourquoi on s'arrête de manger des tomates", INT, "introduction", [
  S(C, "Tu savais que les économistes ne se demandent *jamais* : tout ou rien ? Ils se demandent : *un peu plus ?*", "PENSER *À LA MARGE*", A("🍅", "une tomate de plus ?", "OUI OU NON")),
  S("la marge", "On ne choisit presque jamais *tout ou rien.* On décide d'un peu plus... ou d'un peu moins.", "UN PEU *PLUS*",
    A("➕", "une unité en plus", "OU EN MOINS"), 1),
  S("les deux", "Chaque unité en plus a un *bénéfice marginal*, la satisfaction. Et un *coût marginal*, ce qu'elle coûte.", "BÉNÉFICE *VS* COÛT",
    F(("😋", "bénéfice marginal", "le gain de l'unité en plus"), ("💶", "coût marginal", "le coût de l'unité en plus", True)), 2),
  S("la règle", "Tant que le bénéfice dépasse le coût... on continue. On s'arrête quand les deux sont *égaux.*", "ON S'ARRÊTE QUAND *=*",
    B("Bm = Cm", "bénéfice marginal = coût marginal"), 3),
  S("l'exemple", "Pour les tomates : tu manges la suivante tant qu'elle te rapporte plus de plaisir que son prix. Dès que ce n'est plus le cas... *stop.*", "LES *TOMATES*",
    A("🍅", "plaisir de la dernière tomate", "= SON PRIX", "STOP"), 4),
  S(R, "Voilà. On choisit à la marge : on continue tant que le bénéfice marginal dépasse le coût marginal... et on s'arrête à *l'égalité.*", RT,
    B("Bm = Cm", "le point où on s'arrête")),
], {"Bm": "bénéfice marginal", "Cm": "coût marginal"})

vid("courbe-phillips", "La courbe de Phillips", "Inflation et chômage : l'arbitrage", MAC, "macro", [
  S(C, "Tu savais que quand le chômage *baisse*... les prix ont tendance à *monter ?*", "CHÔMAGE ↓ *PRIX ↑*", A("📉", "chômage et inflation", "VONT EN SENS OPPOSÉS")),
  S("Phillips", "Dans les années soixante, l'économiste Phillips observe un lien entre la hausse des salaires et le chômage, sur cent ans au Royaume-Uni.", "*PHILLIPS*",
    A("🇬🇧", "100 ans de données", "UN LIEN STABLE"), 1),
  S("l'arbitrage", "Conclusion : à *court terme*, il y a un arbitrage. Moins de chômage... mais plus d'inflation. Et l'inverse.", "UN *ARBITRAGE*",
    F(("👷", "chômage ↓", "inflation ↑", True), ("🧊", "chômage ↑", "inflation ↓")), 2),
  S("l'exemple", "Exemple : chômage à quatre pour cent, inflation à six. Un an après : chômage à sept, inflation à deux. La relation est *négative.*", "RELATION *NÉGATIVE*",
    F(("📍", "chômage 4 %", "inflation 6 %"), ("📍", "chômage 7 %", "inflation 2 %", True)), 3),
  S("l'usage", "Pour l'État, c'est un outil. Dépenses publiques, impôts, création monétaire : il choisit où placer son curseur.", "UN *OUTIL*",
    A("🎛️", "dépenses · impôts · monnaie", "LE CURSEUR DE L'ÉTAT"), 4),
  S(R, "Voilà. Courbe de Phillips : à court terme, *chômage et inflation varient en sens opposés.*", RT,
    F(("👷", "chômage ↓", "inflation ↑"), ("🧊", "chômage ↑", "inflation ↓", True))),
])

vid("inflation-vocabulaire", "Inflation, déflation, désinflation", "Ne confonds plus jamais", MAC, "macro", [
  S(C, "Tu savais que *désinflation* ne veut pas dire que les prix *baissent ?*", "LE PIÈGE DE LA *DÉSINFLATION*", A("🏷️", "quatre mots qui se ressemblent", "À NE PAS CONFONDRE")),
  S("inflation", "*Inflation :* les prix augmentent. Une hausse relative et positive du niveau général des prix.", "*INFLATION*",
    F(("📈", "inflation", "les prix montent")), 1),
  S("déflation", "*Déflation :* c'est l'inverse. Les prix *baissent* vraiment.", "*DÉFLATION*",
    F(("📉", "déflation", "les prix baissent", True)), 2),
  S("désinflation", "*Désinflation :* les prix montent toujours... mais *moins vite.* Le taux d'inflation diminue.", "*DÉSINFLATION*",
    F(("🐢", "désinflation", "les prix montent moins vite", True)), 3),
  S("hyper", "Et l'*hyperinflation :* une hausse des prix extrêmement forte.", "*HYPERINFLATION*",
    F(("🚀", "hyperinflation", "hausse énorme des prix")), 4),
  S(R, "Voilà. Déflation : les prix *baissent.* Désinflation : ils montent, mais *plus lentement.*", RT,
    F(("📉", "déflation", "prix ↓"), ("🐢", "désinflation", "prix ↑ mais ralentit", True))),
])

vid("pib-croissance", "Le PIB ne dit pas tout", "Croissance, PIB par tête et leurs limites", MAC, "macro", [
  S(C, "Tu savais qu'un pays très *pollueur*... ou très *inégalitaire* peut avoir un PIB élevé ?", "LE PIB EST *AVEUGLE*", A("🏭", "PIB élevé", "MAIS BIEN-ÊTRE ?")),
  S("le PIB", "Le PIB, c'est la valeur de tout ce qui est produit dans un pays sur une période. Quelle que soit la nationalité des entreprises.", "LE *PIB*",
    A("🏦", "ce qui est produit dans le pays", "SUR UNE PÉRIODE"), 1),
  S("la croissance", "La *croissance*, c'est la variation relative du PIB. Le PIB de cette année moins celui de l'an dernier... divisé par celui de l'an dernier.", "LA *CROISSANCE*",
    B("(PIB₂ − PIB₁) / PIB₁", "× 100 = taux de croissance"), 2),
  S("par tête", "Pour comparer des pays de tailles différentes, on utilise le *PIB par tête :* le PIB divisé par la population.", "PIB *PAR TÊTE*",
    B("PIB / pop.", "niveau de vie moyen"), 3),
  S("les limites", "Mais le PIB reste *matériel.* Il ignore la vie culturelle et politique. Et le PIB par tête ignore les *inégalités* de revenu.", "LES *LIMITES*",
    F(("🎭", "culture, politique", "ignorées"), ("⚖️", "inégalités", "ignorées", True)), 4),
  S(R, "Voilà. Croissance : variation relative du PIB. PIB par tête : on divise par la population. Les deux restent *imparfaits.*", RT,
    A("📊", "PIB · croissance · PIB par tête", "INDICATEURS IMPARFAITS")),
])

vid("externalites", "Les externalités", "Quand tes actes coûtent aux autres", ETA, "État", [
  S(C, "Tu savais qu'une usine peut *créer des emplois*... et *polluer* des voisins qui n'ont rien demandé ?", "L'EFFET *INVISIBLE*", A("🏭", "emplois + pollution", "QUI PAIE ?")),
  S("la définition", "Une *externalité*, c'est l'effet d'une action sur d'autres personnes... sans que le marché en tienne compte.", "L'*EXTERNALITÉ*",
    A("💨", "l'impact sur les autres", "HORS PRIX"), 1),
  S("négative", "Externalité *négative :* l'usine pollue. Elle ne paie que son coût privé. Résultat : trop de production, et un prix trop *bas.*", "EXTERNALITÉ *NÉGATIVE*",
    F(("🏭", "pollution", "trop produit, prix trop bas", True)), 2),
  S("la réponse", "L'État peut alors *taxer* le bien, pour que le producteur paie aussi le coût *social.*", "L'ÉTAT *TAXE*",
    A("🧾", "taxer le bien polluant", "COÛT SOCIAL PAYÉ"), 3),
  S("positive", "Externalité *positive :* un hôpital qui profite à tous les habitants. Le producteur ne reçoit pas tous les bénéfices... donc on en produit *trop peu.* L'État *subventionne.*", "EXTERNALITÉ *POSITIVE*",
    F(("🏥", "bénéfice pour tous", "trop peu produit → subvention")), 4),
  S(R, "Voilà. Externalité négative : *taxe.* Externalité positive : *subvention.* L'État corrige ce que le marché oublie.", RT,
    F(("🏭", "négative", "taxe", True), ("🏥", "positive", "subvention"))),
])

vid("biens-publics", "Le passager clandestin", "Pourquoi l'État produit les biens publics", ETA, "État", [
  S(C, "Tu savais que personne n'a envie de payer pour un *feu d'artifice*... parce qu'il en profitera *quand même ?*", "LE FEU D'ARTIFICE", A("🎆", "tout le monde en profite", "PERSONNE NE PAYE")),
  S("la définition", "Un *bien public* est *non exclusif :* on ne peut empêcher personne d'en profiter. Et *non rival :* le consommer n'empêche pas les autres de le faire.", "BIEN *PUBLIC*",
    F(("🚫", "non exclusif", "on ne peut exclure personne"), ("♾️", "non rival", "il reste pour les autres", True)), 1),
  S("les exemples", "L'éclairage public, la défense nationale, un feu d'artifice.", "DES *EXEMPLES*",
    A("💡", "éclairage · défense · feu d'artifice", "BIENS PUBLICS"), 2),
  S("le problème", "Chacun espère que les autres paieront à sa place. C'est le *passager clandestin.* Résultat : les entreprises privées n'en produisent pas.", "LE *PASSAGER CLANDESTIN*",
    A("🎟️", "je ne paie pas, les autres paieront", "PERSONNE NE PRODUIT", "PROBLÈME"), 3),
  S("la solution", "L'État, lui, peut *obliger* tout le monde à payer, grâce aux *impôts.* Il peut donc produire le bien.", "L'ÉTAT *PRODUIT*",
    A("🏛️", "financé par l'impôt", "TOUT LE MONDE PAIE"), 4),
  S(R, "Voilà. Bien public : non exclusif et non rival. Le privé n'en produit pas... donc l'État s'en charge, avec l'impôt.", RT,
    A("🏛️", "non exclusif + non rival", "L'ÉTAT PRODUIT")),
])

vid("equite-horizontale-verticale", "Équité horizontale ou verticale ?", "Avant ou après le marché", ETA, "État", [
  S(C, "Tu savais que l'État peut réduire les inégalités... *avant* ou *après* que le marché ait joué ?", "AVANT OU *APRÈS ?*", A("🍰", "partager le gâteau", "AVANT OU APRÈS")),
  S("le gâteau", "Image du gâteau : l'*efficience*, c'est sa taille. L'*équité*, c'est la façon de le *partager.*", "LE *GÂTEAU*",
    F(("📏", "efficience", "la taille du gâteau"), ("🔪", "équité", "le partage", True)), 1),
  S("horizontale", "Équité *horizontale :* en *amont.* L'égalité des chances. École, santé, accès pour tous... sans condition.", "ÉQUITÉ *HORIZONTALE*",
    F(("🏫", "en amont", "égalité des chances")), 2),
  S("verticale", "Équité *verticale :* en *aval.* Une fois le marché passé, on redistribue des plus riches vers les plus pauvres. Comme l'impôt sur le revenu.", "ÉQUITÉ *VERTICALE*",
    F(("🧾", "en aval", "redistribution", True)), 3),
  S("le barème", "Le barème est *progressif :* chaque taux s'applique uniquement à la part du revenu dans sa tranche. Pas à tout le revenu.", "LE *BARÈME*",
    B("par tranches", "chaque taux sur sa tranche seulement", "PROGRESSIF"), 4),
  S(R, "Voilà. Horizontale : *en amont*, égalité des chances. Verticale : *en aval*, redistribution.", RT,
    F(("🏫", "horizontale", "en amont"), ("🧾", "verticale", "en aval", True))),
])

d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eco")
for v in V:
    json.dump(v, open(os.path.join(d, v["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
print(len(V), "specs tanda 2")
