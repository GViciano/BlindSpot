"""Builds the campaign level booklet for the physical game, in Spanish and English:
reglas/Campana_Niveles_ES.pdf and reglas/Campaign_Levels_EN.pdf.

One page per level (setup, dice, mission cards to deal, stars to win) and, before each world,
a page with what is new in it. Levels come from campana.js and the card numbers from
objetivos.js, so the booklet always matches the game.
Usage:  python3 reglas/build_niveles.py   (needs Node and Playwright's Chromium)
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'cartas'))
import generar_cartas as gc  # noqa: E402

LEVELS = json.loads(subprocess.run(
    ['node', '-e', 'global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.BLINDSPOTS_CAMPANA))',
     str(ROOT / 'campana.js')], capture_output=True, text=True, check=True).stdout)
OBJS = gc.load_objectives()
COLS = ['azul', 'rojo', 'verde', 'amarillo']


def piles(C):
    """Card numbers usable with C colours, by stars (same filter as the game)."""
    out = {}
    for i, o in enumerate(OBJS):
        cs = [COLS.index(o[k]) for k in ('color', 'color2') if o.get(k)]
        if any(c >= C for c in cs) or (o['tipo'] == 'colores_exactos' and o['n'] > C) or o.get('min_colores', 0) > C:
            continue
        out.setdefault(o['estrellas'], []).append(i + 1)
    return out


def die(colour, face, size=22):
    fill = gc.COLORS.get(colour, colour)
    pip = '#3b2c00' if colour == 'amarillo' else '#ffffff'
    return (f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" class="dsvg">'
            + gc.die_svg(1, 1, size - 2, fill, face, pip) + '</svg>')


GREY, BLACK = '#8b93a1', '#1c1e23'

T = {
    'es': {
        'file': 'Campana_Niveles_ES.pdf', 'lang': 'es', 'title': 'Campaña · Niveles',
        'booklet': 'LIBRO DE CAMPAÑA', 'cover_sub': '25 niveles en 5 mundos para 3 o 4 jugadores',
        'how_t': 'Cómo usar este libro',
        'how': ['Jugad los niveles en orden. Cada hoja explica todo lo necesario para preparar ese nivel: colores, dados, cartas de misión y estrellas para ganar.',
                'Si superáis un nivel, marcad la casilla de vuestro número de jugadores y pasad al siguiente. Si perdéis, repetid el nivel con cartas nuevas: cada partida es distinta.',
                'Antes de cada mundo hay una hoja con sus novedades. Leedla en voz alta antes de empezar el primer nivel del mundo.',
                'Las reglas básicas están en el reglamento. Este libro solo dice qué cambia en cada nivel.'],
        'piles_t': 'Montones de cartas de misión',
        'piles_p': 'Separad las cartas de misión en montones por estrellas. Con 3 colores no se usan las cartas que muestran amarillo ni las que llevan la marca «4» abajo a la izquierda (solo para 4 colores); con 4 colores se usan todas. Estos son los números de carta de cada montón:',
        'piles_c': lambda C: f'Con {C} colores',
        'stars_n': lambda s, n: f'{s}★ · {n} cartas',
        'world': 'MUNDO', 'level': 'NIVEL', 'of': 'de',
        'players3': '3 jugadores', 'players4': '4 jugadores',
        'row_bag': 'Dados en la bolsa', 'row_round': 'Dados por ronda', 'row_rounds': 'Rondas', 'row_stars': 'Estrellas para ganar',
        'per_colour': lambda n, t: f'{n} de cada color ({t})', 'plus_black': ' + 1 negro', 'with_grey': ' (+ 1 gris en la 1.ª ronda)',
        'setup_t': 'Preparación',
        'colours': lambda names: f'<b>Colores:</b> {names}',
        'bag': lambda a, b: f'<b>Bolsa:</b> meted {a} dados de cada color con 3 jugadores, o {b} de cada color con 4. Devolved el resto a la caja.',
        'cards': lambda txt: f'<b>Cartas de misión:</b> barajad cada montón y repartid a cada jugador, boca abajo, {txt}.',
        'card_one': lambda s: f'1 carta de {s}★',
        'and': ' y ',
        'cards_from': lambda C: f'Usad los montones de {C} colores (números de carta abajo).',
        'place': '<b>Sin mirar</b>, cada jugador coloca sus cartas en su soporte, de cara a los demás.',
        'dealer': '<b>Primer repartidor:</b> elegidlo al azar. Se reparte en el sentido de las agujas del reloj y cada jugador reparte una vez.',
        'actions': '<b>Acciones especiales:</b> con 3 jugadores, barajad las 4 cartas de acción y poned 3 boca arriba (la cuarta vuelve a la caja); con 4 jugadores, poned las 4.',
        'grey': '<b>Dado gris:</b> dejad el dado gris junto a la bolsa y barajad las 7 cartas grises boca abajo. En la 1.ª ronda, el primer repartidor revela una y tira el dado gris con los demás.',
        'black': '<b>Dados negros:</b> dejad 3 dados negros (4 con 4 jugadores) junto a la bolsa y el mazo de cartas negras boca abajo. Al empezar cada ronda, antes de sacar dados, el repartidor revela la carta negra de arriba; luego tira 1 dado negro con los demás.',
        'goal_t': 'Para ganar', 'goal': lambda a, b: f'El equipo debe sumar <b>{a}★</b> con 3 jugadores o <b>{b}★</b> con 4 (estrellas de las cartas cumplidas más las estrellas extra).',
        'goal_grey': ' Además, quien tenga el dado gris debe cumplir la carta gris.',
        'goal_black': ' Además, nadie puede recibir un segundo dado negro.',
        'numbers_t': 'Números de carta para este nivel',
        'notes': 'Notas', 'done': 'Superado', 'with3': 'con 3 jugadores', 'with4': 'con 4 jugadores', 'date': 'Fecha',
        'remember': 'Recuerda',
        'tips': {
            1: 'Sois un equipo: hablad de los grupos, pero sin decir lo que pone en las cartas de nadie.',
            2: 'Quien reparte no sabe qué necesita. Haced los grupos pensando en los demás.',
            3: 'Con 2 cartas, cada jugador tiene que cumplir las dos para sumar sus estrellas.',
            4: 'Las cartas con * dan 1★ extra si se consigue la cifra exacta.',
            5: 'Una carta de 3★ vale mucho: centraos en quien la tenga.',
            6: 'Cada jugador puede usar una sola acción en todo el nivel. Decid siempre en voz alta qué dado cambiáis.',
            7: 'Una acción usada ya no está para nadie más: poneos de acuerdo antes.',
            8: 'Eliminar devuelve el dado a la bolsa: puede volver a salir.',
            9: 'Invertir pone la cara opuesta: 1↔6, 2↔5, 3↔4.',
            10: 'Con dos cartas de 4★ hacen falta menos estrellas, pero cada carta es más difícil.',
            11: 'La carta gris es para todos: elegid bien quién se lleva el dado gris.',
            12: 'El dado gris cuenta como dado y para los números, pero no como color.',
            13: 'Si no se cumple la carta gris, el nivel se pierde aunque lleguéis a las estrellas.',
            14: 'Mirad la carta gris antes de hacer los grupos de la primera ronda.',
            15: 'Una sola carta de 5★ por jugador: cada objetivo cuenta mucho.',
            16: 'La carta negra de la ronda se conoce antes de tirar: pensad quién debe llevarse el dado negro.',
            17: 'Quien ya tiene un dado negro no puede coger un grupo con otro.',
            18: 'Cuidado con el último grupo: si quien reparte ya tiene un dado negro, no puede quedarse otro.',
            19: 'Al final, cada uno aplica su carta negra a sus propios dados y elige cuál quita.',
            20: 'Tres cartas por jugador: repartid los dados negros con cabeza.',
            21: 'Entra el amarillo: las cartas pueden pedir dados amarillos.',
            22: 'Con 4 colores hay más variedad en la bolsa y es más difícil juntar un color.',
            23: 'Una carta de 4★ por jugador: ayudad primero a quien tenga la más difícil.',
            24: 'Tres cartas por jugador: hablad mucho y planificad las rondas.',
            25: 'El último nivel: 3 cartas de 3★ por jugador. ¡Suerte!',
        },
        'names': lambda i, l: l.get('nombre') or (f'Primeros pasos {i + 1}' if i < 5 else f'Acciones {i - 4}'),
        'worlds': [
            ('Primeros pasos', 'El juego básico',
             ['En este mundo aprendéis el juego básico. No hay reglas especiales: solo dados de 3 colores (azul, rojo y verde) y cartas de misión.',
              'Cada ronda, quien reparte saca dados de la bolsa, los tira y forma tantos grupos como jugadores. Empezando por su izquierda, cada jugador elige un grupo; quien reparte se queda el último.',
              'Al final se descubren las cartas. Sumad las estrellas de las cartas cumplidas (más las extra): si llegáis a las estrellas del nivel, lo superáis.'],
             []),
            ('Acciones especiales', 'Novedad: cartas de acción',
             ['Desde este mundo el equipo tiene acciones especiales: relanzar un dado, sumarle o restarle 1, invertirlo (poner la cara opuesta: el 1 pasa a 6, el 2 a 5…) y eliminarlo (vuelve a la bolsa).',
              'Con 3 jugadores se usan 3 de las 4 cartas de acción, al azar; con 4 jugadores, las 4.',
              'Cada jugador puede usar una sola acción en todo el nivel, en cualquier momento y sobre cualquier dado a la vista: los de la mesa o los que ya tiene alguien. Quien la usa se queda la carta: ya no está disponible para nadie más, así que poneos de acuerdo.'],
             ['action']),
            ('El dado gris', 'Novedad: dado gris y cartas grises',
             ['En la primera ronda, el primer repartidor revela una carta gris, que ve todo el mundo, y tira el dado gris junto con los demás dados.',
              'Quien acabe la partida con el dado gris tiene que cumplir la carta gris. Si no la cumple, el equipo pierde el nivel aunque llegue a las estrellas.',
              'El dado gris cuenta como dado, para la suma y para los números, pero no cuenta como color. Pensad bien a quién le conviene llevárselo.'],
             ['grey']),
            ('La Bomba', 'Novedad: dados negros y cartas negras',
             ['En estos niveles se sacan más dados por ronda (6 con 3 jugadores, 8 con 4) y, además, cada ronda se tira un dado negro.',
              'Al empezar cada ronda, antes de sacar ningún dado, quien reparte revela la carta negra de arriba del mazo: todos conocen su efecto antes de coger el dado negro. La carta se coloca junto al dado negro y va con él.',
              'Cada jugador solo puede acabar con UN dado negro: si ya tienes uno, no puedes coger un grupo que lleve otro. Cuidado con quien reparte: si le queda un grupo con un dado negro y ya tiene uno, el equipo pierde el nivel en el acto.',
              'Al final de la partida explotan las bombas: quien tiene un dado negro aplica su carta a sus propios dados y elige cuál quita. Si ningún dado cumple la carta, no pasa nada. Las cartas negras no se repiten hasta que han salido todas.'],
             ['black']),
            ('Cuatro colores', 'Novedad: dados amarillos',
             ['Entra el cuarto color: el amarillo. Meted también dados amarillos en la bolsa.',
              'Ahora también salen cartas de misión con dados amarillos y las marcadas con «4», que solo se usan con 4 colores. Con más colores es más difícil reunir muchos dados de un mismo color.',
              'Siguen las acciones especiales, como desde el nivel 6; no hay dado gris ni dados negros. Las misiones son más exigentes.'],
             ['yellow']),
        ],
        'colour_names': ['azul', 'rojo', 'verde', 'amarillo'],
        'new_components': 'Componentes de este mundo',
        'comp': {'action': '4 cartas de acción (A1–A4)', 'grey': '1 dado gris y 7 cartas grises (G1–G7)',
                 'black': '4 dados negros y 9 cartas negras (N1–N9)', 'yellow': 'Dados amarillos'},
        'action_names': ['Relanzar', '+1 / −1', 'Invertir', 'Eliminar'],
    },
    'en': {
        'file': 'Campaign_Levels_EN.pdf', 'lang': 'en', 'title': 'Campaign · Levels',
        'booklet': 'CAMPAIGN BOOK', 'cover_sub': '25 levels in 5 worlds for 3 or 4 players',
        'how_t': 'How to use this book',
        'how': ['Play the levels in order. Each page tells you everything you need to set up that level: colours, dice, mission cards and stars to win.',
                'If you beat a level, tick the box for your player count and move on to the next one. If you lose, replay the level with new cards: every game is different.',
                'Before each world there is a page with what is new in it. Read it aloud before playing the first level of that world.',
                'The basic rules are in the rulebook. This book only tells you what changes in each level.'],
        'piles_t': 'Mission card piles',
        'piles_p': 'Sort the mission cards into piles by stars. With 3 colours, leave out the cards that show yellow and those marked “4” in the bottom left corner (4 colours only); with 4 colours, use them all. These are the card numbers in each pile:',
        'piles_c': lambda C: f'With {C} colours',
        'stars_n': lambda s, n: f'{s}★ · {n} cards',
        'world': 'WORLD', 'level': 'LEVEL', 'of': 'of',
        'players3': '3 players', 'players4': '4 players',
        'row_bag': 'Dice in the bag', 'row_round': 'Dice per round', 'row_rounds': 'Rounds', 'row_stars': 'Stars to win',
        'per_colour': lambda n, t: f'{n} of each colour ({t})', 'plus_black': ' + 1 black', 'with_grey': ' (+ 1 grey in round 1)',
        'setup_t': 'Setup',
        'colours': lambda names: f'<b>Colours:</b> {names}',
        'bag': lambda a, b: f'<b>Bag:</b> put in {a} dice of each colour with 3 players, or {b} of each colour with 4. Return the rest to the box.',
        'cards': lambda txt: f'<b>Mission cards:</b> shuffle each pile and deal each player, face down, {txt}.',
        'card_one': lambda s: f'1 card of {s}★',
        'and': ' and ',
        'cards_from': lambda C: f'Use the {C}-colour piles (card numbers below).',
        'place': '<b>Without looking</b>, each player places their cards in their stand, facing the others.',
        'dealer': '<b>First dealer:</b> choose at random. Dealing passes clockwise; each player deals once.',
        'actions': '<b>Special actions:</b> with 3 players, shuffle the 4 action cards and place 3 face up (the fourth goes back to the box); with 4 players, place all 4.',
        'grey': '<b>Grey die:</b> place the grey die next to the bag and shuffle the 7 grey cards face down. In round 1, the first dealer reveals one and rolls the grey die with the others.',
        'black': '<b>Black dice:</b> place 3 black dice (4 with 4 players) next to the bag and the black card deck face down. At the start of each round, before drawing dice, the dealer reveals the top black card; then they roll 1 black die with the others.',
        'goal_t': 'To win', 'goal': lambda a, b: f'The team must score <b>{a}★</b> with 3 players or <b>{b}★</b> with 4 (stars of completed cards plus bonus stars).',
        'goal_grey': ' In addition, the holder of the grey die must meet the grey card.',
        'goal_black': ' In addition, nobody may receive a second black die.',
        'numbers_t': 'Card numbers for this level',
        'notes': 'Notes', 'done': 'Beaten', 'with3': 'with 3 players', 'with4': 'with 4 players', 'date': 'Date',
        'remember': 'Remember',
        'tips': {
            1: 'You are a team: talk about the groups, but never say what anyone’s cards show.',
            2: 'The dealer doesn’t know what they need. Build the groups thinking of the others.',
            3: 'With 2 cards, a player must complete both to score their stars.',
            4: 'Cards with a * give 1★ extra for hitting the exact amount.',
            5: 'A 3★ card is worth a lot: focus on whoever holds it.',
            6: 'Each player may use only one action during the level. Always say aloud which die you change.',
            7: 'A used action is gone for everyone: agree on it first.',
            8: 'Remove puts the die back into the bag: it may come out again.',
            9: 'Flip turns the die to its opposite face: 1↔6, 2↔5, 3↔4.',
            10: 'With two 4★ cards you need fewer stars, but each card is harder.',
            11: 'The grey card is for everyone: choose carefully who takes the grey die.',
            12: 'The grey die counts as a die and for values, but not as a colour.',
            13: 'If the grey card isn’t met, the level is lost even if you reach the stars.',
            14: 'Look at the grey card before forming the groups in round 1.',
            15: 'A single 5★ card per player: every objective counts.',
            16: 'The round’s black card is known before the roll: think about who should take the black die.',
            17: 'If you already have a black die, you can’t take a group with another one.',
            18: 'Watch the last group: if the dealer already has a black die, they can’t keep another.',
            19: 'At the end, everyone applies their black card to their own dice and chooses which to remove.',
            20: 'Three cards per player: share out the black dice wisely.',
            21: 'Yellow joins the game: cards may ask for yellow dice.',
            22: 'With 4 colours the bag is more varied and gathering one colour is harder.',
            23: 'One 4★ card per player: help whoever has the hardest one first.',
            24: 'Three cards per player: talk a lot and plan the rounds.',
            25: 'The final level: three 3★ cards per player. Good luck!',
        },
        'names': lambda i, l: (f'First Steps {i + 1}' if i < 5 else f'Actions {i - 4}' if i < 10 else f'Grey {i - 9}' if i < 15
                               else f'Bomb {i - 14}' if i < 20 else f'Four Colours {i - 19}'),
        'worlds': [
            ('First Steps', 'The basic game',
             ['In this world you learn the basic game. There are no special rules: just dice in 3 colours (blue, red and green) and mission cards.',
              'Each round, the dealer draws dice from the bag, rolls them and forms one group per player. Starting on their left, each player picks a group; the dealer keeps the last one.',
              'At the end, reveal the cards. Add up the stars of the completed cards (plus bonus stars): if you reach the level’s stars, you beat it.'],
             []),
            ('Special Actions', 'New: action cards',
             ['From this world on, the team has special actions: reroll a die, add or subtract 1, flip it (turn it to the opposite face: 1 becomes 6, 2 becomes 5…) and remove it (it goes back into the bag).',
              'With 3 players, use 3 of the 4 action cards, at random; with 4 players, all 4.',
              'Each player may use just one action during the whole level, at any time and on any visible die: on the table or already in someone’s area. Whoever uses it keeps the card: it is gone for everyone else, so agree on it together.'],
             ['action']),
            ('The Grey Die', 'New: grey die and grey cards',
             ['In round 1, the first dealer reveals a grey card that everyone can see and rolls the grey die together with the other dice.',
              'Whoever ends the game with the grey die must meet the grey card. If not, the team loses the level even if it reaches the stars.',
              'The grey die counts as a die, for sums and for values, but not as a colour. Think carefully about who should take it.'],
             ['grey']),
            ('The Bomb', 'New: black dice and black cards',
             ['In these levels more dice are drawn each round (6 with 3 players, 8 with 4) and, on top of that, a black die is rolled every round.',
              'At the start of each round, before drawing any dice, the dealer reveals the top black card: everyone knows its effect before anyone takes the black die. The card is placed next to the black die and travels with it.',
              'Each player may end up with only ONE black die: if you already have one, you can’t take a group that has another. Watch the dealer: if they are left a group with a black die and already have one, the team loses the level at once.',
              'At the end of the game the bombs go off: whoever has a black die applies its card to their own dice and chooses which to remove. If no die fits the card, nothing happens. Black cards don’t repeat until all have come out.'],
             ['black']),
            ('Four Colours', 'New: yellow dice',
             ['The fourth colour joins in: yellow. Put yellow dice into the bag as well.',
              'Mission cards with yellow dice now come up too, as well as the cards marked “4”, used only with 4 colours. With more colours, gathering many dice of one colour is harder.',
              'Special actions are still used, as from level 6 on; there is no grey die and no black dice. Missions are tougher.'],
             ['yellow']),
        ],
        'colour_names': ['blue', 'red', 'green', 'yellow'],
        'new_components': 'Components for this world',
        'comp': {'action': '4 action cards (A1–A4)', 'grey': '1 grey die and 7 grey cards (G1–G7)',
                 'black': '4 black dice and 9 black cards (N1–N9)', 'yellow': 'Yellow dice'},
        'action_names': ['Reroll', '+1 / −1', 'Flip', 'Remove'],
    },
}

CSS = """
@page { size: A4; margin: 16mm 16mm 18mm; @bottom-center { content: counter(page); font: 600 9pt 'Inter', sans-serif; color: #8a94a6; } }
@page cover { margin: 0; @bottom-center { content: none; } }
:root { --ink: #18202c; --muted: #5d6778; --line: #d9dee6; --blue: #2f6fdb; --orange: #ee8420; --green: #2a9a58; --purple: #8a4fd1; --yellow: #f1c232; --teal: #1d7a6a; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { margin: 0; font: 400 11pt/1.5 'Inter', 'DejaVu Sans', sans-serif; color: var(--ink); }
h1, h2, h3 { font-family: 'Inter Display', 'Inter', sans-serif; margin: 0; line-height: 1.15; }
.page { break-before: page; }
.cover { page: cover; position: relative; width: 210mm; height: 297mm; background: #18202c; color: #fff; overflow: hidden; }
.cover .cd { position: absolute; filter: drop-shadow(0 4px 8px rgba(0,0,0,.45)); }
.cover .logo { position: absolute; left: 0; right: 0; top: 40%; text-align: center; font: 900 50pt 'Inter Display', sans-serif; }
.cover .logo .dot { display: inline-block; width: 28px; height: 28px; border-radius: 50%; background: var(--orange); margin: 0 10px; vertical-align: middle; position: relative; top: -6px; }
.cover .rb { position: absolute; left: 0; right: 0; top: 33%; text-align: center; font: 700 12pt 'Inter', sans-serif; letter-spacing: .4em; color: var(--yellow); }
.cover .tag { position: absolute; left: 0; right: 0; top: 52%; text-align: center; font: 500 15pt 'Inter', sans-serif; color: #c9d1de; }
h2.sec { font-size: 20pt; font-weight: 800; margin-bottom: 10px; }
p { margin: 0 0 8px; }
.piles { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; font-size: 8.6pt; }
.piles h3 { font-size: 11pt; margin: 6px 0; }
.piles .pl { margin-bottom: 6px; } .piles .pl b { display: block; }
/* world page */
.world { position: relative; }
.world .band { border-radius: 14px; padding: 18px 22px; color: #fff; margin-bottom: 18px; }
.world .band .k { font: 700 11pt 'Inter', sans-serif; letter-spacing: .3em; opacity: .85; }
.world .band h1 { font-size: 32pt; font-weight: 900; margin: 4px 0 2px; }
.world .band .sub { font-size: 13pt; opacity: .9; }
.world p { font-size: 11.5pt; line-height: 1.6; }
.world .cards { display: flex; gap: 12px; justify-content: center; margin: 16px 0; flex-wrap: wrap; }
.world .cards figure { margin: 0; width: 36mm; text-align: center; font-size: 8.5pt; color: var(--muted); }
.world .cards svg { width: 36mm; height: auto; display: block; margin-bottom: 4px; filter: drop-shadow(0 1px 2px rgba(0,0,0,.2)); }
.world .comp { border: 1.5px solid var(--line); border-radius: 12px; padding: 10px 16px; }
.world .comp b { display: block; font-size: 9pt; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }
/* level page */
.lvhead { display: flex; align-items: center; gap: 16px; border-bottom: 3px solid var(--ink); padding-bottom: 10px; margin-bottom: 14px; }
.lvnum { width: 64px; height: 64px; border-radius: 16px; background: var(--ink); color: #fff; display: grid; place-items: center; font: 900 28pt 'Inter Display', sans-serif; flex: none; }
.lvhead .k { font: 700 9.5pt 'Inter', sans-serif; letter-spacing: .2em; color: var(--muted); }
.lvhead h1 { font-size: 26pt; font-weight: 900; }
.lvhead .dice { margin-left: auto; display: flex; gap: 6px; }
table.facts { width: 100%; border-collapse: collapse; margin-bottom: 14px; font-size: 10pt; }
table.facts th { background: var(--ink); color: #fff; text-align: left; padding: 6px 10px; font-weight: 600; }
table.facts td { padding: 6px 10px; border-bottom: 1px solid var(--line); }
table.facts td:first-child { font-weight: 600; width: 34%; }
h3.st { font-size: 13pt; font-weight: 800; margin: 4px 0 8px; }
ol.steps { list-style: none; padding: 0; margin: 0 0 12px; counter-reset: s; }
ol.steps > li { counter-increment: s; position: relative; padding-left: 32px; margin-bottom: 7px; }
ol.steps > li::before { content: counter(s); position: absolute; left: 0; top: 0; width: 22px; height: 22px; border-radius: 6px; background: var(--ink); color: #fff; font-weight: 700; font-size: 10pt; display: grid; place-items: center; }
.goal { background: #fdf3e8; border-left: 5px solid var(--orange); border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; }
.goal b.t, .tip b.t { display: block; font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 2px; }
.goal b.t { color: var(--orange); }
.tip { background: #eef8f2; border-left: 5px solid var(--green); border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; }
.tip b.t { color: var(--green); }
.nums { border: 1.5px solid var(--line); border-radius: 10px; padding: 8px 12px; font-size: 8.4pt; color: var(--muted); margin-bottom: 12px; }
.nums b { color: var(--ink); }
.done { display: flex; gap: 22px; align-items: center; font-size: 10pt; border-top: 1.5px dashed var(--line); padding-top: 10px; }
.done .bx { display: inline-block; width: 15px; height: 15px; border: 2px solid var(--ink); border-radius: 3px; vertical-align: -3px; margin-right: 6px; }
.done .line { flex: 1; border-bottom: 1px solid var(--ink); height: 14px; }
.lvp { font-size: 10pt; line-height: 1.42; }
.lvp table.facts td { padding: 4px 10px; } .lvp ol.steps > li { margin-bottom: 5px; } .lvp .goal, .lvp .tip { padding: 8px 12px; margin-bottom: 9px; }
.notes { margin: 4px 0 14px; } .notes b { font-size: 9pt; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.notes .nl { border-bottom: 1px solid var(--line); height: 22px; }
.dsvg { display: inline-block; vertical-align: middle; }
.sw { display: inline-flex; align-items: center; gap: 4px; margin-right: 8px; white-space: nowrap; }
"""

WORLD_COLOURS = ['#2f6fdb', '#1d7a6a', '#6f7785', '#15171b', '#b8860b']
COVER_DICE = ''.join(
    f'<span class="cd" style="left:{x}%;top:{y}%;transform:rotate({r}deg)">{die(c, f, s)}</span>'
    for x, y, r, c, f, s in [(8, 12, -14, 'azul', 5, 100), (30, 6, 9, 'rojo', 3, 84), (72, 9, -8, 'verde', 6, 96),
                             (86, 26, 16, 'verde', 2, 80), (12, 68, 12, 'amarillo', 4, 84), (78, 70, -18, 'azul', 1, 96),
                             (56, 82, 7, '#1c1e23', 6, 74), (30, 84, -6, '#8b93a1', 2, 66)])


def build(lang):
    L = T[lang]
    names = L['colour_names']
    out = [f'<!doctype html><html lang="{L["lang"]}"><head><meta charset="utf-8"><title>BlindSpots · {L["title"]}</title><style>{CSS}</style></head><body>']
    out.append(f'<div class="cover">{COVER_DICE}<div class="rb">{L["booklet"]}</div>'
               f'<div class="logo">BLIND<span class="dot"></span>SPOTS</div><div class="tag">{L["cover_sub"]}</div></div>')
    # how to use + card piles
    p3, p4 = piles(3), piles(4)
    out.append(f'<section class="page"><h2 class="sec">{L["how_t"]}</h2>' + ''.join(f'<p>{x}</p>' for x in L['how']))
    out.append(f'<h2 class="sec" style="margin-top:18px">{L["piles_t"]}</h2><p>{L["piles_p"]}</p><div class="piles">')
    for C, pl in ((3, p3), (4, p4)):
        out.append(f'<div><h3>{L["piles_c"](C)}</h3>' + ''.join(
            f'<div class="pl"><b>{L["stars_n"](s, len(pl[s]))}</b>{", ".join(map(str, pl[s]))}</div>' for s in sorted(pl)) + '</div>')
    out.append('</div></section>')

    for i, lv in enumerate(LEVELS):
        w = i // 5
        if i % 5 == 0:
            wt, wsub, paras, comps = L['worlds'][w]
            cards = ''
            if 'action' in comps:
                cards = ''.join(f'<figure>{gc.action_card_svg(k)}A{k + 1} · {L["action_names"][k]}</figure>' for k in range(4))
            elif 'grey' in comps:
                cards = f'<figure>{gc.grey_card_svg(0)}G1</figure><figure>{gc.grey_card_svg(4)}G5</figure><figure>{gc.grey_back_svg()}</figure>'
            elif 'black' in comps:
                cards = f'<figure>{gc.black_card_svg(1)}N2</figure><figure>{gc.black_card_svg(7)}N8</figure><figure>{gc.black_back_svg()}</figure>'
            elif 'yellow' in comps:
                cards = ''.join(f'<figure>{gc.card_svg(o, i + 1)}{i + 1}</figure>' for i, o in enumerate(OBJS) if o.get('min_colores') == 4 or (o.get('color') == 'amarillo' and o['tipo'] in ('al_menos', 'exactamente')) and o.get('n') == 2)
            else:
                cards = f'<figure>{gc.card_svg(OBJS[0], 1)}1</figure><figure>{gc.card_svg(OBJS[1], 2)}2</figure><figure>{gc.back_svg()}</figure>'
            comp = ''.join(f'<div>• {L["comp"][c]}</div>' for c in comps)
            out.append(f'<section class="page world"><div class="band" style="background:{WORLD_COLOURS[w]}">'
                       f'<div class="k">{L["world"]} {w + 1} · {L["level"]} {i + 1}–{i + 5}</div><h1>{wt}</h1><div class="sub">{wsub}</div></div>'
                       + ''.join(f'<p>{x}</p>' for x in paras) + f'<div class="cards">{cards}</div>'
                       + (f'<div class="comp"><b>{L["new_components"]}</b>{comp}</div>' if comp else '') + '</section>')

        C = lv['colores']
        bag = lv['dados']
        per = lv.get('dados_por_ronda') or {'3': 5, '4': 7}
        grey, black, mods = lv.get('dado_gris'), lv.get('dado_negro'), lv.get('modificadores')
        need = lv['ganar']
        stars = lv['cartas']
        nm = L['names'](i, lv)
        swatches = ''.join(f'<span class="sw">{die(COLS[c], None, 18)}{names[c]}</span>' for c in range(C))
        cards_txt = L['and'].join(L['card_one'](s) for s in stars) if len(stars) <= 2 else ', '.join(L['card_one'](s) for s in stars[:-1]) + L['and'] + L['card_one'](stars[-1])
        steps = [L['colours'](swatches), L['bag'](bag['3'], bag['4']), L['cards'](cards_txt) + ' ' + L['cards_from'](C)]
        if mods:
            steps.append(L['actions'])
        if grey:
            steps.append(L['grey'])
        if black:
            steps.append(L['black'])
        steps += [L['place'], L['dealer']]
        rnd = lambda P: str(per[str(P)]) + (L['plus_black'] if black else '') + (L['with_grey'] if grey else '')
        facts = (f'<table class="facts"><tr><th></th><th>{L["players3"]}</th><th>{L["players4"]}</th></tr>'
                 f'<tr><td>{L["row_bag"]}</td><td>{L["per_colour"](bag["3"], bag["3"] * C)}</td><td>{L["per_colour"](bag["4"], bag["4"] * C)}</td></tr>'
                 f'<tr><td>{L["row_round"]}</td><td>{rnd(3)}</td><td>{rnd(4)}</td></tr>'
                 f'<tr><td>{L["row_rounds"]}</td><td>3</td><td>4</td></tr>'
                 f'<tr><td>{L["row_stars"]}</td><td><b>{need["3"]}★</b></td><td><b>{need["4"]}★</b></td></tr></table>')
        pl = piles(C)
        nums = '<br>'.join(f'<b>{s}★:</b> {", ".join(map(str, pl[s]))}' for s in sorted(set(stars)))
        goal = L['goal'](need['3'], need['4']) + (L['goal_grey'] if grey else '') + (L['goal_black'] if black else '')
        head_dice = ''.join(die(COLS[c], 1 + (c * 2 + i) % 6, 26) for c in range(C)) + (die(GREY, 3, 26) if grey else '') + (die(BLACK, 5, 26) if black else '')
        out.append(f'<section class="page lvp"><div class="lvhead"><div class="lvnum">{i + 1}</div><div><div class="k">{L["world"]} {w + 1} · {L["level"]} {i + 1} {L["of"]} {len(LEVELS)}</div>'
                   f'<h1>{nm}</h1></div><div class="dice">{head_dice}</div></div>{facts}'
                   f'<h3 class="st">{L["setup_t"]}</h3><ol class="steps">' + ''.join(f'<li>{x}</li>' for x in steps) + '</ol>'
                   f'<div class="goal"><b class="t">{L["goal_t"]}</b>{goal}</div>'
                   f'<div class="tip"><b class="t">{L["remember"]}</b>{L["tips"][i + 1]}</div>'
                   f'<div class="nums">{L["numbers_t"]} ({L["piles_c"](C).lower()}):<br>{nums}</div>'
                   f'<div class="notes"><b>{L["notes"]}</b>' + '<div class="nl"></div>' * 2 + '</div>'
                   f'<div class="done"><span><span class="bx"></span>{L["done"]} {L["with3"]}</span><span><span class="bx"></span>{L["done"]} {L["with4"]}</span>'
                   f'<span>{L["date"]}:</span><span class="line"></span></div></section>')
    out.append('</body></html>')
    html_path = HERE / f'niveles_{lang}.html'
    html_path.write_text(''.join(out))
    pdf = HERE / L['file']
    js = (f"let chromium; try {{ ({{ chromium }} = require('playwright')); }} catch (e) {{ ({{ chromium }} = require('/opt/node-tools/node_modules/playwright')); }}"
          f"(async () => {{ const b = await chromium.launch(); const p = await b.newPage(); await p.goto('file://{html_path}'); await p.waitForTimeout(300);"
          f"await p.pdf({{ path: '{pdf}', format: 'A4', printBackground: true, preferCSSPageSize: true }}); await b.close(); }})();")
    subprocess.run(['node', '-e', js], check=True)
    print(lang, '->', pdf)


if __name__ == '__main__':
    for lg in ('es', 'en'):
        build(lg)
