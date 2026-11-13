"""Builds the English rulebook (reglas/rules_en.html) and prints it to reglas/BlindSpots_Rules_EN.pdf.

Usage:  python3 reglas/build_rules.py   (needs Playwright's Chromium for the PDF)
The card pictures come from cartas/generar_cartas.py, so they always match the printed cards.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'cartas'))
import generar_cartas as gc  # noqa: E402

objs = gc.load_objectives()


def card(i):
    """Objective card number i (1-based), as on the printed card."""
    return gc.card_svg(objs[i - 1], i)


def find(**kw):
    """Number of the first objective card with these fields (numbers change when cards are removed)."""
    return next(i + 1 for i, o in enumerate(objs) if all(o.get(k) == v for k, v in kw.items()))


def die(colour, face, size=26):
    fill = gc.COLORS.get(colour, colour)
    pip = '#3b2c00' if colour == 'amarillo' else '#ffffff'
    return (f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">'
            + gc.die_svg(1, 1, size - 2, fill, face, pip) + '</svg>')


COVER_DICE = ''.join(
    f'<span class="cd" style="left:{x}%;top:{y}%;transform:rotate({r}deg)">{die(c, f, int(s * 1.7))}</span>'
    for x, y, r, c, f, s in [
        (8, 14, -14, 'azul', 5, 64), (26, 6, 9, 'rojo', 3, 52), (72, 9, -8, 'verde', 6, 58),
        (86, 24, 16, 'verde', 2, 48), (14, 66, 12, 'amarillo', 4, 50), (80, 70, -18, 'azul', 1, 60),
        (62, 80, 7, 'rojo', 6, 44), (32, 82, -6, 'verde', 2, 40), (90, 52, 4, '#8b93a1', 3, 38),
        (4, 42, -4, '#1c1e23', 5, 40)])

BOMB = ''.join(gc.black_card_svg(k) for k in (0, 2, 7))

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>BlindSpots · Rules</title>
<style>
@page {{ size: A4; margin: 18mm 17mm 20mm; @bottom-center {{ content: counter(page); font: 600 9pt 'Inter', sans-serif; color: #8a94a6; }} }}
@page cover {{ margin: 0; @bottom-center {{ content: none; }} }}
:root {{ --ink: #18202c; --muted: #5d6778; --line: #d9dee6; --blue: #2f6fdb; --orange: #ee8420; --green: #2a9a58;
  --purple: #d7263d; --red: #d7263d; --yellow: #f1c232; --paper: #fdfcf7; --tint: #f2f5fa; }}
* {{ box-sizing: border-box; }}
html {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ margin: 0; font: 400 10pt/1.5 'Inter', 'DejaVu Sans', sans-serif; color: var(--ink); background: #fff; }}
h1, h2, h3 {{ font-family: 'Inter Display', 'Inter', sans-serif; line-height: 1.15; margin: 0; }}
h2 {{ font-size: 19pt; font-weight: 800; letter-spacing: -.01em; margin: 0 0 10px; padding-top: 4px; display: flex; align-items: center; gap: 10px; break-after: avoid; }}
h2 .bar {{ display: inline-flex; gap: 3px; }}
h2 .bar i {{ width: 7px; height: 22px; border-radius: 2px; display: block; }}
h3 {{ font-size: 12pt; font-weight: 700; margin: 16px 0 6px; break-after: avoid; }}
p {{ margin: 0 0 8px; }}
section {{ margin-bottom: 22px; }}
section.page {{ break-before: page; }}
.lead {{ font-size: 11pt; color: var(--muted); }}
table {{ border-collapse: collapse; width: 100%; margin: 8px 0 12px; font-size: 9pt; break-inside: avoid; }}
th {{ text-align: left; background: var(--ink); color: #fff; font-weight: 600; padding: 5px 8px; }}
td {{ padding: 4.5px 8px; border-bottom: 1px solid var(--line); vertical-align: top; }}
tr:nth-child(even) td {{ background: #f7f8fb; }}
td.n {{ font-weight: 700; white-space: nowrap; }}
table.compact {{ font-size: 8.3pt; }} table.compact td {{ padding: 2.6px 8px; }}
ol, ul {{ margin: 0 0 10px; padding-left: 20px; }}
li {{ margin-bottom: 4px; }}
ol.steps {{ list-style: none; padding: 0; counter-reset: s; }}
ol.steps > li {{ counter-increment: s; position: relative; padding-left: 34px; margin-bottom: 8px; }}
ol.steps > li::before {{ content: counter(s); position: absolute; left: 0; top: 0; width: 23px; height: 23px; border-radius: 6px;
  background: var(--ink); color: #fff; font-weight: 700; font-size: 10pt; display: grid; place-items: center; }}
.box {{ border-radius: 10px; padding: 10px 14px; margin: 10px 0 14px; break-inside: avoid; }}
.box b.t {{ display: block; font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; margin-bottom: 3px; }}
.box.example {{ background: #eef4fd; border-left: 5px solid var(--blue); }}
.box.example b.t {{ color: var(--blue); }}
.box.important {{ background: #fdf3e8; border-left: 5px solid var(--orange); }}
.box.important b.t {{ color: var(--orange); }}
.box.tip {{ background: #eef8f2; border-left: 5px solid var(--green); }}
.box.tip b.t {{ color: var(--green); }}
.motto {{ font-family: 'Inter Display', sans-serif; font-weight: 800; font-size: 14pt; text-align: center; margin: 14px 0; }}
.cards {{ display: flex; gap: 12px; justify-content: center; margin: 10px 0 6px; break-inside: avoid; }}
.cards figure {{ margin: 0; text-align: center; font-size: 8pt; color: var(--muted); width: 34mm; }}
.cards svg {{ width: 34mm; height: auto; display: block; margin-bottom: 4px; filter: drop-shadow(0 1px 2px rgba(0,0,0,.18)); }}
.two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }}
.faq p b {{ display: block; }}
.ref {{ border: 2px solid var(--ink); border-radius: 12px; padding: 12px 16px; break-inside: avoid; }}
.small {{ font-size: 8.5pt; color: var(--muted); }}
/* cover */
.cover {{ page: cover; position: relative; width: 210mm; height: 297mm; background: #18202c; color: #fff; overflow: hidden; break-after: page; }}
.cover .cd {{ position: absolute; filter: drop-shadow(0 4px 8px rgba(0,0,0,.45)); }}
.cover .logo {{ position: absolute; left: 0; right: 0; top: 38%; text-align: center; font: 900 54pt 'Inter Display', sans-serif; letter-spacing: .02em; }}
.cover .logo .dot {{ display: inline-block; width: 30px; height: 30px; border-radius: 50%; background: var(--orange); margin: 0 10px; vertical-align: middle; position: relative; top: -6px; }}
.cover .tag {{ position: absolute; left: 0; right: 0; top: 52%; text-align: center; font: 500 15pt 'Inter', sans-serif; color: #c9d1de; line-height: 1.6; }}
.cover .meta {{ position: absolute; left: 0; right: 0; bottom: 30mm; text-align: center; font: 600 12pt 'Inter', sans-serif; letter-spacing: .12em; text-transform: uppercase; color: #fff; }}
.cover .meta span {{ display: inline-block; margin: 0 12px; padding: 6px 14px; border: 1.5px solid rgba(255,255,255,.35); border-radius: 999px; }}
.cover .rb {{ position: absolute; left: 0; right: 0; top: 30%; text-align: center; font: 700 12pt 'Inter', sans-serif; letter-spacing: .4em; color: var(--yellow); }}
</style></head><body>

<div class="cover">
  {COVER_DICE}
  <div class="rb">RULEBOOK</div>
  <div class="logo">BLIND<span class="dot"></span>SPOTS</div>
  <div class="tag">You can see everyone else's mission.<br>Everyone can see yours.<br>Nobody can see their own.</div>
  <div class="meta"><span>3–4 players</span><span>Ages 10+</span><span>20 min</span></div>
</div>

<section>
  <h2><span class="bar"><i style="background:var(--blue)"></i><i style="background:var(--orange)"></i><i style="background:var(--green)"></i></span>Game Idea</h2>
  <p class="lead">A cooperative game of dice and deduction for 3 or 4 players.</p>
  <p>In BlindSpots, everyone can see your mission, except you. Each player places one or more objective cards so that every other player can read them, while the owner sees only the back. Over several rounds you split colourful dice into groups and choose which group to take. Your teammates know what you need; you must trust their hints and read their choices.</p>
  <p>You win or lose together. At the end of the game all cards are revealed. If the team has completed its missions (or collected enough stars, depending on the level), everybody wins.</p>
  <p class="motto">Everyone sees your mission. Everyone helps you.<br>Only you are in the dark.</p>
</section>

<section>
  <h2><span class="bar"><i style="background:var(--purple)"></i><i style="background:var(--yellow)"></i></span>Components</h2>
  <table>
    <tr><th>Qty</th><th>Component</th><th>Notes</th></tr>
    <tr><td class="n">60</td><td>Coloured dice</td><td>15 each in blue, red, green and yellow</td></tr>
    <tr><td class="n">1</td><td>Grey die</td><td>Grey die variant (campaign levels 11–15)</td></tr>
    <tr><td class="n">4</td><td>Black dice</td><td>Black die variant, the “Bomb” (campaign levels 16–20)</td></tr>
    <tr><td class="n">1</td><td>Cloth bag</td><td>Holds the coloured dice in play</td></tr>
    <tr><td class="n">{len(objs)}</td><td>Objective cards</td><td>Numbered 1–{len(objs)}, 1 to 5 stars each</td></tr>
    <tr><td class="n">7</td><td>Grey cards</td><td>Numbered G1–G7, grey back</td></tr>
    <tr><td class="n">9</td><td>Black cards</td><td>Numbered N1–N9, black back</td></tr>
    <tr><td class="n">4</td><td>Action cards</td><td>Numbered A1–A4: Reroll, +1 / −1, Flip, Remove</td></tr>
    <tr><td class="n">5</td><td>Card stands</td><td>Hold your cards facing the other players</td></tr>
    <tr><td class="n">1</td><td>Campaign log</td><td>Track your progress through the 25 levels</td></tr>
    <tr><td class="n">1</td><td>Rulebook</td><td>This booklet</td></tr>
  </table>
  <p>The cards carry no text: only dice, colours, numbers and symbols, so they can be played in any language. The small number in the bottom right corner identifies each card and matches the card list on the separate card sheet.</p>
</section>

<section class="page">
  <h2><span class="bar"><i style="background:var(--green)"></i><i style="background:var(--blue)"></i></span>Setup</h2>
  <p>These steps describe a free game. When you play the campaign, the level you are playing fixes the colours, cards, dice and stars to win (see <i>Campaign</i>).</p>
  <ol class="steps">
    <li><b>Choose the colours.</b> With 3 colours, play with blue, red and green. With 4, add yellow.</li>
    <li><b>Fill the bag.</b> Place 15 dice of each colour in play into the bag. Return the other dice to the box.</li>
    <li><b>Agree on the mission.</b> Decide how many objectives each player receives (1 to 3) and which star values may come up. Then decide what the team needs to win: either <i>every objective</i>, or a total number of stars (see <i>End of the Game</i>).</li>
    <li><b>Deal the objective cards.</b> Shuffle the objective cards that fit your game and deal the agreed number to each player, face down. Leave out cards that show a colour not in play.</li>
    <li><b>Place your cards without looking.</b> Without looking at the front, slide your cards into your card stand so that the front faces the other players. From now on you may look at everyone's cards except your own.</li>
    <li><b>Choose the first dealer.</b> Pick a player at random. Play passes clockwise; each player deals once.</li>
    <li><b>Variants.</b> If you play with the grey die, black dice or action cards, prepare them now (see <i>Variants</i>).</li>
  </ol>
  <div class="box important"><b class="t">Important</b>Never look at your own cards until the end of the game. If you see one by accident, swap it for a new card from the deck.</div>
</section>

<section class="page">
  <h2><span class="bar"><i style="background:var(--orange)"></i><i style="background:var(--purple)"></i></span>Playing the Game</h2>
  <p>A game lasts as many rounds as there are players. In each round, one player is the <b>dealer</b>. The first dealer starts; after each round, the role passes to the left.</p>
  <div class="two">
    <div>
      <h3>1. Draw and roll</h3>
      <p>The dealer draws dice from the bag at random, without looking, and rolls them:</p>
      <table><tr><th>Players</th><th>Dice per round</th></tr><tr><td>3</td><td>5</td></tr><tr><td>4</td><td>7</td></tr></table>
      <p class="small">Rule of thumb: (players × 2) − 1. Dice that leave the bag never return to it, unless an action says so.</p>
      <h3>2. Form groups</h3>
      <p>The dealer splits the rolled dice into as many groups as there are players. Groups do not have to be the same size, but each group must contain at least one die. The dealer may not change the value shown on any die.</p>
    </div>
    <div>
      <h3>3. Choose groups</h3>
      <p>Starting with the player to the dealer's left and going clockwise, each player chooses one of the remaining groups and places it in their personal area. <b>The dealer takes the last group.</b></p>
      <p>The dealer knows what the others need, but not what they need themselves. Building the groups is the heart of the game: give each teammate a group that helps them, and hope that what is left suits you.</p>
      <h3>4. Next round</h3>
      <p>The dice in your area stay there until the end of the game and all count towards your mission. The player to the left of the dealer becomes the new dealer and a new round begins.</p>
    </div>
  </div>
</section>

<section>
  <h2><span class="bar"><i style="background:var(--blue)"></i><i style="background:var(--green)"></i></span>Communication</h2>
  <p>Talking is part of the game, within limits. You may discuss the groups on the table and give advice, but you may never reveal what a card says.</p>
  <table>
    <tr><th>Allowed</th><th>Not allowed</th></tr>
    <tr><td>“I think group B suits you better.”</td><td>“Your card says: no blue dice.”</td></tr>
    <tr><td>“That die could be dangerous for someone.”</td><td>Reading out, describing or pointing at a symbol on someone's card</td></tr>
    <tr><td>“I'd rather not take the green dice.”</td><td>Telling a player how many stars their cards are worth</td></tr>
  </table>
  <p>When in doubt, ask the table. The spirit of the game: hints, not answers.</p>
</section>

<section class="page">
  <h2><span class="bar"><i style="background:var(--yellow)"></i><i style="background:var(--orange)"></i></span>Objective Cards</h2>
  <p>Each objective card states one condition about <b>all the dice in your area at the end of the game</b>. Its stars (1 to 5) show its difficulty and how many stars it is worth when completed. If you hold several cards, together they form your mission.</p>
  <div class="cards">
    <figure>{card(find(tipo='ninguno', color='azul'))}No blue dice</figure>
    <figure>{card(find(tipo='al_menos', color='azul', n=2))}At least 2 blue dice<br>(exactly 2: +1★)</figure>
    <figure>{card(find(tipo='exactamente', color='rojo', n=2))}Exactly 2 red dice</figure>
    <figure>{card(find(tipo='menos_numero_que_nadie', numero=2))}Fewer dice showing a 2 than any other player</figure>
  </div>
  <h3>Reading the symbols</h3>
  <table>
    <tr><th>Symbol</th><th>Meaning</th><th>Example</th></tr>
    <tr><td>Die with a red “no” sign</td><td>None of these dice</td><td>No blue dice</td></tr>
    <tr><td>2 × die</td><td>2 or more of these dice</td><td>2 green dice</td></tr>
    <tr><td>≥2 × die</td><td>At least 2 of these dice</td><td>At least 2 blue dice</td></tr>
    <tr><td>=2 × die</td><td>Exactly 2, no more, no fewer</td><td>Exactly 2 green dice</td></tr>
    <tr><td>≤1 × die</td><td>At most 1 of these dice</td><td>At most 1 blue die</td></tr>
    <tr><td>Σ</td><td>The sum of the values shown</td><td>Your blue dice add up to 12 or more</td></tr>
    <tr><td>#</td><td>The number of dice</td><td>7 or more dice in total</td></tr>
    <tr><td>Four-colour die</td><td>A die of any colour</td><td>Your dice add up to 20 or less</td></tr>
    <tr><td>White die face</td><td>A value, regardless of colour</td><td>No die showing a 3</td></tr>
    <tr><td>Colour wheel</td><td>Different colours</td><td>Dice of exactly 3 different colours</td></tr>
    <tr><td>♛ ▲ / ♛ ▼</td><td>More / fewer than every other player</td><td>Fewer dice showing a 4 than any other player</td></tr>
  </table>
  <div class="two">
    <div>
      <h3>The bonus star</h3>
      <p>Cards with an asterisk line at the bottom, such as <b>* =2 → +1★</b>, reward precision. The objective is met with the amount shown or more (or, for “at most” cards, that amount or fewer). If you hit the amount <b>exactly</b>, the card earns 1 extra star.</p>
      <h3>Comparisons with other players</h3>
      <p>Cards with a crown compare you with every other player: you must be strictly first. A tie does not count, with one exception: for “fewer than any other player” cards, having none at all counts even if other players have none either.</p>
    </div>
    <div>
      <h3>Values, colours and special dice</h3>
      <ul>
        <li><b>Value</b> means the number of pips on the die, from 1 to 6. Even values are 2, 4 and 6; odd values are 1, 3 and 5.</li>
        <li><b>Straights</b> are consecutive values, such as 2-3-4-5. A colour straight must be made of dice of one colour.</li>
        <li>The <b>grey</b> and <b>black</b> dice count as dice, for sums and for values, but never as a colour.</li>
      </ul>
    </div>
  </div>
</section>



<section class="page">
  <h2><span class="bar"><i style="background:var(--purple)"></i><i style="background:var(--blue)"></i></span>End of the Game</h2>
  <p>The game ends after the last dealer's round. If you play with black dice, resolve the bombs first (see <i>Variants</i>). Then everyone turns their card stand around and checks their cards against the dice in their area.</p>
  <p>The team wins in one of two ways, agreed during setup:</p>
  <ul>
    <li><b>Every objective.</b> Every card of every player must be completed.</li>
    <li><b>Team stars.</b> Each completed card is worth its stars, plus 1 bonus star for an exact hit. Add up the stars of the whole team. If the total reaches the target, you win.</li>
  </ul>
  <div class="box example"><b class="t">Example</b>Ana completes her 3-star card and hits its bonus. Bruno completes a 2-star card and fails a 1-star card. Carla completes a 4-star card. The team scores 4 + 2 + 4 = <b>10 stars</b>.</div>
  <p>In addition, the team loses whatever its score if:</p>
  <ul>
    <li>the player holding the grey die has not met the grey card, or</li>
    <li>a player received a second black die (see <i>Variants</i>).</li>
  </ul>
  <p>Lost? Shuffle, deal new cards and try again. Every game is different.</p>
</section>

<section>
  <h2><span class="bar"><i style="background:var(--orange)"></i><i style="background:var(--yellow)"></i><i style="background:var(--green)"></i></span>Variants</h2>
  <p>The three variants below are introduced step by step in the campaign. In a free game, you may add the grey die.</p>
  <h3>Special actions</h3>
  <p><b>Setup.</b> With 3 players, shuffle the 4 action cards and place 3 of them face up; return the fourth to the box. With 4 players, use all 4.</p>
  <p><b>Using an action.</b> At any time during the game, any player may use one available action on <b>any visible die</b>: in the dealer's roll, in a group, or in any player's area. Then take the card: it is no longer available to anyone. Each player may use only one action per game. Once all the dice have been dealt, there is a last chance: before the cards are revealed (and before the bombs go off), players may still use the actions left.</p>
  <table>
    <tr><th>Card</th><th>Effect</th></tr>
    <tr><td class="n">A1 Reroll</td><td>Roll the die again.</td></tr>
    <tr><td class="n">A2 +1 / −1</td><td>Turn the die to one pip more or one pip less (never below 1 or above 6).</td></tr>
    <tr><td class="n">A3 Flip</td><td>Turn the die to its opposite face: 1 ↔ 6, 2 ↔ 5, 3 ↔ 4.</td></tr>
    <tr><td class="n">A4 Remove</td><td>Put the die back into the bag (not the grey or black die).</td></tr>
  </table>
  <div class="box tip"><b class="t">Tip</b>Announce each action clearly: who you are, which die, whose die it was and its value before and after (“I flip Bruno's red die: from 5 to 2”). Agree on it as a team: a used action is gone for everyone.</div>
</section>

<section class="page">
  <h3 style="margin-top:0">The grey die</h3>
  <div class="two">
    <div>
      <p><b>Setup.</b> Shuffle the 7 grey cards and place them face down.</p>
      <p><b>First round.</b> The first dealer also rolls the grey die and reveals the top grey card, face up for everyone, including you. The grey die joins the groups like any other die.</p>
      <p><b>End of the game.</b> Whoever holds the grey die must meet the grey card. If not, the team loses, even if it has enough stars. The grey die counts as a die, for sums and for values, but not as a colour.</p>
    </div>
    <div class="cards" style="justify-content:flex-start"><figure>{gc.grey_card_svg(0)}G1: at least 1 die of each colour</figure><figure>{gc.grey_card_svg(6)}G7: total of no more than 15</figure></div>
  </div>
  <table>
    <tr><th>Card</th><th>Rule for the holder of the grey die</th></tr>
    <tr><td class="n">G1</td><td>At least 1 die of each colour in play</td></tr>
    <tr><td class="n">G2</td><td>Total of at least 15 (grey die included)</td></tr>
    <tr><td class="n">G3</td><td>No other die with the same value as the grey die</td></tr>
    <tr><td class="n">G4</td><td>At most 6 dice (grey die included)</td></tr>
    <tr><td class="n">G5</td><td>At least one other die with the same value as the grey die</td></tr>
    <tr><td class="n">G6</td><td>No more than 3 dice of the same colour</td></tr>
    <tr><td class="n">G7</td><td>Total of no more than 15 (grey die included)</td></tr>
  </table>

  <h3>The black die: the Bomb</h3>
  <p><b>Setup.</b> Shuffle the 9 black cards and place them face down. The black cards form a single deck from game to game: a card only comes back once all the others have been drawn. When the deck runs out, shuffle all 9 again.</p>
  <p><b>Each round.</b> Before drawing any dice, the dealer reveals the top black card, so everyone knows its effect before anyone takes the black die. Then they draw coloured dice as the level states (6 with 3 players, 8 with 4), roll them together with one black die and place the card next to that black die. The card travels with the die.</p>
  <p><b>One black die each.</b> Each player may end the game with only <b>one</b> black die. If you already have one, you may not choose a group that contains another.</p>
  <div class="box important"><b class="t">Careful with the dealer</b>If the last group contains a black die and the dealer already has one, <b>the team loses the level at once</b>.</div>
</section>

<section>
  <p><b>The bombs go off.</b> After the last round and before scoring, each player holding a black die, in turn order, applies its card to <b>their own dice</b> and removes them. You choose which dice, among those the card allows. If no die fits the card, nothing happens. The black die itself is never removed by its card. Removed dice go back to the box.</p>
  <div class="cards"><figure>{gc.black_card_svg(0)}N1: your lowest die</figure><figure>{gc.black_card_svg(2)}N3: same value as the black die</figure><figure>{gc.black_card_svg(7)}N8: lower than or equal to the black die</figure></div>
  <table>
    <tr><th>Card</th><th>Remove from your area</th></tr>
    <tr><td class="n">N1</td><td>Your lowest die (your choice among ties)</td></tr>
    <tr><td class="n">N2</td><td>Your highest die (your choice among ties)</td></tr>
    <tr><td class="n">N3</td><td>A die with the same value as the black die</td></tr>
    <tr><td class="n">N4</td><td>A die of the colour you have most of</td></tr>
    <tr><td class="n">N5</td><td>A die of the colour you have fewest of</td></tr>
    <tr><td class="n">N6</td><td>Any 2 of your dice, your choice</td></tr>
    <tr><td class="n">N7</td><td>Two dice with the same value</td></tr>
    <tr><td class="n">N8</td><td>A die with a value lower than or equal to the black die</td></tr>
    <tr><td class="n">N9</td><td>A die with a value higher than or equal to the black die</td></tr>
  </table>
  <p>The black die counts as a die, for sums and for values, but not as a colour. Actions may not be used while the bombs go off.</p>
</section>

<section class="page">
  <h2><span class="bar"><i style="background:var(--blue)"></i><i style="background:var(--orange)"></i><i style="background:var(--green)"></i><i style="background:var(--purple)"></i><i style="background:var(--yellow)"></i></span>Campaign</h2>
  <p>The campaign leads 3 or 4 players through 25 levels in five worlds of five levels each. Each level fixes the colours, the objective cards each player receives, the dice in the bag and the stars the team needs. Beat a level to unlock the next one and tick it in the campaign log. If you lose, replay the level with new cards. You may replay any level you have already beaten.</p>
  <p><b>Dealing campaign cards.</b> Sort the objective cards by stars. Each player receives one card of each value shown in the <i>Cards</i> column: “3 + 1” means one 3-star card and one 1-star card. <b>Stars to win:</b> use the value for your player count; add up the stars of all completed cards, plus bonus stars.</p>
  <table class="compact">
    <tr><th>Level</th><th>Name</th><th>Colours</th><th>Cards</th><th>Dice per colour<br>3 / 4 players</th><th>Stars to win<br>3 / 4 players</th><th>Rules</th></tr>
    {''.join(f'<tr><td class="n">{n}</td><td>{nm}</td><td>{c}</td><td>{cards}</td><td>{dice}</td><td>{stars}</td><td>{rule}</td></tr>' for n, nm, c, cards, dice, stars, rule in [
      (1, 'First Steps 1', 3, '1', '6 / 10', '2 / 3', 'Basic game'), (2, 'First Steps 2', 3, '2', '6 / 10', '4 / 6', 'Basic game'),
      (3, 'First Steps 3', 3, '1 + 1', '6 / 10', '5 / 7', 'Basic game'), (4, 'First Steps 4', 3, '2 + 2', '6 / 10', '10 / 14', 'Basic game'),
      (5, 'First Steps 5', 3, '3', '6 / 10', '9 / 12', 'Basic game'), (6, 'Actions 1', 3, '3 + 1', '6 / 10', '10 / 13', 'Special actions'),
      (7, 'Actions 2', 3, '3 + 2', '6 / 10', '13 / 18', 'Special actions'), (8, 'Actions 3', 3, '3 + 3', '6 / 10', '15 / 20', 'Special actions'),
      (9, 'Actions 4', 3, '4 + 3', '6 / 10', '18 / 25', 'Special actions'), (10, 'Actions 5', 3, '4 + 4', '6 / 10', '12 / 16', 'Special actions'),
      (11, 'Grey 1', 3, '3', '6 / 10', '6 / 8', 'Grey die + actions'), (12, 'Grey 2', 3, '1 + 3', '6 / 10', '10 / 13', 'Grey die + actions'),
      (13, 'Grey 3', 3, '2 + 3', '6 / 10', '12 / 16', 'Grey die + actions'), (14, 'Grey 4', 3, '3 + 3', '6 / 10', '14 / 19', 'Grey die + actions'),
      (15, 'Grey 5', 3, '5', '6 / 10', '10 / 13', 'Grey die + actions'), (16, 'Bomb 1', 3, '4', '6 / 11', '8 / 12', 'Black die + actions'),
      (17, 'Bomb 2', 3, '2 + 3', '6 / 11', '12 / 17', 'Black die + actions'), (18, 'Bomb 3', 3, '1 + 2 + 3', '6 / 11', '15 / 20', 'Black die + actions'),
      (19, 'Bomb 4', 3, '3 + 4', '6 / 11', '18 / 24', 'Black die + actions'), (20, 'Bomb 5', 3, '2 + 2 + 3', '6 / 11', '20 / 26', 'Black die + actions'),
      (21, 'Four Colours 1', 4, '2 + 3', '6 / 10', '13 / 17', 'Special actions'), (22, 'Four Colours 2', 4, '3 + 3', '6 / 10', '15 / 20', 'Special actions'),
      (23, 'Four Colours 3', 4, '3 + 4', '6 / 10', '21 / 24', 'Special actions'), (24, 'Four Colours 4', 4, '2 + 2 + 3', '6 / 10', '19 / 23', 'Special actions'),
      (25, 'Four Colours 5', 4, '3 + 3 + 3', '6 / 10', '24 / 33', 'Special actions')])}
  </table>
  <p class="small">In the Bomb levels (16–20), the dealer draws 6 coloured dice per round with 3 players and 8 with 4, plus one black die.</p>
  <div class="box tip"><b class="t">New rules along the way</b>Before levels 6, 11 and 16, read the matching section of <i>Variants</i> aloud: special actions, the grey die and the black die. From level 6 on, special actions are used in every level. Each new world adds one idea; the levels within a world grow harder.</div>
</section>

<section>
  <h2><span class="bar"><i style="background:var(--green)"></i><i style="background:var(--yellow)"></i></span>Free Play</h2>
  <p>Outside the campaign, set up the game to suit your group:</p>
  <table>
    <tr><th>Setting</th><th>Options</th></tr>
    <tr><td>Players</td><td>3 or 4</td></tr>
    <tr><td>Colours</td><td>3 or 4</td></tr>
    <tr><td>Objectives per player</td><td>1, 2 or 3</td></tr>
    <tr><td>Difficulty</td><td>Any combination of 1★ to 5★ cards</td></tr>
    <tr><td>To win</td><td>Every objective, or a team star total</td></tr>
    <tr><td>Grey die</td><td>On or off</td></tr>
  </table>
  <div class="box tip"><b class="t">Your first game</b>We recommend 3 colours, 1 objective per player and cards of 1★ to 3★.</div>
</section>

<section class="faq">
  <h2><span class="bar"><i style="background:var(--purple)"></i><i style="background:var(--orange)"></i></span>Frequently Asked Questions</h2>
  <div class="two">
    <div>
      <p><b>Can a group be empty?</b> No. Every group contains at least one die.</p>
      <p><b>May the dealer see the values before forming groups?</b> Yes. The dice are rolled first and then split as they lie.</p>
      <p><b>Two of my cards seem to contradict each other.</b> Cards dealt to the same player must be compatible. If you deal by hand, reshuffle a card that clearly contradicts another.</p>
      <p><b>Two players have the same crown card.</b> Only one player can be strictly first at the same thing. Replace the second copy.</p>
    </div>
    <div>
      <p><b>Does the grey or black die count for “dice of exactly 3 colours”?</b> No. They count as dice and for values, never as a colour.</p>
      <p><b>Can an action target the black die?</b> Yes. If the black die is removed, its card is discarded with it.</p>
      <p><b>The black card says “your lowest die” and I have two 1s.</b> Choose either one.</p>
      <p><b>Can an action remove the grey or black die?</b> No. Remove only works on coloured dice; the other actions can change the grey and black dice.</p>
    </div>
  </div>
</section>

<section>
  <div class="ref">
    <h2 style="font-size:15pt"><span class="bar"><i style="background:var(--blue)"></i><i style="background:var(--orange)"></i><i style="background:var(--green)"></i></span>Quick Reference</h2>
    <ol class="steps">
      <li>The dealer draws (players × 2) − 1 dice and rolls them.</li>
      <li>The dealer forms one group per player, at least one die each.</li>
      <li>Clockwise from the dealer's left, each player takes a group; the dealer takes the last one.</li>
      <li>The role of dealer passes to the left. Play as many rounds as there are players.</li>
      <li>Bombs go off (black die only), then reveal all cards and score.</li>
    </ol>
  </div>
  <p class="motto">Everyone sees your mission. Only you are in the dark.</p>
</section>
</body></html>
"""

out_html = HERE / 'rules_en.html'
out_html.write_text(html)
print('html ->', out_html)

js = f"""
let chromium; try {{ ({{ chromium }} = require('playwright')); }} catch (e) {{ ({{ chromium }} = require('/opt/node-tools/node_modules/playwright')); }}
(async () => {{
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://{out_html}'); await p.waitForTimeout(300);
  await p.pdf({{ path: '{HERE / "BlindSpots_Rules_EN.pdf"}', format: 'A4', printBackground: true, preferCSSPageSize: true }});
  await b.close(); console.log('pdf ok');
}})();
"""
subprocess.run(['node', '-e', js], check=True)
