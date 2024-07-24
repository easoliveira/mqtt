#Emulação de dispositivos MQTT

Um ambiente para fazer teste de carga e compreender o uso do protocolo MQTT. 

##Conteúdo:

- `mqtt_teste_payload.sh` Script para criar um payload que incrementa byte a byte o envio para o topico topic/payload, é possivel alterar quantos bytes de início.
- `mqtt_publisher_threads.py` Cria N processos de publisher.py durante um tempo pré determinado
- `mqtt_subs_publ.py` Cria N threads publishers e subscriber 
- `LogaProcessamentoPS.sh` Captura o uso de CPU e memória e gera uma imagem no diretorio 



##Uso

1. Instalar  Mosquitto e o gnuplot
```
sudo apt-get install mosquitto mosquitto-clients
sudo apt-get install gnuplot
```

2. O broker vai ser inicializado por padrão.  Para ver os logs é necessário
pará-lo e reinicializá-lo.

```
sudo /etc/init.d/mosquitto stop
sudo mosquitto –v
```

#para testar o payload
3. Configure o mosquito para subescribe no tópico configurado no script mqtt_teste_payload.sh:
```
mosquitto_sub -t test/payload
```

4. após execute o script para enviar informações para o tópico:
```
sh mqtt_teste_payload.sh
```

5. Analise em qual momento, quantos bytes ocorre o erro.

#para testar o publishers

6. Em um terminal abra execute o script de monitoramento de cpu e memória:

```
sh LogaProcessamentoPS.sh
```

7. Em um novo terminal repita o passo 3.

8. Abra outro terminal, execute o script que instanciará vários publishers. Altere os parametros conforme necessário
 ```python3 mqtt_publisher_threadsT.py --broker localhost --topic test/payload --frequency 1000 --threads 50 --increment 50 --max-threads 10000
```

9. Ao final, será gerado N arquivos de log e um mem-graph.png com o uso de CPU e memória.

#para testar o publishers e subescribes

10. Repita o passo 6

11. Em um novo terminal execute o script
```
pip install paho-mqtt
python3 mqtt_subs_publ.py

```