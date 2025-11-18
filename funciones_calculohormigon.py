#modulo para calculos del diseño de mezclas de hormigon
import numpy as np
import pandas as pd

def calculo_consumo_agua_aire(asentamiento, tmax):
    '''
    Funcion que calcula el consumo aproximado de agua y cantidad de aire aprisionado
    basado en los valores dados por el metodo ACI 211.1
    Parametros: asentamiento(cm) ; tmax:tamaño maximo del agregado grueso(mm)
    Retorna: consumo_agua(kg/m^3) ; aire_aprisionado(% de aire)
    '''
    tabla_agua = {
        '2.5-5.0': {
            9.5: [207, 3.0],
            12.5: [199, 2.5],
            19: [190, 2.0],
            25: [179, 1.5],
            36: [166, 1.0],
            50: [154, 0.5],
            75: [130, 0.3],
            150: [113, 0.2]
        },
        '7.5-10.0': {
            9.5: [228, 3.0],
            12.5: [216, 2.5],
            19: [205, 2.0],
            25: [193, 1.5],
            36: [181, 1.0],
            50: [169, 0.5],
            75: [145, 0.3],
            150: [124, 0.2]
        },
        '15.0-17.5': {
            9.5: [243, 3.0],
            12.5: [228, 2.5],
            19: [216, 2.0],
            25: [202, 1.5],
            36: [190, 1.0],
            50: [178, 0.5],
            75: [160, 0.3],
            150: [None, 0.2] 
        }
    }
    #Para determinar el rango de asentamiento:
    if asentamiento<=5.0:
        rango_asentamiento='2.5-5.0'
    elif asentamiento<=10:
        rango_asentamiento='7.5-10.0'
    else:
        rango_asentamiento='15.0-17.5'
    #se aproxima al tmax mas cercano
    tmax_disp=[9.5, 12.5, 19, 25, 36, 50, 75, 150]
    tmax_cercano=min(tmax_disp, key=lambda x: abs(x-tmax))

    #obtencion de los valores de la tabla
    try:
        consumo_agua=tabla_agua[rango_asentamiento][tmax_cercano][0]
        aire_aprisionado=tabla_agua[rango_asentamiento][tmax_cercano][1]
        return consumo_agua, aire_aprisionado
    except KeyError:
        return None, None
    
def procesar_asentamiento_str(asentamiento_str):
    '''
    Si el asentamiento esta dado en un intervalo, lo convierte a un valor numerico para 
    mayor trabajabilidad
    '''
    if pd.isna(asentamiento_str):
        return None
    asentamiento_str=str(asentamiento_str).lower().replace('cm','').strip()

    if '-' in asentamiento_str:
        #se tomara el prmedio del rango
        partes=asentamiento_str.split('-')
        try:
            valores=[float(p.strip()) for p in partes if p.strip()]
            return sum(valores)/len(valores)#promedio
        except:
            return None
    else:#caso de valor unico
        try:
            return float(asentamiento_str)
        except:
            return None
        
def calculo_fcm(fck):
    fcm=int(fck)+80
    return fcm

def calculo_relacion_ac(fcm, con_aire=False):
    '''
    Paso 5 ACI - Relacion Agua/Cemento 
    Parametros: fcm(kg/cm^2) ; con_aire(booleano)
    Retorna: Relacion a/c
    '''
    if not con_aire:
        tabla={
            420: 0.41,
            350: 0.48,
            280: 0.57,
            210: 0.68,
            140: 0.82
        }
    else:
        tabla={
            350:0.40,
            280:0.48,
            210: 0.59,
            140: 0.74
        }
    
    resistencias=sorted(tabla.keys(), reverse=True)

    if fcm in tabla:#no hace falta interpolar
        return tabla[fcm]
    #fuera de rango
    if fcm>max(resistencias):
        return tabla[max(resistencias)]
    elif fcm<min(resistencias):
        return tabla[min(resistencias)]
    #interpolacion lineal
    for i in range(len(resistencias)-1):
        fcm_superior=resistencias[i]
        fcm_inferior=resistencias[i+1]

        if fcm_inferior<=fcm<=fcm_superior:
            ac_superior=tabla[fcm_superior]
            ac_inferior=tabla[fcm_inferior]

            diferencia_fcm= fcm_superior-fcm_inferior
            diferencia_ac=ac_superior-ac_inferior
            diferencia_fcm_objetivo=fcm-fcm_inferior

            x=(diferencia_fcm_objetivo*diferencia_ac)/diferencia_fcm

            relacion_ac=ac_inferior+x
            return round(relacion_ac, 3)
    return None

def calculo_cemento(agua, relacion_ac):
    cemento=agua/relacion_ac
    return cemento

def calculo_agregado_grueso(tmax, modulo_finura, pesos_unitarios, porcentajes):
    '''
    Calculo del consumo de agregado grueso
    Parametros: tmax(mm) ; modulo_finura ; pesos_unitarios(kg/m^3) ; porcentajes(%)
    Retorna: dict con pesos de cada fraccion y total
    '''
    tabla_volumen = {
        9.6: {2.40: 0.50, 2.60: 0.48, 2.80: 0.46, 3.00: 0.44},
        12.7: {2.40: 0.59, 2.60: 0.57, 2.80: 0.55, 3.00: 0.53},
        19.1: {2.40: 0.66, 2.60: 0.64, 2.80: 0.62, 3.00: 0.60},
        25.4: {2.40: 0.71, 2.60: 0.69, 2.80: 0.67, 3.00: 0.65},
        38.1: {2.40: 0.75, 2.60: 0.73, 2.80: 0.71, 3.00: 0.69}
    }
    #aproximar tmax
    tmax_disponibles=[9.6, 12.7, 19.1, 25.4, 38.1]
    tmax_cercano=min(tmax_disponibles, key=lambda x: abs(x-tmax))

    #modulos de finura
    modulos_disp=[2.40, 2.60, 2.80, 3.00]

    #interpolacion volumen
    if modulo_finura in modulos_disp:
        v_ag=tabla_volumen[tmax_cercano][modulo_finura]
    else:
        mf_inferior=max([mf for mf in modulos_disp if mf<=modulo_finura])
        mf_superior=min([mf for mf in modulos_disp if mf>=modulo_finura])

        if mf_inferior is None:
            mf_inferior=min(modulos_disp)
        if mf_superior is None:
            mf_superior=max(modulos_disp)

        v_inferior=tabla_volumen[tmax_cercano][mf_inferior]
        v_superior=tabla_volumen[tmax_cercano][mf_superior]

        if mf_superior!=mf_inferior:
            v_ag= v_inferior + (v_superior-v_inferior)*(modulo_finura-mf_inferior)/(mf_superior-mf_inferior)
        else:
            v_ag=v_inferior
        
        resultados={'volumen_total': v_ag}
        #v_fraccion=v_ag*(%fraccion/100)
        #p_fraccion=v_fraccion*PUV_fraccion
        for fraccion, porcentaje in porcentajes.items():
            if fraccion in pesos_unitarios:
                v_fraccion=v_ag*(porcentaje/100)
                p_fraccion=v_fraccion*pesos_unitarios[fraccion]

                resultados[f'volumen_{fraccion}']=round(v_fraccion, 2)
                resultados[f'peso_{fraccion}']=round(p_fraccion, 2)

        #peso totoal del AG
        peso_total_ag=sum([resultados[f'peso_{fraccion}'] for fraccion in porcentajes.keys() if f'peso_{fraccion}' in resultados])
        resultados['peso_total_ag']=round(peso_total_ag, 2)

        return resultados
    
def calculo_agregado_fino(agua, cemento, agregado_grueso, aire, densidades, porcentajes_af):
    '''
    Calculo de el consumo de agregado fino
    Parametros: agua; cemento; agregado_grueso; aire; densidades; porcentajes_af
    Retorna: dict con volumenes y pesos de cada fraccion del AF
    '''
    resultados={}

    resultados['V_agua']=agua#en litros
    resultados['V_cemento']= cemento/densidades['cemento']
    resultados['V_aire']=aire
    
    vol_ag=0
    for key, value in agregado_grueso.items():
        if key.startswith('peso_') and not key.startswith('peso_total'):
            fraccion=key.replace('peso_','')
            #volumen de cada fraccion=peso/densidad
            v_fraccion=value/densidades.get(fraccion, densidades.get('agregado_grueso'))
            resultados[f'V_{fraccion}']=v_fraccion
            vol_ag+=v_fraccion
    
    resultados['V_agregado_grueso']=vol_ag

    volumen_total_ocupado=(
        resultados['V_agua']+
        resultados['V_cemento']+
        resultados['V_agregado_grueso']+
        resultados['V_aire']
    )
    resultados['V_agregado_fino']=1000-volumen_total_ocupado

    #distribucion del volumen de AF en sus fracciones(6ta y arena lavada)
    for fraccion, porcentaje in porcentajes_af.items():
        v_fraccion=resultados['V_agregado_fino']*(porcentaje/100)
        resultados[f'V_{fraccion}']=v_fraccion
        
        p_fraccion=v_fraccion*densidades[fraccion]
        resultados[f'P_{fraccion}']=p_fraccion
        
        #peso total del AF
        peso_total_af=sum([resultados[f'P_{fraccion}'] for fraccion in porcentajes_af.keys()])
        resultados['P_agregado_fino']=peso_total_af

        #redondeo
        for key in resultados:
            if isinstance(resultados[key], float):
                resultados[key]=round(resultados[key], 2)
        
        return resultados
    
def correccion_humedad(agua, materiales_secos, contenidos_humedad, absorciones):
    '''
    Correcion por humedad de los agregados
    Parametros: agua; materiales_secos; contenidos_humedad; absorciones
    Retorna: dict con pesos naturales, agua corregida y ajustes 
    '''
    resultados={
        'materiales_naturales': {},
        'ajustes_agua': {},
        'agua_corregida': agua,
        'sumatoria_agua': 0
    }

    for material, peso_seco in materiales_secos.items():
        if material in contenidos_humedad and material in absorciones:
            C=absorciones[material]#cap de absorcion
            H=contenidos_humedad[material]#humedad %

            #agua=((C-H)/100)*peso_seco
            ajuste_agua=((C-H)/100)*peso_seco
            peso_natural=peso_seco*(H/100 + 1)

            resultados['materiales_naturales'][material]=round(peso_natural, 2)
            resultados['ajustes_agua'][material]=round(ajuste_agua, 2)
            resultados['sumatoria_agua']+=ajuste_agua

            #peso final de agua=peso agua+sumatoria agua
            resultados['agua_corregida']=round(agua+resultados['sumatoria_agua'], 2)
            resultados['sumatoria_agua']=round(resultados['sumatoria_agua'], 2)

            return resultados