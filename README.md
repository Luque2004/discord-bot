# Discord Bot — Pokémon Champions

Bot de Discord que muestra **builds competitivas de Pokémon Champions** (VGC) e información
detallada de cualquier Pokémon, en **español o en inglés**.

Las builds están sacadas del metajuego de la regulación vigente y se consultan desde el propio
repositorio, que además hace de API pública (ver [Las APIs](#las-apis)).

---

## Comandos

Todos son *slash commands*: se escriben con `/` y Discord va **autocompletando** el nombre del
Pokémon mientras escribes, así que no hay que acordarse de cómo se escriben las formas raras.

| Comando | Qué hace |
|---|---|
| `/builds <pokémon>` | Manda un embed por cada build: naturaleza, EVs, objeto, habilidad y movimientos. Sugiere los 246 Pokémon legales en Champions. |
| `/pokemon <pokémon>` | Tipos, habilidades y estadísticas base. Sugiere los 1351 Pokémon de PokeAPI, esté o no en Champions. |
| `/ayuda` | Manual de uso en español. |
| `/help` | Manual de uso en inglés. |

### Cambiar de idioma

Cada embed lleva dos reacciones: 🇪🇸 y 🇺🇸. Al pulsar una, el bot **reescribe el mismo mensaje**
con los nombres, objetos, movimientos y habilidades en ese idioma, y **quita tu reacción** para que
puedas volver a pulsarla. Se puede alternar las veces que haga falta.

Por defecto los embeds salen en español.

---

## Las APIs

Los datos vienen de dos sitios:

| Fuente | Para qué |
|---|---|
| **API propia** (los JSON de este repo, servidos por GitHub Pages) | Las builds de Champions: 246 Pokémon y 439 builds, en español y en inglés. |
| **[PokeAPI](https://pokeapi.co)** | Sprites, tipos, habilidades, estadísticas y los nombres traducidos. |

Los dos JSON de builds son públicos y se pueden consultar desde cualquier sitio:

```
https://luque2004.github.io/discord-bot/bot_0/builds__vgc_api.json      (inglés)
https://luque2004.github.io/discord-bot/bot_0/builds__vgc_api_es.json   (español)
```

Formato de cada entrada:

```json
"garchomp": [
  {
    "pokemon_name": "Garchomp",
    "builds": {
      "1": {
        "build_name": "Ofensiva Vidasfera",
        "item": "Vidasfera",
        "nature": "Alegre",
        "ability": "Piel Tosca",
        "moves": { "move1": "Garra Dragón", "move2": "Terremoto", "move3": "Avalancha / Pataleta", "move4": "Protección" },
        "evs": { "HP": "2", "AT": "32", "DEF": "0", "SPA": "0", "SPD": "0", "SPEED": "32" }
      }
    }
  }
]
```

> Champions usa **Stat Points** (0-32, 66 en total), no los EVs clásicos de 0-252.

Como los JSON se sirven desde este mismo repositorio, **un `git push` publica a la vez el código y
los datos**. GitHub Pages tarda 1-2 minutos en desplegar.

---

## Poner el bot en marcha

Requisitos: Python 3 y un bot creado en el [portal de desarrolladores de Discord](https://discord.com/developers/applications)
con los tres *intents* privilegiados activados (**Presence**, **Server Members** y **Message Content**):
el bot usa `discord.Intents.all()` y, si falta alguno, no arranca (`PrivilegedIntentsRequired`).

### Invitarlo a un servidor

Usa esta URL cambiando `TU_CLIENT_ID` por el *Application ID* del portal:

```
https://discord.com/oauth2/authorize?client_id=TU_CLIENT_ID&scope=bot&permissions=93248
```

`93248` es la suma de los permisos que necesita:

| Permiso | Valor | Para qué |
|---|---|---|
| Ver canales | 1024 | Ver el canal donde se usa |
| Enviar mensajes | 2048 | Responder |
| Gestionar mensajes | 8192 | Quitar tu bandera al cambiar de idioma |
| Insertar enlaces | 16384 | Mandar los embeds |
| Leer el historial | 65536 | Encontrar el mensaje al que reaccionas |
| Añadir reacciones | 64 | Poner las banderas |

Con el *scope* `bot` ya funcionan los comandos slash. Si le falta **Gestionar mensajes**, el
bot traduce igual pero tu bandera se queda puesta, y en la consola aparece
`No puedo quitar la reacción: al bot le falta el permiso 'Gestionar mensajes'`. Para añadir un
permiso a un bot ya invitado, vuelve a abrir la URL: Discord actualiza su rol sin echarlo.

### Arrancarlo

```bash
pip install discord.py requests python-dotenv
```

Crea un archivo `bot_0/.env` con el token (no se sube al repo, está en el `.gitignore`):

```
DISCORD_TOKEN=tu_token_aqui
```

Y arranca:

```bash
py bot_0/Main.py
```

En la consola debería aparecer `Bot encendido! 246 de Champions y 1351 de PokeAPI cargados!`.

> Los comandos slash pueden tardar unos minutos en aparecer en Discord la primera vez.

**¿Hay que reiniciarlo al actualizar las builds?**

- **Si cambian builds de Pokémon que ya estaban: no.** El bot guarda cada JSON de builds 1 hora
  en memoria; pasada la hora lo vuelve a descargar, así que como mucho en 1 hora (más los 1-2
  minutos de GitHub Pages) sirve las nuevas.
- **Si entran Pokémon nuevos al roster: sí.** La lista del autocompletado se carga una sola vez,
  al arrancar (`on_ready`), y sin reiniciar no los sugeriría.

---

## Cómo está organizado `Main.py`

| Parte | Qué hace |
|---|---|
| `on_ready` | Descarga las dos listas de Pokémon y registra los comandos en Discord. |
| `buscar_sugerencias` | Filtra una lista por lo que el usuario lleva escrito (primero los que empiezan por ese texto). La usan los dos autocompletados. |
| `cargar_builds(idioma)` | Descarga el JSON de builds de un idioma y lo guarda **1 hora** en `cache_builds` (las builds cambian con cada regulación). |
| `pedir_pokemon(nombre)` | Pide un Pokémon a PokeAPI y guarda en `cache_pokemon` solo lo que usa el bot, **sin caducidad** (esos datos no cambian). |
| `nombre_es(url)` | Traduce al español un tipo o una habilidad de PokeAPI y guarda la traducción en `traducciones_pokeapi`, también sin caducidad. |
| `crear_embed_build` / `crear_embed_pokemon` | Construyen los embeds. Se usan tanto al enviar como al traducir. |
| `enviar_builds` / `enviar_pokemon` | Mandan los embeds y les ponen las banderas. Reciben *cómo* enviar, así que sirven para cualquier comando. |
| `on_raw_reaction_add` | Al reaccionar con una bandera, reconstruye el embed en el otro idioma y quita la reacción del usuario. |

Las tres cachés viven en memoria: al reiniciar el bot se vacían y se vuelven a llenar con el uso.

---

## Mantenimiento

Las builds se actualizan con la skill **`builds-champions`** de
[Luque2004/claude-skills](https://github.com/Luque2004/claude-skills), que detecta la regulación
vigente, regenera los dos JSON y los alias de nombres de `Main.py`.

---

## Licencia

[GNU AGPL-3.0](LICENSE) © 2026 Max Luque

Puedes descargarlo, usarlo y modificarlo **gratis**. A cambio, si despliegas este bot (o una
versión modificada) y otras personas lo usan, tienes que **publicar tu código fuente** con esta
misma licencia. Se puede cobrar por alojarlo o mantenerlo, pero no convertirlo en algo cerrado.

Código fuente: <https://github.com/Luque2004/discord-bot>
