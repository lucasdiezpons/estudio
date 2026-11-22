"""Tanda 3 TikToks Sciences éco (chap. 1 y 4). Uso: python3 generar_specs_eco3.py → specs/eco/*.json"""
import json, os
from generar_specs_eco import A, F, B, S, C, R, RT, vid, V
V.clear()
INT, ETA = "Sciences éco · Introduction", "Sciences éco · L'État"

vid("main-invisible", "La main invisible", "Pourquoi l'égoïsme peut servir tout le monde", INT, "marché", [
  S(C, "Tu savais que les économies de marché fonctionnent... parce que chacun pense à *soi ?* Pas parce que les gens sont gentils.", "L'ÉGOÏSME *UTILE*", A("🤝", "chacun pense à soi", "ET ÇA MARCHE")),
  S("décentralisé", "Des milliers d'entreprises et de ménages décident *chacun de leur côté :* qui embaucher, quoi produire, quoi acheter.", "DÉCISIONS *DÉCENTRALISÉES*",
    A("🏪", "entreprises + ménages", "CHACUN DÉCIDE"), 1),
  S("les prix", "Ce qui les guide : les *prix.* Ils reflètent la valeur d'un bien pour la société... et ce qu'il coûte à produire.", "LES *PRIX* GUIDENT",
    F(("🏷️", "valeur pour la société", "le prix"), ("🏭", "coût de production", "le prix", True)), 2),
  S("Smith", "En mille sept cent soixante-seize, Adam Smith l'appelle la *main invisible :* l'intérêt personnel mène à l'intérêt de la société.", "ADAM *SMITH*",
    A("✋", "Adam Smith, 1776", "LA MAIN INVISIBLE"), 3),
  S("la limite", "Mais attention : le marché n'est pas toujours efficace, ni équitable. C'est là que l'*État* peut intervenir.", "LES *LIMITES*",
    A("⚠️", "pas toujours efficace ni équitable", "L'ÉTAT INTERVIENT"), 4),
  S(R, "Voilà. Les marchés marchent grâce à l'*intérêt personnel* et aux *prix.* La main invisible, c'est ça.", RT,
    A("✋", "intérêt personnel + prix", "LA MAIN INVISIBLE")),
])

vid("echange-profite", "L'échange profite-t-il à tous ?", "Smith, Ricardo et la Corée du Sud", INT, "échange", [
  S(C, "Tu savais qu'on avait conseillé à la Corée du Sud d'*importer* son acier... plutôt que d'en produire ?", "LE CONSEIL *RATÉ*", A("🇰🇷", "Corée du Sud, années 60", "IMPORTER OU PRODUIRE ?")),
  S("l'idée", "L'idée de départ : chacun se *spécialise*, devient plus efficace, puis échange. Donc l'échange profite à tous. C'est vrai entre agents... et entre pays.", "SE *SPÉCIALISER*",
    A("🔁", "spécialisation + échange", "TOUT LE MONDE GAGNE ?"), 1),
  S("Ricardo", "Ricardo disait : le Portugal fait du *vin*, l'Angleterre du *textile.* C'est l'avantage comparatif. Avant lui, Smith parlait d'avantage absolu.", "L'AVANTAGE *COMPARATIF*",
    F(("🇵🇹", "Portugal", "le vin"), ("🇬🇧", "Angleterre", "le textile", True)), 2),
  S("les limites", "Mais l'échange crée aussi des *perdants.* Dans les pays développés, la concurrence des pays émergents a fait mal à certains secteurs.", "DES *PERDANTS*",
    A("🏚️", "concurrence des pays émergents", "CERTAINS SECTEURS SOUFFRENT"), 3),
  S("la Corée", "La Corée a quand même développé son industrie... et son miracle économique est venu de là.", "LE *MIRACLE*",
    A("🏭", "industrie lourde en Corée", "MIRACLE ÉCONOMIQUE"), 4),
  S(R, "Voilà. L'échange profite *souvent* à tous... mais il faut des *conditions équitables* avant d'échanger.", RT,
    A("🌍", "échange + conditions équitables", "À NUANCER")),
])

vid("capitalisme-planifie", "Capitalisme ou économie planifiée ?", "Les trois questions de tout système", INT, "système", [
  S(C, "Tu savais que *tout* pays doit répondre à trois questions ? Quoi produire, comment produire... et pour *qui ?*", "TROIS QUESTIONS", A("❓", "quoi · comment · pour qui", "LE SYSTÈME RÉPOND")),
  S("le système", "Le *système économique*, c'est la manière d'organiser et de distribuer les ressources pour répondre aux besoins des citoyens.", "LE *SYSTÈME*",
    A("🧩", "organiser les ressources", "POUR LES BESOINS"), 1),
  S("capitalisme", "Le *capitalisme :* propriété privée des facteurs de production, échanges par les prix, et production tournée vers le *profit.*", "LE *CAPITALISME*",
    F(("🏢", "propriété privée", "prix + profit", True)), 2),
  S("planifié", "L'économie *planifiée :* des planificateurs centraux décident des réponses. Attention : ce n'est *pas* la même chose que le communisme.", "LE *PLANIFIÉ*",
    F(("📋", "planificateurs centraux", "décident de tout")), 3),
  S("le piège", "Piège : ne pas confondre système planifié centralisateur... et communisme.", "NE CONFONDS *PAS*",
    A("🚫", "planifié ≠ communisme", "ATTENTION", "PIÈGE"), 4),
  S(R, "Voilà. Capitalisme : *marchés, propriété privée, profit.* Planifié : *décisions centrales.*", RT,
    F(("🏢", "capitalisme", "marchés + profit"), ("📋", "planifié", "planificateurs", True))),
])

vid("monopole-naturel", "Le monopole naturel", "Pourquoi un seul réseau, et pourquoi l'État s'en mêle", ETA, "État", [
  S(C, "Tu savais qu'il n'y a qu'*un seul* réseau ferroviaire en France... et que c'est *normal ?*", "UN SEUL *RÉSEAU*", A("🚆", "un seul réseau", "POURQUOI ?")),
  S("coûts fixes", "Poser des rails ou des câbles coûte une fortune. Ce sont des *coûts fixes* très élevés. Plus on produit, plus le coût moyen *baisse.*", "COÛTS *FIXES*",
    A("🏗️", "coûts d'installation énormes", "COÛT MOYEN ↓"), 1),
  S("économies d'échelle", "On appelle ça des *économies d'échelle.* Mieux vaut qu'une seule entreprise fasse tout... C'est un *monopole naturel.*", "ÉCONOMIES D'ÉCHELLE",
    A("📉", "plus on produit, moins ça coûte", "MONOPOLE NATUREL"), 2),
  S("le risque", "Le risque : une entreprise seule fixe un prix *trop élevé* et produit *trop peu.* C'est son pouvoir de marché.", "LE *RISQUE*",
    F(("💶", "prix au-dessus du coût marginal", "quantité plus faible", True)), 3),
  S("la réponse", "L'État peut alors imposer un prix égal au *coût marginal.* Ou produire lui-même le bien.", "LA *RÉPONSE*",
    F(("⚖️", "tarifer au coût marginal", "comme en concurrence"), ("🏛️", "ou produire lui-même", "l'État")), 4),
  S(R, "Voilà. Monopole naturel : *coûts fixes énormes*, coût moyen qui baisse. L'État *régule* pour éviter les abus.", RT,
    A("🚆", "coûts fixes + économies d'échelle", "L'ÉTAT RÉGULE")),
])

vid("quatre-hypotheses", "Quand le marché est parfait", "Le premier théorème du bien-être", ETA, "État", [
  S(C, "Tu savais que le marché n'est efficace... que si *quatre conditions* sont réunies ?", "QUATRE *CONDITIONS*", A("✅", "premier théorème du bien-être", "4 HYPOTHÈSES")),
  S("le théorème", "Le premier théorème du bien-être dit : un marché libre mène à un équilibre où les gains à l'échange sont *maximisés.* C'est la main invisible, version moderne.", "LE *THÉORÈME*",
    A("🏆", "gains à l'échange maximisés", "SI 4 CONDITIONS"), 1),
  S("H1 et H2", "Un : les entreprises *prennent les prix comme donnés.* Deux : il n'y a *pas d'externalités.*", "*H1* ET *H2*",
    F(("1️⃣", "prix donnés", "pas de monopole"), ("2️⃣", "pas d'externalités", "pas de pollution", True)), 2),
  S("H3 et H4", "Trois : il n'y a *pas de bien public.* Quatre : les consommateurs sont *parfaitement informés.*", "*H3* ET *H4*",
    F(("3️⃣", "pas de bien public", "tout est privé"), ("4️⃣", "info parfaite", "pas d'asymétrie", True)), 3),
  S("l'État", "Quand *une seule* condition manque, le marché n'est plus efficace. L'État peut intervenir.", "UNE SEULE *SUFFIT*",
    A("🏛️", "une condition fausse", "L'ÉTAT INTERVIENT", "STOP"), 4),
  S(R, "Voilà. Quatre conditions : prix donnés, pas d'externalités, pas de bien public, information parfaite. S'il en manque une, l'État peut agir.", RT,
    A("✅", "4 conditions", "SINON → L'ÉTAT")),
])

vid("trois-raisons-etat", "Pourquoi l'État intervient", "Efficience, équité, stabilisation", ETA, "État", [
  S(C, "Tu savais que l'État intervient dans l'économie pour *trois raisons* seulement ?", "TROIS *RAISONS*", A("🏛️", "l'État dans l'économie", "3 RAISONS")),
  S("efficience", "Un : l'*efficience.* Corriger ce que le marché fait mal : monopoles, pollution, biens publics, manque d'information.", "L'*EFFICIENCE*",
    A("🔧", "corriger le marché", "LA TAILLE DU GÂTEAU"), 1),
  S("équité", "Deux : l'*équité.* Rendre la répartition des revenus plus juste. C'est la façon de partager le gâteau.", "L'*ÉQUITÉ*",
    A("🍰", "partager le gâteau", "RÉPARTITION PLUS JUSTE"), 2),
  S("stabilité", "Trois : la *stabilisation.* Maintenir la croissance, lutter contre le chômage et l'inflation.", "LA *STABILISATION*",
    A("📈", "croissance · chômage · inflation", "STABILISER L'ACTIVITÉ"), 3),
  S("les outils", "Pour ça, deux outils : la politique *budgétaire*, avec les dépenses et les impôts. Et la politique *monétaire.*", "DEUX *OUTILS*",
    F(("🧾", "budgétaire", "dépenses + impôts"), ("💱", "monétaire", "monnaie en circulation", True)), 4),
  S(R, "Voilà. Efficience, équité, stabilisation. Trois raisons, deux outils.", RT,
    F(("🔧", "efficience", "corriger le marché"), ("🍰", "équité", "partager"), ("📈", "stabilisation", "activité", True))),
])

d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eco")
for v in V:
    json.dump(v, open(os.path.join(d, v["id"] + ".json"), "w"), ensure_ascii=False, indent=1)
print(len(V), "specs tanda 3")
