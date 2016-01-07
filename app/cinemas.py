# -*- encoding: utf-8 -*-

from collections import OrderedDict

_cidades = {
    "sao-paulo":[
        "cinemark-aricanduva",
        "cinemark-villa-lobos",
        "cinemark-raposo",
        "cinemark-shopping-metro-santa-cruz",
        "cinemark-paulista",
        "cinemark-sp-market",
        "cinemark-cidade-jardim",
        "cinemark-central-plaza",
        "cinemark-shopping-iguatemi-sp",
        "cinemark-metro-tatuape",
        "cinemark-patio-higienopolis",
        "cinemark-shopping-d",
        "cinemark-market-place",
        "cinemark-tucuruvi",
        "cinemark-eldorado",
        "cinemark-shopping-interlagos",
        "cinemark-boulevard-tatuape",
        "cinemark-center-norte",
        "cinemark-mooca",
    ],
    "rio-de-janeiro":[
        "cinemark-barra-downtown",
        "cinemark-village-mall",
        "cinemark-metropolitano-barra",
        "cinemark-botafogo",
        "cinemark-carioca-shopping",
    ],
    "brasilia":[
        "cinemark-pier-21",
        "cinemark-iguatemi-brasilia",
    ],

    "jacarei":[ "cinemark-jacarei", ],
    "goiania":[
        "cinemark-passeio-das-aguas",
        "cinemark-flamboyant-goiania",
    ],
    "barueri":[ "cinemark-tambore",],
    "recife":[ "cinemark-riomar-recife",],
    "sao-bernardo-do-campo":[
        "cinemark-golden-square",
        "cinemark-extra-anchieta",
    ],
    "niteroi":[ "cinemark-plaza-shopping-niteroi", ],
    "florianopolis":[ "cinemark-floripa-shopping", ],
    "santos":[ "cinemark-praia-mar-shopping", ],
    "osasco":[ "cinemark-osasco",],
    "sao-jose-dos-pinhais":[ "cinemark-sao-jose-dos-pinhais",],
    "campinas":[ "cinemark-shopping-iguatemi-campinas",],
    "manaus":[ "cinemark-manaus",],
    "campo-grande":[ "cinemark-campo-grande",],
    "natal":[ "cinemark-natal",],
    "londrina":[ "cinemark-boulevard-londrina",],
    "cuiaba":[ "cinemark-goiabeiras",],
    "cotia":[ "cinemark-granja-viana",],
    "taubate":[ "cinemark-via-vale-taubate",],
    "salvador":[ "cinemark-salvador",],
    "vila-velha":[ "cinemark-vila-velha",],
    "ribeirao-preto":[ "cinemark-ribeirao-preto",],
    "vitoria":[ "cinemark-vitoria",],
    "guarulhos":[ "cinemark-guarulhos",],
    "betim":[ "cinemark-metropolitan",],
    "uberlandia":[ "cinemark-uberlandia",],
    "palmas":[ "cinemark-capim-dourado",],
    "canoas":[ "cinemark-canoas",],
    "sao-caetano-do-sul":[ "cinemark-sao-caetano",],
    "taguatinga":[ "cinemark-taguatinga",],
    "porto-alegre":[
        "cinemark-bourbon-ipiranga",
        "cinemark-barra-sul",
    ],
    "belo-horizonte":[
        "cinemark-patio-savassi",
        "cinemark-diamond-mall",
        "cinemark-bh-shopping",
    ],
    "curitiba":[
        "cinemark-mueller",
        "cinemark-barigui",
    ],
    "santo-andre":[
        "cinemark-atrium",
        "cinemark-grand-plaza-shopping",
    ],
    "aracaju":[
        "cinemark-shopping-jardins-aracaju",
        "cinemark-riomar",
    ],
    "sao-jose-dos-campos":[
        "cinemark-center-vale",
        "cinemark-colinas",
    ],
}

CINEMAS = {
    "url": "http://www.ingresso.com/%s/home/local/cinema/%s",
    "cidades": OrderedDict(sorted(_cidades.items(), key=lambda t: t[0]))
}
