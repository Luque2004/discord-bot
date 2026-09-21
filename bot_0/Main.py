import discord
from discord.ext import commands  
from discord import app_commands


###################### import para abrir api#######
import requests
##################################################
########################################## esconder token##################################
from dotenv import load_dotenv
import os
load_dotenv()
Token = os.getenv("DISCORD_TOKEN")




bot= commands.Bot(command_prefix=".", intents=discord.Intents.all()) 
lista_pokemon = {}         # Pokémon de Champions:  "garchomp" -> "Garchomp", "ninetales-alola" -> "Ninetales de Alola"
lista_todos_pokemon = {}   # todos los de PokeAPI: "bulbasaur" -> "Bulbasaur", "ninetales-alola" -> "Ninetales Alola"
@bot.event
async def on_ready():
    global lista_pokemon, lista_todos_pokemon
    data = cargar_builds("es")
    lista_pokemon = {clave: info[0]["pokemon_name"] for clave, info in data.items()}
    todos = requests.get("https://pokeapi.co/api/v2/pokemon?limit=100000").json()
    lista_todos_pokemon = {p["name"]: p["name"].replace("-", " ").title() for p in todos["results"]}
    print(f"Bot encendido! {len(lista_pokemon)} de Champions y {len(lista_todos_pokemon)} de PokeAPI cargados!")
    await bot.tree.sync()


 

########################################### info bot ###############################
@bot.tree.command(name="ayuda",description="uso ")
async def slash_command(interaction:discord.Interaction):
    texto_info_bot = "/builds\nSaca las builds de un Pokémon. Empieza a escribir el nombre y elige de la lista que aparece.\nReacciona con 🇺🇸 o 🇪🇸 en una build para verla en inglés o en español.\n\n/pokemon\nInformación detallada de un Pokémon (tipos, habilidades, stats). Elige de la lista o escribe cualquier Pokémon, aunque no esté en Champions.\nSi escribes una forma a mano usa guiones: urshifu-rapid, ogerpon-wellspring"
   
    embed_info = discord.Embed(title="Español", description="")
    embed_info.add_field(name="**Manual de uso**", value=texto_info_bot, inline=True)
    await interaction.response.send_message(embed=embed_info)
    
##########################################################################################################
########################################### info bot ####################################################
@bot.tree.command(name="help",description="usage")
async def slash_command(interaction:discord.Interaction):
    texto_info_bot_ingles = "/builds\nShows the builds of a Pokémon. Start typing the name and pick one from the list.\nReact with 🇺🇸 or 🇪🇸 on a build to see it in English or Spanish.\n\n/pokemon\nDetailed info of a Pokémon (types, abilities, stats). Pick one from the list or type any Pokémon, even if it is not in Champions.\nIf you type a form by hand use hyphens: urshifu-rapid, ogerpon-wellspring"
    embed_info_english = discord.Embed(title="Usage Manual", description="")
    embed_info_english.add_field(name="**Info**", value=texto_info_bot_ingles, inline=True)
    await interaction.response.send_message(embed=embed_info_english)
#############################################################################################################







################################################################################################## VGC




################################################################################################## idioma de las builds
BANDERA_ES = "\U0001F1EA\U0001F1F8"   # 🇪🇸
BANDERA_EN = "\U0001F1FA\U0001F1F8"   # 🇺🇸

# id del mensaje -> {"pokemon": ..., "build_number": ..., "image": ...}
# (se guarda en memoria: si el bot se reinicia, los embeds antiguos dejan de reaccionar)
mensajes_builds = {}
# id del mensaje -> {"pokemon": clave de PokeAPI}   (embeds de /pokemon)
mensajes_pokemon = {}
################# Api de las builds en diferente idioma
APIS_BUILDS = {
    "es": "https://luque2004.github.io/discord-bot/bot_0/builds__vgc_api_es.json",
    "en": "https://luque2004.github.io/discord-bot/bot_0/builds__vgc_api.json",
}
######################### cargar builds
def cargar_builds(idioma):
    ########## descarga el json de builds en el idioma pedido ("es" o "en")
    response_builds = requests.get(APIS_BUILDS[idioma])
    return response_builds.json()
#################################################################### Autocompletar para facilitar busqueda
def buscar_sugerencias(diccionario, current):
    ########## filtra un diccionario clave -> nombre por lo escrito.
    ########## primero los que EMPIEZAN por el texto, después los que lo CONTIENEN
    texto = current.lower()
    empiezan = [(clave, nombre) for clave, nombre in diccionario.items()
                if clave.startswith(texto) or nombre.lower().startswith(texto)]
    contienen = [(clave, nombre) for clave, nombre in diccionario.items()
                 if (texto in clave or texto in nombre.lower()) and (clave, nombre) not in empiezan]
    return [app_commands.Choice(name=nombre, value=clave) for clave, nombre in (empiezan + contienen)[:25]]

async def autocompletar(interaction:discord.Interaction,current:str):
    ########## solo los Pokémon de Champions (para /builds)
    return buscar_sugerencias(lista_pokemon, current)

async def autocompletar_todos(interaction:discord.Interaction,current:str):
    ########## todos los Pokémon de PokeAPI (para /pokemon)
    return buscar_sugerencias(lista_todos_pokemon, current)

############## Slash command para builds
@bot.tree.command(name="builds", description="Builds de un pokemon en Champions")
@app_commands.describe(pokemon="Empieza a escribir y elige de la lista")
@app_commands.autocomplete(pokemon = autocompletar)
async def builds_slash(interaction: discord.Interaction, pokemon : str):
    await interaction.response.defer()
    await enviar_builds(pokemon, interaction.followup.send)

############## Slash command para info de un pokemon
@bot.tree.command(name="pokemon", description="Información de un Pokémon (tipos, habilidades, stats)")
@app_commands.describe(pokemon="Empieza a escribir y elige de la lista (o escribe cualquier Pokémon)")
@app_commands.autocomplete(pokemon = autocompletar_todos)
async def pokemon_slash(interaction: discord.Interaction, pokemon: str):
    await interaction.response.defer()
    nombre_pokemon = pokemon
    ########################################## arreglar nombres de pokemon
    if nombre_pokemon =="mimikyu": nombre_pokemon ="778"
    if nombre_pokemon =="tornadus":nombre_pokemon ="tornadus-incarnate"
    if nombre_pokemon =="landorus":nombre_pokemon ="landorus-incarnate"
    if nombre_pokemon =="thundurus":nombre_pokemon ="thundurus-incarnate"
    if nombre_pokemon =="ogerpon-wellspring": nombre_pokemon ="ogerpon-wellspring-mask"
    if nombre_pokemon =="ogerpon-hearthflame": nombre_pokemon ="ogerpon-hearthflame-mask"
    if nombre_pokemon =="ogerpon-cornerstone": nombre_pokemon ="ogerpon-cornerstone-mask"
    if nombre_pokemon =="urshifu-single": nombre_pokemon ="urshifu-single-strike"
    if nombre_pokemon =="urshifu-rapid": nombre_pokemon ="urshifu-rapid-strike"
    if nombre_pokemon =="indeedee-f": nombre_pokemon ="indeedee-female"
    # --- alias builds-champions (generado; no editar a mano) ---
    nombre_pokemon = nombre_pokemon.lower()
    if nombre_pokemon =="aegislash": nombre_pokemon ="aegislash-shield"
    if nombre_pokemon =="aegislash-escudo": nombre_pokemon ="aegislash-shield"
    if nombre_pokemon =="alolan-ninetales": nombre_pokemon ="ninetales-alola"
    if nombre_pokemon =="alolan-persian": nombre_pokemon ="persian-alola"
    if nombre_pokemon =="alolan-raichu": nombre_pokemon ="raichu-alola"
    if nombre_pokemon =="basculegion": nombre_pokemon ="basculegion-male"
    if nombre_pokemon =="basculegion-macho": nombre_pokemon ="basculegion-male"
    if nombre_pokemon =="farfetch'd": nombre_pokemon ="farfetchd"
    if nombre_pokemon =="floette": nombre_pokemon ="floette-eternal"
    if nombre_pokemon =="floette-eterna": nombre_pokemon ="floette-eternal"
    if nombre_pokemon =="floette-flor-eterna": nombre_pokemon ="floette-eternal"
    if nombre_pokemon =="galarian-slowbro": nombre_pokemon ="slowbro-galar"
    if nombre_pokemon =="galarian-slowking": nombre_pokemon ="slowking-galar"
    if nombre_pokemon =="galarian-stunfisk": nombre_pokemon ="stunfisk-galar"
    if nombre_pokemon =="gourgeist": nombre_pokemon ="gourgeist-average"
    if nombre_pokemon =="gourgeist-mediano": nombre_pokemon ="gourgeist-average"
    if nombre_pokemon =="hisuian-arcanine": nombre_pokemon ="arcanine-hisui"
    if nombre_pokemon =="hisuian-avalugg": nombre_pokemon ="avalugg-hisui"
    if nombre_pokemon =="hisuian-decidueye": nombre_pokemon ="decidueye-hisui"
    if nombre_pokemon =="hisuian-goodra": nombre_pokemon ="goodra-hisui"
    if nombre_pokemon =="hisuian-qwilfish": nombre_pokemon ="qwilfish-hisui"
    if nombre_pokemon =="hisuian-samurott": nombre_pokemon ="samurott-hisui"
    if nombre_pokemon =="hisuian-typhlosion": nombre_pokemon ="typhlosion-hisui"
    if nombre_pokemon =="hisuian-zoroark": nombre_pokemon ="zoroark-hisui"
    if nombre_pokemon =="indeedee": nombre_pokemon ="indeedee-male"
    if nombre_pokemon =="indeedee-f": nombre_pokemon ="indeedee-female"
    if nombre_pokemon =="indeedee-hembra": nombre_pokemon ="indeedee-female"
    if nombre_pokemon =="indeedee-m": nombre_pokemon ="indeedee-male"
    if nombre_pokemon =="indeedee-macho": nombre_pokemon ="indeedee-male"
    if nombre_pokemon =="kommoo": nombre_pokemon ="kommo-o"
    if nombre_pokemon =="lycanroc": nombre_pokemon ="lycanroc-midday"
    if nombre_pokemon =="lycanroc-dia": nombre_pokemon ="lycanroc-midday"
    if nombre_pokemon =="lycanroc-diurno": nombre_pokemon ="lycanroc-midday"
    if nombre_pokemon =="maushold": nombre_pokemon ="maushold-family-of-four"
    if nombre_pokemon =="maushold-familia-cuatro": nombre_pokemon ="maushold-family-of-four"
    if nombre_pokemon =="maushold-familia-de-cuatro": nombre_pokemon ="maushold-family-of-four"
    if nombre_pokemon =="meowstic": nombre_pokemon ="meowstic-male"
    if nombre_pokemon =="meowstic-macho": nombre_pokemon ="meowstic-male"
    if nombre_pokemon =="mimikyu": nombre_pokemon ="mimikyu-disguised"
    if nombre_pokemon =="mimikyu-disfrazado": nombre_pokemon ="mimikyu-disguised"
    if nombre_pokemon =="morpeko": nombre_pokemon ="morpeko-full-belly"
    if nombre_pokemon =="morpeko-saciada": nombre_pokemon ="morpeko-full-belly"
    if nombre_pokemon =="morpeko-saciado": nombre_pokemon ="morpeko-full-belly"
    if nombre_pokemon =="mr.mime": nombre_pokemon ="mr-mime"
    if nombre_pokemon =="mr.rime": nombre_pokemon ="mr-rime"
    if nombre_pokemon =="mrmime": nombre_pokemon ="mr-mime"
    if nombre_pokemon =="mrrime": nombre_pokemon ="mr-rime"
    if nombre_pokemon =="palafin": nombre_pokemon ="palafin-zero"
    if nombre_pokemon =="palafin-forma-normal": nombre_pokemon ="palafin-zero"
    if nombre_pokemon =="palafin-normal": nombre_pokemon ="palafin-zero"
    if nombre_pokemon =="pyroar": nombre_pokemon ="pyroar-male"
    if nombre_pokemon =="pyroar-macho": nombre_pokemon ="pyroar-male"
    if nombre_pokemon =="sirfetch'd": nombre_pokemon ="sirfetchd"
    if nombre_pokemon =="squawkabilly": nombre_pokemon ="squawkabilly-green-plumage"
    if nombre_pokemon =="squawkabilly-plumaje-verde": nombre_pokemon ="squawkabilly-green-plumage"
    if nombre_pokemon =="squawkabilly-verde": nombre_pokemon ="squawkabilly-green-plumage"
    if nombre_pokemon =="toxtricity": nombre_pokemon ="toxtricity-amped"
    if nombre_pokemon =="toxtricity-aguda": nombre_pokemon ="toxtricity-amped"
    if nombre_pokemon =="toxtricity-forma-aguda": nombre_pokemon ="toxtricity-amped"
    if nombre_pokemon =="toxtricity-forma-grave": nombre_pokemon ="toxtricity-low-key"
    if nombre_pokemon =="toxtricity-grave": nombre_pokemon ="toxtricity-low-key"
    # --- fin alias builds-champions ---
    ####################################################################
    await enviar_pokemon(nombre_pokemon, interaction.followup.send)


def crear_embed_build(build_info, pokemon_image):
    ########## construye el embed de una build a partir de su diccionario del json
    build_name = build_info["build_name"]
    nature = build_info["nature"]
    HP = build_info["evs"]["HP"]
    AT = build_info["evs"]["AT"]
    DEF = build_info["evs"]["DEF"]
    SPA = build_info["evs"]["SPA"]
    SPD = build_info["evs"]["SPD"]
    SPEED = build_info["evs"]["SPEED"]
    move1 = build_info["moves"]["move1"]
    move2 = build_info["moves"]["move2"]
    move3 = build_info["moves"]["move3"]
    move4 = build_info["moves"]["move4"]
    ability = build_info["ability"]
    item = build_info["item"]

    # texto para las estadísticas
    text_stat = f"**Nature:** {nature}\n**HP:** {HP}\n**AT:** {AT}\n**DEF:** {DEF}\n**SPA:** {SPA}\n**SPD:** {SPD}\n**SPEED:** {SPEED}\n"
    text_move = f"{move1}\n{move2}\n{move3}\n{move4}\n"
    text_ability_item = f"{ability}\n**Item**\n{item}" ########## los combino para el espacio

    # crear embed
    embed_builds = discord.Embed(title=build_name, description="")
    embed_builds.add_field(name="**Spread**", value=text_stat, inline=True)
    embed_builds.add_field(name="",value="",inline=True)
    embed_builds.add_field(name="**Abiliity**",value= text_ability_item,inline=True)
    embed_builds.add_field(name="**Move set**", value= text_move,inline=False)
    embed_builds.set_thumbnail( url=pokemon_image)
    return embed_builds


async def enviar_builds(nombre_pokemon, enviar):
    ########## manda un embed por build. "enviar" es la función con la que se manda
    ########## (ctx.send desde .builds, interaction.followup.send desde /builds)
    #############################################api imagenes############
    api_vgc = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}"
    response_pokemon = requests.get(api_vgc)
    data_img = response_pokemon.json()
    pokemon_image = data_img["sprites"]["front_default"]

    ############################################################ api
    data = cargar_builds("es")   # por defecto se muestran en español
    pokemon_builds = data.get(nombre_pokemon, [])
    if not pokemon_builds:
        await enviar(f"No tengo builds de **{nombre_pokemon}**")
        return

    # bucle para hacer distintos embeds
    for build_number, build_info in pokemon_builds[0].get("builds", {}).items():
        embed_builds = crear_embed_build(build_info, pokemon_image)
        mensaje = await enviar(embed=embed_builds)

        ########## reacciones para cambiar de idioma ##########
        await mensaje.add_reaction(BANDERA_ES)
        await mensaje.add_reaction(BANDERA_EN)
        # guardamos qué build es este mensaje para poder reconstruirlo en otro idioma
        mensajes_builds[mensaje.id] = {"pokemon": nombre_pokemon, "build_number": build_number, "image": pokemon_image}


traducciones_pokeapi = {}   # caché: url de PokeAPI -> nombre en español (para no repetir peticiones)

def nombre_es(url):
    ########## nombre en español de un recurso de PokeAPI (tipo, habilidad, especie...)
    if url not in traducciones_pokeapi:
        datos = requests.get(url).json()
        traducciones_pokeapi[url] = next((n["name"] for n in datos["names"] if n["language"]["name"] == "es"), datos["name"])
    return traducciones_pokeapi[url]


def crear_embed_pokemon(data, idioma):
    ########## construye el embed de información de un pokemon (data = respuesta de PokeAPI) en "es" o "en"
    if idioma == "es":
        titulo = lista_pokemon.get(data["name"]) or nombre_es(data["species"]["url"])
        pokemon_types = "\n".join(nombre_es(t["type"]["url"]) for t in data["types"])
        abilities = "\n".join(nombre_es(a["ability"]["url"]) for a in data["abilities"])
        etiqueta_tipo, etiqueta_habilidad, etiqueta_stats = "Tipo", "Habilidad", "Estadísticas"
    else:
        titulo = lista_todos_pokemon.get(data["name"], data["name"])
        pokemon_types = "\n".join(t["type"]["name"] for t in data["types"])
        abilities = "\n".join(a["ability"]["name"] for a in data["abilities"])
        etiqueta_tipo, etiqueta_habilidad, etiqueta_stats = "Type", "Ability", "Stats"

    ############################################################# extraer las stats
    stat_hp = data["stats"][0]["base_stat"]
    stat_attack = data["stats"][1]["base_stat"]
    stat_defense = data["stats"][2]["base_stat"]
    stat_special_attack = data["stats"][3]["base_stat"]
    stat_special_defense = data["stats"][4]["base_stat"]
    stat_speed = data["stats"][5]["base_stat"]
    texto_stats = f"**HP:** {stat_hp}\n**AT:** {stat_attack}\n**DEF:** {stat_defense}\n**SPA:** {stat_special_attack}\n**SPD:** {stat_special_defense}\n**SPEED:** {stat_speed}\n"
    stats_total = stat_hp + stat_attack + stat_defense + stat_special_defense + stat_special_attack + stat_speed

    embed_pokemon = discord.Embed(title=titulo, description="")
    embed_pokemon.set_thumbnail(url=data["sprites"]["front_default"])
    embed_pokemon.add_field(name=f"**{etiqueta_tipo}**", value=pokemon_types, inline=True)
    embed_pokemon.add_field(name="", value="", inline=True)   ############# field vacio para agrandar el espacio
    embed_pokemon.add_field(name=f"**{etiqueta_habilidad}**", value=abilities, inline=True)
    embed_pokemon.add_field(name=f"**{etiqueta_stats}**", value=texto_stats, inline=False)
    embed_pokemon.set_footer(text=f"Total: {stats_total}")
    return embed_pokemon


async def enviar_pokemon(nombre_pokemon, enviar):
    ########## manda el embed de información de un pokemon (datos de PokeAPI).
    ########## "enviar" es la función con la que se manda (interaction.followup.send)
    api_vgc = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}"
    response_pokemon = requests.get(api_vgc)
    if response_pokemon.status_code != 200:
        await enviar(f"No encuentro ningún Pokémon llamado **{nombre_pokemon}**")
        return
    data = response_pokemon.json()
    mensaje = await enviar(embed=crear_embed_pokemon(data, "es"))   # por defecto en español

    ########## reacciones para cambiar de idioma ##########
    await mensaje.add_reaction(BANDERA_ES)
    await mensaje.add_reaction(BANDERA_EN)
    mensajes_pokemon[mensaje.id] = {"pokemon": data["name"]}


@bot.event
async def on_raw_reaction_add(payload):
    ########## salta cada vez que alguien reacciona a cualquier mensaje
    if payload.user_id == bot.user.id:
        return  # ignoramos las reacciones que pone el propio bot
    if payload.message_id not in mensajes_builds and payload.message_id not in mensajes_pokemon:
        return  # no es un embed nuestro, no hacemos nada

    emoji = str(payload.emoji)
    if emoji == BANDERA_ES:
        idioma = "es"
    elif emoji == BANDERA_EN:
        idioma = "en"
    else:
        return  # cualquier otra reacción se ignora

    if payload.message_id in mensajes_builds:
        ########## embed de /builds: misma build, JSON del otro idioma
        info = mensajes_builds[payload.message_id]
        data = cargar_builds(idioma)
        build_info = data[info["pokemon"]][0]["builds"][info["build_number"]]
        embed_nuevo = crear_embed_build(build_info, info["image"])
    else:
        ########## embed de /pokemon: mismos datos de PokeAPI, nombres en el otro idioma
        info = mensajes_pokemon[payload.message_id]
        data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{info['pokemon']}").json()
        embed_nuevo = crear_embed_pokemon(data, idioma)

    canal = bot.get_channel(payload.channel_id)
    mensaje = await canal.fetch_message(payload.message_id)
    await mensaje.edit(embed=embed_nuevo)

    # quitamos la reacción del usuario para que pueda volver a cambiar de idioma
    # (necesita el permiso "Gestionar mensajes"; si no lo tiene, simplemente no la quita)
    try:
        usuario = await bot.fetch_user(payload.user_id)
        await mensaje.remove_reaction(payload.emoji, usuario)
    except discord.Forbidden:
        pass
##################################################################################################


bot.run(Token)# iniciar ##### trabajo pendiente: esconder el token para que nadie lo manipule

