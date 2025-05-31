FACT TABLE
Na fact table temos um datetime_id que remete para a tabela 
de dimensão Date-Time, onde constam os parametros relativos à hora, dia,
mês e anos, onde ocurreu cada medição. Por enquanto consta o parametro 
is_weekend, para constatar se uma medição foi realizada durante o fim de semana.

O location_id aponta para a tabela Location, onde temos o nome da localização,
bem como as suas coordenadas de GPS.

Por último temos o parameter_id, dentro da tabela de dimensão Parameters, onde esta incluido
a etiqueta do parametro medido (PM2.5, PM10, NO2, Total Vehicle, Small Vehicle, Large Vehicle, Normal Vehicle),
bem como as respetivas unidades, e se se trata de uma unidade de medida da qualidade do ar,
ou de tráfico.

Na tabela de facto, apartir das Foreign Keys pode-se presenciar os resultados das medidas. 
