from enum import Enum


class EnumExpressionsPT_BR(Enum):
    CAIXA_nome_id = ('if(\"tipo_caixa\" =9,' +
                     '(CASE' +
                     'WHEN count(1) = 0 THEN 1001' +
                     'ELSE 1001+ aggregate(' +
                     '\'caixas\',' +
                     '\'max\',' +
                     '\"nome_id\",' +
                     '\"nome\" LIKE \'C%\'' +
                     ')' +
                     'END' +
                     '), if(\"tipo_caixa\" =10,' +
                     '(CASE' +
                     'WHEN count(1) = 0 THEN 1001' +
                     'ELSE 1001 + aggregate(' +
                     '\'caixas\',' +
                     '\'max\',' +
                     '\"nome_id\",' +
                     '\"nome\" LIKE \'C%\'' +
                     ')' +
                     'END' +
                     '), if(\"tipo_caixa\" =11,' +
                     '(CASE' +
                     'WHEN count(1) = 0 THEN 1001' +
                     'ELSE 1001 + aggregate(' +
                     '\'caixas\',' +
                     '\'max\',' +
                     '\"nome_id\",' +
                     '\"nome\" LIKE \'C%\'' +
                     ')' +
                     'END' +
                     '), (CASE' +
                     'WHEN count(1) = 0 THEN 1' +
                     'ELSE 1 + aggregate(' +
                     '\'caixas\',' +
                     '\'max\',' +
                     '\"nome_id\",' +
                     '\"nome\" LIKE \'C%\'' +
                     ')' +
                     'END' +
                     ')))))'
                     )

    CAIXA_nome = ('if(\"tipo_caixa\" =9,\'PV_\'|| \"nome_id\",if(\"tipo_caixa\"=10,\'Selim_\' ||' +
                  '\"nome_id\",if(\"tipo_caixa\"=11,\'QV_\' ||\"nome_id\", \'C\' || \"nome_id\")))')

    CAIXA_c_terreno = 'round( raster_value( \'dem_ramais\',1, $geometry ),3)'

    CAIXA_cx_jusante = ('if(\"tipo_caixa\" =9,\'continuação_rede\',if(\"tipo_caixa\"=10,\'continuação_rede\',' +
                        'if(\"posicao_caixa\"=3,\'ponto_deságue\',if(\"posicao_caixa\"=5,' +
                        '\'continuação_quadravizinha\',\'C\' || (\"nome_id\" +1)))))')

    CAIXA_coord_x = 'round($x ,4)'
    CAIXA_coord_y = 'round($y ,4)'
    CAIXA_gabarito = '2'

    TRECHO_extensao = 'round($length ,2)'
    TRECHO_trecho = ('aggregate(' +
                     '\'caixas\',' +
                     '\'concatenate\',' +
                     '\"nome\", ' +
                     'intersects($geometry, start_point(geometry(@parent))),' +
                     '\'-\'' +
                     ') || \'-\' || aggregate(' +
                     '\'caixas\',' +
                     '\'concatenate\',' +
                     '\"nome\",' +
                     'intersects($geometry, end_point(geometry(@parent))),' +
                     '\'-\'' +
                     ')'
                     )
    TRECHO_cx_montante = ('aggregate(' +
                          '\'caixas\', ' +
                          '\'concatenate\', ' +
                          '\"nome\", ' +
                          'intersects($geometry, start_point(geometry(@parent))),' +
                          '\'-\'' +
                          ')'
                          )
    TRECHO_cx_jusante = ('aggregate(' +
                         '\'caixas\', ' +
                         '\'concatenate\', ' +
                         '\"nome\", ' +
                         'intersects($geometry, end_point(geometry(@parent))),' +
                         '\'-\'' +
                         ')')
    TRECHO_ramal_id = ('aggregate(' +
                       '\'caixas\', ' +
                       '\'min\', ' +
                       '\"ramal_id\", ' +
                       'intersects($geometry, start_point(geometry(@parent))),' +
                       '\'-\'' +
                       ')')
    TRECHO_percentual_pav_1 = ('CASE' +
                               'WHEN \"pavimento_2\" IS NULL OR \"pavimento_2\" = \'\' OR \"pavimento_2\" = 0 THEN 100' +
                               'ELSE 100 - \"percentual_pav_2\"' +
                               'END')
    TRECHO_percentual_pav_2 = ('CASE' +
                               'WHEN \"pavimento_2\" IS NULL OR \"pavimento_2\" = \'\' OR \"pavimento_2\" = 0 THEN 0' +
                               'END')
    TRECHO_pvc_diam = '\'150\''
    TRECHO_coord_Xi = 'round(x( point_n( $geometry,1)),4)'
    TRECHO_coord_Yi = 'round(y( point_n( $geometry,1)),4)'
    TRECHO_coord_Xf = 'round(x(end_point( $geometry)),4)'
    TRECHO_coord_Yf = 'round(y(end_point( $geometry)),4)'


class EnumExpressionsES_ES(Enum):
    CAJAS_nombre_id = ('if(\"tipo_caja\" =9,' +
                       '(CASE' +
                       'WHEN count(1) = 0 THEN 1001' +
                       'ELSE 1001 + aggregate(' +
                       '\'cajas\', ' +
                       '\'max\', ' +
                       '\"nombre_id\", ' +
                       '\"nombre\" LIKE \'C%\'' +
                       ')' +
                       'END' +
                       '), if(\"tipo_caja\" =10,' +
                       '(CASE' +
                       'WHEN count(1) = 0 THEN 1001' +
                       'ELSE 1001 + aggregate(' +
                       '\'cajas\', ' +
                       '\'max\', ' +
                       '\"nombre_id\", ' +
                       '\"nombre\" LIKE \'C%\'' +
                       ')' +
                       'END' +
                       '), if(\"tipo_caja\" =11,' +
                       '(CASE' +
                       'WHEN count(1) = 0 THEN 1001' +
                       'ELSE 1001 + aggregate('
                       '\'cajas\',' +
                       '\'max\',' +
                       '\"nombre_id\",' +
                       '\"nombre\" LIKE \'C%\'' +
                       ')' +
                       'END' +
                       '), (CASE' +
                       'WHEN count(1) = 0 THEN 1' +
                       'ELSE 1 + aggregate(' +
                       '\'cajas\',' +
                       '\'max\',' +
                       '\"nombre_id\",' +
                       '\"nombre\" LIKE \'C%\'' +
                       ')' +
                       'END' +
                       '))))')
