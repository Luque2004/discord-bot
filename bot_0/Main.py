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
   
   
    
@bot.command()
async def builds(ctx,nombre_pokemon):
    ################################################################ arreglar pokemons 
    if nombre_pokemon =="tornadus":nombre_pokemon ="tornadus-incarnate"
    if nombre_pokemon =="landorus":nombre_pokemon ="landorus-incarnate"
    if nombre_pokemon =="thundurus":nombre_pokemon ="thundurus-incarnate"
    if nombre_pokemon =="ogerpon-wellspring": nombre_pokemon ="ogerpon-wellspring-mask"
    if nombre_pokemon =="ogerpon-hearthflame": nombre_pokemon ="ogerpon-hearthflame-mask"
    if nombre_pokemon =="ogerpon-cornerstone": nombre_pokemon ="ogerpon-cornerstone-mask"
    if nombre_pokemon =="urshifu-single": nombre_pokemon ="urshifu-single-strike"
    if nombre_pokemon =="urshifu-rapid": nombre_pokemon ="urshifu-rapid-strike"
    if nombre_pokemon =="indeedee-f": nombre_pokemon ="indeedee-female"
    ################################################################
   
    #############################################api imagenes############       
    api_vgc = f"https://pokeapi.co/api/v2/pokemon/{nombre_pokemon}"
    

    response_pokemon = requests.get(api_vgc)
    data_img= response_pokemon.json()
    pokemon_image= data_img["sprites"]["front_default"]
  
    ############################################################ api
    api_builds = f"https://luque2004.github.io/pokemon_api/builds__vgc_api.json"
    response_builds = requests.get(api_builds)
    data = response_builds.json()
    ###########################################################
    pokemon_builds =data.get(nombre_pokemon, [])
 # bucle para hacer distintos embeds
    for build_number, build_info in pokemon_builds[0].get("builds", {}).items():
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
        tera = build_info["tera"]
        
        

        # texto para las estadísticas
        text_stat = f"**Nature:** {nature}\n**HP:** {HP}\n**AT:** {AT}\n**DEF:** {DEF}\n**SPA:** {SPA}\n**SPD:** {SPD}\n**SPEED:** {SPEED}\n"
        text_move = f"{move1}\n{move2}\n{move3}\n{move4}\n"
        text_ability_item = f"{ability}\n**Item**\n{item}\n**Tera**\n{tera}" ########## los combino para el espacio

        # crear embed 
        embed_builds = discord.Embed(title=build_name, description="")
        embed_builds.add_field(name="**Spread**", value=text_stat, inline=True)
        embed_builds.add_field(name="",value="",inline=True)
        embed_builds.add_field(name="**Abiliity**",value= text_ability_item,inline=True)        
        embed_builds.add_field(name="**Move set**", value= text_move,inline=False)
        
       
        embed_builds.set_thumbnail( url=pokemon_image)
        
        
        await ctx.send(embed=embed_builds)
        

    
    
   


    


    


    
    







bot.run(Token)# iniciar ##### trabajo pendiente: esconder el token para que nadie lo manipule

