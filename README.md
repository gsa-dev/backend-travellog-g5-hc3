# backend-travellog-g5-hc3

Resumo

Esboço do fluxo do backend do projeto

![image](https://user-images.githubusercontent.com/28959980/180124020-2dc79a2f-c23f-41f9-b7b6-3a2b82ce5032.png)

Primeiro foi criado um hook utilizando o lambda da AWS, esse lambda e reponsavel de receber a notificação da VTEX de novos pedidos, buscar a informação dos pedidos na VTEX, converter o valor dos pedidos em pontos e salvar no DynamoDB (fluxo 1,2 e 3 imagem acima). A tabela do Dynamo foi dimensionada em 2 colunas , uma para receber o id do usuario e a outra para receber os valores dos pontos.

![image](https://user-images.githubusercontent.com/28959980/180125135-c12ba0ca-e57c-4465-a258-5b8f4002b6c6.png)

Para configurar o hook na VTEX foi feito um POST no endpoint https://travellog.myvtex.com/api/orders/hook/config?_stats=1 

![image](https://user-images.githubusercontent.com/28959980/180128370-77da13bc-5fee-4a5e-91a4-0c03149fe835.png)

Segunda parte (fluxo 4 e 5) do desenvolvimento foi criar uma API para buscar a informação de quantos pontos o usuario tem disponivel e tambem conseguir debitar pontos da sua conta. Para o desenvolvimento da api  foi utilizado o API Gateway e Lambda da AWS.

![image](https://user-images.githubusercontent.com/28959980/180124735-798cec67-edb0-4e06-99e2-9ee88e0ed93e.png)

Para pegar os pontos basta da um GET no endpoint https://nzqmk80qxe.execute-api.us-east-1.amazonaws.com/prod/score passando como parametro o ID do usuario, nas reposta vai ter os pontos adicionados, debitados e a soma total.

![image](https://user-images.githubusercontent.com/28959980/180125511-c98bd011-d2db-4ed6-abe2-8b29597914b6.png)

Para subtrair os pontos tem que da um PATCH, passando no body da request o ID e valor

![image](https://user-images.githubusercontent.com/28959980/180125916-91608bbc-a743-429b-8c84-aa116cebc891.png)
