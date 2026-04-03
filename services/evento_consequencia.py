
#arquivo para criar as logicas de atualização dos eventos em tempo real

from fastapi import HTTPException




def atualizar_placar(session, jogo, evento, tipo_evento):
    #logica para atualizar o placar do jogo com base no tipo de evento
    autor = next((p for p in evento.participantes if p.papel == 1), None)
    if not autor: 
        raise HTTPException(status_code=400, detail="Autor do gol não encontrado entre os participantes")
    
    is_gol_contra = tipo_evento.acao_slug == "gol_contra"

    if not is_gol_contra: 
        if autor.id_time == jogo.id_time_casa:
            jogo.gols_time_casa += 1
        elif autor.id_time == jogo.id_time_visitante:
            jogo.gols_time_visitante += 1
        
    else: 
        if autor.id_time == jogo.id_time_casa:
            jogo.gols_time_visitante += 1
        elif autor.id_time == jogo.id_time_visitante:
            jogo.gols_time_casa += 1
     

def adicionar_cartao(session, jogo, evento, tipo_evento):
    #logica para adicionar o cartao ao jogador e possivelmente expulsar o jogador
    pass
    

    
        

def adicionar_substituicao(session, jogo, evento, tipo_evento):
    #logica para registrar a substituição de jogadores no evento
    pass

def registrar_periodo(session, jogo, evento, tipo_evento):
    #logica para registrar o periodo do jogo (1T, 2T, etc)
    pass


MAPA_EVENTOS = {
    "gol": atualizar_placar,
    "gol_contra": atualizar_placar, # Reutiliza a lógica que você já fez       
    "substituicao": adicionar_substituicao,    
    "intervalo": registrar_periodo, # Apenas para marcar 1T/2T
}