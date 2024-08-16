docker build -t imagem_clientes_microservice .
docker run --name clientes-microservice -it -p 5050:5000 -d imagem_clientes_microservice

SERVER_IP=$(curl checkip.amazonaws.com)
echo ""
echo "    Acessar: http://$SERVER_IP:5050/ "
echo ""
