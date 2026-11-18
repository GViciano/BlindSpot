"""Reglamento en castellano: crea reglas/reglas_es.html y lo imprime en reglas/BlindSpots_Reglas_ES.pdf.

Uso:  python3 reglas/build_rules_es.py   (necesita el Chromium de Playwright para el PDF)
Usa el mismo diseño que el reglamento en inglés (los estilos se leen de build_rules.py) y las mismas
ilustraciones de cartas de cartas/generar_cartas.py. La tabla de la campaña sale de campana.js.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'cartas'))
import generar_cartas as gc  # noqa: E402

objs = gc.load_objectives()
CAMP = json.loads(subprocess.run(
    ['node', '-e', 'global.window={};require(process.argv[1]);process.stdout.write(JSON.stringify(window.BLINDSPOTS_CAMPANA))',
     str(HERE.parent / 'campana.js')], capture_output=True, text=True, check=True).stdout)

# Same look as the English rulebook: its stylesheet is reused as it is.
_src = (HERE / 'build_rules.py').read_text()
CSS = _src[_src.index('<style>') + 7:_src.index('</style>')].replace('{{', '{').replace('}}', '}')


def camp_name(i, l):
    return l.get('nombre') or (f'Primeros pasos {i + 1}' if i < 5 else f'Acciones {i - 4}')


def camp_rule(l):
    parts = [n for k, n in (('dado_gris', 'Dado gris'), ('dado_negro', 'Dado negro'), ('silencio', 'En silencio'),
                           ('solitario', 'Misión en solitario'), ('modificadores', 'acciones')) if l.get(k)]
    if not l.get('ganar'):
        parts.append('todo o nada')
    if not parts:
        return 'Juego básico'
    txt = ' + '.join(parts)
    return 'Acciones especiales' if txt == 'acciones' else txt[0].upper() + txt[1:]


def camp_rows():
    out = []
    for i, l in enumerate(CAMP):
        per = l.get('dados_por_ronda') or {'3': 5, '4': 7}
        need = l.get('ganar')
        stars = f'{need["3"]} / {need["4"]}' if need else 'Todas'
        out.append(f'<tr><td class="n">{i + 1}</td><td>{camp_name(i, l)}</td><td>{l["colores"]}</td><td>{" + ".join(map(str, l["cartas"]))}</td>'
                   f'<td>{l["dados"]["3"]} / {l["dados"]["4"]}</td><td>{per["3"]} / {per["4"]}{" +1" if l.get("dado_negro") else ""}</td>'
                   f'<td>{stars}</td><td>{camp_rule(l)}</td></tr>')
    return ''.join(out)


def card(i):
    return gc.card_svg(objs[i - 1], i)


def find(**kw):
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


def bar(*cols):
    return '<span class="bar">' + ''.join(f'<i style="background:var(--{c})"></i>' for c in cols) + '</span>'


html = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>BlindSpots · Reglas</title>
<style>{CSS}</style></head><body>

<div class="cover">
  {COVER_DICE}
  <div class="rb">REGLAMENTO</div>
  <div class="logo">BLIND<span class="dot"></span>SPOTS</div>
  <div class="tag">Ves la misión de todos los demás.<br>Todos ven la tuya.<br>Nadie ve la suya.</div>
  <div class="meta"><span>3–4 jugadores</span><span>+10 años</span><span>20 min</span></div>
</div>

<section>
  <h2>{bar('blue', 'orange', 'green')}Idea del juego</h2>
  <p class="lead">Un juego cooperativo de dados y deducción para 3 o 4 jugadores.</p>
  <p>En BlindSpots todo el mundo ve tu misión, menos tú. Cada jugador coloca una o varias cartas de objetivo de forma que los demás puedan leerlas, mientras que él solo ve el reverso. Durante varias rondas repartís dados de colores en grupos y elegís qué grupo os lleváis. Tus compañeros saben lo que necesitas; tú tienes que fiarte de sus pistas y leer sus decisiones.</p>
  <p>Se gana o se pierde en equipo. Al final de la partida se descubren todas las cartas. Si el equipo ha cumplido sus misiones (o ha reunido suficientes estrellas, según el nivel), ganáis todos.</p>
  <p class="motto">Todos ven tu misión. Todos te ayudan.<br>Solo tú estás a oscuras.</p>
</section>

<section>
  <h2>{bar('red', 'yellow')}Componentes</h2>
  <table>
    <tr><th>Cant.</th><th>Componente</th><th>Notas</th></tr>
    <tr><td class="n">60</td><td>Dados de colores</td><td>15 de cada: azul, rojo, verde y amarillo</td></tr>
    <tr><td class="n">1</td><td>Dado gris</td><td>Variante del dado gris (niveles 11–15 y 28 de la campaña)</td></tr>
    <tr><td class="n">4</td><td>Dados negros</td><td>Variante del dado negro, la «Bomba» (niveles 16–20 y 29)</td></tr>
    <tr><td class="n">1</td><td>Bolsa de tela</td><td>Para los dados de colores en juego</td></tr>
    <tr><td class="n">{len(objs)}</td><td>Cartas de objetivo</td><td>Numeradas del 1 al {len(objs)}, de 1 a 5 estrellas</td></tr>
    <tr><td class="n">7</td><td>Cartas grises</td><td>Numeradas G1–G7, reverso gris</td></tr>
    <tr><td class="n">9</td><td>Cartas negras</td><td>Numeradas N1–N9, reverso negro</td></tr>
    <tr><td class="n">4</td><td>Cartas de acción</td><td>Numeradas A1–A4: relanzar, +1 / −1, invertir, eliminar</td></tr>
    <tr><td class="n">5</td><td>Soportes para cartas</td><td>Sostienen tus cartas de cara a los demás jugadores</td></tr>
    <tr><td class="n">1</td><td>Hoja de campaña</td><td>Para apuntar vuestro avance por los {len(CAMP)} niveles</td></tr>
    <tr><td class="n">1</td><td>Reglamento</td><td>Este libreto</td></tr>
  </table>
  <p>Los dibujos de las cartas (dados, colores, números y símbolos) se entienden en cualquier idioma; debajo, cada carta repite su regla en inglés. El número pequeño de la esquina inferior derecha identifica cada carta y coincide con el listado de cartas. Las cartas de objetivo están numeradas por dificultad, de las de 1 estrella a las de 5. Las cartas marcadas con «4» abajo a la izquierda solo se usan con 4 colores.</p>
</section>

<section class="page">
  <h2>{bar('green', 'blue')}Preparación</h2>
  <p>Estos pasos describen una partida libre. En la campaña, el nivel que jugáis fija los colores, las cartas, los dados y las estrellas para ganar (consulta <i>Campaña</i>).</p>
  <ol class="steps">
    <li><b>Elegid los colores.</b> Con 3 colores se juega con azul, rojo y verde. Con 4, se añade el amarillo.</li>
    <li><b>Llenad la bolsa.</b> Meted 15 dados de cada color en juego. Devolved el resto a la caja.</li>
    <li><b>Acordad la misión.</b> Decidid cuántos objetivos recibe cada jugador (de 1 a 3) y qué valores de estrellas pueden salir. Después, decidid qué necesita el equipo para ganar: o <i>todos los objetivos</i>, o un total de estrellas (consulta <i>Final de la partida</i>).</li>
    <li><b>Repartid las cartas de objetivo.</b> Barajad las cartas de objetivo que encajen con la partida y repartid a cada jugador las acordadas, boca abajo. Dejad fuera las que muestran un color que no está en juego.</li>
    <li><b>Colocad vuestras cartas sin mirar.</b> Sin mirar el anverso, meted vuestras cartas en vuestro soporte de forma que el anverso mire a los demás. A partir de ahora podéis mirar las cartas de todos menos las vuestras.</li>
    <li><b>Elegid al primer repartidor.</b> Elegid un jugador al azar. Se juega en el sentido de las agujas del reloj y cada jugador reparte una vez.</li>
    <li><b>Variantes.</b> Si jugáis con el dado gris, los dados negros o las cartas de acción, preparadlos ahora (consulta <i>Variantes</i>).</li>
  </ol>
  <div class="box important"><b class="t">Importante</b>No mires nunca tus propias cartas hasta el final de la partida. Si ves una sin querer, cámbiala por otra del mazo.</div>
</section>

<section class="page">
  <h2>{bar('orange', 'red')}Cómo se juega</h2>
  <p>Una partida dura tantas rondas como jugadores. En cada ronda, un jugador es quien <b>reparte</b>. Empieza el primer repartidor y, al acabar cada ronda, el papel pasa al de su izquierda.</p>
  <div class="two">
    <div>
      <h3>1. Sacar y tirar</h3>
      <p>Quien reparte saca dados de la bolsa al azar, sin mirar, y los tira:</p>
      <table><tr><th>Jugadores</th><th>Dados por ronda</th></tr><tr><td>3</td><td>5</td></tr><tr><td>4</td><td>7</td></tr></table>
      <p class="small">Regla general: (jugadores × 2) − 1. Los dados que salen de la bolsa no vuelven a ella, salvo que una acción lo diga.</p>
      <h3>2. Formar grupos</h3>
      <p>Quien reparte divide los dados tirados en tantos grupos como jugadores. Los grupos no tienen que ser iguales, pero cada uno debe tener al menos un dado. No se puede cambiar el valor de ningún dado.</p>
    </div>
    <div>
      <h3>3. Elegir grupos</h3>
      <p>Empezando por el jugador a la izquierda de quien reparte y en el sentido de las agujas del reloj, cada jugador elige uno de los grupos que quedan y lo pone en su zona. <b>Quien reparte se queda el último grupo.</b></p>
      <p>Quien reparte sabe lo que necesitan los demás, pero no lo que necesita él. Formar los grupos es el corazón del juego: da a cada compañero un grupo que le ayude y espera que lo que quede te venga bien.</p>
      <h3>4. Siguiente ronda</h3>
      <p>Los dados de tu zona se quedan ahí hasta el final y todos cuentan para tu misión. El jugador a la izquierda de quien repartió pasa a repartir y empieza una nueva ronda.</p>
    </div>
  </div>
</section>

<section>
  <h2>{bar('blue', 'green')}Comunicación</h2>
  <p>Hablar forma parte del juego, con límites. Podéis comentar los grupos de la mesa y aconsejaros, pero nunca podéis revelar lo que dice una carta.</p>
  <table>
    <tr><th>Se puede</th><th>No se puede</th></tr>
    <tr><td>«Creo que el grupo B te va mejor».</td><td>«Tu carta dice: ningún dado azul».</td></tr>
    <tr><td>«Ese dado puede ser peligroso para alguien».</td><td>Leer, describir o señalar un símbolo de la carta de otro</td></tr>
    <tr><td>«Prefiero no llevarme los verdes».</td><td>Decirle a un jugador cuántas estrellas valen sus cartas</td></tr>
  </table>
  <p>Si hay dudas, se pregunta a la mesa. El espíritu del juego: pistas, no respuestas.</p>
</section>

<section class="page">
  <h2>{bar('yellow', 'orange')}Cartas de objetivo</h2>
  <p>Cada carta de objetivo pone una condición sobre <b>todos los dados de tu zona al final de la partida</b>. Sus estrellas (de 1 a 5) indican su dificultad y cuántas estrellas vale si se cumple. Si tienes varias cartas, juntas forman tu misión.</p>
  <div class="cards">
    <figure>{card(find(tipo='ninguno', color='azul'))}Ningún dado azul</figure>
    <figure>{card(find(tipo='al_menos', color='azul', n=2))}Al menos 2 dados azules<br>(exactamente 2: +1★)</figure>
    <figure>{card(find(tipo='exactamente', color='rojo', n=2))}Exactamente 2 dados rojos</figure>
    <figure>{card(find(tipo='menos_numero_que_nadie', numero=2))}Menos dados con un 2 que cualquier otro jugador</figure>
  </div>
  <h3>Cómo se leen los símbolos</h3>
  <table>
    <tr><th>Símbolo</th><th>Significado</th><th>Ejemplo</th></tr>
    <tr><td>Dado tachado</td><td>Ninguno de estos dados</td><td>Ningún dado azul</td></tr>
    <tr><td>6 × dado</td><td>6 o más de estos dados</td><td>6 dados en total</td></tr>
    <tr><td>≥2 × dado</td><td>Al menos 2 de estos dados</td><td>Al menos 2 dados azules</td></tr>
    <tr><td>=2 × dado</td><td>Exactamente 2, ni más ni menos</td><td>Exactamente 2 dados verdes</td></tr>
    <tr><td>≤1 × dado</td><td>Como máximo 1 de estos dados</td><td>Como máximo 1 dado azul</td></tr>
    <tr><td>Σ</td><td>La suma de los valores</td><td>Tus dados azules suman 12 o más</td></tr>
    <tr><td>#</td><td>El número de dados</td><td>7 dados o más en total</td></tr>
    <tr><td>Dado de cuatro colores</td><td>Un dado de cualquier color</td><td>Tus dados suman 20 o menos</td></tr>
    <tr><td>Cara de dado blanca</td><td>Un valor, sea del color que sea</td><td>Ningún dado con un 3</td></tr>
    <tr><td>? +1 +2…</td><td>Números seguidos, empezando por cualquiera</td><td>Una escalera de 3, como 4-5-6</td></tr>
    <tr><td>Rueda de colores</td><td>Colores distintos</td><td>Dados de exactamente 3 colores distintos</td></tr>
    <tr><td>♛ ▲ / ♛ ▼</td><td>Más / menos que cualquier otro jugador</td><td>Menos dados con un 4 que cualquier otro jugador</td></tr>
  </table>
  <div class="two">
    <div>
      <h3>La estrella extra</h3>
      <p>Las cartas con una línea con asterisco abajo, como <b>* =2 → +1★</b>, premian la precisión. El objetivo se cumple con la cantidad indicada o más (o, en las de «como máximo», con esa cantidad o menos). Si consigues la cantidad <b>exacta</b>, la carta da 1 estrella extra.</p>
      <h3>Comparaciones con los demás</h3>
      <p>Las cartas con corona te comparan con todos los demás jugadores: tienes que ser el primero en solitario. Un empate no vale, con una excepción: en las de «menos … que cualquier otro jugador», no tener ninguno cuenta aunque otros tampoco tengan ninguno.</p>
    </div>
    <div>
      <h3>Valores, colores y dados especiales</h3>
      <ul>
        <li>El <b>valor</b> es el número de puntos del dado, del 1 al 6. Los pares son 2, 4 y 6; los impares, 1, 3 y 5.</li>
        <li>Una <b>escalera</b> son valores seguidos, como 2-3-4-5, empezando por cualquier número. Una escalera de color tiene que ser de dados de un solo color.</li>
        <li>Los dados <b>gris</b> y <b>negro</b> cuentan como dados, para las sumas y para los valores, pero nunca como color.</li>
      </ul>
    </div>
  </div>
</section>

<section>
  <h2>{bar('red', 'blue')}Final de la partida</h2>
  <p>La partida termina tras la ronda del último repartidor. Si jugáis con dados negros, primero explotan las bombas (consulta <i>Variantes</i>). Después, todos giran su soporte y comprueban sus cartas con los dados de su zona.</p>
  <p>El equipo gana de una de estas dos formas, acordada al preparar la partida:</p>
  <ul>
    <li><b>Todos los objetivos.</b> Hay que cumplir todas las cartas de todos los jugadores.</li>
    <li><b>Estrellas del equipo.</b> Cada carta cumplida vale sus estrellas, más 1 estrella extra si se consigue la cantidad exacta. Se suman las estrellas de todo el equipo. Si el total llega al objetivo, ganáis.</li>
  </ul>
  <div class="box example"><b class="t">Ejemplo</b>Ana cumple su carta de 3 estrellas y consigue la extra. Bruno cumple una carta de 2 estrellas y falla una de 1. Carla cumple una carta de 4 estrellas. El equipo suma 4 + 2 + 4 = <b>10 estrellas</b>.</div>
  <p>Además, el equipo pierde, tenga las estrellas que tenga, si:</p>
  <ul>
    <li>quien tiene el dado gris no ha cumplido la carta gris, o</li>
    <li>un jugador ha recibido un segundo dado negro (consulta <i>Variantes</i>).</li>
  </ul>
  <p>¿Habéis perdido? Barajad, repartid cartas nuevas y volved a intentarlo. Cada partida es distinta.</p>
</section>

<section>
  <h2>{bar('orange', 'yellow', 'green')}Variantes</h2>
  <p>Las tres variantes siguientes se presentan poco a poco en la campaña. En una partida libre se puede añadir el dado gris.</p>
  <h3>Acciones especiales</h3>
  <p><b>Preparación.</b> Con 3 jugadores, barajad las 4 cartas de acción y poned 3 boca arriba; la cuarta vuelve a la caja. Con 4 jugadores, usad las 4.</p>
  <p><b>Usar una acción.</b> En cualquier momento de la partida, cualquier jugador puede usar una acción disponible sobre <b>cualquier dado a la vista</b>: en la tirada, en un grupo o en la zona de cualquier jugador. Después se queda la carta: ya no está disponible para nadie más. Cada jugador puede usar solo una acción por partida. Cuando se han repartido todos los dados hay una última oportunidad: antes de descubrir las cartas (y antes de que exploten las bombas) aún se pueden usar las acciones que queden.</p>
  <table>
    <tr><th>Carta</th><th>Efecto</th></tr>
    <tr><td class="n">A1 Relanzar</td><td>Vuelve a tirar el dado.</td></tr>
    <tr><td class="n">A2 +1 / −1</td><td>Gira el dado a un punto más o un punto menos (nunca por debajo de 1 ni por encima de 6).</td></tr>
    <tr><td class="n">A3 Invertir</td><td>Gira el dado a su cara opuesta: 1 ↔ 6, 2 ↔ 5, 3 ↔ 4.</td></tr>
    <tr><td class="n">A4 Eliminar</td><td>Devuelve el dado a la bolsa (no el dado gris ni el negro).</td></tr>
  </table>
  <div class="box tip"><b class="t">Consejo</b>Anunciad cada acción con claridad: quién la usa, qué dado, de quién era y su valor antes y después («Invierto el dado rojo de Bruno: de 5 a 2»). Poneos de acuerdo: una acción usada ya no está para nadie.</div>
</section>

<section>
  <h3>El dado gris</h3>
  <div class="two">
    <div>
      <p><b>Preparación.</b> Barajad las 7 cartas grises y dejadlas boca abajo.</p>
      <p><b>Primera ronda.</b> El primer repartidor tira además el dado gris y revela la carta gris de arriba, boca arriba para todos, incluido tú. El dado gris entra en los grupos como cualquier otro.</p>
      <p><b>Final de la partida.</b> Quien tenga el dado gris tiene que cumplir la carta gris. Si no, el equipo pierde, aunque tenga estrellas suficientes. El dado gris cuenta como dado, para las sumas y para los valores, pero no como color.</p>
    </div>
    <div class="cards" style="justify-content:flex-start"><figure>{gc.grey_card_svg(0)}G1: al menos 1 dado de cada color</figure><figure>{gc.grey_card_svg(6)}G7: no sumar más de 15</figure></div>
  </div>
  <table>
    <tr><th>Carta</th><th>Regla para quien tiene el dado gris</th></tr>
    <tr><td class="n">G1</td><td>Al menos 1 dado de cada color en juego</td></tr>
    <tr><td class="n">G2</td><td>Sumar al menos 15 (dado gris incluido)</td></tr>
    <tr><td class="n">G3</td><td>Ningún otro dado con el mismo valor que el dado gris</td></tr>
    <tr><td class="n">G4</td><td>Como máximo 6 dados (dado gris incluido)</td></tr>
    <tr><td class="n">G5</td><td>Al menos otro dado con el mismo valor que el dado gris</td></tr>
    <tr><td class="n">G6</td><td>No más de 3 dados de un mismo color</td></tr>
    <tr><td class="n">G7</td><td>No sumar más de 15 (dado gris incluido)</td></tr>
  </table>

  <h3>El dado negro: la Bomba</h3>
  <p><b>Preparación.</b> Barajad las 9 cartas negras y dejadlas boca abajo. Las cartas negras forman un único mazo de partida en partida: una carta no vuelve a salir hasta que han salido todas las demás. Cuando se acaba el mazo, se barajan las 9 de nuevo.</p>
  <p><b>Cada ronda.</b> Antes de sacar ningún dado, quien reparte revela la carta negra de arriba, para que todos sepan su efecto antes de que nadie coja el dado negro. Después saca los dados de colores que indique el nivel (6 con 3 jugadores y 8 con 4 en los niveles 16–20; 7 y 9 en el nivel 29), los tira junto con un dado negro y pone la carta al lado de ese dado negro. La carta va con el dado.</p>
  <p><b>Un dado negro por jugador.</b> Cada jugador puede terminar la partida con un <b>solo</b> dado negro. Si ya tienes uno, no puedes elegir un grupo que lleve otro.</p>
  <div class="box important"><b class="t">Cuidado con quien reparte</b>Si el último grupo lleva un dado negro y quien reparte ya tiene uno, <b>el equipo pierde el nivel en el acto</b>.</div>
</section>

<section>
  <p><b>Explotan las bombas.</b> Tras la última ronda y antes de puntuar, cada jugador con un dado negro, en orden de turno, aplica su carta a <b>sus propios dados</b> y los quita. Tú eliges qué dados, entre los que permite la carta. Si ningún dado cumple la carta, no pasa nada. La carta nunca quita el propio dado negro. Los dados quitados vuelven a la caja.</p>
  <div class="cards"><figure>{gc.black_card_svg(0)}N1: tu dado más bajo</figure><figure>{gc.black_card_svg(2)}N3: mismo valor que el dado negro</figure><figure>{gc.black_card_svg(7)}N8: menor o igual que el dado negro</figure></div>
  <table>
    <tr><th>Carta</th><th>Quita de tu zona</th></tr>
    <tr><td class="n">N1</td><td>Tu dado de valor más bajo (eliges entre los empatados)</td></tr>
    <tr><td class="n">N2</td><td>Tu dado de valor más alto (eliges entre los empatados)</td></tr>
    <tr><td class="n">N3</td><td>Un dado con el mismo valor que el dado negro</td></tr>
    <tr><td class="n">N4</td><td>Un dado del color del que más tengas</td></tr>
    <tr><td class="n">N5</td><td>Un dado del color del que menos tengas</td></tr>
    <tr><td class="n">N6</td><td>Los 2 dados tuyos que quieras</td></tr>
    <tr><td class="n">N7</td><td>Dos dados con el mismo valor</td></tr>
    <tr><td class="n">N8</td><td>Un dado de valor menor o igual que el dado negro</td></tr>
    <tr><td class="n">N9</td><td>Un dado de valor mayor o igual que el dado negro</td></tr>
  </table>
  <p>El dado negro cuenta como dado, para las sumas y para los valores, pero no como color. Mientras explotan las bombas no se pueden usar acciones.</p>
</section>

<section class="page">
  <h2>{bar('blue', 'orange', 'green', 'red', 'yellow')}Campaña</h2>
  <p>La campaña lleva a 3 o 4 jugadores por {len(CAMP)} niveles en seis mundos de cinco niveles. Cada nivel fija los colores, las cartas de objetivo de cada jugador, los dados de la bolsa y las estrellas que necesita el equipo. Superad un nivel para desbloquear el siguiente y marcadlo en la hoja de campaña. Si perdéis, repetid el nivel con cartas nuevas. Podéis volver a jugar cualquier nivel ya superado.</p>
  <p><b>Reparto de cartas en la campaña.</b> Separad las cartas de objetivo por estrellas. Cada jugador recibe una carta de cada valor de la columna <i>Cartas</i>: «3 + 1» es una carta de 3 estrellas y otra de 1. <b>Estrellas para ganar:</b> usad el valor de vuestro número de jugadores; se suman las estrellas de las cartas cumplidas, más las extra.</p>
  <table class="compact">
    <tr><th>Nivel</th><th>Nombre</th><th>Colores</th><th>Cartas</th><th>Dados por color<br>3 / 4 jugadores</th><th>Dados por ronda<br>3 / 4 jugadores</th><th>Estrellas<br>3 / 4 jugadores</th><th>Reglas</th></tr>
    {camp_rows()}
  </table>
  <p class="small">«+1»: más un dado negro por ronda. En los niveles 26–30 (niveles B) cada nivel añade un reto: <b>En silencio</b> (no se puede hablar ni dar pistas, sin acciones), <b>Misión en solitario</b> (cada jugador ve solo su propia carta, al revés que siempre; se puede hablar pero no decir lo que pone) y <b>Todo o nada</b> (hay que cumplir todas las cartas de todos; las estrellas no cuentan).</p>
  <div class="box tip"><b class="t">Reglas nuevas por el camino</b>Antes de los niveles 6, 11 y 16, leed en voz alta la parte de <i>Variantes</i> que corresponda: acciones especiales, dado gris y dado negro. Desde el nivel 6 hay acciones especiales en todos los niveles. Antes de los niveles 21, 26, 27 y 30, leed en voz alta el reto (cuatro colores, en silencio, misión en solitario y todo o nada). Cada mundo nuevo añade una idea y los niveles de un mismo mundo son cada vez más difíciles.</div>
</section>

<section>
  <h2>{bar('green', 'yellow')}Partida libre</h2>
  <p>Fuera de la campaña, preparad la partida a vuestro gusto:</p>
  <table>
    <tr><th>Ajuste</th><th>Opciones</th></tr>
    <tr><td>Jugadores</td><td>3 o 4</td></tr>
    <tr><td>Colores</td><td>3 o 4</td></tr>
    <tr><td>Objetivos por jugador</td><td>1, 2 o 3</td></tr>
    <tr><td>Dificultad</td><td>Cualquier combinación de cartas de 1★ a 5★</td></tr>
    <tr><td>Para ganar</td><td>Todos los objetivos, o un total de estrellas del equipo</td></tr>
    <tr><td>Dado gris</td><td>Sí o no</td></tr>
  </table>
  <div class="box tip"><b class="t">Vuestra primera partida</b>Recomendamos 3 colores, 1 objetivo por jugador y cartas de 1★ a 3★.</div>
</section>

<section class="faq">
  <h2>{bar('red', 'orange')}Preguntas frecuentes</h2>
  <div class="two">
    <div>
      <p><b>¿Puede haber un grupo vacío?</b> No. Todos los grupos tienen al menos un dado.</p>
      <p><b>¿Quien reparte ve los valores antes de formar los grupos?</b> Sí. Primero se tiran los dados y luego se reparten tal como han caído.</p>
      <p><b>Dos de mis cartas parecen contradecirse.</b> Las cartas de un mismo jugador tienen que ser compatibles. Si repartís a mano, cambiad una carta que contradiga claramente a otra.</p>
      <p><b>Dos jugadores tienen la misma carta de corona.</b> Solo un jugador puede ser el primero en lo mismo. Cambiad la segunda.</p>
    </div>
    <div>
      <p><b>¿El dado gris o el negro cuentan para «dados de exactamente 3 colores»?</b> No. Cuentan como dados y para los valores, nunca como color.</p>
      <p><b>¿Una acción puede usarse sobre el dado negro?</b> Sí, salvo eliminarlo. Si cambia su valor, la carta se aplica con el valor nuevo.</p>
      <p><b>La carta negra dice «tu dado más bajo» y tengo dos unos.</b> Elige cualquiera de los dos.</p>
      <p><b>¿Una acción puede eliminar el dado gris o el negro?</b> No. Eliminar solo sirve para dados de colores; las demás acciones sí pueden cambiar el dado gris y el negro.</p>
    </div>
  </div>
</section>

<section>
  <div class="ref">
    <h2 style="font-size:15pt">{bar('blue', 'orange', 'green')}Resumen</h2>
    <ol class="steps">
      <li>Quien reparte saca (jugadores × 2) − 1 dados y los tira.</li>
      <li>Quien reparte forma un grupo por jugador, con al menos un dado cada uno.</li>
      <li>Desde su izquierda, cada jugador coge un grupo; quien reparte se queda el último.</li>
      <li>Reparte el siguiente jugador a la izquierda. Se juegan tantas rondas como jugadores.</li>
      <li>Explotan las bombas (solo con dado negro); después se descubren las cartas y se puntúa.</li>
    </ol>
  </div>
  <p class="motto">Todos ven tu misión. Solo tú estás a oscuras.</p>
</section>
</body></html>
"""

out_html = HERE / 'reglas_es.html'
out_html.write_text(html)
print('html ->', out_html)
js = f"""
let chromium; try {{ ({{ chromium }} = require('playwright')); }} catch (e) {{ ({{ chromium }} = require('/opt/node-tools/node_modules/playwright')); }}
(async () => {{
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://{out_html}'); await p.waitForTimeout(300);
  await p.pdf({{ path: '{HERE / "BlindSpots_Reglas_ES.pdf"}', format: 'A4', printBackground: true, preferCSSPageSize: true }});
  await b.close(); console.log('pdf ok');
}})();
"""
subprocess.run(['node', '-e', js], check=True)
