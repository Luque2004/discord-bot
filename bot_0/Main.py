import discord
from discord.ext import commands  


###################### import para abrir api#######
import requests
##################################################
########################################## esconder token##################################
from dotenv import load_dotenv
import os
load_dotenv()
Token = os.getenv("DISCORD_TOKEN")




bot= commands.Bot(command_prefix=".", intents=discord.Intents.all()) 
@bot.event
async def on_ready():
    print("Bot encendido!")
    await bot.tree.sync()




########################################### info bot ###############################
@bot.tree.command(name="ayuda",description="uso ")
async def slash_command(interaction:discord.Interaction):
    texto_info_bot = f".builds:\n Comando para sacar las builds de determinado Pokémon\nAdvertencia: Si el nombre de Pokémon tiene espacios deberas de reemplazarlo por (-)\nEjemplo: gouging fire = gouging-fire y si es una forma especial: urshifu rapid = urshifu-rapid\n.pokemon\nComando para sacar información detallada de determinado pokemon\nEjemplo: .info charmander (se aplica la logica de .builds)" 
   
    embed_info = discord.Embed(title="Español", description="")
    embed_info.add_field(name="**Manual de uso**", value=texto_info_bot, inline=True)
    await interaction.response.send_message(embed=embed_info)
    
##########################################################################################################
########################################### info bot ####################################################
@bot.tree.command(name="help",description="usage")
async def slash_command(interaction:discord.Interaction):
    texto_info_bot_ingles=".builds\n Command retrieves determinated Pókemon builds\nWarning: if the Pokémon name contains spaces you should replace those spaces with (-)\nExample: gouging fire = gouging-fire this also applies to special forms: urshifu rapid =urshifu-rapid\n.pokemon \nComand retrieves detailled information of determinated pokemon\nExample: .info charmander (applies the .builds structure)"
    embed_info_english = discord.Embed(title="Usage Manual", description="")
    embed_info_english.add_field(name="**Info**", value=texto_info_bot_ingles, inline=True)
    await interaction.response.send_message(embed=embed_info_english)
#############################################################################################################







################################################################################################## VGC


@bot.command()
async def pokemon(ctx, nombre_pokemon):
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
    
    
    api_vgc = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}"
    response_pokemon = requests.get(api_vgc)
    data = response_pokemon.json()
    pokemon_image= data["sprites"]["front_default"]
    pokemon_image_shiny = data["sprites"]["front_shiny"]
  
    #########################################################extraer habiliidad
    abilities =""
    for i in range(len(data["abilities"])):
        abilities+=data["abilities"][i]["ability"]["name"]+"\n"
      
    #########################################################################
    ############################################################ extraer los tipos
    pokemon_types =""
    for i in range(len(data["types"])):
        pokemon_types+=data["types"][i]["type"]["name"]+"\n"
    
    #############################################################
    ############################################################# extraer las stats
    stat_hp = data["stats"][0]["base_stat"]
    stat_attack = data["stats"][1]["base_stat"]
    stat_defense = data["stats"][2]["base_stat"]
    stat_special_attack = data["stats"][3]["base_stat"]
    stat_special_defense = data["stats"][4]["base_stat"]
    stat_speed = data["stats"][5]["base_stat"]
    
    texto_stats =f"**HP:** {stat_hp}\n**AT:** {stat_attack}\n**DEF:** {stat_defense}\n**SPA:** {stat_special_attack}\n **SPD:** {stat_special_defense}\n**SPEED:** {stat_speed}\n"
    
    stats_total=(stat_hp+stat_attack+stat_defense+stat_special_defense+stat_special_attack+stat_speed)
        
    #############################################################
  
    embed_pokemon = discord.Embed(title =data["name"],description="")
    embed_pokemon.set_thumbnail(url=pokemon_image,)
    # embed_pokemon.set_thumbnail(url=pokemon_image_shiny)
    embed_pokemon.add_field(name="**Type**",value= pokemon_types, inline=True)
    embed_pokemon.add_field (name="",value="",inline=True)############# field vacio para agrandar el espacio 
    embed_pokemon.add_field(name="**Ability**",value= abilities,inline=True)
    embed_pokemon.add_field(name= "**Stats**",value=texto_stats,inline=False)
    embed_pokemon.set_footer(text=f"Total: {stats_total}")
    
   
    
    


    await ctx.send(embed=embed_pokemon)
    
    ########################## cargar mi api
   
   
    
################################################################################################## idioma de las builds
BANDERA_ES = "\U0001F1EA\U0001F1F8"   # 🇪🇸
BANDERA_EN = "\U0001F1FA\U0001F1F8"   # 🇺🇸

# id del mensaje -> {"pokemon": ..., "build_number": ..., "image": ...}
# (se guarda en memoria: si el bot se reinicia, los embeds antiguos dejan de reaccionar)
mensajes_builds = {}

APIS_BUILDS = {
    "es": "https://luque2004.github.io/discord-bot/bot_0/builds__vgc_api_es.json",
    "en": "https://luque2004.github.io/discord-bot/bot_0/builds__vgc_api.json",
}

def cargar_builds(idioma):
    ########## descarga el json de builds en el idioma pedido ("es" o "en")
    response_builds = requests.get(APIS_BUILDS[idioma])
    return response_builds.json()


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


@bot.event
async def on_raw_reaction_add(payload):
    ########## salta cada vez que alguien reacciona a cualquier mensaje
    if payload.user_id == bot.user.id:
        return  # ignoramos las reacciones que pone el propio bot
    if payload.message_id not in mensajes_builds:
        return  # no es un embed de builds, no hacemos nada

    emoji = str(payload.emoji)
    if emoji == BANDERA_ES:
        idioma = "es"
    elif emoji == BANDERA_EN:
        idioma = "en"
    else:
        return  # cualquier otra reacción se ignora

    info = mensajes_builds[payload.message_id]
    data = cargar_builds(idioma)
    build_info = data[info["pokemon"]][0]["builds"][info["build_number"]]

    canal = bot.get_channel(payload.channel_id)
    mensaje = await canal.fetch_message(payload.message_id)
    await mensaje.edit(embed=crear_embed_build(build_info, info["image"]))

    # quitamos la reacción del usuario para que pueda volver a cambiar de idioma
    # (necesita el permiso "Gestionar mensajes"; si no lo tiene, simplemente no la quita)
    try:
        usuario = await bot.fetch_user(payload.user_id)
        await mensaje.remove_reaction(payload.emoji, usuario)
    except discord.Forbidden:
        pass
##################################################################################################


@bot.command()
async def builds(ctx,nombre_pokemon):
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
   
    #############################################api imagenes############
    api_vgc = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}"


    response_pokemon = requests.get(api_vgc)
    data_img= response_pokemon.json()
    pokemon_image= data_img["sprites"]["front_default"]

    ############################################################ api
    data = cargar_builds("es")   # por defecto se muestran en español
    ###########################################################
    pokemon_builds =data.get(nombre_pokemon, [])
 # bucle para hacer distintos embeds
    for build_number, build_info in pokemon_builds[0].get("builds", {}).items():
        embed_builds = crear_embed_build(build_info, pokemon_image)
        mensaje = await ctx.send(embed=embed_builds)

        ########## reacciones para cambiar de idioma ##########
        await mensaje.add_reaction(BANDERA_ES)
        await mensaje.add_reaction(BANDERA_EN)
        # guardamos qué build es este mensaje para poder reconstruirlo en otro idioma
        mensajes_builds[mensaje.id] = {"pokemon": nombre_pokemon, "build_number": build_number, "image": pokemon_image}
        

    
    
   


    


    


    
    







bot.run(Token)# iniciar ##### trabajo pendiente: esconder el token para que nadie lo manipule

